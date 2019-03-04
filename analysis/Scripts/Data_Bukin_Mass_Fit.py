import ROOT, Imports, os
from ROOT import TChain, TCanvas, TH1

particle = "Xic"

if particle == "Lc":
    mass_range = [2240, 2340]
    peak_range = [2288, 2280, 2290]
    normalisation_factor = 6
    exponential_normalisation_factor = 1
    exponential_range = [0.001, -0.2, 0.2]
    width_range = [2, 0, 10]
    


if particle == "Xic":
    mass_range = [2420, 2520]
    peak_range = [2469, 2460, 2480]
    normalisation_factor = 1
    exponential_normalisation_factor = 1
    exponential_range = [0.0, -1.0, 1.0]
    width_range = [8, 0, 20]

Imports.datatree()
tree = Imports.tree


c1 = ROOT.TCanvas("c1")

histogram1 = ROOT.TH1F("histogram1", "hist 1", 300, 2240, 2340)
histogram2 = ROOT.TH1F("histogram2", "hist 1", 300, 2240, 2340)
histogram1.SetLineColor(8)
histogram1.SetLineStyle(2)
histogram2.SetLineColor(46)
histogram2.SetLineStyle(2)
masshist = ROOT.TH1F("masshist", "Histogram of" + particle[:-1] + "_{c} mass", 300, mass_range[0], mass_range[1])
masshist.GetXaxis().SetTitle("M(" + particle[:-1] + "_{c}^{+}) [MeV/c^{2}]")
masshist.GetYaxis().SetTitle("Number of events")

mass= ROOT.RooRealVar("mass","Mass",mass_range[0],mass_range[1],"MeV/c^{2}")
nbins = 300
varname = "lcplus_MM"

DataCuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus0_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && pplus1_ProbNNpi > 0.5 && pplus0_P < 120000 && kminus_P < 115000 && pplus1_P < 80000 && pplus0_PIDp > 0 && kminus_PIDK > 0"


name2 = tree.GetName() + ""
tree.Draw(varname+">>masshist("+str(nbins)+","+str(mass_range[0])+","+str(mass_range[1])+")", DataCuts)
masshist = ROOT.gDirectory.Get("masshist")

masshist.SetTitle("Mass Fit of" + particle)
masshist.GetYaxis().SetTitle("Number of events")
masshist.SetLineColor(4)
masshist.SetLineWidth(3)

masshist.Draw()
#  Syntax is RooRealVar("name","title",initial_value,minrange,maxrange)

Bukin_Xp = ROOT.RooRealVar("Bukin_Xp", "Peak position", peak_range[0], peak_range[1], peak_range[2])
Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width", width_range[0], width_range[1], width_range[2])
Bukin_xi = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter", 0, -1, 1)
Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail", 0, -1, 1)
Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", 0, -1, 1)

Bukin_PDF = ROOT.RooBukinPdf("Bukin_PDF", "Bukin shape", mass, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)

Bukin_Norm = ROOT.RooRealVar("Bukin_Norm", "Bukin Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 2)


exponential = ROOT.RooRealVar("exponential","C", exponential_range[0], exponential_range[1], exponential_range[2])
myexponential = ROOT.RooExponential("myexponential","Exponential", mass, exponential)

exponential_Norm  = ROOT.RooRealVar("exponential_Norm","Exponential Yield", tree.GetEntries()/nbins * 3/exponential_normalisation_factor, 0, tree.GetEntries() * 2)

Actual_signalshape = ROOT.RooExtendPdf("Actual_signalshape", "Signal shape", Bukin_PDF, Bukin_Norm)
Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 3)

signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

masshist_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), masshist)

frame = mass.frame()
masshist_RooFit.plotOn(frame)
signalshape.plotOn(frame)
frame.Draw()

fitresult = signalshape.fitTo(masshist_RooFit)
frame = mass.frame()
frame.SetTitle("Bukin mass fit of " + particle)
masshist_RooFit.plotOn(frame)
signalshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2))
signalshape.plotOn(frame, ROOT.RooFit.Components("myexponential"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
signalshape.plotOn(frame)
frame.SetTitle("Bukin mass fit of " + particle)
frame.GetYaxis().SetTitle("Number of events")
frame.Draw()
fitresult = signalshape.fitTo(masshist_RooFit)


#######################
# Here is where the pull histogram is defined as well as the pads of the canvas
######################
signal_yield = Actual_signalshape_Norm.getValV()
signal_error = Actual_signalshape_Norm.getError()
chi2ndf = frame.chiSquare()

leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Signal shape", "l")
leg.AddEntry(histogram2, "Background", "l")
leg.Draw("same")
graph_name = (particle + "_Bukin_Mass_Fit.pdf")
filepath = ("/Users/simoncalo/LHCb_data")
fullpath = os.path.join(filepath, graph_name)
c1.SaveAs(fullpath)

pullhist = frame.pullHist()
    

cpull = ROOT.TCanvas("cpull","cpull",600,700)
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
frame.SetTitle("Bukin mass fit of " + particle)
frame.Draw()

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


graph_name = (particle + "_Bukin_Mass_Fit_pull.pdf")
filepath = ("/Users/simoncalo/LHCb_data")
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

signal_yield = Actual_signalshape_Norm.getValV()
signal_error = Actual_signalshape_Norm.getError()
chi2ndf = frame.chiSquare()
print("N(" + particle + ") = %.0f +- %.0f"%(signal_yield,signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")












