
#################
# Example of sWeight / sPlot using RooStats,
# as per https://arxiv.org/abs/physics/0402083
#################


import ROOT
from Imports import *

getData        = True  # Load data.
makesWeights   = True  # Generate sWeights, write to workspace. Requires getData.
makeFriendTree = True  # create friend tree for simple future sweight plotting. Requires makesWeights.
plotVariable   = True  # make an sPlot using sWeights in RooDataSet from workspace.
testFriendTree = True  # test sWeights from friend tree to do an sPlot.

outputdir = pwd+"output/"
inputdir = pwd + "4_reduced/"

if(getData) :
  
  # Get the data

  f = ROOT.TFile.Open(inputdir+"4_Lc_cut_reduced.root", "READONLY")
  tree = f.Get("DecayTree;48")
  #tree.Print()
  cuts = "1==1"
      
  mass = ROOT.RooRealVar("lcplus_MM","Lc_mass",2240,2340,"MeV/c^{2}")
  momentum = ROOT.RooRealVar("lcplus_P","Lc_P",5000,200000,"MeV/c")
  lifetime = ROOT.RooRealVar("lcplus_TAU","Lc_tau",0,0.007,"ns")
  print ("I am adding data to a tree") #Just to keep us informed 
  # Get RooDataSet (unbinned) from TTree.
  # We add momentum/lifetime for easy plotting of their sWeighted versions later


  data = ROOT.RooDataSet("data","data set", tree, ROOT.RooArgSet(mass,momentum, lifetime), cuts)
  print ("built the data set, plotting...") # Just to keep us informed
  c = ROOT.TCanvas("c","c")
  frame = lifetime.frame()
  data.plotOn(frame)
  frame.Draw()



