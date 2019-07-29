import ROOT, os
from ROOT import TChain, TFile

#### This function requires a .root file as an input that in its structure has DecayTree immediately there without any intermediate structure. The TTree is divided into bins and these are saved in the saving_dir (which is a string of the saving directory) ####

def split_in_bins_n_save (root_file, saving_dir):

    ybins = [ [2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]] #Rapidity bins
    
    ptbins = [ [3000,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,20000]]  #changed the PT bins. The last bin (15k-20k) has been merged into the previous one
    
    particles = ["Lc", "Xic"]
    
    tree = root_file.Get("DecayTree")
    
    for particle in particles:
        if particle == "Lc":
            mass_cuts = "lcplus_MM < 2375"
        if particle == "Xic":
            mass_cuts = "lcplus_MM > 2375"
        for ybin in ybins:
            for ptbin in ptbins:
                yptcut = "lcplus_PT >= {0} && lcplus_PT < {1} && lcplus_RAPIDITY >= {2} && lcplus_RAPIDITY < {3}".format(ptbin[0], ptbin[1], ybin[0], ybin[1])
                allcuts = " {0} && {1}".format(yptcut, mass_cuts)
                wfile = TFile.Open(saving_dir + particle + "_bin_y{0}-{1}_pt{2}-{3}.root".format(ybin[0],ybin[1],ptbin[0],ptbin[1]), "RECREATE")
                subtree = tree.CopyTree(allcuts) #apply the cuts defined by allcuts string
                wfile.cd()
                subtree.Write()
                wfile.Close()
