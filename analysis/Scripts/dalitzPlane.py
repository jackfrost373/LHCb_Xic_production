
#################
# Dalitz plot / sPlot
# Requires sweights script and Imports.py
#################


import ROOT
from Imports import *



# Define what type of plot you want
dataType = "MC" #dataType = MC (monte carlo), or = data
particle = "Lc" # valid types :- Xic or Lc (For MC studies)
# Define if you want to add sWeights
addsWeights = True
inputdir = pwd + "4_reduced/"
outputdir = pwd + "output/"

# Get the data
if dataType == "data":
  f = ROOT.TFile.Open(inputdir+"4_Lc_cut_reduced.root", "READONLY")
  tree = f.Get("DecayTree;48")
  cuts = "(1==1)"
elif dataType == "MC": #Todo: check both trees for updates from ganga?
  cuts = getMCCuts(particle)
  addsWeights = False  #double check to ensure sWeights never used for MC files
  if particle == "Xic":
    Xic_MC_datatree_1()
    tree = Xic_MC_tree_1 #Todo: check tree 1 or 2 or both?
  if particle == "Lc":
    Lc_MC_datatree()
    tree = Lc_MC_tree

if(addsWeights) :
  # If we made an sWeight friend tree: add it, and use sWeights. Make sure same cuts (--> #entries) as swTree!
  wfile = ROOT.TFile.Open("{0}dalitz_temp.root".format(outputdir),"RECREATE")
  swcuts = "lcplus_MM >= 2240 && lcplus_MM <= 2340 && lcplus_P >= 5000 && lcplus_P <= 200000 && lcplus_TAU >= 0 && lcplus_TAU <= 0.007"
  tree.Print()
  cuttree = tree.CopyTree(swcuts)
  print("cutTree nEvents = {0}".format(cuttree.GetEntries()))
  cuttree.AddFriend("swTree",pwd+"/output/sWeight_swTree.root")
  weightvar = "swTree.sw_sig"
else :
  cuttree = tree
  weightvar = "1"



def invariantMass(p1, p2) :
  # build invariant mass string
  m1  = p1+"_M" ; ptot1 = p1+"_P" ; px1 = p1+"_PX" ; py1 = p1+"_PY" ; pz1 = p1+"_PZ"
  m2  = p2+"_M" ; ptot2 = p2+"_P" ; px2 = p2+"_PX" ; py2 = p2+"_PY" ; pz2 = p2+"_PZ"
  E1 = "sqrt({0}**2 + {1}**2)".format(m1,ptot1)
  E2 = "sqrt({0}**2 + {1}**2)".format(m2,ptot2)
  pvecdot = "({0}*{1} + {2}*{3} + {4}*{5})".format(px1,px2, py1,py2, pz1,pz2)
  M2 = "({0}**2 + {1}**2 + 2*{2}*{3} - 2*{4})".format(m1,m2,E1,E2,pvecdot)
  return M2
  


m2_pK  = invariantMass("pplus0","kminus")
m2_Kpi = invariantMass("kminus","pplus1")

c1 = ROOT.TCanvas("c1","c1")
ROOT.gStyle.SetOptStat(0)

cuttree.Draw("{0}:{1}>>dalitzHist(100,300e3,2500e3,100,1800e3,5800e3)".format(m2_pK,m2_Kpi), "{0}*{1}".format(cuts,weightvar))
dalitzHist = ROOT.gDirectory.Get("dalitzHist")
dalitzHist.SetTitle("Dalitz plot of pK#pi")
dalitzHist.GetYaxis().SetTitle("m^{2}_{pK} [MeV^{2}/c^{4}]")
dalitzHist.GetXaxis().SetTitle("m^{2}_{K#pi} [MeV^{2}/c^{4}]")

if(addsWeights) :
  # set negative sWeight bin contents to zero for color visibility
  dalitzHist.SetMinimum(0)
  dalitzHist.SetTitle("sWeighed Dalitz plot of pK#pi")

dalitzHist.Draw("colz")
c1.Update()
c1.SaveAs(pwd+"output/Dalitz.pdf")


