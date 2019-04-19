import ROOT, os, Imports
from ROOT import TChain, TFile

subjobs = 201
filedir = "/Users/simoncalo/LHCb_data/datafiles/31_reduced"
filename = "Lc2pKpiTuple.root"
excludedjobs = []

user = "Simon"


if user == "Simon":
    directory = "/Users/simoncalo/LHCb_data/datafiles/"
elif user == "Chris":
    directory = ""
elif user == "Jacco":
    directory = ""


alldata = TChain("tuple_Lc2pKpi/DecayTree")

for job in range(1, subjobs) :
    if not job in excludedjobs :
        alldata.Add("{0}/{1}/output/{2}".format(filedir,job,filename))

#globalCuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus0_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && pplus1_ProbNNpi > 0.5 && pplus0_P < 120000 && kminus_P < 115000 && pplus1_P < 80000 && pplus0_PIDp > 0 && kminus_PIDK > 0"

globalCuts = Imports.getDataCuts()

ybins = [ [2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]]

pbins = [ [3000,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,15000], [15000,20000]]

particles = ["Lc", "Xic"]

for particle in particles:
    if particle == "Lc":
        mass_cuts = "lcplus_MM < 2375"
    if particle == "Xic":
        mass_cuts = "lcplus_MM > 2375"
    for ybin in ybins:
        for pbin in pbins:
            yptcut = "lcplus_PT >= {0} && lcplus_PT < {1} && lcplus_RAPIDITY >= {2} && lcplus_RAPIDITY < {3}".format(pbin[0], pbin[1], ybin[0], ybin[1])
            allcuts = "{0} && {1} && {2}".format(globalCuts, yptcut, mass_cuts)
            subtree = alldata.CopyTree(allcuts)
            wfile = TFile.Open(directory + particle + "_splitfile_y{0}-{1}_p{2}-{3}.root".format(ybin[0],ybin[1],pbin[0],pbin[1]), "RECREATE")
            wfile.cd()
            subtree.Write()
            wfile.Close()





