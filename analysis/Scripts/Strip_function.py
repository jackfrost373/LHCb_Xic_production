import ROOT, os
from ROOT import TChain, TFile

#This function allows you to strip your data, in the sense of eliminating the events which do not conform to your interests. This is done in clusters of subjobs to avoid overloading the memory.
#min corresponds to the lowest subjob number, max to the highest (this will be clearer in the for loop), cuts corresponds to the cuts that want to be applied and the directory is both the directory of the files that are TChained and the directory in which the stripped file will be saved.

def strip_n_save (min, max, cuts, files_directory, saving_directory):


    filename = "Lc2pKpiTuple.root" #This filename is kept as such because for this analysis all of the tuples have this name, but it should become an input parameter for a more reusable version

    alldata = TChain("tuple_Lc2pKpi/DecayTree")

    for job in range(min, max) :
        
        alldata.Add("{0}/{1}/output/{2}".format(files_directory,job,filename))
    
    #Open (or create in this case) a file where you are going to save your TTree (or TChain)
    wfile = TFile.Open(saving_directory + "_cluster_{0}-{1}.root".format(min, max), "RECREATE")
    #copy the tree, but with the desired cuts
    subtree = alldata.CopyTree( cuts )
    wfile.cd()
    subtree.Write()
    print ("created cluster_{0}-{1}.root".format(min, max))
    wfile.Close()





