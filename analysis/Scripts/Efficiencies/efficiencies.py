from ROOT import TChain, TCanvas, TH1, TFile
import sys

sys.path.append('../')

import ROOT, os, Imports, getopt
from Imports import TUPLE_PATH, RAW_TUPLE_PATH, TABLE_PATH, OUTPUT_DICT_PATH, MC_jobs_Dict
import pprint

dict_path = OUTPUT_DICT_PATH + "Efficiencies/"
table_path = TABLE_PATH + "Efficiencies/"

ybins = Imports.getYbins()
ptbins = Imports.getPTbins()

def main(argv):

    ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH FOR ROOT

    try:
        opts, args = getopt.getopt(argv,"hstp")
    except getopt.GetoptError:
        print("The arguments are wrong")
        sys.exit(2)

    options = []
    arguments = []

    for opt,arg in opts:
        options.append(opt)
        arguments.append(arg)

    if not options:
        options = ["-s","-t","-p"]

    if "-h" in options:
        print(textwrap.dedent(
            """\

            Welcome to the efficiencies.py script.

            The parameters are
            -h : help
            -s : Selection
            -t : Trigger
            -p : PID

            Running with no parameter will output all the data at once.
            """))

        sys.exit()


    for opt in options:

        if opt == "-s":

            selecEffDict = {}
            years = []

            print("\nCreation of the selection efficiency files")

            n = len(MC_jobs_Dict)
            i = 0

            for job in MC_jobs_Dict:
                #FOR THE PROGRESSION BAR
                if i < n:
                    j = (i + 1) / n
                    sys.stdout.write('\r')
                    sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                    sys.stdout.flush()
                    i += 1
                if job == "NA":
                    continue

                particle = MC_jobs_Dict[job][3]
                year = MC_jobs_Dict[job][0]
                pol = MC_jobs_Dict[job][1]
                subjobs = MC_jobs_Dict[job][2]
                identifier = MC_jobs_Dict[job][4]

                if year not in years:
                    years.append(year)

                filename = "MC_Lc2pKpiTuple_" + identifier + ".root"

                if int(year) <= 2012:
                    run = 1
                    cuts = Imports.getDataCuts(run)
                else:
                    run = 2
                    cuts = Imports.getDataCuts(run)

                Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree") # !!! QUESTION : NOT BETTER ISTEAD OF CHAIN; JUST GETENTRIES FROM EACH ONE BY ONE, ONCE WITHOUT CUT AND ONCE WITH?

                for subjob in os.listdir(RAW_TUPLE_PATH + job):
                    Lc_MC_tree.Add(RAW_TUPLE_PATH + job + "/" + subjob + "/" + filename)

                N= float(Lc_MC_tree.GetEntries()) #WHY DID SIMON USE A HARDCODED NUMBER OF ENTRIES??
                #k = float(Lc_MC_tree.GetEntries(cuts + " && " + turbo)) SIMON VERSION
                k = float(Lc_MC_tree.GetEntries(cuts))
                eff = float(k/N)
                binom_error = (1/N)*((k*(1-k/N))**(0.5))

                selecEffDict[particle + "_" + str(year) + "_" + pol] = {'val': eff, 'err': binom_error}


            print("\nSelection efficiency calculations are done!")

            latexTable(selecEffDict,years,"Selection")

            prettyEffDict = pprint.pformat(selecEffDict)
            dictF = open(dict_path + "Selection_Eff_Dict.py","w")
            dictF.write("selDict = " + str(prettyEffDict))
            dictF.close()

        elif opt == "-t":

            print("\nCreation of the trigger efficiency files")

            trigEffDict = {}
            years = []

            n = len(MC_jobs_Dict)
            i = 0

            for job in MC_jobs_Dict:
                #FOR THE PROGRESSION BAR
                if i < n:
                    j = (i + 1) / n
                    sys.stdout.write('\r')
                    sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
                    sys.stdout.flush()
                    i += 1
                if job == "NA":
                    continue

                particle = MC_jobs_Dict[job][3]
                year = MC_jobs_Dict[job][0]
                pol = MC_jobs_Dict[job][1]
                subjobs = MC_jobs_Dict[job][2]
                identifier = MC_jobs_Dict[job][4]

                if year not in years:
                    years.append(year)

                filename = "MC_Lc2pKpiTuple_" + identifier + ".root"

                if int(year) <= 2012:
                    run = 1
                    cuts = "lcplus_L0HadronDecision_TOS == 1 && lcplus_Hlt1TrackAllL0Decision_TOS == 1"
                    turbo = "lcplus_Hlt2CharmHadD2HHHDecision_TOS==1"
                else:
                    run = 2
                    cuts = Imports.getDataCuts(run)
                    turbo = "lcplus_Hlt1TrackMVADecision_TOS==1"

                #WHAT DO I NEED FOR TRIGGER CUTS?!!

                Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree") # !!! QUESTION : NOT BETTER ISTEAD OF CHAIN; JUST GETENTRIES FROM EACH ONE BY ONE, ONCE WITHOUT CUT AND ONCE WITH?

                for subjob in os.listdir(RAW_TUPLE_PATH + job):
                    Lc_MC_tree.Add(RAW_TUPLE_PATH + job + "/" + subjob + "/" + filename)

                N=float(Lc_MC_tree.GetEntries( turbo + " && lcplus_L0HadronDecision_TOS==1"))
                k = float(Lc_MC_tree.GetEntries(cuts + " && " + turbo ))
                eff = float(k/N)
                binom_error = (1/N)*((k*(1-k/N))**(0.5))

                trigEffDict[particle + "_" + str(year) + "_" + pol] = {'val': eff, 'err': binom_error}

            print("\nTrigger efficiency calculations are done!")

            latexTable(trigEffDict,years,"Trigger")

            prettyEffDict = pprint.pformat(trigEffDict)
            dictF = open(dict_path + "Trigger_Eff_Dict.py","w")
            dictF.write("trigDict = " + str(prettyEffDict))
            dictF.close()


        elif opt == "-p":
            print("\nCreation of the selection efficiency files")

            ybins = Imports.getYbins()
            ptbins = Imports.getPTbins()

            cuts = "lcplus_L0HadronDecision_TOS"

            f_text = open("PID_eff_nobins.txt", "w+")
            directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/"

            for job in MC_jobs_Dict:
                if job == "NA": #AT the moment only do Magdown, will need to implement to us magdown as proxy for magup
                    continue

                particle = MC_jobs_Dict[job][3]
                year = MC_jobs_Dict[job][0]
                mag = MC_jobs_Dict[job][1]
                n_subjobs = MC_jobs_Dict[job][2]
                ID = MC_jobs_Dict[job][4]

                if int(year) <= 2012:
                    turbo = "lcplus_Hlt2CharmHadD2HHHDecision_TOS == 1"
                else:
                    turbo = "lcplus_Hlt1TrackMVADecision_TOS==1"
                
                Lc_MC_filename = "MC_Lc2pKpiTuple_" + ID + ".root"

                Lc_MC_filedir = directory + str(job)
                #Lc_MC_filename = "MC_Lc2pKpiTuple_" + ID + ".root"

                Lc_MC_tree = ROOT.TChain("tuple_Lc2pKpi/DecayTree")

                for subjob in range(n_subjobs) :
                    Lc_MC_tree.Add("{0}/{1}/{2}".format(Lc_MC_filedir,subjob,Lc_MC_filename))

                string = calcPIDefficiency(year=year, mag=mag, bdtbin=0, tupleloc=tupleloc, pidbinvars = ["P", "ETA", "nTracks"], b2hhbinvars = ["P", "ETA", "nTracks"], optionstring = "_MC", ignoreB2hhStatErr = False, correctKinematics = False, binningscheme = "", extra_cuts = turbo, MC_tree = Lc_MC_tree, mother_particle = particle)
                f_text.write(string)

                #for ybin in ybins:
                #    for ptbin in ptbins:
                #      yptcut = "lcplus_PT >= {0} && lcplus_PT < {1} && lcplus_RAPIDITY >= {2} && lcplus_RAPIDITY < {3}".format(ptbin[0], ptbin[1], ybin[0], ybin[1])
                #      string = calcPIDefficiency(year=year, mag=mag, bdtbin=0, tupleloc=tupleloc,
                #                  pidbinvars = ["P","ETA", "nTracks"], b2hhbinvars = ["P","ETA", "nTracks"], optionstring="_MC",
                #                  ignoreB2hhStatErr = False, correctKinematics = False, binningscheme="", extra_cuts=(yptcut + " && " + turbo), MC_tree = Lc_MC_tree, mother_particle = particle, ybin=ybin, ptbin=pt$
                #      f_text.write(string)

            f_text.close()

        else:
            sys.exit()

