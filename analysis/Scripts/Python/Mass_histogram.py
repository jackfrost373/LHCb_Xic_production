import ROOT, os, Imports
from ROOT import TChain, TCanvas, TH1
from Imports import *

subjobs = 101
filedir = pwd+"4_reduced"
filename = "charm_29r2_g.root"
excludedjobs = []


tree = TChain("tuple_Lc2pKpi/DecayTree")

for job in range(1, subjobs) :
        #tree.Add("{0}/{1}/output/{2}".format(filedir,job,filename))
    tree.Add(filedir + "/" + str(job) + "/output/" + filename)
    
ROOT.gStyle.SetOptStat(11111111)
c1 = ROOT.TCanvas("c1")

masshist = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)
masshist.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
masshist.GetYaxis().SetTitle("Number of events")

#DataCuts_old = "lcplus_P < 300000 && pplus0_PIDK < 21 && pplus1_PIDp < -3 && lcplus_OWNPV_CHI2 < 80 && pplus0_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && pplus1_ProbNNpi > 0.75 && pplus1_IPCHI2_OWNPV < 450 && pplus0_P < 120000 && kminus_P < 115000 && pplus1_P < 80000"

#DataCuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus0_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && pplus1_ProbNNpi > 0.5 && pplus0_P < 120000 && kminus_P < 115000 && pplus1_P < 80000 && pplus0_PIDp > 0 && kminus_PIDK > 0"

#DataCuts = "lcplus_MM > 2400 && lcplus_MM < 2450 || lcplus_MM > 2490"
DataCuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)"

#DataCuts_RICH = "pplus0_hasRich == 1 && pplus1_hasRich == 1 && kminus_hasRich == 1"

choice = input ("Do you want to draw the mass of L_{c} and Xi_{c} with the cuts? ")

if choice == "yes":
    tree.Draw("lcplus_MM>>masshist(" + str(300) + "," + str(2200) + "," + str(2550) + ")", DataCuts)
    masshist = ROOT.gDirectory.Get("masshist")
    masshist.SetTitle("Mass histogram with cuts")
    masshist.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
    masshist.GetYaxis().SetTitle("Number of events")
    c1.Update()
    c1.Draw()
    graph_name = ("mass_cut_test.pdf")
    filepath = (pwd)
    fullpath = os.path.join(filepath, graph_name)
    c1.SaveAs(fullpath)
else:
    tree.Draw("lcplus_MM>>masshist(" + str(300) + "," + str(2200) + "," + str(2600) + ")")
    masshist = ROOT.gDirectory.Get("masshist")
    masshist.SetTitle("Mass histogram without any cuts")
    masshist.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
    masshist.GetYaxis().SetTitle("Number of events")
    c1.Update()
    c1.Draw()
    graph_name = ("mass.pdf")
    filepath = (pwd)
    fullpath = os.path.join(filepath, graph_name)
    c1.SaveAs(fullpath)


