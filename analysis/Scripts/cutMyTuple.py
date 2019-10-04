####
#Quick and Dirty Script to Make a new nTuple which has my cuts
####

import ROOT
from Imports import *

####
#
####

particle="Lc"
ganga_job="4_reduced"
directory=pwd+ganga_job
datatree() #get the data//this TChain's the data for us...
if particle == "Lc":
        mass_cuts = "lcplus_MM < 2375"
if particle == "Xic":
        mass_cuts = "lcplus_MM > 2375"
cuts=getDataCuts() + " && " + mass_cuts #get the string which we will use for cutting the data

#tree.Print()

#Now copy my tree using the cuts

wfile = ROOT.TFile.Open("/dache/bfys/cpawley/"+ganga_job+"/"+ganga_job+"_"+particle+"cut.root","RECREATE")
wfile.cd()
cutTree=tree.CopyTree(cuts)
cutTree.Write()
wfile.Close()
