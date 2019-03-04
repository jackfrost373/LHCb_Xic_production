
#################
# Example of sWeight / sPlot using RooStats,
# as per https://arxiv.org/abs/physics/0402083
#################


import ROOT


getData      = True # Load data.
makesWeights = True # Generate sWeights. Requires getData.
plotVariable = True  # make an sPlot using sWeights



if(getData) :

  # Get the data
  fileloc = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/31/1/output/Lc2pKpiTuple.root"
  cuts = "1==1"

  f = ROOT.TFile.Open(fileloc, "READONLY")
  tree = f.Get("tuple_Lc2pKpi/DecayTree")

  mass = ROOT.RooRealVar("lcplus_MM","mass",2240,2340,"MeV/c^{2}")
  momentum = ROOT.RooRealVar("lcplus_P","P",5000,200000,"MeV/c")
  lifetime = ROOT.RooRealVar("lcplus_PVConstrainedDTF_ctau[0]","ctau",0,3,"mm")

  # Get RooDataSet (unbinned) from TTree.
  # We add momentum/lifetime for easy plotting of sWeighted momentum later, but we will also build a friendTree.
  data = ROOT.RooDataSet("data","data set", tree, ROOT.RooArgSet(mass,momentum, lifetime), cuts)



if(makesWeights) :

  # build the fit model
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

  sig_norm = ROOT.RooRealVar("sig_norm","Signal Yield", tree.GetEntries()/200 * 3/10, 0, tree.GetEntries()*2)
  bkg_norm = ROOT.RooRealVar("bkg_norm","Background Yield", tree.GetEntries()/200 * 3, 0, tree.GetEntries()*2)
  model    = ROOT.RooAddPdf("model","Full model", ROOT.RooArgList(sigshape, bkgshape), ROOT.RooArgList(sig_norm, bkg_norm) )


  # Fit the model
  model.fitTo(data)

  # Display the quality of the fit
  c1 = ROOT.TCanvas("c1","c1")
  frame = mass.frame()
  data.plotOn(frame)
  model.plotOn(frame, ROOT.RooFit.Components("sigshape"), ROOT.RooFit.LineColor(8) , ROOT.RooFit.LineStyle(2))
  model.plotOn(frame, ROOT.RooFit.Components("bkgshape"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
  model.plotOn(frame)
  frame.Draw()
  c1.Update()
  c1.SaveAs("sWeight_fit.pdf")

  print("Chi2/NDF: {0}".format(frame.chiSquare()))


  # Constrain all parameters besides the signal yield
  for var in [gauss_mean, gauss_width, cb_width, cb_alpha, cb_n, sigfrac, exponent] :
    var.setConstant()

  # Create sPlot object. This will instantiate 'sig_norm_sw' and 'bkg_norm_sw' vars in the data. 
  sData = ROOT.RooStats.SPlot("sData", "an SPlot", data, model, ROOT.RooArgList(sig_norm, bkg_norm) )

  # Check sWeights
  if(False) :
    print("")
    print("sWeight sanity check:")
    print("sig Yield is {0}, from sWeights it is {1}".format(sig_norm.getVal(), sData.GetYieldFromSWeight("sig_norm")))
    print("big Yield is {0}, from sWeights it is {1}".format(bkg_norm.getVal(), sData.GetYieldFromSWeight("bkg_norm")))
    print("First 10 events:")
    for i in range(10) :
      print(" {0}: sigWeight = {1}, bkgWeight = {2}, totWeight = {3}".format(
          i, sData.GetSWeight(i,"sig_norm"), sData.GetSWeight(i,"bkg_norm"), sData.GetSumOfEventSWeight(i)))

  # Save dataset with weights to workspace file for later quick use
  ws = ROOT.RooWorkspace("ws","workspace")
  getattr(ws,'import')(data, ROOT.RooFit.Rename("swdata")) # silly workaround due to 'import' keyword
  ws.writeToFile("sWeight_ws.root")






if(plotVariable) :

  # Plot sWeighted variable distribution from dataset (with sWeights)

  variable = "lcplus_P"
  #variable = "lcplus_PVConstrainedDTF_ctau[0]"

  # load sWeights from file
  fws = ROOT.TFile.Open("sWeight_ws.root","READONLY")
  ws = fws.Get('ws')
  var = ws.var(variable)
  data = ws.data("swdata")

  data_sig = ROOT.RooDataSet("data_sig", "sWeighed signal data", data, data.get(), "1==1", "sig_norm_sw")
  data_bkg = ROOT.RooDataSet("data_bkg", "sWeighed bkgrnd data", data, data.get(), "1==1", "bkg_norm_sw")

  c2 = ROOT.TCanvas("c2","c2")

  frame = var.frame()
  frame.SetTitle("sWeight example")
  data.plotOn(frame)
  data_sig.plotOn(frame, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.MarkerColor(8) , ROOT.RooFit.Name("data_sig") )
  data_bkg.plotOn(frame, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.MarkerColor(46), ROOT.RooFit.Name("data_bkg") )
  frame.Draw()

  leg = ROOT.TLegend(0.65,0.77,0.89,0.88)
  leg.AddEntry(frame.findObject("data_sig"), "Signal",     "lp")
  leg.AddEntry(frame.findObject("data_bkg"), "Background", "lp")
  leg.SetBorderSize(0)
  leg.Draw("same")

  c2.Update()
  c2.SaveAs("sWeight_{0}.pdf".format(var.getTitle()))







#  Note that the added column must have the same #entries! (i.e. come from the same tree with the same cuts applied!)
