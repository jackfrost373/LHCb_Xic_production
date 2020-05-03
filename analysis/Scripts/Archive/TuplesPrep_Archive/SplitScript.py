import ROOT, os, Imports
import Strip
from ROOT import TChain, TFile

#### This function requires a .root file as an input that in its structure has DecayTree immediately there without any intermediate structure. The TTree is divided into bins and these are saved in the saving_dir (which is a string of the saving directory) ####

def split_in_bins_n_save (root_file, saving_dir, run, mother_particle = "Lc"):

    ybins = Imports.getYbins() #Rapidity bins
    
    ptbins = Imports.getPTbins()

    if run == 1:
        particles = ["Lc", "Xic"]
    else:
        particles = []
        particles.append(mother_particle)
    
    os.mkdir(saving_dir + "ybins/")
    os.mkdir(saving_dir + "ptbins/")
    os.mkdir(saving_dir + "y_ptbins/")
    
    tree = root_file
    for particle in particles:
        if particle == "Lc":
            mass_cuts = "lcplus_MM < 2375"
        if particle == "Xic":
            mass_cuts = "lcplus_MM > 2375"
        for ybin in ybins:
            ycuts = "lcplus_RAPIDITY >= {0} && lcplus_RAPIDITY < {1}".format(ybin[0], ybin[1])
            allcuts = " {0} && {1}".format(ycuts, mass_cuts)
            Strip.strip_n_save(0,0, allcuts, "", saving_dir + "ybins/" + particle + "_ybin_{0}-{1}.root".format(ybin[0], ybin[1]), extra_variables = [""], bins = True, tree = tree)
            for ptbin in ptbins:
                ptcuts = "lcplus_PT >= {0} && lcplus_PT < {1}".format(ptbin[0], ptbin[1])
                if (ybin[0] == 2.0):
                    allcuts = " {0} && {1}".format(ptcuts, mass_cuts)
                    Strip.strip_n_save(0,0, allcuts, "", saving_dir + "ptbins/" + particle + "_ptbin_{0}-{1}.root".format(ptbin[0], ptbin[1]), extra_variables = [""], particle = mother_particle, bins = True,tree = tree)
                yptcut = ycuts + " && " + ptcuts
                allcuts = " {0} && {1}".format(yptcut, mass_cuts)
                Strip.strip_n_save(0,0, allcuts, "", saving_dir + "y_ptbins/" + particle + "_ybin_{0}-{1}_ptbin_{2}-{3}.root".format(ybin[0],ybin[1],ptbin[0],ptbin[1]), extra_variables = [""], particle = mother_particle, bins = True, tree = tree)
