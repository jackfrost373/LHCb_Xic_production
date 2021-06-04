import ROOT, os, Imports, sys, getopt, textwrap
from ROOT import TChain, TFile
from Imports import TUPLE_PATH, TUPLE_PATH_NOTRIG, RAW_TUPLE_PATH, DATA_jobs_Dict

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hy:r:t")
    except getopt.GetoptError:
        print("The arguments are wrong")
        sys.exit(2)

    options = []
    arguments = []

    for opt,arg in opts:
        options.append(opt)
        arguments.append(arg)

    if "-y" in options and "-r" in options:
        print("You cannot use those two arguments at the same time. Exiting...")
        sys.exit(2)

    if "-h" in options:
        print(textwrap.dedent(
            """\

            Welcome to the tuple preparation script.

            The parameters are
            -h : help
            -y : prep tuples for specific year
            -r : prepares for specific run (1 or 2)
            -t : create the second dataset with no trigger cuts (can be added to any other parameter)

            Running with no parameter will prepare everything.
            """))

        sys.exit()

    #a dictionary containing the details of the all the years' data according to joblog.txt and the passed arguments
    #Run 1 is automatically Lc, and Run 2 has particle specified.
    folders_dict = {}

    if len(options) == 0:
        folders_dict = DATA_jobs_Dict

    if "-y" in options:
        for elem in DATA_jobs_Dict:
            if arguments[0] in DATA_jobs_Dict[elem][0]:
                folders_dict[elem] = DATA_jobs_Dict[elem]

    if "-r" in options:
        run1 = ["2011", "2012"]
        run2 = ["2016", "2017", "2018"]

        if arguments[0] == "1":
            run = run1
        elif arguments[0] == "2":
            run = run2
        else:
            print("Wrong run value. Exiting...")
            sys.exit()

        for year in run:
            for elem in DATA_jobs_Dict:
                if year in DATA_jobs_Dict[elem][0]:
                    folders_dict[elem] = DATA_jobs_Dict[elem]

    path = [TUPLE_PATH]

    if "-t" in options or len(options) == 0:
        path.append(TUPLE_PATH_NOTRIG)

    for PATH in path:
        if PATH == TUPLE_PATH:
            print("PREPARATION: DATA SET WITH TRIGGER")
            trig = True
        else:
            print("PREPARATION: DATA SET WITHOUT TRIGGER")
            trig = False

        #vestige of using turbo output for run 2 data. Still present in case we want to switch back to using Turbo line.
        withTurbo = False

        for element in folders_dict:
            if element in ["42", "43", "45", "46"]:
               extra_variables = [
                    "lcplus_Hlt1TrackAllL0Decision_TOS",
                    "lcplus_Hlt2CharmHadD2HHHDecision_TOS",
                    "lcplus_L0HadronDecision_TOS",
                    ]
               cutsRun = 1
               particle = "Lc"
            else:
               extra_variables = [
                    "nSPDHits",
                    "nTracks",
                    "lcplus_L0HadronDecision_TOS",
                    "lcplus_Hlt1TrackMVADecision_TOS",
                    "lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS",
                    "lcplus_Hlt2CharmHadLcpToPpKmPipTurboDecision_TOS",
                    "lcplus_Hlt2CharmHadD2HHHDecision_TOS",
                    ]
               particle = "Lc"
               cutsRun = 2

            name = folders_dict[element][0]
            subjobs = folders_dict[element][1]
            saving_directory = PATH + name + "_clusters/"

            cuts = Imports.getDataCuts(cutsRun, trig)

            if not os.path.exists(saving_directory):
               os.makedirs(saving_directory)

            file_directory = RAW_TUPLE_PATH + element

            print ("\nStarting process for " + name)

            step = subjobs//20 #carry out the process in 20 clusters of datafiles to avoid memory overflow
            Max = step
            Min = 0

        # Loop used to apply global cuts on the data
            print("Creation of Clusters")
            n = 20
            i = 0
            while (Max <= subjobs):
                #FOR THE PROGRASSION BAR
                if i < n:
                    j = (i + 1) / n
                    sys.stdout.write('\r')
                    sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                    sys.stdout.flush()
                    i += 1

                if Max == Min:
                    break

                strip_n_save(Min, Max, cuts, file_directory, saving_directory, extra_variables, particle)
                temp = Max
                if (Max+step > subjobs):
                    Max = subjobs
                else:
                    Max += step
                Min = temp

            clusters = os.listdir(saving_directory)

            print("\n\nTChaining the clusters")
            final_chain = TChain("DecayTree")
            n = len(clusters)
            i = 0
            for element in clusters:
                if i < n:
                    j = (i + 1) / n
                    sys.stdout.write('\r')
                    sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                    sys.stdout.flush()
                    i += 1
                final_chain.Add(saving_directory + element)


            if not os.path.exists(PATH + name + "/bins"):
               os.makedirs(PATH + name + "/bins")
            saving_dir = PATH + name + "/bins/"
            print("\n\nCreating the final files")
            split_in_bins_n_save(final_chain, saving_dir, withTurbo, particle) # split the datafile into mass-y-pt bins

            print ("\nProcess completed for " + name)

        #CREATION OF THE TOTAL YEAR DATA FILES (e.g. 2012_MagUp/Xic_Total.root)
        print("\Creation of the Total Year data files")
        mother_particle = ["Xic", "Lc"]
        BASE_PATH = PATH

        n = len(os.listdir(BASE_PATH))
        p = 0
        for i in os.listdir(BASE_PATH):
            if p < n:
                    j = (p + 1) / n
                    sys.stdout.write('\r')
                    sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                    sys.stdout.flush()
                    p += 1

            if "cluster" in i:
                continue

            for part in mother_particle:
                totfile = ROOT.TFile.Open(BASE_PATH + i + "/{}_total.root".format(part),"RECREATE")
                totfile.cd()
                tree = TChain("DecayTree")

                for j in os.listdir(BASE_PATH + i +"/bins/ybins"):
                        if part in j:
                                tree.Add(BASE_PATH + i +"/bins/ybins/"+j)
                tree.Write()
                totfile.Close()
                del totfile

        print("\nDeleting Clusters")
        os.system("rm -rf {}*_clusters".format(BASE_PATH))

    print("\nNTuple Preparation is done, happy analysis!")

