#This script is used to fit all of the datafiles split into bins in a loop, by calling the Universal mass fit function on the data

import ROOT, os, Universal_Mass_Fit_function
from ROOT import TChain, TFile
from Universal_Mass_Fit_function import Shape_fit

user = "Nikhef"
#shape = "Bukin" # select the shape that you want to fit your data with
shape = input("please indicate the PDF (GaussCB, Bukin, Ipatia or Apolonios): ")
particles = ["Lc", "Xic"]

directory = Imports.getDirectory(user)


ybins = [ [2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]] # Rapidity bins

ptbins = [ [3000,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,15000]] # Transverse momentum bins

text = open(directory + "Output.txt", "w+") # This is the text file in which all of the interesting parameters from the fit are printed

# loop used to fit all the bins and print all of the interesting parameters of the fit
for particle in particles:
    for ybin in ybins:
        for ptbin in ptbins:
            location = (directory + particle + "_splitfile_y{0}-{1}_pt{2}-{3}.root".format(ybin[0],ybin[1],ptbin[0],ptbin[1]))
            file = ROOT.TFile(location, "READONLY")
            tree = file.Get("DecayTree")
            text.write(Shape_fit(shape, tree, particle, ybin, ptbin, Data = True, Pull = False, user = user))
            file.Close()
                    
text.close()
