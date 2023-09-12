
import ROOT
ROOT.gStyle.SetOptStat(0)
from array import array
from math import sqrt


def calcEff(N, k) :
  p = k / N
  e = sqrt(N * p * (1-p)) / N
  return p,e


fAll = ROOT.TFile.Open("Lc2pKpi_tree.root")
fCut = ROOT.TFile.Open("Lc2pKpi_tightcuts_tree.root")

tAll = fAll.Get("DecayTree")
tCut = fCut.Get("DecayTree")

ptbins = [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 15.0, 20.0]
ybins  = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
ptbins_c = array('f', ptbins)
ybins_c = array('f', ybins)


nAll = tAll.GetEntries()
nCut = tCut.GetEntries()
eff,err = calcEff(nAll, nCut)
print("nEntries all: {}".format(nAll))
print("nEntries cut: {}".format(nCut))
print(" -> overall Gen. level efficiency: {:.3f} +- {:.3f} %".format(eff*100, err*100))


c1 = ROOT.TCanvas("c1")

yhist_all = ROOT.TH1F("yhist_all", "yhist_all", len(ybins)-1, ybins_c)
yhist_cut = ROOT.TH1F("yhist_cut", "yhist_cut", len(ybins)-1, ybins_c)
yhist_eff = ROOT.TH1F("yhist_eff", "yhist_eff", len(ybins)-1, ybins_c)

for hist in yhist_cut, yhist_all, yhist_eff :
  hist.SetTitle("#Lambda_{c} tightcut (25103064) vs PHSP rapidsim")
  hist.GetXaxis().SetTitle("#Lambda_{c} y")

tAll.Draw("Lc_y>>+yhist_all")
tCut.Draw("Lc_y>>+yhist_cut")


yhist_all.SetLineColor(9)
yhist_all.SetLineWidth(2)
yhist_all.Draw("E1")
yhist_all.GetYaxis().SetRangeUser(0., nAll/len(ybins)*2)
yhist_cut.SetLineColor(8)
yhist_cut.SetLineWidth(2)
yhist_cut.Draw("E1SAME")
c1.Update()
c1.SaveAs("plots/Lc_yhist_yields.pdf")

print("\nGen. level effs:")
print("ybin \t\t eff \t +- err")
#yhist_cut.Divide(yhist_all)
for ibin in range(len(ybins)-1) :
  v_all = yhist_all.GetBinContent(ibin+1)
  v_cut = yhist_cut.GetBinContent(ibin+1)
  v_eff,v_err = calcEff(v_all, v_cut)
  yhist_eff.SetBinContent(ibin+1, v_eff*100)
  yhist_eff.SetBinError(  ibin+1, v_err*100)
  print("{}-{}\t\t {:.2f} \t +- {:.2f}".format(ybins[ibin], ybins[ibin+1], v_eff*100, v_err*100))

yhist_eff.GetYaxis().SetRangeUser(0., eff*100*2)
yhist_eff.GetYaxis().SetTitle("Gen. level efficiency [%]")
yhist_eff.SetLineColor(46)
yhist_eff.SetLineWidth(2)
yhist_eff.Draw("E1")

c1.Update()
c1.SaveAs("plots/Lc_yhist_eff.pdf")

