import ROOT, os
from ROOT import TChain, TCanvas, TH1
import ROOT.Ostap as Ostap
from Imports import *

particle = "Xic"

if particle == "Lc":
    mass_range = [2240, 2340]
    peak_range = [2288, 2270, 2300]
    peak_width = [2, 0, 40]
    normalisation_factor = 6

    Lc_MC_datatree()
    MC_tree = Lc_MC_tree


if particle == "Xic":
    mass_range = [2420, 2520]
    peak_range = [2469, 2460, 2480]
    peak_width = [8, 0, 20]
    normalisation_factor = 4
    
    Xic_MC_datatree_1()
    MC_tree = Xic_MC_tree_1


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

Bukin_PDF = Ostap.Models.Bukin("Bukin_PDF", "Bukin shape", mass, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)

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
filepath = (pwd)
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
filepath = (pwd)
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

MC_signal_yield = Bukin_Norm.getValV()
MC_signal_error = Bukin_Norm.getError()
chi2ndf = MC_frame.chiSquare()
print("N(MC_Lc) = %.0f +- %.0f"%(MC_signal_yield,MC_signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")


Apolo_Mu = ROOT.RooRealVar("Apolo_Mu", "Peak width",  peak_range[0], peak_range[1], peak_range[2])
Apolo_Beta = ROOT.RooRealVar("Apolo_Beta", "Beta", 1, 0, 25)
Apolo_Sig1 = ROOT.RooRealVar("Apolo_Sig1", "Sigma1",peak_width[0], peak_width[1], peak_width[2])
Apolo_Sig2 = ROOT.RooRealVar("Apolo_Sig2", "Sigma2", peak_width[0], peak_width[1], peak_width[2])

Apolo_PDF = Ostap.Models.Apolonios2("Apolo_PDF", "Apolonios shape", mass, Apolo_Mu, Apolo_Sig1, Apolo_Sig2, Apolo_Beta)

Apolo_Norm = ROOT.RooRealVar("Apolo_Norm", "Apolo Yield", MC_tree.GetEntries()/nbins * 3/normalisation_factor, 0, MC_tree.GetEntries() * 2)

MC_masshist_RooFit = ROOT.RooDataHist("MC_masshist_RooFit","MC masshist RooFit", ROOT.RooArgList(mass), MC_masshist)

MC_signalshape = ROOT.RooExtendPdf("MC_signalshape", "Signal shape", Apolo_PDF, Apolo_Norm)


MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)
MC_signalshape.plotOn(MC_frame)
MC_frame.Draw()

fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)
MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)

MC_signalshape.plotOn(MC_frame)
MC_frame.SetTitle("Apolo mass fit of " + particle +  " MC")
MC_frame.GetYaxis().SetTitle("Number of events")
MC_frame.Draw()
fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)

leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Apolo Pdf", "l")
leg.Draw("same")
graph_name = ("MC_" + particle + "_Apolonios_Mass_Fit.pdf")
filepath = (pwd)
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
MC_frame.SetTitle("Apolo mass fit of " + particle +  " MC")
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

graph_name = ("MC_" + particle + "_Apolonios_Mass_Fit_pull.pdf")
filepath = (pwd)
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

