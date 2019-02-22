import ROOT, os
from ROOT import TChain, TCanvas, TH1
from Imports import *

Xic_MC_filedir = ximc2pwd+"18"
Xic_MC_filename = "MC_Lc2pKpiTuple_25103036.root"

Xic_MC_tree = TChain("tuple_Lc2pKpi/DecayTree")
excludedjobs = []
for job in range(25) :
    if not job in excludedjobs :
        #print ("- Adding subjob {0}".format(job))
        Xic_MC_tree.Add("{0}/{1}/output/{2}".format(Xic_MC_filedir,job,Xic_MC_filename))

c1 = ROOT.TCanvas("c1")

histogram1 = ROOT.TH1F("histogram1", "hist 1", 300, 2240, 2340)
histogram2 = ROOT.TH1F("histogram2", "hist 1", 300, 2240, 2340)
histogram1.SetLineColor(8)
histogram1.SetLineStyle(2)
histogram2.SetLineColor(46)
histogram2.SetLineStyle(2)

mass= ROOT.RooRealVar("mass","Mass",2420,2520,"MeV/c^{2}")
nbins = 300
varname = "lcplus_MM"

IDcuts = "abs(pplus1_ID)==211 && abs(kminus_ID)==321 && abs(pplus0_ID)==2212 && abs(lcplus_ID)==4122" #cuts to ensure right particles in the Monte Carlo

Xic_MC_name = Xic_MC_tree.GetName() + ""
Xic_MC_tree.Draw(varname+">>Xic_MC_masshist("+str(nbins)+","+str(2420)+","+str(2520)+")", IDcuts)
Xic_MC_masshist = ROOT.gDirectory.Get("Xic_MC_masshist")

Xic_MC_masshist.SetTitle(varname)
Xic_MC_masshist.GetYaxis().SetTitle("Number of events")
Xic_MC_masshist.SetLineColor(4) # blue for Data
Xic_MC_masshist.SetLineWidth(3)

Xic_MC_masshist.Draw()


# Build the variables for the Gaussian
#  Syntax is RooRealVar("name","title",initial_value,minrange,maxrange)
gauss_mean_Xic  = ROOT.RooRealVar("gauss_mean_Xic","Mean Xic",2469,2460,2480)
gauss_width_Xic = ROOT.RooRealVar("gauss_width_Xic","Width Xic",10,2,20)
myGauss_Xic     = ROOT.RooGaussian("myGauss_Xic","Gaussian Xic", mass, gauss_mean_Xic, gauss_width_Xic)


cb_width_Xic    = ROOT.RooRealVar("cb_width_Xic","CB Width Xic",6,2,20)
cb_alpha_Xic    = ROOT.RooRealVar("cb_alpha_Xic","Exp.const Xic",1.0,0.0,5.0)
cb_n_Xic        = ROOT.RooRealVar("cb_n_Xic","Exp.crossover Xic",1.0,0.0,15.0)
# these are all the parameters required by a crystal ball shape
myCB_Xic        = ROOT.RooCBShape("myCB_Xic","Crystal Ball Xic", mass, gauss_mean_Xic, cb_width_Xic, cb_alpha_Xic, cb_n_Xic)

gauss_Norm_Xic  = ROOT.RooRealVar("gauss_Norm_Xic","Gauss Yield Xic", Xic_MC_tree.GetEntries()/nbins * 3, 0, Xic_MC_tree.GetEntries() * 4)
cb_Norm_Xic     = ROOT.RooRealVar("cb_Norm_Xic","CB Yield Xic", Xic_MC_tree.GetEntries()/nbins * 3/5, 0, Xic_MC_tree.GetEntries() * 2)


Xic_MC_signalshape = ROOT.RooAddPdf("Xic_MC_signalshape","Xic MC Signal shape", ROOT.RooArgList(myGauss_Xic, myCB_Xic), ROOT.RooArgList(gauss_Norm_Xic, cb_Norm_Xic) )

Xic_MC_masshist_RooFit = ROOT.RooDataHist("Xic_MC_masshist_RooFit","Xic MC masshist RooFit", ROOT.RooArgList(mass), Xic_MC_masshist)

# Transform the histogram into something RooFit can deal with
masshist_Xic_RooFit = ROOT.RooDataHist("masshist_Xic_RooFit","masshist Xic RooFit", ROOT.RooArgList(mass), Xic_MC_masshist)

# plot everything on a frame, then plot the frame on the canvas.
# First: without fitting, to see if our initial 'guesses' are OK
frame = mass.frame()
masshist_Xic_RooFit.plotOn(frame)
Xic_MC_signalshape.plotOn(frame)
frame.Draw()
#fitresult = signalshape.fitTo(masshist_Lc_RooFit)
#c1.Update()
#c1.Draw()

fitresult = Xic_MC_signalshape.fitTo(masshist_Xic_RooFit)
frame = mass.frame()
masshist_Xic_RooFit.plotOn(frame)
Xic_MC_signalshape.plotOn(frame, ROOT.RooFit.Components("myGauss_Xic"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
Xic_MC_signalshape.plotOn(frame, ROOT.RooFit.Components("myCB_Xic"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2))
Xic_MC_signalshape.plotOn(frame)
frame.SetTitle("Mass fit of Xic MC 2")
frame.GetYaxis().SetTitle("Number of events")
frame.Draw()
fitresult = Xic_MC_signalshape.fitTo(masshist_Xic_RooFit)
#c1.Update()
#c1.Draw()

signal_yield = gauss_Norm_Xic.getValV() + cb_Norm_Xic.getValV()
signal_error = gauss_Norm_Xic.getError() + cb_Norm_Xic.getError()
chi2ndf = frame.chiSquare()
yield_string = ("N(Xic) = %.0f +- %.0f"%(signal_yield,signal_error))
chi2ndf_string = "chi^{2}/ndf = " + str(chi2ndf)
#leg = ROOT.TLegend(0.11 + 0.59, 0.77, 0.3 + 0.59, 0.89)
#leg = ROOT.TLegend(0.11,0.77,0.3,0.89)
leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Gaussian", "l")
leg.AddEntry(histogram2, "Crystal ball", "l")
leg.Draw("same")
graph_name = ("Xic_MC_2_Mass_Fit.pdf")
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
frame.SetTitle("Mass fit of Xic MC 2")
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


graph_name = ("Xic_MC_2_Mass_Fit_pull.pdf")
filepath = pwd
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

Xic_MC_signal_yield = gauss_Norm_Xic.getValV() + cb_Norm_Xic.getValV()
Xic_MC_signal_error = gauss_Norm_Xic.getError() + cb_Norm_Xic.getError()
chi2ndf = frame.chiSquare()
print("N(MC_XIc) = %.0f +- %.0f"%(Xic_MC_signal_yield,Xic_MC_signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")



