
########################
# Example of (kinematic) event reweighing, 
#  to match simulation to data distributions
########################

import ROOT
from array import array

########################
## User settings

datafile_loc = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/31/1/output/Lc2pKpiTuple.root"
simfile_loc  = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/29/1/output/MC_Lc2pKpiTuple_25103006.root"
datatreename = "tuple_Lc2pKpi/DecayTree"
simtreename = datatreename

variables = ["lcplus_P", "lcplus_ETA"]

#binning = { "lcplus_P" : [5000, 20000, 30000, 35000, 40000, 45000, 50000, 60000, 70000, 80000, 100000, 150000, 200000, 300000, 450000] ,
#          "lcplus_ETA" : [2.0, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 4.0, 4.5, 5.5] }
binning = { "lcplus_P" : [5000, 30000, 40000, 50000, 60000, 80000, 150000, 450000] ,
          "lcplus_ETA" : [2.0, 2.9, 3.3, 4.0, 5.5] }

cuts = { "data" : "1==1",
          "sim" : "1==1" }  # sim should include MCTruth

weights = { "data" : "1==1",  # data should contain sweight (but add friendTree then!)
             "sim" : "1==1" }

outputdir = "./output/"
showplots = True




##############################

# set some stuff
ROOT.gStyle.SetOptStat(0) # remove hist info box
#if not showplots : ROOT.gROOT.SetBatch(True) 
nbins = 100 # bins for regular drawing
ranges = [ [binning[variables[0]][0], binning[variables[0]][-1]],
           [binning[variables[1]][0], binning[variables[1]][-1]] ]

# get data
datafile = ROOT.TFile.Open(datafile_loc)
simfile  = ROOT.TFile.Open(simfile_loc)
datatree = datafile.Get(datatreename)
simtree  = simfile.Get(simtreename)

# make dictionaries for easy access/looping
treedict = { "data" : datatree,
             "sim"  : simtree }
colourdict = { "data" : 9,         # blue
               "sim"  : 46,        # red
               "kweighed" : 28 }  # brown
histdict = {}
canvasdict = {}




##############################
# Define functions
#############################


lines = []
def drawBinningLines(binning=binning, variables=variables, lines=lines) :
  # Draw red lines at the 2D bin edges
  if(lines == []) :
    xmax = max(binning[variables[0]])
    xmin = min(binning[variables[0]])
    for y in binning[variables[1]] :
      lines += [ ROOT.TLine(xmin, y, xmax, y) ]
    ymax = max(binning[variables[1]])
    ymin = min(binning[variables[1]])
    for x in binning[variables[0]] :
      lines += [ ROOT.TLine(x, ymin, x, ymax) ]

  for line in lines :
    line.SetLineColor(2) # red
    line.Draw("same")



def makeKweightsTable(treedict=treedict, variables=variables, binning=binning, cuts=cuts, weights=weights) : 
  # Make a look-up-table (=2D hist) for the kinematic weights
  print("Making and dividing histograms for kWeights")
 
  xbins = array('d', binning[variables[0]])
  ybins = array('d', binning[variables[1]])
  nbinsx  = len(xbins)
  nbinsy  = len(ybins)
  binnedHist2D_data = ROOT.TH2F("binnedHist2D_data", "binnedHist2D_data", nbinsx-1, xbins, nbinsy-1, ybins )
  binnedHist2D_sim  = ROOT.TH2F("binnedHist2D_sim" , "binnedHist2D_sim" , nbinsx-1, xbins, nbinsy-1, ybins )

  for datatype in ["data","sim"] :
    treedict[datatype].Draw("{0}:{1}>>+binnedHist2D_{2}".format(variables[1],variables[0], datatype),
      "({0})*{1}".format(cuts[datatype], weights[datatype]) )
  
  for hist in [ binnedHist2D_data, binnedHist2D_sim ] :
    hist.Sumw2() # set errors as sqrt(sum(weights^2)) (not sqrt(N))
    hist.Scale( 1./hist.Integral() )  # normalize histogram

  # the big trick
  binnedHist2D_data.Divide( binnedHist2D_sim )

  binnedHist2D_data.SetName("kWeights")
  binnedHist2D_data.SetTitle("kWeights")
  binnedHist2D_data.GetXaxis().SetTitle(variables[1])
  binnedHist2D_data.GetYaxis().SetTitle(variables[0])

  return binnedHist2D_data



