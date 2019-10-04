import ROOT, os
from ROOT import TChain, TCanvas, TH1
from Imports import *

Lc_TIP_MC_datatree()
Lb_TIP_MC_datatree()

c1 = ROOT.TCanvas("c1")

DataCuts = "1==1"
Background_cuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)" #to select area of background on both sides
IDcuts = "abs(pplus1_ID)==211 && abs(kminus_ID)==321 && abs(pplus0_ID)==2212 && abs(lcplus_ID)==4122 && (lcplus_BKGCAT == 0 || lcplus_BKGCAT == 50)" #cuts to ensure right particles in the Monte Carlo
#IDcuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)"
LbIDcuts="abs(pplus1_ID)==211 && abs(kminus_ID)==321 && abs(pplus0_ID)==2212 && abs(lcplus_ID)==4122" #cuts to ensure right particles in the Monte Carlo

name = "Lc(MC)_vs_Lb(MC)"

histogram1 = ROOT.TH1F("histogram1", "Histogram of L_{c} TIP", 300, 2200, 2600)
histogram2 = ROOT.TH1F("histogram2", "Histogram of L_{b} TIP", 300, 2200, 2600)

histogram1.SetLineColor(2) # red for L_c
histogram1.SetLineWidth(1)

histogram2.SetLineColor(9) # blue for L_b
histogram2.SetLineWidth(1)
histogram1.GetXaxis().SetTitle("TIP []")
histogram2.GetXaxis().SetTitle("TIP []")
extralabel1="Lc MC"
extralabel2="Lb MC"
leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
leg.SetHeader("Legend")
leg.AddEntry(histogram1, extralabel1, "l")
leg.AddEntry(histogram2, extralabel2, "l")

plot_comparison("lcplus_TIP", -100, 120,
                        tree1=Lc_TIP_MC_tree, tree2=Lb_TIP_MC_tree,cuts1=IDcuts, cuts2=LbIDcuts,  bins=100,  extralabel1="Lc MC", extralabel2="Lb MC",
                        normalized=True, legendLocation="Right")


leg.Draw("same")
c1.SetLogy()
c1.Update()
c1.Draw()
graph_name = (name + "lcplus_TIP.pdf")
filepath = (pwd)
fullpath = os.path.join(filepath, graph_name)
c1.SaveAs(fullpath)
  
