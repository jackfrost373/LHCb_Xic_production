import ROOT, os, Imports
from ROOT import TChain, TCanvas, TH1

Imports.datatree()
Imports.Lc_MC_datatree()

c1 = ROOT.TCanvas("c1")

masshist = ROOT.TH1F("masshist", "Histogram of L_{c}^{+} mass", 300, 2200, 2600)
masshist.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
masshist.GetYaxis().SetTitle("Number of events")


DataCuts = "1==1"
Background_cuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)" #to select area of background on both sides
IDcuts = "abs(pplus1_ID)==211 && abs(kminus_ID)==321 && abs(pplus0_ID)==2212 && abs(lcplus_ID)==4122 && (lcplus_BKGCAT == 0 || lcplus_BKGCAT == 50)" #cuts to ensure right particles in the Monte Carlo
#IDcuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)"

variables_to_plot = ["lcplus_P", "lcplus_OWNPV_CHI2", "pplus0_ProbNNp", "kminus_ProbNNk", "pplus1_ProbNNpi", "pplus0_P", "kminus_P", "pplus1_P", "kminus_PIDK", "pplus0_PIDp", "lcplus_IPCHI2_OWNPV", "lcplus_ETA", "lcplus_PT", "lcplus_TAU", "lcplus_PVConstrainedDTF_chi2"]

name = "Lc_vs_MC"

histogram1 = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)
histogram2 = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)

histogram1.SetLineColor(2) # red for real background data
histogram1.SetLineWidth(1)

histogram2.SetLineColor(9) # blue for MC
histogram2.SetLineWidth(1)
extralabel1="Lc Full Background"
extralabel2="Lc MC"
leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
leg.SetHeader("Legend")
leg.AddEntry(histogram1, extralabel1, "l")
leg.AddEntry(histogram2, extralabel2, "l")

for variable in variables_to_plot:

    if variable == "lcplus_P":
        Imports.plot_comparison("lcplus_P", 15000, 400000,
                        tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts,  bins=100, cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                        normalized=True, legendLocation="Right")
        line = ROOT.TLine(300000, 0, 300000, 0.04)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "lcplus_P.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)
    elif variable == "lcplus_OWNPV_CHI2":
        Imports.plot_comparison("lcplus_OWNPV_CHI2", 0, 130,
                        tree1=Imports.tree, tree2=Imports.Lc_MC_tree,cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                        normalized=True, legendLocation="Right")

        line2 = ROOT.TLine(80, 0, 80, 0.03)
        line2.SetLineColor(2)
        line2.SetLineStyle(4)
        line2.SetLineWidth(1)
        line2.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "lcplus_OWNPV_CHI2.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)
    elif variable == "pplus0_ProbNNp":
        Imports.plot_comparison("pplus0_ProbNNp", -1, 1.5,
                        tree1=Imports.tree, tree2=Imports.Lc_MC_tree,cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                        normalized=True, legendLocation="Right")

        line = ROOT.TLine(0.5, 0, 0.5, 0.18)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "pplus0_ProbNNp.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)
    elif variable == "kminus_ProbNNk":
        Imports.plot_comparison("kminus_ProbNNk", -0.1, 1.1,
                        tree1=Imports.tree, tree2=Imports.Lc_MC_tree,cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                        normalized=True, legendLocation="Right")
        line = ROOT.TLine(0.4, 0, 0.4, 0.11)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "kminus_ProbNNk.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)

    elif variable == "pplus1_ProbNNpi":
        Imports.plot_comparison("pplus1_ProbNNpi", -0.1, 1.3,
                tree1=Imports.tree, tree2=Imports.Lc_MC_tree,cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                normalized=True, legendLocation="Right")
        line = ROOT.TLine(0.5, 0, 0.5, 0.22)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "pplus1_ProbNNpi.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)

    elif variable == "pplus0_P":
        Imports.plot_comparison("pplus0_P", 5000, 155000,
                        tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts, cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                        normalized=True, legendLocation="Right")
                        
        line = ROOT.TLine(120000, 0, 120000, 0.04)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = ( name + "pplus0_P.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)

    elif variable == "kminus_P":
        Imports.plot_comparison("kminus_P", 1000, 150000,
                        tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts, cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                        normalized=True, legendLocation="Right")
        line = ROOT.TLine(115000, 0, 115000, 0.05)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "kminus_P.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)

    elif variable == "pplus1_P":
        Imports.plot_comparison("pplus1_P", 1000, 145000,
                tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts, cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                normalized=True, legendLocation="Right")
        line = ROOT.TLine(80000, 0, 80000, 0.08)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "pplus1_P.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)

    elif variable == "kminus_PIDK":
        Imports.plot_comparison("kminus_PIDK", -20, 100,
                tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts, cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                normalized=True, legendLocation="Right")
        line = ROOT.TLine(0, 0, 0, 0.03)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "kminus_PIDK.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)

    elif variable == "pplus0_PIDp":
        Imports.plot_comparison("pplus0_PIDp", -20, 100,
                tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                normalized=True, legendLocation="Right")
        line = ROOT.TLine(0, 0, 0, 0.03)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw()
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "pplus0_PIDp.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)
    elif variable == "lcplus_IPCHI2_OWNPV":
        Imports.plot_comparison("lcplus_IPCHI2_OWNPV", -5, 12,
                            tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                            normalized=True, legendLocation="Right")

        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + "lcplus_IPCHI2_OWNPV.pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)
    elif variable == "lcplus_ETA":
        Imports.plot_comparison(variable, -2, 20,
                            tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                            normalized=True, legendLocation="Right")
        
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + variable + ".pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)
    elif variable == "lcplus_PT":
        Imports.plot_comparison(variable, 20, 18000,
                        tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                        normalized=True, legendLocation="Right")

        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + variable + ".pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)
    elif variable == "lcplus_TAU":
        Imports.plot_comparison(variable, 0, 0.006,
                            tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",
                            normalized=True, legendLocation="Right")
        
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + variable + ".pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)
    elif variable == "lcplus_PVConstrainedDTF_chi2":
        Imports.plot_comparison(variable, -50, 50,tree1=Imports.tree, tree2=Imports.Lc_MC_tree, cuts1=Background_cuts,  cuts2=IDcuts, extralabel1="background data", extralabel2="Monte Carlo",normalized=True, legendLocation="Right")
        
        leg.Draw("same")
        c1.Update()
        c1.Draw()
        graph_name = (name + variable + ".pdf")
        filepath = ("/Users/simoncalo/LHCb_data")
        fullpath = os.path.join(filepath, graph_name)
        c1.SaveAs(fullpath)