def makeKweightsFriendTree(kweightsTable, simtree=simtree, variables=variables, 
    outputfilename=outputdir+"kWeight_kwTree.root", cutoff = 5.) : 
  # Loop over tree and look up the kWeight for each entry

  # TTrees directly access memory, so we define pointers.
  var1    = array( 'd', [0] )
  var2    = array( 'd', [0] )
  simtree.SetBranchAddress(variables[0], var1)
  simtree.SetBranchAddress(variables[1], var2)

  nEntries = int(simtree.GetEntries())

  # first get naive kWeights
  kwlist = []
  print("Getting kWeights for {0} entries...".format(nEntries))
  for i in range(nEntries) :
    if(i%10000==0) : print("{0:.2f} %".format(float(i)/nEntries*100.))
    simtree.GetEntry(i)
    kw = kweightsTable.GetBinContent( kweightsTable.FindBin( var1[0] , var2[0] ) )
    if( kw > cutoff ) : kw = cutoff
    kwlist += [kw]

  # calculate normalisation
  kwtotal  = sum(kwlist)
  kw2total = sum( [i**2 for i in kwlist] )
  if(kw2total==0) :
    print("Error: kweight sum is zero. Something must have gone wrong!")
    return
  norm = float(kwtotal) / kw2total
  print("--> kWeight normalisation is {0}".format(norm))
 
  # open kweights file
  kwfile = ROOT.TFile.Open(outputfilename, "RECREATE")
  kwtree = ROOT.TTree("kwTree","kwTree")
  kweight = array( 'f', [0] )
  kwtree.Branch('kweight', kweight, 'kweight/F')

  # normalize and write
  print("Normalizing kWeights...")
  for i in range(nEntries) :
    if(i%10000==0) : print("{0:.2f} %".format(float(i)/nEntries*100.))
    kweight[0] = kwlist[i] * norm
    kwtree.Fill()

  kwtree.Write()
  kwfile.Close()
  print("kWeights written to {0}".format(outputfilename))
  


  
    

##############################
# Plot to show what distributions we're dealing with
##############################

c1 = ROOT.TCanvas()

if(showplots) :
  
  print("Making histograms for plotting")

  # Make the 1D histograms
  for i in range(2) :
    for datatype in ["data","sim"] :
      histname = "{0}_1D_var{1}".format(datatype, i)
      treedict[datatype].Draw("{0}>>{1}({2},{3},{4})".format(variables[i], histname,
        nbins, ranges[i][0], ranges[i][1]), 
        "({0})*{1}".format(cuts[datatype], weights[datatype]) )
      histdict[ histname ] = ROOT.gDirectory.Get( histname )
      histdict[ histname ].SetTitle(histname)
      histdict[ histname ].GetXaxis().SetTitle(variables[i])
      histdict[ histname ].SetLineWidth(2)
      histdict[ histname ].SetLineColor( colourdict[ datatype ] )

  # Make the 2D histograms
  for datatype in ["data","sim"] :
    histname = "{0}_2D".format(datatype)
    treedict[datatype].Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(variables[1],variables[0], histname,
      nbins, ranges[0][0], ranges[0][1], nbins, ranges[1][0], ranges[1][1] ),
      "({0})*{1}".format(cuts[datatype], weights[datatype]) )
    histdict[ histname ] = ROOT.gDirectory.Get( histname )
    histdict[ histname ].SetTitle(histname)
    histdict[ histname ].GetXaxis().SetTitle(variables[1])
    histdict[ histname ].GetYaxis().SetTitle(variables[0])

  print("Drawing histograms")

  # Draw the 1D histograms
  for i in range(2) :
    canvasdict[ "c_1D_var{0}".format(i) ] = ROOT.TCanvas("c_1D_var{0}".format(i))
    histdict[ "data_1D_var{0}".format(i) ].DrawNormalized()
    histdict[  "sim_1D_var{0}".format(i) ].DrawNormalized("same")
    canvasdict[ "c_1D_var{0}".format(i) ].Update()

  # Draw the 2D histograms
  for datatype in ["data","sim"] :
    canvasdict[ "c_2D_{0}".format(datatype) ] = ROOT.TCanvas("c_2D_{0}".format(datatype))
    histdict[ "{0}_2D".format(datatype) ].Draw("colz")
    drawBinningLines()
    canvasdict[ "c_2D_{0}".format(datatype) ].Update()
    canvasdict[ "c_2D_{0}".format(datatype) ].SaveAs(outputdir+"2D_{0}.pdf".format(datatype))






##############################
# Make kinematic weights and draw resulting weighed distributions
##############################

kwfilename = outputdir + "kWeight_kwTree.root"

# Make kWeight table
c1.cd()
kweightTable = makeKweightsTable() 

if(showplots) :
  c_2D_kWeights = ROOT.TCanvas("c_2D_kWeights")
  kweightTable.Draw("colz")
  c_2D_kWeights.SaveAs(outputdir+"kWeights.pdf")


# Make kWeights friend tree for simtree
makeKweightsFriendTree(kweightTable)

# Add friendtree
simtree.AddFriend("kwTree",kwfilename)


# Draw new kinematic-weighed distributions
if(showplots) :

  c1.cd()
  for i in range(2) :
    histname = "kweighedsim_1D_var{0}".format(i)
    
    simtree.Draw("{0}>>{1}({2},{3},{4})".format(variables[i], histname, nbins, ranges[i][0], ranges[i][1]), 
      "({0})*({1})*kwTree.kweight".format(cuts["sim"], weights["sim"]) )

    histdict[ histname ] = ROOT.gDirectory.Get( histname )
    histdict[ histname ].SetTitle(histname)
    histdict[ histname ].GetXaxis().SetTitle(variables[i])
    histdict[ histname ].SetLineWidth(2)
    histdict[ histname ].SetLineStyle(9)
    histdict[ histname ].SetLineColor( colourdict[ "kweighed" ] )
    
    canvasdict[ "c_1D_var{0}".format(i) ].cd()
    histdict[ histname ] .DrawNormalized("same")
    canvasdict[ "c_1D_var{0}".format(i) ].Update()
    canvasdict[ "c_1D_var{0}".format(i) ].SaveAs(outputdir+"1D_var{0}.pdf".format(i))
