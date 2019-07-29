import ROOT, os
from ROOT import TChain, TCanvas, TH1
from Imports import *

subjobs = 101
filedir = pwd+"/4_reduced"
filename = "charm_29r2_g.root"
excludedjobs = []

tree = TChain("tuple_Lc2pKpi/DecayTree")

for job in range(1, subjobs) :
    if not job in excludedjobs :
        tree.Add("{0}/{1}/output/{2}".format(filedir,job,filename))


c1 = ROOT.TCanvas("c1")

masshist_Lc = ROOT.TH1F("masshist_Lc", "Histogram of L_{c} mass", 300, 2240, 2340)
masshist_Lc.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
masshist_Lc.GetYaxis().SetTitle("Number of events")

mass= ROOT.RooRealVar("mass","Mass",2420,2520,"MeV/c^{2}")
nbins = 300
varname = "lcplus_MM"

DataCuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus0_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && pplus1_ProbNNpi > 0.5 && pplus0_P < 120000 && kminus_P < 115000 && pplus1_P < 80000 && pplus0_PIDp > 0 && kminus_PIDK > 0"


name2 = tree.GetName() + ""
tree.Draw(varname+">>masshist_Lc("+str(nbins)+","+str(2420)+","+str(2520)+")", DataCuts)
masshist_Lc = ROOT.gDirectory.Get("masshist_Lc")
#name2 = tree.GetName() + ""
#masshist_Lc = ROOT.gDirectory.Get(name2+"_"+varname)
masshist_Lc.SetTitle("Mass Fit of Xic")
masshist_Lc.GetYaxis().SetTitle("Number of events")
masshist_Lc.SetLineColor(4) # blue for Data
masshist_Lc.SetLineWidth(3)
histogram1 = ROOT.TH1F("histogram1", "hist 1", 300, 2240, 2340)
histogram2 = ROOT.TH1F("histogram2", "hist 1", 300, 2240, 2340)
histogram1.SetLineColor(8)
histogram1.SetLineStyle(2)
histogram2.SetLineColor(46)
histogram2.SetLineStyle(2)


#masshist_Lc = ROOT.gDirectory.Get(name2+"_"+varname)
masshist_Lc.Draw()
# Build the variables for the Gaussian
#  Syntax is RooRealVar("name","title",initial_value,minrange,maxrange)
gauss_mean_Lc  = ROOT.RooRealVar("gauss_mean_Lc","Mean Lc",2470,2460,2480)
gauss_width_Lc = ROOT.RooRealVar("gauss_width_Lc","Width Lc",8,2,20)
myGauss_Lc     = ROOT.RooGaussian("myGauss_Lc","Gaussian Lc", mass, gauss_mean_Lc, gauss_width_Lc)

exponential_Lc = ROOT.RooRealVar("exponential_Lc","C", 0.0, -1.0, 1.0)
myexponential_Lc = ROOT.RooExponential("myexponential_Lc","Exponential", mass, exponential_Lc)

cb_width_Lc    = ROOT.RooRealVar("cb_width_Lc","CB Width Lc",6,2,20)
cb_alpha_Lc    = ROOT.RooRealVar("cb_alpha_Lc","Exp.const Lc",1.0,0.0,5.0)
cb_n_Lc        = ROOT.RooRealVar("cb_n_Lc","Exp.crossover Lc",1.0,0.0,15.0)
# these are all the parameters required by a crystal ball shape
myCB_Lc        = ROOT.RooCBShape("myCB_Lc","Crystal Ball Lc", mass, gauss_mean_Lc, cb_width_Lc, cb_alpha_Lc, cb_n_Lc)

gauss_Norm_Lc  = ROOT.RooRealVar("gauss_Norm_Lc","Gauss Yield Lc", tree.GetEntries()/nbins * 3, 0, tree.GetEntries() * 4)
cb_Norm_Lc     = ROOT.RooRealVar("cb_Norm_Lc","CB Yield Lc", tree.GetEntries()/nbins * 3/5, 0, tree.GetEntries() * 2)
exponential_Norm_Lc  = ROOT.RooRealVar("exponential_Norm_Lc","Exponential Yield Lc", tree.GetEntries()/nbins * 3, 0, tree.GetEntries() * 2)