#### This function takes a ROOT file as an input, keeps the variables in useful_vars in the tree and throws the other ones away. The pruned tree is then returned. ###
def setBranch_funct (root_file, extra_variables):

    useful_vars = ["lcplus_MM",
                   "lcplus_P",
                   "lcplus_PT",
                   "lcplus_ETA",
                   "lcplus_RAPIDITY",
                   "lcplus_TIP",
                   "lcplus_IPCHI2_OWNPV",
                   "lcplus_OWNPV_CHI2",
                   "lcplus_TAU",
                   "pplus_M",
                   "pplus_P",
                   "pplus_PT",
                   "pplus_RAPIDITY",
                   "pplus_ETA",
                   "pplus_ProbNNp",
                   "piplus_M",
                   "piplus_P",
                   "piplus_PT",
                   "piplus_RAPIDITY",
                   "piplus_ETA",
                   "piplus_ProbNNpi",
                   "pplus_PIDp",
                   "kminus_M",
                   "kminus_P",
                   "kminus_PT",
                   "kminus_RAPIDITY",
                   "kminus_ETA",
                   "kminus_ProbNNk",
                   "kminus_PIDK",
                   "PVNTRACKS",
                   "piplus_PX",
                   "pplus_PX",
                   "kminus_PX",
                   "piplus_PY",
                   "pplus_PY",
                   "kminus_PY",
                   "piplus_PZ",
                   "pplus_PZ",
                   "kminus_PZ"] # list of variables kept in the tree

    for extra_variable in extra_variables:
        if not (extra_variable == ""): #if extra_variable is something needed, then it will be added to the array
            useful_vars.append(extra_variable)

    tfile = root_file  #These 2 lines depend on the type of file fed into the function
    tfile.SetBranchStatus("*", False) #first deactivate all branches

    for element in useful_vars: # then reactivate the ones present in useful_vars
        tfile.SetBranchStatus(element, True)

    return tfile # return the pruned TTree