if(makesWeights) :

  # build the fit model
  print ("Building the fit model...")
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
  print ("plotting the fit...")
  c1 = ROOT.TCanvas("c1","c1")
  frame = mass.frame()
  data.plotOn(frame)
  model.plotOn(frame, ROOT.RooFit.Components("sigshape"), ROOT.RooFit.LineColor(8) , ROOT.RooFit.LineStyle(2))
  model.plotOn(frame, ROOT.RooFit.Components("bkgshape"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
  model.plotOn(frame)
  frame.Draw()
  c1.Update()
  c1.SaveAs("{0}sWeight_fit.pdf".format(outputdir))

  print("Chi2/NDF: {0}".format(frame.chiSquare()))


  # Fix all parameters besides the signal yield
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
  ws.writeToFile("{0}sWeight_ws.root".format(outputdir))

  #f.Close()  # keeps mass fit plot alive






if(makeFriendTree) :
  # Make a new TTree that contains the sWeights for every event.
  # Makes use of the previously defined data and sData objects.

  from array import array

  wfile = ROOT.TFile.Open("{0}sWeight_swTree.root".format(outputdir),"RECREATE")
  swtree = ROOT.TTree("swTree","swTree")

  # TTrees directly access memory, so we define pointers.
  sw_mass = array( 'f', [0] )
  sw_sig  = array( 'f', [0] )
  sw_bkg  = array( 'f', [0] )
  swtree.Branch('sw_mass', sw_mass, 'sw_mass/F')
  swtree.Branch('sw_sig',  sw_sig,  'sw_sig/F' )
  swtree.Branch('sw_bkg',  sw_bkg,  'sw_bkg/F' )

  nEntries = int(data.sumEntries())
  print ("Writing sWeights for {0} entries...".format(nEntries))
  for i in range(nEntries) :
    if(i%10000==0) : print("{0:.2f} %".format(float(i)/nEntries*100.))
    sw_mass[0] = data.get(i).getRealValue("lcplus_MM") 
    sw_sig[0]  = sData.GetSWeight(i, "sig_norm")
    sw_bkg[0]  = sData.GetSWeight(i, "bkg_norm")
    swtree.Fill()

  print("...done")
  swtree.Write()
  wfile.Close()
  





if(plotVariable) :

  # Plot sWeighted variable distribution from RooDataSet.

  #variable = "lcplus_P"
  variable = "lcplus_TAU"

  # load sWeights from file (note: could have used 'data' as above, if we just made them)
  fws = ROOT.TFile.Open("{0}sWeight_ws.root".format(outputdir),"READONLY")
  ws = fws.Get('ws')
  var = ws.var(variable)
  data = ws.data("swdata")

  data_sig = ROOT.RooDataSet("data_sig", "sWeighed signal data", data, data.get(), "1==1", "sig_norm_sw")
  data_bkg = ROOT.RooDataSet("data_bkg", "sWeighed bkgrnd data", data, data.get(), "1==1", "bkg_norm_sw")

  c2 = ROOT.TCanvas("c2","c2")

  frame = var.frame()
  frame.SetTitle("sPlot from RooDataSet")
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
  c2.SaveAs("{0}sPlot_{1}.pdf".format(outputdir,var.getTitle()))








if(testFriendTree) :

  # Make an sPlot using the sWeights from the friendTree, without RooFit / RooStats functionality.
  # Can be used to plot any variable in the original TTree.

  #[var,nbins,xmin,xmax] = ["lcplus_P",100,5000,200000]
  [var,nbins,xmin,xmax] = ["lcplus_TAU",100,0,0.007]

  # Load original TTree
  f = ROOT.TFile.Open(inputdir+"4_Lc_cut_reduced.root", "READONLY")
  tree = f.Get("DecayTree;48")
    
  # cuts should match those applied when creating the sWeight TTree --> should have same #entries!
  #  Note: limited range of RooRealVars in RooDataSet (used to create sWeights) also cuts events.
  datacuts = "1==1"
  datacuts += " && lcplus_MM >= 2240 && lcplus_MM <= 2340 && lcplus_P >= 5000 && lcplus_P <= 200000 && lcplus_TAU >= 0 && lcplus_TAU <= 0.007"
     
  print("beginning CopyTree")
  wfile = ROOT.TFile.Open(outputdir+"cuttree.root","RECREATE")
  cuttree = tree.CopyTree(datacuts)
  
  print("cutTree nEvents = {0}".format(cuttree.GetEntries()))

  # add sWeight tree as friend. Should match #entries!
  cuttree.AddFriend("swTree","{0}sWeight_swTree.root".format(outputdir))

  # plot sWeighted distribution of a variable
  ROOT.gStyle.SetOptStat(0)
  c4 = ROOT.TCanvas('c4','c4')
  cuttree.Draw("{0}>>histAll({1},{2},{3})".format(var,nbins,xmin,xmax))
  cuttree.Draw("{0}>>histSig({1},{2},{3})".format(var,nbins,xmin,xmax), "swTree.sw_sig")
  cuttree.Draw("{0}>>histBkg({1},{2},{3})".format(var,nbins,xmin,xmax), "swTree.sw_bkg")
  histAll = ROOT.gDirectory.Get("histAll")
  histSig = ROOT.gDirectory.Get("histSig")
  histBkg = ROOT.gDirectory.Get("histBkg")
  
  histSig.SetLineColor(8)
  histBkg.SetLineColor(46)
  histAll.SetTitle('sPlot from swTree')
  histAll.GetXaxis().SetTitle(var)
  histAll.Draw()
  histSig.Draw("same")
  histBkg.Draw("same")
  
  leg = ROOT.TLegend(0.65,0.77,0.89,0.88)
  leg.AddEntry(histSig, "Signal",     "lp")
  leg.AddEntry(histBkg, "Background", "lp")
  leg.SetBorderSize(0)
  leg.Draw("same")

  c4.Update()
  c4.SaveAs("{0}sPlot_swTree_{1}.pdf".format(outputdir,var))




