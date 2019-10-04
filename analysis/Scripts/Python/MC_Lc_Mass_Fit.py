import ROOT,os
from ROOT import TChain, TCanvas, TH1
from Imports import *

Lc_MC_filedir =mcpwd+"15"
Lc_MC_filename = "MC_Lc2pKpiTuple_25103006.root"

#Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree")
#excludedjobs = []

#for job in range(63) :
#    if not job in excludedjobs :
#        Lc_MC_tree.Add("{0}/{1}/output/{2}".format(Lc_MC_filedir,job,Lc_MC_filename))
Lc_MC_datatree()
c1 = ROOT.TCanvas("c1")

histogram1 = ROOT.TH1F("histogram1", "hist 1", 300, 2240, 2340)
histogram2 = ROOT.TH1F("histogram2", "hist 1", 300, 2240, 2340)
histogram1.SetLineColor(8)
histogram1.SetLineStyle(2)
histogram2.SetLineColor(46)
histogram2.SetLineStyle(2)

mass= ROOT.RooRealVar("mass","Mass",2240,2340,"MeV/c^{2}")
nbins = 300
varname = "lcplus_MM"

IDcuts = "abs(pplus1_ID)==211 && abs(kminus_ID)==321 && abs(pplus0_ID)==2212 && abs(lcplus_ID)==4122" #cuts to ensure right particles in the Monte Carlo

Lc_MC_name = Lc_MC_tree.GetName() + ""
Lc_MC_tree.Draw(varname+">>Lc_MC_masshist("+str(nbins)+","+str(2240)+","+str(2340)+")", IDcuts)
Lc_MC_masshist = ROOT.gDirectory.Get("Lc_MC_masshist")
#name2 = tree.GetName() + ""
#masshist_Lc = ROOT.gDirectory.Get(name2+"_"+varname)
Lc_MC_masshist.SetTitle(varname)
Lc_MC_masshist.GetYaxis().SetTitle("Number of events")
Lc_MC_masshist.SetLineColor(4) # blue for Data
Lc_MC_masshist.SetLineWidth(3)

Lc_MC_masshist.Draw()

gauss_mean_Lc  = ROOT.RooRealVar("gauss_mean_Lc","Mean Lc",2288,2280,2290)
gauss_width_Lc = ROOT.RooRealVar("gauss_width_Lc","Width Lc",2,0,10)
myGauss_Lc     = ROOT.RooGaussian("myGauss_Lc","Gaussian Lc", mass, gauss_mean_Lc, gauss_width_Lc)

cb_width_Lc    = ROOT.RooRealVar("cb_width_Lc","CB Width Lc",2,0,15)
cb_alpha_Lc    = ROOT.RooRealVar("cb_alpha_Lc","Exp.const Lc",1.0,0.0,5.0)
cb_n_Lc        = ROOT.RooRealVar("cb_n_Lc","Exp.crossover Lc",1.0,0.0,15.0)
# these are all the parameters required by a crystal ball shape
myCB_Lc        = ROOT.RooCBShape("myCB_Lc","Crystal Ball Lc", mass, gauss_mean_Lc, cb_width_Lc, cb_alpha_Lc, cb_n_Lc)

gauss_Norm_Lc  = ROOT.RooRealVar("gauss_Norm_Lc","Gauss Yield Lc", Lc_MC_tree.GetEntries()/nbins * 3, 0, Lc_MC_tree.GetEntries() * 2)
cb_Norm_Lc     = ROOT.RooRealVar("cb_Norm_Lc","CB Yield Lc", Lc_MC_tree.GetEntries()/nbins * 3/10, 0, Lc_MC_tree.GetEntries() * 2)

Lc_MC_Actual_signalshape = ROOT.RooAddPdf ("Lc_MC_Actual_signalshape", "Shape of the interesting events", ROOT.RooArgList(myGauss_Lc, myCB_Lc), ROOT.RooArgList(gauss_Norm_Lc, cb_Norm_Lc))
Lc_MC_Actual_signalshape_Norm = ROOT.RooRealVar("Lc_MC_Actual_signalshape_Norm","Signal Yield", Lc_MC_tree.GetEntries()/nbins * 3/10, 0, Lc_MC_tree.GetEntries() * 2)


Lc_MC_signalshape = ROOT.RooAddPdf("MC_signalshape","MC Signal shape", ROOT.RooArgList(myGauss_Lc, myCB_Lc), ROOT.RooArgList(gauss_Norm_Lc, cb_Norm_Lc) )

Lc_MC_masshist_RooFit = ROOT.RooDataHist("MC_masshist_RooFit","MC masshist RooFit", ROOT.RooArgList(mass), Lc_MC_masshist)

Lc_MC_frame = mass.frame()
Lc_MC_masshist_RooFit.plotOn(Lc_MC_frame)
Lc_MC_signalshape.plotOn(Lc_MC_frame)
Lc_MC_frame.Draw()
#fitresult = signalshape.fitTo(masshist_Lc_RooFit)
#c1.Update()
#c1.Draw()

fitresult = Lc_MC_signalshape.fitTo(Lc_MC_masshist_RooFit)
Lc_MC_frame = mass.frame()
Lc_MC_masshist_RooFit.plotOn(Lc_MC_frame)
Lc_MC_signalshape.plotOn(Lc_MC_frame, ROOT.RooFit.Components("myGauss_Lc"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2))
Lc_MC_signalshape.plotOn(Lc_MC_frame, ROOT.RooFit.Components("myCB_Lc"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
Lc_MC_signalshape.plotOn(Lc_MC_frame)
Lc_MC_frame.SetTitle("Mass fit of Lc MC")
Lc_MC_frame.GetYaxis().SetTitle("Number of events")
Lc_MC_frame.Draw()
fitresult = Lc_MC_signalshape.fitTo(Lc_MC_masshist_RooFit)
#c1.Update()
#c1.Draw()

signal_yield = gauss_Norm_Lc.getValV() + cb_Norm_Lc.getValV()
signal_error = gauss_Norm_Lc.getError() + cb_Norm_Lc.getError()
chi2ndf = Lc_MC_frame.chiSquare()
yield_string = ("N(Lc) = %.0f +- %.0f"%(signal_yield,signal_error))
chi2ndf_string = "chi^{2}/ndf = " + str(chi2ndf)
#leg = ROOT.TLegend(0.11 + 0.59, 0.77, 0.3 + 0.59, 0.89)
#leg = ROOT.TLegend(0.11,0.77,0.3,0.89)
leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Gaussian", "l")
leg.AddEntry(histogram2, "Crystal ball", "l")
leg.Draw("same")
graph_name = ("MC_Lc_Mass_Fit.pdf")
filepath = pwd
fullpath = os.path.join(filepath, graph_name)
c1.SaveAs(fullpath)


pullhist = Lc_MC_frame.pullHist()

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
Lc_MC_frame.SetTitle("Mass fit of Lc MC")
Lc_MC_frame.Draw()

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


graph_name = ("MC_Lc_Mass_Fit_pull.pdf")
filepath = pwd
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

Lc_MC_signal_yield = gauss_Norm_Lc.getValV() + cb_Norm_Lc.getValV()
Lc_MC_signal_error = gauss_Norm_Lc.getError() + cb_Norm_Lc.getError()
chi2ndf = Lc_MC_frame.chiSquare()
print("N(MC_Lc) = %.0f +- %.0f"%(Lc_MC_signal_yield,Lc_MC_signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")
