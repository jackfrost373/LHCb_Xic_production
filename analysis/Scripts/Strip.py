import ROOT, os
from ROOT import TChain, TFile

def strip_n_save (min, max, cuts, directory):


    filename = "Lc2pKpiTuple.root"

    alldata = TChain("tuple_Lc2pKpi/DecayTree")

    for job in range(min, max) :
        
        alldata.Add("{0}31/{1}/output/{2}".format(directory,job,filename))



    subtree = alldata.CopyTree( cuts )
    wfile = TFile.Open(directory + "_cluster_{0}-{1}.root".format(min, max), "RECREATE")
    wfile.cd()
    subtree.Write()
    print ("created cluster_{0}-{1}.root".format(min, max))
    wfile.Close()





