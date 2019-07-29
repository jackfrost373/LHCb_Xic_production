import ROOT,Imports, os
from ROOT import TChain, TCanvas, TH1

particle = "Lc"

if particle == "Lc":
    mass_range = [2240, 2340]
    peak_range = [2288, 2280, 2290]
    peak_width = [2, 0, 10]
    normalisation_factor = 6

    Imports.Lc_MC_datatree()
    MC_tree = Imports.Lc_MC_tree


if particle == "Xic":
    mass_range = [2420, 2520]
    peak_range = [2469, 2460, 2480]
    peak_width = [8, 0, 20]
    normalisation_factor = 4
    
    Imports.Xic_MC_datatree_1()
    MC_tree = Imports.Xic_MC_tree_1


c1 = ROOT.TCanvas("c1")

histogram1 = ROOT.TH1F("histogram1", "hist 1", 300, 2240, 2340)
histogram1.SetLineColor(9)
histogram1.SetLineWidth(1)


mass= ROOT.RooRealVar("mass","Mass",mass_range[0],mass_range[1],"MeV/c^{2}")
nbins = 300
varname = "lcplus_MM"

IDcuts = "abs(pplus1_ID)==211 && abs(kminus_ID)==321 && abs(pplus0_ID)==2212 && abs(lcplus_ID)==4122" #cuts to ensure right particles in the Monte Carlo

MC_name = MC_tree.GetName() + ""
MC_tree.Draw(varname+">>MC_masshist("+str(nbins)+","+str(mass_range[0])+","+str(mass_range[1])+")", IDcuts)
MC_masshist = ROOT.gDirectory.Get("MC_masshist")
#name2 = tree.GetName() + ""
#masshist_Lc = ROOT.gDirectory.Get(name2+"_"+varname)
MC_masshist.SetTitle(varname)
MC_masshist.GetYaxis().SetTitle("Number of events")
MC_masshist.SetLineColor(4) # blue for Data
MC_masshist.SetLineWidth(3)

MC_masshist.Draw()

Bukin_Xp = ROOT.RooRealVar("Bukin_Xp", "Peak position", peak_range[0], peak_range[1], peak_range[2])
Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width", peak_width[0], peak_width[1], peak_width[2])
Bukin_xi = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter", 0, -1, 1)
Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail", 0, -1, 1)
Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", 0, -1, 1)

Bukin_PDF = ROOT.RooBukinPdf("Bukin_PDF", "Bukin shape", mass, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)

Bukin_Norm = ROOT.RooRealVar("Bukin_Norm", "Bukin Yield", MC_tree.GetEntries()/nbins * 3/normalisation_factor, 0, MC_tree.GetEntries() * 2)

MC_masshist_RooFit = ROOT.RooDataHist("MC_masshist_RooFit","MC masshist RooFit", ROOT.RooArgList(mass), MC_masshist)

MC_signalshape = ROOT.RooExtendPdf("MC_signalshape", "Signal shape", Bukin_PDF, Bukin_Norm)


MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)
MC_signalshape.plotOn(MC_frame)
MC_frame.Draw()

fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)
MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)

MC_signalshape.plotOn(MC_frame)
MC_frame.SetTitle("Bukin mass fit of " + particle +  " MC")
MC_frame.GetYaxis().SetTitle("Number of events")
MC_frame.Draw()
fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)

leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Bukin Pdf", "l")
leg.Draw("same")
graph_name = ("MC_" + particle + "_Bukin_Mass_Fit.pdf")
filepath = ("/Users/simoncalo/LHCb_data")
fullpath = os.path.join(filepath, graph_name)
c1.SaveAs(fullpath)


pullhist = MC_frame.pullHist()

cpull = ROOT.TCanvas("cpull","cpull",600,700)
# add two TPads in the single canvas
pullpad1 = ROOT.TPad("pullpad1", "",0.0,0.25,1.0,1.0)
pullpad2 = ROOT.TPad("pullpad2", "",0.0,0.0,1.0,0.25)

pullpad1.SetTopMargin(0.05)
pullpad1.SetBottomMargin(0)
pullpad1.SetLeftMargin(0.12)
pullpad1.SetRightMargin(0.05)
pullpad2.SetTopMargin(0)
pullpad2.SetBottomMargin(0.25)
pullpad2.SetLeftMargin(0.12)
pullpad2.SetRightMargin(0.05)

pullpad1.cd()
MC_frame.SetTitle("Bukin mass fit of " + particle +  " MC")
MC_frame.Draw()

pullpad2.cd()
framepull = mass.frame()
framepull.addPlotable(pullhist)
framepull.SetTitle("")
framepull.GetYaxis().SetTitle("Pull")
framepull.GetYaxis().SetTitleOffset(0.4)
framepull.GetYaxis().SetTitleSize(0.1)
framepull.GetYaxis().SetLabelSize(0.1)
framepull.GetXaxis().SetTitleSize(0.1)
framepull.GetXaxis().SetLabelSize(0.1)
framepull.Draw()

cpull.cd()
pullpad1.Draw()
pullpad2.Draw()
leg.Draw("same")
cpull.Update()
cpull.Draw()

graph_name = ("MC_" + particle + "_Bukin_Mass_Fit_pull.pdf")
filepath = ("/Users/simoncalo/LHCb_data")
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

MC_signal_yield = Bukin_Norm.getValV()
MC_signal_error = Bukin_Norm.getError()
chi2ndf = MC_frame.chiSquare()
print("N(MC_Lc) = %.0f +- %.0f"%(MC_signal_yield,MC_signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")
