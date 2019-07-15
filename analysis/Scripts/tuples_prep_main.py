import ROOT, os, sys, Imports
from ROOT import TChain, TFile
sys.path.append('./tuples_prep_scripts/') #step necessary to import the scripts placed in the subdirectory of the current directory
import Strip, SetBranch, SplitScript

folders_dict = {"39":["2018_MagDown",2155] , "31":["2017_MagDown", 1843], "40":["2016_MagDown",1859], "41":["2015_MagDown", 579], "42":["2012_MagDown", 1155], "43":["2011_MagDown", 907], "45":["2011_MagUp", 817], "46":["2012_MagUp", 1342], "47":["2015_MagUp", 370], "48":["2016_MagUp", 1771], "49":["2017_MagUp", 1839], "50":["2018_MagUp", 2298] } #a dictionary containing the details of the all the years' data according to joblog.txt

cuts = Imports.getDataCuts()
dir = "/dcache/bfys/scalo/"
os.mkdir(dir + "pruned_trees")

for element in folders_dict:
    name = folders_list[element][0]
    subjobs = folders_list[element][1]
    saving_directory = dir + name + "_clusters/"
    os.mkdir(saving_directory)
    file_directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/" + element
        
    step = subjobs//20 #carry out the process in 20 clusters of datafiles to avoid memory overflow
    max = step
    min = 0

# Loop used to apply global cuts on the data
        
    while (max <= subjobs):
        if max == min:
            break
        Strip.strip_n_save(min, max, cuts, file_directory, saving_directory)
        temp = max
        if (max+step > subjobs):
            max = subjobs
        else:
            max += step
        min = temp

    clusters = os.listdir(saving_directory)

    tree_file = TFile.Open(dir + "pruned_trees/" + name + "_stripped&pruned.root", "RECREATE")
    tree = TChain("tuple_Lc2pKpi/DecayTree")

# Loop used to set branches on the trees. To modify the branches see SetBranch script

    for element in clusters:
        element = SetBranch.setBranch_funct(element) #see comment below
        tree.Add(str(element))

#tree = SetBranch.setBranch_funct(tree) #perhaps move this step within the for loop above to speed up the process or will this make it slower since it is repeated many times? If this line is kept, the object fed into setBranch becomes a TTree and not a .root file
    tree_file.cd()
    tree.Write()
    tree_file.Close()
    print("created full TChain stripped with global cuts and pruned tree of " + name)

    os.mkdir(dir + name + "/bins")
    saving_dir = dir + name + "/bins/"
    root_file = dir + "pruned_trees/" + name + "_stripped&pruned.root"
    SplitScript.split_in_bins&save(root_file, saving_dir) # split the datafile into mass-y-pt bins

    print ("process completed for " + name)