##############################################################
############ PID EFF IMPORTS AND METHODS #####################
from math import sqrt
import re

perfhists_loc = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v7r0/"
tupleloc = ""

#mother_particle = "Xic"

# variables to draw sWeighed distributions for, and their range
#drawvars = [["muplus_P", [0,100000]], ["muplus_eta", [1.5,5.0]], ["nTracks",[0,500]]]
drawvars = []

particles = ["pplus","kminus", "piplus"]

pidcuts_r1 = {"pplus":["P","P_MC12TuneV2_ProbNNp > 0.5 && DLLp > 0"],
           "kminus":["K", "K_MC12TuneV2_ProbNNK > 0.4 && DLLK > 0"],
           "piplus":["Pi", "Pi_MC12TuneV2_ProbNNpi > 0.5"]}

pidcuts_r2 = {"pplus":["P","P_MC15TuneV1_ProbNNp > 0.5 && DLLp > 0"],
           "kminus":["K", "K_MC15TuneV1_ProbNNK > 0.4 && DLLK > 0"],
           "piplus":["Pi", "Pi_MC15TuneV1_ProbNNpi > 0.5"]}

yeardict = {
  "2011" : "Strip20r1",
  "2012" : "Strip20",
  "2015" : "Turbo15",
  "2016" : "Turbo16",
  "2017" : "Turbo17",
  "2018" : "Turbo18"
  }

