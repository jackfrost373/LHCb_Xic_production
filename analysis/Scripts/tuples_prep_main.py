import ROOT, os, sys, Imports
from ROOT import TChain, TFile
sys.path.append('./tuples_prep_scripts/') #step necessary to import the scripts placed in the subdirectory of the current directory
import Strip, SetBranch, SplitScript

folders_dict = Imports.getFoldersDict()  #a dictionary containing the details of the all the years' data according to joblog.txt

cuts = Imports.getDataCuts()
dir = "/dcache/bfys/scalo/"


extra_variable = ""

for element in folders_dict:
    #These commented lines should be uncommented in case nTracks is a variable needed for the PID efficiency calculation
    #if int(element) > 41 && int(element) < 47:
    #   extra_variable = "nTracks"
    #else:
    #   extra_variable = "Brunel_nTracks"
    name = folders_dict[element][0]
    subjobs = folders_dict[element][1]
    saving_directory = dir + name + "_clusters/"
    os.mkdir(saving_directory)
    file_directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/" + element
    y_2017 = False
    if element == "31":
        y_2017 = True
        
    step = subjobs//20 #carry out the process in 20 clusters of datafiles to avoid memory overflow
    max = step
    min = 0

# Loop used to apply global cuts on the data
        
    while (max <= subjobs):
        if max == min:
            break
        Strip.strip_n_save(min, max, cuts, file_directory, saving_directory, y_2017)
        temp = max
        if (max+step > subjobs):
            max = subjobs
        else:
            max += step
        min = temp

    clusters = os.listdir(saving_directory)

    final_chain = TChain("DecayTree")
    for element in clusters:
        final_chain.Add(saving_directory + element)

    os.mkdir(dir + name)
    os.mkdir(dir + name + "/bins")
    saving_dir = dir + name + "/bins/"
    SplitScript.split_in_bins_n_save(final_chain, saving_dir) # split the datafile into mass-y-pt bins

    print ("process completed for " + name)