#### This function requires a .root file as an input that in its structure has DecayTree immediately there without any intermediate structure. The TTree is divided into bins and these are saved in the saving_dir (which is a string of the saving directory) ####
def split_in_bins_n_save (root_file, saving_dir, withTurbo, mother_particle = "Lc"):

    ybins = Imports.getYbins() #Rapidity bins

    ptbins = Imports.getPTbins()

    #Also vestige of using turbo output: the variables would be preseparated, so no need to do it ourselves
    if not withTurbo:
        particles = ["Lc", "Xic"]
    else:
        particles = []
        particles.append(mother_particle)

    if not os.path.exists(saving_dir + "ybins/"):
        os.mkdir(saving_dir + "ybins/")
    if not os.path.exists(saving_dir + "ptbins/"):
        os.mkdir(saving_dir + "ptbins/")
    if not os.path.exists(saving_dir + "y_ptbins/"):
        os.mkdir(saving_dir + "y_ptbins/")

    extra_variables = [""]
    tree = root_file
    for particle in particles:
        if particle == "Lc":
            mass_cuts = "lcplus_MM < 2375"
        if particle == "Xic":
            mass_cuts = "lcplus_MM > 2375"

        print("Particle: " + particle)
        for ybin in ybins:

            ycuts = "lcplus_RAPIDITY >= {0} && lcplus_RAPIDITY < {1}".format(ybin[0], ybin[1])
            allcuts = " {0} && {1}".format(ycuts, mass_cuts)

            strip_n_save(0,0, allcuts, "", saving_dir + "ybins/" + particle + "_ybin_{0}-{1}.root".format(ybin[0], ybin[1]), extra_variables,particle, bins = True, tree = tree)

            n = len(ptbins)
            i = 0
            print("Files with y({0})".format(ybin))
            for ptbin in ptbins:
                #FOR THE PROGRESSION BAR
                if i < n:
                    j = (i + 1) / n
                    sys.stdout.write('\r')
                    sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                    sys.stdout.flush()
                    i += 1

                ptcuts = "lcplus_PT >= {0} && lcplus_PT < {1}".format(ptbin[0], ptbin[1])
                if (ybin[0] == 2.0):
                    allcuts = " {0} && {1}".format(ptcuts, mass_cuts)
                    strip_n_save(0,0, allcuts, "", saving_dir + "ptbins/" + particle + "_ptbin_{0}-{1}.root".format(ptbin[0], ptbin[1]), extra_variables, particle, bins = True,tree = tree)
                yptcut = ycuts + " && " + ptcuts
                allcuts = " {0} && {1}".format(yptcut, mass_cuts)
                strip_n_save(0,0, allcuts, "", saving_dir + "y_ptbins/" + particle + "_ybin_{0}-{1}_ptbin_{2}-{3}.root".format(ybin[0],ybin[1],ptbin[0],ptbin[1]), extra_variables, particle, bins = True, tree = tree)
            print("\n")

#### Function that takes as inputs: min and max which are 2 integers that indicates from which subjob to which subjob the TChain ranges; cuts are the cuts applied to the TTrees; directory is the directory in which the subjobs are to be found and saving_directory is the directory in which the stripped files are then saved. ####
def strip_n_save (Min, Max, cuts, directory, saving_directory, extra_variables, particle, bins = False, tree = None):

    if not (bins):
        filename = "{0}2pKpiTuple.root".format(particle)
        alldata = TChain("tuple_{0}2pKpi/DecayTree".format(particle))

        extra_dir = ""
        for job in range(Min, Max) :
            if os.path.exists("{0}/{1}{2}/{3}".format(directory,job,extra_dir,filename)):
                alldata.Add("{0}/{1}{2}/{3}".format(directory,job,extra_dir,filename))

    #Check if there are any issues with the data
        if (alldata.GetEntries() == 0):
            print("Error: entries = 0 for range " + str(Min) + "-" + str(Max))
            return
        if (alldata.GetEntries() == -1):
            print("Error: entries = -1 for range " + str(Min) + "-" + str(Max))
            return

        alldata = setBranch_funct(alldata, extra_variables)

        extra_string = particle + "_cluster_{0}-{1}.root".format(Min, Max)
    else:
        if not (tree == None):
            alldata = tree
        extra_string = ""


    wfile = TFile.Open(saving_directory + extra_string, "RECREATE")
    subtree = alldata.CopyTree( cuts )

    wfile.cd()
    subtree.Write()
    wfile.Close()

if __name__ == '__main__':
    main(sys.argv[1:])