MC_signal_yield = Apolo_Norm.getValV()
MC_signal_error = Apolo_Norm.getError()
chi2ndf = MC_frame.chiSquare()
print("N(MC_Lc) = %.0f +- %.0f"%(MC_signal_yield,MC_signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")


###################
#  Ipatia 2 - needs a source file -
#  https://github.com/GerhardRaven/P2VV/blob/master/P2VV/RooIpatia2.h
#  Documentation at https://arxiv.org/pdf/1312.5000.pdf
###################
# load the source file

#ROOT.gROOT.ProcessLine(".L -std=c++14 src/RooIpatia2.cxx++g")
ROOT.gROOT.ProcessLine(".L src/RooIpatia2_cxx.so")

#Fitting Parameters

Ipatia_l = ROOT.RooRealVar("Ipatia_l", "l", 1 , 0 , 30)
Ipatia_zeta = ROOT.RooRealVar("Ipatia_zeta", "zeta", 2, 0, 10)
Ipatia_fb = ROOT.RooRealVar("Ipatia_fb", "fb", 0.001, 0, 0.05)
Ipatia_sigma=ROOT.RooRealVar("Ipatia_sigma", "sigma", peak_width[0], peak_width[1], peak_width[2])
Ipatia_mu=ROOT.RooRealVar("Ipatia_mu", "mu", peak_range[0], peak_range[1], peak_range[2])             
Ipatia_a = ROOT.RooRealVar("Ipatia_a", "a", 3,0,10)
Ipatia_n = ROOT.RooRealVar("Ipatia_n", "n",1,0,10)
Ipatia_a2 = ROOT.RooRealVar("Ipatia_a2", "a2", 3,0,10)
Ipatia_n2 = ROOT.RooRealVar("Ipatia_n2", "n2",1,0,10)

Ipatia_PDF = ROOT.RooIpatia2("Ipatia_PDF", "Ipatia shape", mass, Ipatia_l, Ipatia_zeta, Ipatia_fb, Ipatia_sigma, Ipatia_mu, Ipatia_a, Ipatia_n, Ipatia_a2, Ipatia_n2)

Ipatia_Norm = ROOT.RooRealVar("Ipatia_Norm", "Ipatia Yield", MC_tree.GetEntries()/nbins * 3/normalisation_factor, 0, MC_tree.GetEntries() * 2)

MC_masshist_RooFit = ROOT.RooDataHist("MC_masshist_RooFit","MC masshist RooFit", ROOT.RooArgList(mass), MC_masshist)

MC_signalshape = ROOT.RooExtendPdf("MC_signalshape", "Signal shape", Ipatia_PDF, Ipatia_Norm)


MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)
MC_signalshape.plotOn(MC_frame)
MC_frame.Draw()

fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)
MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)

MC_signalshape.plotOn(MC_frame)
MC_frame.SetTitle("Ipatia mass fit of " + particle +  " MC")
MC_frame.GetYaxis().SetTitle("Number of events")
MC_frame.Draw()
fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)

leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Ipatia Pdf", "l")
leg.Draw("same")
graph_name = ("MC_" + particle + "_Ipatia_Mass_Fit.pdf")
filepath = (pwd)
fullpath = os.path.join(filepath, graph_name)
c1.SaveAs(fullpath)


pullhist = MC_frame.pullHist()

cpull = ROOT.TCanvas("cpull","cpull",600,700)
#add two TPads in the single canvas
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

#pullpad1.cd()
#MC_frame.SetTitle("Ipatia mass fit of " + particle +  " MC")
#MC_frame.Draw()

#pullpad2.cd()
#framepull = mass.frame()
#framepull.addPlotable(pullhist)
#framepull.SetTitle("")
#framepull.GetYaxis().SetTitle("Pull")
#framepull.GetYaxis().SetTitleOffset(0.4)
#framepull.GetYaxis().SetTitleSize(0.1)
#framepull.GetYaxis().SetLabelSize(0.1)
#framepull.GetXaxis().SetTitleSize(0.1)
#framepull.GetXaxis().SetLabelSize(0.1)
#framepull.Draw()

#cpull.cd()
#pullpad1.Draw()
#pullpad2.Draw()
#leg.Draw("same")
#cpull.Update()
#cpull.Draw()

#graph_name = ("MC_" + particle + "_Ipatia_Mass_Fit_pull.pdf")
#filepath = (pwd)
#fullpath = os.path.join(filepath, graph_name)
#cpull.SaveAs(fullpath)

#MC_signal_yield = Ipatia_Norm.getValV()
#MC_signal_error = Ipatia_Norm.getError()
#chi2ndf = MC_frame.chiSquare()
#print("N(MC_Lc) = %.0f +- %.0f"%(MC_signal_yield,MC_signal_error))
#print("chi2/ndf = " + str(chi2ndf))
#print("")

gauss_mean  = ROOT.RooRealVar("gauss_mean","Mean Lc", peak_range[0], peak_range[1], peak_range[2])
gauss_width = ROOT.RooRealVar("gauss_width","Width Lc",peak_width[0], peak_width[1], peak_width[2])