# def getMCCuts (particle):
#     IDcuts = "abs(piplus_ID)==211 && abs(kminus_ID)==321 && abs(pplus_ID)==2212 && abs(lcplus_ID)==4122"
#     if particle == "Lc":
#         BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 10 || lcplus_BKGCAT == 20 || lcplus_BKGCAT == 50)"
#         BKGCAT = "1==1"
#         return IDcuts + "&&" + BKGCAT
#     elif particle == "Xic":
#         BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 10 || lcplus_BKGCAT == 20 || lcplus_BKGCAT == 50)"#Deleted lcplus_BKGCAT == 20 which is needed for 2018
#         BKGCAT = "1==1"
#         return IDcuts + "&&" + BKGCAT


def getPIDcuts() :
    return "(1==1)"

#Not entirely sure what this does and whether it is relevant
def setParameterFromOptions(PARNAME, optionstring, default=0) :
# parse parameter value from options: "PID17" --> gets 17
    if(PARNAME in optionstring) :
        param = re.findall( r'(?:{0})([0-9]+)'.format(PARNAME), optionstring )[0]
        print("==> OPTIONS: setting {0} to {1}".format(PARNAME,param))
        return param
    else:
        return default

#var needs to be changed
#This function draws the distribution of var with all the different weights in weightlist and then draws them all on the same canvas.
#it appears not to be an essential tool, but rather a check. On top of this, not necessary when dealing with MC
def drawWeighedDistributions(tree, var="B_MKPi", weightlist=["1"], window=[5100,5600],nbins=100,colors=[1,9,8,46]) :
    cDraw = ROOT.TCanvas("cDraw_{0}".format(var))
    histos = []
    for i in range(len(weightlist)) :
        weight = weightlist[i]
        tree.Draw("{0}>>drawweighed_{1}({2},{3},{4})".format(var,weight,nbins,window[0],window[1]),weight)
        histos += [ ROOT.gDirectory.Get("drawweighed_{0}".format(weight)) ]
        histos[i].SetLineColor(colors[i])
    histos[0].Draw()
    for histo in histos :
        histo.Draw("same")
    cDraw.Update()
    cDraw.SaveAs("output/sWeighed_{0}.pdf".format(var))
    return[cDraw,histos]
