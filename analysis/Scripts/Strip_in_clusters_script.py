import ROOT, os, Imports, Strip_function
from ROOT import TChain, TFile

subjobs = 1843
#subjobs = 100
filename = "Lc2pKpiTuple.root"
excludedjobs = []

user = input("Please indicate the user (Simon, Chris or Nikhef): ")

directory = Imports.getDirectory(user) + "31"

step = subjobs//20
cuts = Imports.getDataCuts()
max = step
min = 0

while (max <= subjobs):
    Strip_function.strip_n_save(min, max, cuts, files_directory, saving_directory)
    temp = max
    if (max+step > subjobs):
        max = subjobs
    else:
        max += step
    min = temp