Actual_signalshape = ROOT.RooAddPdf ("Actual_signalshape", "Shape of the interesting events", ROOT.RooArgList(myGauss_Lc, myCB_Lc), ROOT.RooArgList(gauss_Norm_Lc, cb_Norm_Lc))
Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", tree.GetEntries()/nbins * 3/2, 0, tree.GetEntries() * 2)

signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential_Lc), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm_Lc) )


# Transform the histogram into something RooFit can deal with
masshist_Lc_RooFit = ROOT.RooDataHist("masshist_Lc_RooFit","masshist Lc RooFit", ROOT.RooArgList(mass), masshist_Lc)

# plot everything on a frame, then plot the frame on the canvas.
# First: without fitting, to see if our initial 'guesses' are OK
frame = mass.frame()
masshist_Lc_RooFit.plotOn(frame)
signalshape.plotOn(frame)
frame.Draw()
#fitresult = signalshape.fitTo(masshist_Lc_RooFit)
#c1.Update()
#c1.Draw()

fitresult = signalshape.fitTo(masshist_Lc_RooFit)
frame = mass.frame()
masshist_Lc_RooFit.plotOn(frame)
signalshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2))
signalshape.plotOn(frame, ROOT.RooFit.Components("myexponential_Lc"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
signalshape.plotOn(frame)
frame.SetTitle("Mass fit of Xic")
frame.GetYaxis().SetTitle("Number of events")
frame.Draw()
fitresult = signalshape.fitTo(masshist_Lc_RooFit)
#c1.Update()
#c1.Draw()

signal_yield = Actual_signalshape_Norm.getValV()
signal_error = Actual_signalshape_Norm.getError()
chi2ndf = frame.chiSquare()
yield_string = ("N(Xic) = %.0f +- %.0f"%(signal_yield,signal_error))
chi2ndf_string = "chi^{2}/ndf = " + str(chi2ndf)
#leg = ROOT.TLegend(0.11 + 0.59, 0.77, 0.3 + 0.59, 0.89)
#leg = ROOT.TLegend(0.11,0.77,0.3,0.89)
leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Signal Shape", "l")
leg.AddEntry(histogram2, "Background", "l")
leg.Draw("same")
graph_name = ("Xic_Mass_Fit.pdf")
filepath = pwd
fullpath = os.path.join(filepath, graph_name)
c1.SaveAs(fullpath)

pullhist = frame.pullHist()

# Define a new canvas. We are going to split it into two pads.
cpull = ROOT.TCanvas("cpull","cpull",600,700)
# add two TPads in the single canvas
pullpad1 = ROOT.TPad("pullpad1", "",0.0,0.25,1.0,1.0)
pullpad2 = ROOT.TPad("pullpad2", "",0.0,0.0,1.0,0.25)

# Set the right margins
pullpad1.SetTopMargin(0.05)
pullpad1.SetBottomMargin(0)
pullpad1.SetLeftMargin(0.12)
pullpad1.SetRightMargin(0.05)
pullpad2.SetTopMargin(0)
pullpad2.SetBottomMargin(0.25)
pullpad2.SetLeftMargin(0.12)
pullpad2.SetRightMargin(0.05)

# plot the 'normal' frame on the top pad, this contained our fit curve and data
pullpad1.cd()
frame.SetTitle("Mass fit of Xic")
frame.Draw()

# Now let's plot the pullhist on the bottom pad, and make the labels the right size
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

# Draw the pads on the canvas
cpull.cd()
pullpad1.Draw()
pullpad2.Draw()
leg.Draw("same")
cpull.Update()
cpull.Draw()


graph_name = ("Xic_Mass_Fit_pull.pdf")
filepath = pwd
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

signal_yield = Actual_signalshape_Norm.getValV()
signal_error = Actual_signalshape_Norm.getError()
chi2ndf = frame.chiSquare()
print("N(Xic) = %.0f +- %.0f"%(signal_yield,signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")









