import ROOT, os, Imports, Strip
from ROOT import TChain, TFile

subjobs = 1843
#subjobs = 100
filename = "Lc2pKpiTuple.root"
excludedjobs = []

user = input("Please indicate the user ")

directory = Imports.getDirectory(user)

step = subjobs//20
cuts = Imports.getDataCuts()
max = step
min = 1

while (max <= subjobs):
    Strip.strip_n_save(min, max, cuts, directory)
    temp = max
    if (max+step > subjobs):
        max = subjobs
    else:
        max += step
    min = temp