#################################################
#correctKinematics set to false?
#I removed nTracks from the variables. Should I keep it?
#nTracks was removed because it was not in the datadiles originally. If it is now there, this variable should be included.
def calcPIDefficiency( year="2016", mag="Up", bdtbin=0, tupleloc=tupleloc,
    pidbinvars = ["P","ETA"], b2hhbinvars = ["P","ETA"], optionstring="_MC",
    ignoreB2hhStatErr = False, correctKinematics = False, binningscheme="", extra_cuts="1==1", MC_tree="MC", mother_particle="Lc", ybin=[0,0], ptbin=[0,0]
    ) :

    assert(len(pidbinvars) == len(b2hhbinvars))
    assert(mag in ["MagUp","MagDown"])

    #Not sure about the role of these 2 variables
    pidcut    = float( setParameterFromOptions("PID", optionstring, 5) )
    windowmin = float( setParameterFromOptions("XMIN", optionstring, 5100) )
    window = [windowmin, 5600.]

    simulation = False
    if ("_MC" in optionstring) : simulation = True

    print("\n*************************************************")
    print("Calculating PID efficiency for {0} {1}, BDTbin {2}, PIDcut {3} ({4}), particle: {5}".format(year,mag,bdtbin,pidcut,optionstring,mother_particle))
    print("  (binning vars: {0} --> {1})".format(pidbinvars, b2hhbinvars))

    mag = "MagDown" #USE MAGDOWN AS PROXY FOR MAGUP

# get PIDCalib perfhists
    perfhistFiles = {}
    Total_perfhists = {}
    Passed_perfhists = {}
    for particle in particles :
        extravar = ""
        if ("Turbo" in yeardict[year]):
            pidcuts = pidcuts_r2
            extravar = "_Brunel"
        else:
            pidcuts = pidcuts_r1

        perfhistfilename = perfhists_loc + "PerfHists_{0}_{1}_{2}_BHH_Binning_P_ETA_nTracks{3}.root".format(pidcuts[particle][0], yeardict[year], mag, extravar)#readded BHH_Binning
        print("Opening {0}".format(perfhistfilename))
        perfhistFiles[particle] = ROOT.TFile.Open(perfhistfilename) #__{1}_P_{2}_Eta_nTracks{3}.format(pidcuts[particle][1], pidcuts[particle][0], pidcuts[particle][0], extravar)
        Total_perfhists[particle] = perfhistFiles[particle].Get("TotalHist_{0}_All__{1}_P_{2}_Eta_nTracks{3}".format(pidcuts[particle][1], pidcuts[particle][0], pidcuts[particle][0], extravar)) ##It seem$
#perfhists[particle].Sumw2() # already created. #not my comment
        Passed_perfhists[particle] = perfhistFiles[particle].Get("PassedHist_{0}_All__{1}_P_{2}_Eta_nTracks{3}".format(pidcuts[particle][1], pidcuts[particle][0], pidcuts[particle][0], extravar))
        if(Total_perfhists[particle]) == None:
            print(" Error: Cannot find TotalHist_{0}_All__{1}_P_{2}_Eta_nTracks{3}".format(pidcuts[particle][1], pidcuts[particle][0], pidcuts[particle][0], extravar))
        if(Passed_perfhists[particle]) == None:
            print(" Error: Cannot find Passedist_{0}_All__{1}_P_{2}_Eta_nTracks{3}".format(pidcuts[particle][1], pidcuts[particle][0], pidcuts[particle][0], extravar))


    # Obtain binning used by PIDCalib
    ndims = len(pidbinvars) #should I add 1 here because there is also nTracks or should we ignore the 3rd dimension since data does not have this variable?
    axesbins = {}
    if(ndims>0) : axesbins[0] = Passed_perfhists["kminus"].GetXaxis().GetXbins() #Why is it K all the times?
    if(ndims>1) : axesbins[1] = Passed_perfhists["kminus"].GetYaxis().GetXbins()
    if(ndims>2) : axesbins[2] = Passed_perfhists["kminus"].GetZaxis().GetXbins()

    n_Tracks_bins_array = Passed_perfhists["kminus"].GetZaxis().GetXbins()
    print("here is the nTracks binning")
    for element in n_Tracks_bins_array:
        print(element)

    axesbins_python = {}
    print("Found PIDCalib binning:")
    for i in range(ndims) :
        axesbins_python[i] = [ axesbins[i][j] for j in range(axesbins[i].GetSize()) ] #loop over all of the bins right?
        print(" {0} : {1}".format(pidbinvars[i], axesbins_python[i]))

    nbinranges = []
    for i in range(ndims) :
        nbinranges += [1] # first bin, without underflow
        nbinranges += [ axesbins[i].GetSize() -1 ]


    # get b2hh tree
    ## at this stage I need to get the files that are going to be used. Perhaps make a TChain of the MC files for the particle chosen?
    files = []
