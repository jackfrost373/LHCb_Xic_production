import ROOT, os, sys, Imports
from ROOT import TChain, TFile
sys.path.append('./tuples_prep_scripts/') #step necessary to import the scripts placed in the subdirectory of the current directory
import Strip, SetBranch, SplitScript

folders_dict = Imports.getFoldersDict()  #a dictionary containing the details of the all the years' data according to joblog.txt

dir = "/dcache/bfys/scalo/"

particle = "Lc"

for element in folders_dict:
    #These commented lines should be uncommented in case nTracks is a variable needed for the PID efficiency calculation
    if int(element) < 47:
       extra_variables = ["nTracks", "lcplus_Hlt1AllL0Decision_TOS", "lcplus_Hlt2CharmHad2DHHHDecision_TOS"]
       run = 1
    else:
       extra_variables = ["Brunel_nTracks", "lcplus_Hlt1TrackMVADecision_TOS"]
       run = 2
    if (int(element) > 114 and int(element) < 118):
        particle = "Xic"
    cuts = Imports.getDataCuts(run)
    name = folders_dict[element][0]
    subjobs = folders_dict[element][1]
    saving_directory = dir + name + "_clusters/"
    os.mkdir(saving_directory)
    file_directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/" + element
    step = subjobs//20 #carry out the process in 20 clusters of datafiles to avoid memory overflow
    max = step
    min = 0

# Loop used to apply global cuts on data
        
    while (max <= subjobs):
        if max == min:
            break
        Strip.strip_n_save(min, max, cuts, file_directory, saving_directory, extra_variables, particle = particle)
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
    SplitScript.split_in_bins_n_save(final_chain, saving_dir, run, mother_particle = particle) # split the datafile into mass-y-pt bins

    print ("process completed for " + name)
