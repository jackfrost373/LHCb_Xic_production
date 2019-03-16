import ROOT, os, Data_Bukin_Mass_Fit_function
from ROOT import TChain, TFile
from Data_Bukin_Mass_Fit_function import Bukin_fit

user = "Simon"

if user == "Simon":
    directory = "/Users/simoncalo/LHCb_data/datafiles/"
elif user == "Chris":
    directory = ""
elif user == "Jacco":
    directory = ""


ybins = [ [2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]]

pbins = [ [3000,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,15000], [15000,20000]]

text = open("/Users/simoncalo/LHCb_data/Output.txt", "w+")
particles = ["Lc", "Xic"]

for particle in particles:
    for ybin in ybins:
        for pbin in pbins:
            location = (directory + particle + "_splitfile_y{0}-{1}_p{2}-{3}.root".format(ybin[0],ybin[1],pbin[0],pbin[1]))
            file = ROOT.TFile(location, "READONLY")
            tree = file.Get("DecayTree")
                        #tree.SetName("tree")
            text.write(Bukin_fit(tree, particle, ybin, pbin))
                    
                    
text.close()