#  if("Up"   in mag) : files += bdkpi_reduce.getCutFiles(year,"up",   baseloc=tupleloc, optionstring=optionstring) ## Get rid of this bdkpi which seems to be a library/script imported by Jacco from s$

    #Lc_MC_filedir = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/"+"30"
    #Lc_MC_filename = "MC_Lc2pKpiTuple_25103029.root"

    #treeload = ROOT.TChain("tuple_Lc2pKpi/DecayTree")

    #for job in range(27) :
    # treeload.Add("{0}/{1}/output/{2}".format(Lc_MC_filedir,job,Lc_MC_filename))
    treeload = MC_tree
    if treeload.GetEntries() == 0:
        print("treeload entries are zero")

    elif treeload.GetEntries() == -1:
        print("treeload entries are -1")
    else:
        print("you're fine")
        print("Total entries: " + str(treeload.GetEntries()))

    # define cuts: should be identical to sWeight production, in order to have same #entries
    if not simulation :
        cuts_pid  = getPIDcuts()#.replace(">",">=").replace("<","<=")
    # cuts_mass = "{0} > {1} && {0} < {2}".format(masshypovar(decay,year), window[0], window[1])
    #  cuts_b2hh = "( ({0}) && ({1}) && ({2}) )".format(cuts_pid, cuts_bdt, cuts_mass)
    if simulation :
        if int(year) > 2012:
            run = 2
        else:
            run = 1

        Mc_cuts = Imports.getMCCuts(mother_particle, run) #possibly use the hardcoded function
        cuts_b2hh = Mc_cuts + " && " + extra_cuts


    #dummyfile = ROOT.TFile.Open("./dummy.root","RECREATE")
    #tree = treeload.CopyTree(cuts_b2hh)
    #dummyfile.cd()
    #tree.Write()
    #dummyfile.Close()
    print("\nnEntries in file after cuts: {0}".format(treeload.GetEntries(cuts_b2hh)))

#This section is relevant when calculating efficiencies for data rather than for MC.
    # add sWeights
    if not simulation :
        swfilename = ""
        print("adding sWeight tree: {0}".format(swfilename))
        tree.AddFriend("swTree",swfilename)
        #if decay in ["KPi","PiK"] : weight = "swTree.sw_n_bd"
        #if decay in ["KK"]        : weight = "swTree.sw_n_bs"
    if simulation :
        weight = "1."

    if not simulation :
        # Draw weighed 1D distributions for given variables
        drawweights = ["1","swTree.sw_n_bd","swTree.sw_n_bs","swTree.sw_n_comb"]
        for i in drawvars :
            [drawvar, drawwindow] = i
            [cDraw,cDrawHistos] = drawWeighedDistributions(tree, drawvar, drawweights, drawwindow)


# define decay-specific parameters
# if(decay=="KPi") : b2hh_particlemap = { "muplus" : "K" , "muminus" : "Pi" }
# if(decay=="PiK") : b2hh_particlemap = { "muplus" : "Pi", "muminus" : "K"  }
#  if(decay=="KK")  : b2hh_particlemap = { "muplus" : "K",  "muminus" : "K"  }


