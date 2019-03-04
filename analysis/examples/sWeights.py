
#################
# Example of sWeight / sPlot using RooStats,
# as per https://arxiv.org/abs/physics/0402083
#################


import ROOT


xmin = 2240
xmax = 2340
nbins = 200

fileloc = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/31/1/output/Lc2pKpiTuple.root"
cuts = "1==1"



# Get the data

f = ROOT.TFile.Open(fileloc, "READONLY")
tree = f.Get("tuple_Lc2pKpi/DecayTree")

c1 = ROOT.TCanvas("c1","c1")
tree.Draw("lcplus_MM>>masshist({0},{1},{2})".format(nbins,xmin,xmax),cuts)
masshist = ROOT.gDirectory.Get("masshist")

mass = ROOT.RooRealVar("mass","mass",xmin,xmax)
data = ROOT.RooDataHist("data","data histogram", ROOT.RooArgList(mass), masshist)



# build the model

gauss_mean  = ROOT.RooRealVar("gauss_mean","Mean",2288,2280,2290)
gauss_width = ROOT.RooRealVar("gauss_width","Width",2,0,10)
Gauss       = ROOT.RooGaussian("Gauss","Gaussian signal part", mass, gauss_mean, gauss_width)

cb_width    = ROOT.RooRealVar("cb_width","CB Width",2,0,15)
cb_alpha    = ROOT.RooRealVar("cb_alpha","CB Exp.const",1.0,0.0,5.0)
cb_n        = ROOT.RooRealVar("cb_n","CB Exp.crossover",1.0,0.0,15.0)
CB          = ROOT.RooCBShape("myCB","Crystal Ball signal part", mass, gauss_mean, cb_width, cb_alpha, cb_n)

sigfrac     = ROOT.RooRealVar("sigfrac","Gauss / CB fraction", 0.5, 0, 1)
sigshape    = ROOT.RooAddPdf ("sigshape", "Shape of the Signal", ROOT.RooArgList(Gauss, CB), ROOT.RooArgList(sigfrac))

exponent    = ROOT.RooRealVar("exponent","C", 0.001, -0.2, 0.2)
bkgshape    = ROOT.RooExponential("bkgshape","Exponential Bkg shape", mass, exponent)

sig_norm = ROOT.RooRealVar("sig_norm","Signal Yield", tree.GetEntries()/nbins * 3/10, 0, tree.GetEntries()*2)
bkg_norm = ROOT.RooRealVar("bkg_norm","Background Yield", tree.GetEntries()/nbins * 3, 0, tree.GetEntries()*2)
model    = ROOT.RooAddPdf("model","Full model", ROOT.RooArgList(sigshape, bkgshape), ROOT.RooArgList(sig_norm, bkg_norm) )



# Fit the model
model.fitTo(data)


# Display the quality of the fit
frame = mass.frame()
data.plotOn(frame)
model.plotOn(frame, ROOT.RooFit.Components("sigshape"), ROOT.RooFit.LineColor(8) , ROOT.RooFit.LineStyle(2))
model.plotOn(frame, ROOT.RooFit.Components("bkgshape"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
model.plotOn(frame)
frame.Draw()
c1.Update()

print("Chi2/NDF: {0}".format(frame.chiSquare()))



# Constrain all parameters besides the signal yield
for var in [gauss_mean, gauss_width, cb_width, cb_alpha, cb_n, sigfrac, exponent] :
  var.setConstant()

# Create sPlot object
sData = ROOT.RooStats.SPlot("sData", "an SPlot", ROOT.RooArgSet(data), ROOT.RooArgList(model), ROOT.RooArgList(sig_norm, bkg_norm) )

# Check sWeights
print("sWeight sanity check:")
print("sig Yield is {0}, from sWeights it is {1}".format(sig_norm.getVal(), sData.GetYieldFromSWeight("sig_norm")))
print("big Yield is {0}, from sWeights it is {1}".format(bkg_norm.getVal(), sData.GetYieldFromSWeight("bkg_norm")))
print("First 10 events:")
for i in range(10) :
  print("{0}: sigWeight = {1}, bkgWeight = {2}, totWeight = {3}".format(
      i, sData.GetSWeight(i,"sig_norm"), sData.GetSWeight(i,"bkg_norm"), sData.GetSumOfEventSWeight(i)))




