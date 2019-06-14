import ROOT, os, Imports
from ROOT import TChain, TFile

# for the reduced sample, the number of subjobs is 201
subjobs = 1843
#filedir = "/Users/simoncalo/LHCb_data/datafiles/31_reduced"
filename = "Lc2pKpiTuple.root"
excludedjobs = []


#user = "Nikhef"
user = input("Please indicate the user (Simon, Chris or Nikhef): ")


directory = Imports.getDirectory(user)
Imports.datatree()
alldata = Imports.tree

#alldata = TChain("tuple_Lc2pKpi/DecayTree")

#for job in range(subjobs) :
#    if not job in excludedjobs :
#       alldata.Add("{0}/{1}/output/{2}".format(filedir,job,filename))



globalCuts = Imports.getDataCuts()

ybins = [ [2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]]

ptbins = [ [3000,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,15000], [15000,20000]]


particles = ["Lc", "Xic"]

for particle in particles:
    if particle == "Lc":
        mass_cuts = "lcplus_MM < 2375"
    if particle == "Xic":
        mass_cuts = "lcplus_MM > 2375"
    for ybin in ybins:
        for ptbin in pbtins:
            yptcut = "lcplus_PT >= {0} && lcplus_PT < {1} && lcplus_RAPIDITY >= {2} && lcplus_RAPIDITY < {3}".format(pbin[0], pbin[1], ybin[0], ybin[1])
            allcuts = "{0} && {1} && {2}".format(globalCuts, yptcut, mass_cuts)
            subtree = alldata.CopyTree(allcuts)
            wfile = TFile.Open(directory + particle + "_splitfile_y{0}-{1}_pt{2}-{3}.root".format(ybin[0],ybin[1],ptbin[0],ptbin[1]), "RECREATE")
            wfile.cd()
            subtree.Write()
            wfile.Close()