# draw b2hh histogram in same binning as PIDCalib perfhists #this part is easy. It is simply drawing the data in the same binning as the perfhists
#I am not entirely sure that this makes sense because I am trying to plot mass (lcplus_MM) as a function of P and ETA aren't I? To see what regions contain more data
#No, you're not. You have to do this for the single daughter particles because you want to see where most of them are in those bins since it's the PID of those particles that you are interested in
    print("Drawing b2hh histograms")
    c1 = ROOT.TCanvas("c1")
    b2hhHists = {}
    for particle in particles :
        histname = "P_ETA_Hist_{0}".format(particle)
        if(ndims>0) : var0 = "{0}_{1}".format(particle,b2hhbinvars[0])
        if(ndims>1) : var1 = "{0}_{1}".format(particle,b2hhbinvars[1])
        if(ndims>2) : var2 = "{0}_{1}".format(particle,b2hhbinvars[2])
        if(ndims>2 and ("nTracks" in b2hhbinvars[2] or "SPD" in b2hhbinvars[2])) : var2 = b2hhbinvars[2]

        if(ndims==1) :
            print("entering the wrong ndims condition")
            b2hhHists[particle] = ROOT.TH1F(histname,histname, axesbins[0].GetSize()-1, axesbins[0].GetArray())
            treeload.Draw("{0}>>+{1}".format(var0,histname),"{0}".format(weight))
        if(ndims==2) :
            print("entering the right ndims condition")
            b2hhHists[particle] = ROOT.TH2F(histname,histname, axesbins[0].GetSize()-1, axesbins[0].GetArray(),
                                      axesbins[1].GetSize()-1, axesbins[1].GetArray())
            treeload.Draw("{0}:{1}>>+{2}".format(var1,var0,histname), cuts_b2hh,"COLZ")
            #"{0}*({1})".format(weight, cuts_b2hh),)
        if(ndims==3) :
            print("entering the 3D condition")
            b2hhHists[particle] = ROOT.TH3F(histname,histname, axesbins[0].GetSize()-1, axesbins[0].GetArray(),
                                      axesbins[1].GetSize()-1, axesbins[1].GetArray(),
                                      axesbins[2].GetSize()-1, axesbins[2].GetArray())
            treeload.Draw("{0}:{1}:{2}>>+{3}".format(var2,var1,var0,histname), cuts_b2hh)
            # "{0}".format(weight))

        if(ndims>0) : b2hhHists[particle].GetXaxis().SetTitle( var0 )
        if(ndims>1) : b2hhHists[particle].GetYaxis().SetTitle( var1 )
        if(ndims>2) : b2hhHists[particle].GetZaxis().SetTitle( var2 )
        c1.Update()
        c1.Draw()
        c1.SaveAs("./"+ mother_particle +  "_PID_efficiency_" + particle + ".pdf")

    if(ignoreB2hhStatErr) :
        # ignore stat errors on the b2hh sample, since already counted in yield
        print("Setting b2hh stat errors to 0")
        for particle in particles :
            histo = b2hhHists[particle]
            for binx in range(1,histo.GetNbinsX()+1) :
                for biny in range(1,histo.GetNbinsY()+1) :
                    for binz in range(1,histo.GetNbinsZ()+1) :
                        ibin = histo.GetBin(binx,biny,binz)
                        b2hhHists[particle].SetBinError(ibin, 0.)



    #Since we will begin with MC, we might consider setting this to False initially
    if(correctKinematics) :
        # apply 1/PID efficiencies as weights, to correct kinematics due to the PID cut itself.
        print("Applying 1/PIDeff as additional weights to correct kinematics")
        for particle in particles :
            #beforehist = b2hhHists[particle].ProjectionX().Clone("beforehist")
            #b2hhHists[particle].Divide( perfhists[ b2hh_particlemap[particle] ] )
            #afterhist = b2hhHists[particle].ProjectionX().Clone("afterhist")

            # To get the errors right, we have to do this bin-by-bin instead.
            weighthist = ROOT.TH1F("weighthist","weighthist",25,0,1) # for visualizing weight distribution
            histo = b2hhHists[particle]
            perfhist = perfhists[ b2hh_particlemap[particle] ] #This needs to be changed
            for binx in range(1,histo.GetNbinsX()+1) :
                for biny in range(1,histo.GetNbinsY()+1) :
                    for binz in range(1,histo.GetNbinsZ()+1) :
                        ibin = histo.GetBin(binx,biny,binz)
                        b2hh_val = histo.GetBinContent(ibin)
                        b2hh_err = histo.GetBinError(ibin)
                        pid_val  = perfhist.GetBinContent(ibin)
                        pid_err  = perfhist.GetBinError(ibin)
                        if(pid_val < 0.05) : pid_val = 0.05 # cutoff to avoid large weights
                        weighthist.Fill(pid_val, b2hh_val)
                        if not pid_val == 0 : newval = b2hh_val / pid_val
                        else : newval = 0.
                        newerr = 0.
                        if not b2hh_val == 0 : newerr += (b2hh_err/b2hh_val)**2
                        if not pid_val  == 0 : newerr += (pid_err /pid_val )**2
                        newerr = sqrt( newerr ) * newval ## TODO is this correct? gives the same total error!
                        b2hhHists[particle].SetBinContent(ibin, newval)
                        b2hhHists[particle].SetBinError(ibin, newerr)
            weighthist.SetTitle("PID eff distribution ; PID eff ; Count")
            #cweight = ROOT.TCanvas("cweight","cweight")
            #weighthist.Draw("H")
            #cweight.Update()
            #cweight.SaveAs("weighthist{0}.pdf".format(particle))


    if(False) :
        # do a naive bin-by-bin loop, to see if it matches the faster 'Integrate' result below
        print("Performing naive check:")
        for particle in particles :
            efftotal = 0.
            errtotal = 0.
            ntotal = 0.
            histo = b2hhHists[particle]
            perfhist = perfhists[ b2hh_particlemap[particle] ]
            for binx in range(1,histo.GetNbinsX()+1) :
                for biny in range(1,histo.GetNbinsY()+1) :
                    for binz in range(1,histo.GetNbinsZ()+1) :
                        ibin = histo.GetBin(binx,biny,binz)
                        #print(" ibin location XYZ: {0}, {1}, {2}".format( histo.GetXaxis().GetBinCenter(binx),
                        #  histo.GetYaxis().GetBinCenter(biny), histo.GetZaxis().GetBinCenter(binz) ))
                        b2hh_val = histo.GetBinContent(ibin)
                        b2hh_err = histo.GetBinError(ibin)
                        pid_val  = perfhist.GetBinContent(ibin)
                        pid_err  = perfhist.GetBinError(ibin)
                        efftotal += b2hh_val * pid_val
                        errtotal += b2hh_err * pid_val + pid_err * b2hh_val
                        ntotal += b2hh_val
                        #print("Bin: {0},{1},{2} - eff = {3:.3f} ; val = {4:.3f} --> TOT={5:.3f}".format(binx,biny,binz,pid_val, b2hh_val, efftotal/ntotal))
            result = efftotal / ntotal
            reserr = errtotal / ntotal
            print(" --> bin-looped result for {0}: {1} +- {2}".format(particle,result, reserr))




    # Multiply to obtain total efficiency
    effs = {}
    for particle in particles :
        b2hhHist = b2hhHists[particle]
        #b2hhHist.Sumw2() # is already created
        ntotal = b2hhHist.Integral(*nbinranges)
        if ntotal == 0:
            return ("For particle {0} year: {1} Mag{2}, bin:y{3}-{4} pt {5}-{6} there are no entries".format(mother_particle, year, mag, ybin[0], ybin[1], ptbin[0], ptbin[1]))
        print("ntotal is " + str(ntotal))
    #Again, this part was done because there was no nTracks in the variables. Thus PID eff. histograms needed to be projected on 2 axes only.
        # compressed_Total_perfhist =Total_perfhists[particle].Project3D("yx")
        # compressed_Passed_perfhist =Passed_perfhists[particle].Project3D("yx")
        compressed_Total_perfhist = Total_perfhists[particle]
        compressed_Passed_perfhist = Passed_perfhists[particle]

        compressed_perfhist = compressed_Passed_perfhist.Divide(compressed_Total_perfhist)
        if compressed_perfhist == False:
            print("Divide operation failed")
        b2hhHist.Multiply( compressed_Passed_perfhist ) #In this case it will need to be the perfhist only related to the particle, skipping this particlemap parame
        #b2hhHist.Multiply(compressed_Passed_perfhist.Divide(compressed_Total_perfhist))
        efftotal_error = ROOT.Double(0)
        efftotal = b2hhHist.IntegralAndError(*(nbinranges + [efftotal_error]))
        print("efftotal is " + str(efftotal))
        efftotal = efftotal / ntotal
        efftotal_error = efftotal_error / ntotal
        print("PID eff {0}  \t= {1:.8f} +- {2:.8f}".format(particle, efftotal, efftotal_error))
        effs[particle] = [efftotal, efftotal_error]

    # compute total eff, assuming full correlation for the error
    totaleff = effs["pplus"][0] * effs["kminus"][0]*effs["piplus"][0]
    totaleff_error = (effs["pplus"][1] / effs["pplus"][0] + effs["kminus"][1] / effs["kminus"][0] + effs["piplus"][1] / effs["piplus"][0]) * totaleff
    return ("For particle {2} year: {3} Mag{4}, bin: y{5}-{6} pt{7}-{8} the total eff for pKpi:  \t= {0:.8f} +- {1:.8f}".format(totaleff, totaleff_error, mother_particle, year, mag, ybin[0], ybin[1], ptbin[0], ptbin[1]))
    #return [totaleff, totaleff_error]

