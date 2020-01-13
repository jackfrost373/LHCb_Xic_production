import ROOT, os, SetBranch
from ROOT import TChain, TFile

#### Function that takes as inputs: min and max which are 2 integers that indicates from which subjob to which subjob the TChain ranges; cuts are the cuts applied to the TTrees; directory is the directory in which the subjobs are to be found and saving_directory is the directory in which the stripped files are then saved. ####

def strip_n_save (min, max, cuts, directory, saving_directory, extra_variables, particle = "Lc", bins = False, tree = None):
    
    if not (bins):
        filename = "{0}2pKpiTuple.root".format(particle)
        alldata = TChain("tuple_{0}2pKpi/DecayTree".format(particle))
        extra_dir = ""
        for job in range(min, max) :
            alldata.Add("{0}/{1}{2}/{3}".format(directory,job,extra_dir,filename))
    
    #Check if there are any issues with the data
        if (alldata.GetEntries() == 0):
            print("Error: entries = 0 for range " + str(min) + "-" + str(max))
            return
        if (alldata.GetEntries() == -1):
            print("Error: entries = -1 for range " + str(min) + "-" + str(max))
            return

        alldata = SetBranch.setBranch_funct(alldata, extra_variables)
        extra_string = "_cluster_{0}-{1}.root".format(min, max)
    else:
        if not (tree == None):
            alldata = tree
        extra_string = ""
      
    wfile = TFile.Open(saving_directory + extra_string, "RECREATE")
    subtree = alldata.CopyTree( cuts )
    wfile.cd()
    subtree.Write()
    wfile.Close()