myGauss     = ROOT.RooGaussian("myGauss","Gaussian", mass, gauss_mean, gauss_width)
myGaussNorm = ROOT.RooRealVar("gauss norm", "gauss Yield", MC_tree.GetEntries()/nbins * 3/normalisation_factor, 0, MC_tree.GetEntries() * 2)

fracGausApolo = ROOT.RooRealVar("fracGausApolo", "fracGausApolo", 0.5, 0, 1)

GausApoloPDF= ROOT.RooAddPdf ("Gaus Apolo", "Gaus Apolo", ROOT.RooArgList(myGauss,Apolo_PDF), ROOT.RooArgList(fracGausApolo))
GausApoloNorm = ROOT.RooRealVar("GausApolo_Norm","Signal Yield", MC_tree.GetEntries()/nbins * 3/normalisation_factor, 0, MC_tree.GetEntries() * 2)


MC_masshist_RooFit = ROOT.RooDataHist("MC_masshist_RooFit","MC masshist RooFit", ROOT.RooArgList(mass), MC_masshist)

MC_signalshape = ROOT.RooExtendPdf("MC_signalshape", "Signal shape", GausApoloPDF, GausApoloNorm)


MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)
MC_signalshape.plotOn(MC_frame)
MC_frame.Draw()

fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)
MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)


GausApoloPDF.plotOn(MC_frame,ROOT.RooFit.Components("myGauss"),ROOT.RooFit.LineColor(8),ROOT.RooFit.LineStyle(2))
GausApoloPDF.plotOn(MC_frame,ROOT.RooFit.Components("Apolo_PDF"),ROOT.RooFit.LineColor(6),ROOT.RooFit.LineStyle(2))
GausApoloPDF.plotOn(MC_frame)


MC_frame.SetTitle("GausApolo mass fit of " + particle +  " MC")
MC_frame.GetYaxis().SetTitle("Number of events")
MC_frame.Draw()
fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)

leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Apolo_PDF", "l")
leg.Draw("same")
graph_name = ("MC_" + particle + "_GausApolo_Mass_Fit.pdf")
filepath = (pwd)
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
MC_frame.SetTitle("GausApolo mass fit of " + particle +  " MC")
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

graph_name = ("MC_" + particle + "_GausApolo_Mass_Fit_pull.pdf")
filepath = (pwd)
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

MC_signal_yield = GausApoloNorm.getValV()
MC_signal_error = GausApoloNorm.getError()
chi2ndf = MC_frame.chiSquare()
print("N(MC_Lc) = %.0f +- %.0f"%(MC_signal_yield,MC_signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")


#Now we do BUKIN and Gauss Combo
fracGausBukin = ROOT.RooRealVar("fracGausBukin", "fracGausBukin", 0.5, 0, 1)
GausBukinPDF= ROOT.RooAddPdf ("Gaus Bukin", "Gaus Bukin", ROOT.RooArgList(myGauss,Bukin_PDF), ROOT.RooArgList(fracGausBukin))
GausBukinNorm = ROOT.RooRealVar("GausBukin_Norm","Signal Yield", MC_tree.GetEntries()/nbins * 3/normalisation_factor, 0, MC_tree.GetEntries() * 2)


MC_masshist_RooFit = ROOT.RooDataHist("MC_masshist_RooFit","MC masshist RooFit", ROOT.RooArgList(mass), MC_masshist)

MC_signalshape = ROOT.RooExtendPdf("MC_signalshape", "Signal shape", GausBukinPDF, GausBukinNorm)

fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)
MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)

GausBukinPDF.plotOn(MC_frame,ROOT.RooFit.Components("myGauss"),ROOT.RooFit.LineColor(8),ROOT.RooFit.LineStyle(2))
GausBukinPDF.plotOn(MC_frame,ROOT.RooFit.Components("Bukin_PDF"),ROOT.RooFit.LineColor(6),ROOT.RooFit.LineStyle(2))
GausBukinPDF.plotOn(MC_frame)

MC_frame.SetTitle("GausBukin mass fit of " + particle +  " MC")
MC_frame.GetYaxis().SetTitle("Number of events")
MC_frame.Draw()
fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)

leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Gaus Bukin Pdf", "l")
leg.Draw("same")
graph_name = ("MC_" + particle + "_GausBukin_Mass_Fit.pdf")
filepath = (pwd)
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
MC_frame.SetTitle("GausBukin mass fit of " + particle +  " MC")
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

graph_name = ("MC_" + particle + "_GausBukin_Mass_Fit_pull.pdf")
filepath = (pwd)
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

MC_signal_yield = GausBukinNorm.getValV()
MC_signal_error = GausBukinNorm.getError()
chi2ndf = MC_frame.chiSquare()
print("N(MC_Lc) = %.0f +- %.0f"%(MC_signal_yield,MC_signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")

#######
#Crystal Ball + Gauss
#######

#Define CB parameters (not been used yet)

cb_sigma = ROOT.RooRealVar("CB_Sigma", "CB_Sigma", 6, 2, 20)
cb_a = ROOT.RooRealVar("CB_a" , "CB_a" , 5, 0, 30)
cb_n = ROOT.RooRealVar("CB_n", "CB_n", 2, 0,10)
CBPDF = ROOT.RooCBShape("CBPDF", "Crystal Ball", mass, gauss_mean, cb_sigma, cb_a, cb_n)

CB_Norm = ROOT.RooRealVar("CB_Norm", "CB Yield", MC_tree.GetEntries()/nbins * 3/normalisation_factor, 0, MC_tree.GetEntries() * 2)

fracGausCB = ROOT.RooRealVar("fracGausCB", "fracGausCB", 0.5, 0, 1.0) # relative amount of Gauss to CB

GausCBPDF = ROOT.RooAddPdf("GausCBPDF", "CB+Gaus", ROOT.RooArgList(myGauss,CBPDF),ROOT.RooArgList(fracGausCB))

GausCBNorm = ROOT.RooRealVar("GausCB_Norm","Signal Yield", MC_tree.GetEntries()/nbins * 3/normalisation_factor, 0, MC_tree.GetEntries() * 2)

# Then do the fitting


MC_masshist_RooFit = ROOT.RooDataHist("MC_masshist_RooFit","MC masshist RooFit", ROOT.RooArgList(mass), MC_masshist)

MC_signalshape = ROOT.RooExtendPdf("MC_signalshape", "Signal shape", GausCBPDF, GausCBNorm)

fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)
MC_frame = mass.frame()
MC_masshist_RooFit.plotOn(MC_frame)


MC_frame.SetTitle("GausCB mass fit of " + particle +  " MC")
MC_frame.GetYaxis().SetTitle("Number of events")
MC_frame.Draw()
fitresult = MC_signalshape.fitTo(MC_masshist_RooFit)

GausCBPDF.plotOn(MC_frame,ROOT.RooFit.Components("myGauss"),ROOT.RooFit.LineColor(8),ROOT.RooFit.LineStyle(2))
GausCBPDF.plotOn(MC_frame,ROOT.RooFit.Components("CBPDF"),ROOT.RooFit.LineColor(6),ROOT.RooFit.LineStyle(2))
GausCBPDF.plotOn(MC_frame)
MC_frame.Draw()
c1.Update()

leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
#leg.SetHeader("Legend")
leg.AddEntry( histogram1, "Gaus CB Pdf", "l")
leg.Draw("same")
graph_name = ("MC_" + particle + "_GausCB_Mass_Fit.pdf")
filepath = (pwd)
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
MC_frame.SetTitle("GausCB mass fit of " + particle +  " MC")
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

graph_name = ("MC_" + particle + "_GausCB_Mass_Fit_pull.pdf")
filepath = (pwd)
fullpath = os.path.join(filepath, graph_name)
cpull.SaveAs(fullpath)

MC_signal_yield = GausCBNorm.getValV()
MC_signal_error = GausCBNorm.getError()
chi2ndf = MC_frame.chiSquare()
print("N(MC_Lc) = %.0f +- %.0f"%(MC_signal_yield,MC_signal_error))
print("chi2/ndf = " + str(chi2ndf))
print("")


# Then plot