#################################################


def latexTable(dict, years, type):
    csvF = open(table_path + type + "_Eff_Values.tex","w")
    csvF.write("\\begin{tabular}{ll|c|c|c|c|c|c|}\n")
    csvF.write("\\cline{3-6}\n")
    csvF.write("& & \\multicolumn{2}{c|}{$\Xi_c$} & \multicolumn{2}{c|}{$\\Lambda_c$} \\\\ \\cline{3-8}\n")
    csvF.write("& & Efficiency & Err. & Efficiency & Err. & Ratio & Ratio Err. \\\\ \\cline{1-8}\n")

    for year in years:
        csvF.write("\multicolumn{{1}}{{|l|}}{{\multirow{{2}}{{*}}{}}} & \multicolumn{{1}}{{|l|}}{} & {:.3e} & {:.3e} & {:.3e} & {:.3e} & {:.3f} & {} \\\\\n".format("{" + str(year) + "}", "{MagDown}",dict["Lc_{}_MagDown".format(year)]["val"],dict["Lc_{}_MagDown".format(year)]["err"],dict["Xic_{}_MagDown".format(year)]["val"],dict["Xic_{}_MagDown".format(year)]["err"],dict["Xic_{}_MagDown".format(year)]["val"]/dict["Lc_{}_MagDown".format(year)]["val"],"Todo"))
        csvF.write("\multicolumn{{1}}{{|l|}}{{}} & \multicolumn{{1}}{{|l|}}{} & {:.3e} & {:.3e} & {:.3e} & {:.3e} & {:.3f} & {} \\\\ \\cline{{1-8}}\n".format("{MagUp}",dict["Lc_{}_MagUp".format(year)]["val"],dict["Lc_{}_MagUp".format(year)]["err"],dict["Xic_{}_MagUp".format(year)]["val"],dict["Xic_{}_MagUp".format(year)]["err"],dict["Xic_{}_MagUp".format(year)]["val"]/dict["Lc_{}_MagUp".format(year)]["val"],"Todo"))

    csvF.write("\end{tabular}")
    csvF.close()

if __name__ == "__main__":
    main(sys.argv[1:])
