
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

binning = { "lcplus_P" : [5000, 20000, 30000, 35000, 40000, 45000, 50000, 60000, 70000, 80000, 100000, 150000, 200000, 300000, 450000] ,
          "lcplus_ETA" : [2.0, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 4.0, 4.5, 5.5] }
#binning = { "lcplus_P" : [5000, 30000, 40000, 60000, 90000, 450000] ,
#          "lcplus_ETA" : [2.0, 2.7, 3.1, 3.7, 5.5] }

cuts = { "data" : "1==1",
          "sim" : "1==1" }  # sim should include MCTruth

weights = { "data" : "1==1",  # data should contain sweight (but add friendTree then!)
             "sim" : "1==1" }

outputdir = "./output/"

makeplots = True
nbins = 100 # bins for regular drawing




##############################

# set some stuff
ROOT.gStyle.SetOptStat(0) # remove hist info box
if not makeplots : ROOT.gROOT.SetBatch(True) # prevent graphical output
ranges = [ [binning[variables[0]][0], binning[variables[0]][-1]],
           [binning[variables[1]][0], binning[variables[1]][-1]] ]

# get data
datafile = ROOT.TFile.Open(datafile_loc)
simfile  = ROOT.TFile.Open(simfile_loc)
datatree = datafile.Get(datatreename)
simtree  = simfile.Get(simtreename)

# Make global dictionaries for easy access/looping.
# This will also prevent objects from going out-of-scope when created in function calls.
treedict = { "data" : datatree,
             "sim"  : simtree }
colourdict = { "data" : 9,         # 9=blue
               "sim"  : 28,        # 28=brown
               "kweighed" : 46 }   # 46=red
styledict  = { "data" : 1,         # 1=solid
               "sim"  : 1,         # 1=solid
               "kweighed" : 7 }    # 7=small dashed
histdict = {}
canvasdict = {}




##############################
# Define functions
#############################


def makeBinningLines(binning=binning, variables=variables) :
  # make red lines at the 2D bin edges
  lines = []
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

  return lines 



def makeKweightsTable(treedict=treedict, variables=variables, binning=binning, cuts=cuts, weights=weights) : 
  # Make a look-up-table (=2D hist) for the kinematic weights

  print("Making and dividing histograms for kWeights")
 
  # Create 2D histograms with variable-sized bin widths
  xbins = array('d', binning[variables[0]])
  ybins = array('d', binning[variables[1]])
  binnedHist2D_data = ROOT.TH2F("binnedHist2D_data", "binnedHist2D_data", len(xbins)-1, xbins, len(ybins)-1, ybins )
  binnedHist2D_sim  = ROOT.TH2F("binnedHist2D_sim" , "binnedHist2D_sim" , len(xbins)-1, xbins, len(ybins)-1, ybins )

  # Fill histograms with TTree::Draw
  for datatype in ["data","sim"] :
    treedict[datatype].Draw("{0}:{1}>>+binnedHist2D_{2}".format(variables[1],variables[0], datatype),
      "({0})*{1}".format(cuts[datatype], weights[datatype]) )
  
  for hist in [ binnedHist2D_data, binnedHist2D_sim ] :
    hist.Sumw2() # set errors as sqrt(sum(weights^2)) (not sqrt(N))
    hist.Scale( 1./hist.Integral() )  # normalize histogram

  # The big trick. Idea: [sim] x [kWeight] = [data]
  #  --> [kWeight] = [data] / [sim]
  binnedHist2D_data.Divide( binnedHist2D_sim )

  # binnedHist2D_data is now the kWeight histogram.
  binnedHist2D_data.SetName("kWeights")
  binnedHist2D_data.SetTitle("kWeights")
  binnedHist2D_data.GetXaxis().SetTitle(variables[0])
  binnedHist2D_data.GetYaxis().SetTitle(variables[1])

  return binnedHist2D_data




def makeKweightsFriendTree(kweightsTable, simtree=simtree, variables=variables, 
    outputfilename=outputdir+"kWeight_kwTree.root", cutoff = 5.) : 
  # Loop over tree and look up the kWeight for each entry.
  #  kWeights larger than cutoff will be set to cutoff value.

  # TTrees directly access memory, so we define pointers.
  var1    = array( 'd', [0] )
  var2    = array( 'd', [0] )
  simtree.SetBranchAddress(variables[0], var1)
  simtree.SetBranchAddress(variables[1], var2)

  nEntries = int(simtree.GetEntries())

  # first get naive kWeights, by looping over tree
  kwlist = []
  print("Getting kWeights for {0} entries...".format(nEntries))
  for i in range(nEntries) :
    if(i%10000==0) : print("{0:.2f} %".format(float(i)/nEntries*100.))

    # Get tree entry to fill var1 and var2
    simtree.GetEntry(i)

    # Find the bin content in the kWeighsTable, corresponding to the right var1, var2 bin
    kw = kweightsTable.GetBinContent( kweightsTable.FindBin( var1[0] , var2[0] ) )
    if( kw > cutoff ) : kw = cutoff
    kwlist += [kw]

  # calculate normalisation
  kwtotal  = sum(kwlist)
  kw2total = sum( [i**2 for i in kwlist] )
  if(kw2total==0) : print("Error: kweight sum is zero. Something must have gone wrong!")
  norm = float(kwtotal) / kw2total
  print("--> kWeight normalisation is {0}".format(norm))
 
  # open kweights file to save our kWeights
  kwfile = ROOT.TFile.Open(outputfilename, "RECREATE")
  kwtree = ROOT.TTree("kwTree","kwTree")
  kweight = array( 'f', [0] )
  kwtree.Branch('kweight', kweight, 'kweight/F')

  # Normalize kWeights and write
  print("Normalizing kWeights...")
  for i in range(nEntries) :
    if(i%10000==0) : print("{0:.2f} %".format(float(i)/nEntries*100.))
    kweight[0] = kwlist[i] * norm
    kwtree.Fill()

  kwtree.Write()
  kwfile.Close()
  print("kWeights written to {0}".format(outputfilename))
  


  
    

##############################
# First, plot to show what distributions we're dealing with
##############################

c1 = ROOT.TCanvas() # Dummy canvas for TTree::Draw calls

if(makeplots) :
  
  print("Making histograms for plotting")

  # Make the 1D histograms
  for i in range(2) :
    vari = "var{0}".format(i)
    var = variables[i]
    for datatype in ["data","sim"] :
      histname = datatype+"_1D_"+vari
      treedict[datatype].Draw("{0}>>{1}({2},{3},{4})".format(var, histname,
        nbins, ranges[i][0], ranges[i][1]), 
        "({0})*{1}".format(cuts[datatype], weights[datatype]) )
      histdict[ histname ] = ROOT.gDirectory.Get( histname )
      histdict[ histname ].SetTitle("")
      histdict[ histname ].GetXaxis().SetTitle(var)
      histdict[ histname ].SetLineWidth(2)
      histdict[ histname ].SetLineStyle( styledict[  datatype ] )
      histdict[ histname ].SetLineColor( colourdict[ datatype ] )

  # Make the 2D histograms
  for datatype in ["data","sim"] :
    histname = datatype+"_2D"
    treedict[datatype].Draw("{0}:{1}>>{2}({3},{4},{5},{6},{7},{8})".format(variables[1],variables[0], histname,
      nbins, ranges[0][0], ranges[0][1], nbins, ranges[1][0], ranges[1][1] ),
      "({0})*{1}".format(cuts[datatype], weights[datatype]) )
    histdict[ histname ] = ROOT.gDirectory.Get( histname )
    histdict[ histname ].SetTitle(histname)
    histdict[ histname ].GetXaxis().SetTitle(variables[0])
    histdict[ histname ].GetYaxis().SetTitle(variables[1])

  print("Drawing histograms")

  # Draw the 1D histograms
  for i in range(2) :
    vari = "var{0}".format(i)
    cname = "c_1D_"+vari
    canvasdict[ cname ] = ROOT.TCanvas(cname)
    histdict[ "data_1D_"+vari ].DrawNormalized()
    histdict[  "sim_1D_"+vari ].DrawNormalized("same")
    canvasdict[ cname ].Update()

  # Draw the 2D histograms
  binedgelines = makeBinningLines(binning, variables)
  for datatype in ["data","sim"] :
    cname = "c_2D_"+datatype
    canvasdict[ cname ] = ROOT.TCanvas(cname)
    histdict[ datatype+"_2D" ].Draw("colz")
    for line in binedgelines : line.Draw("same")
    canvasdict[ cname ].Update()
    canvasdict[ cname ].SaveAs(outputdir+"kWeights_2D_"+datatype+".pdf")






##############################
# Make kinematic weights, save as friendtree.
# This is the core business of this script.
##############################

kwfilename = outputdir + "kWeight_kwTree.root"
c1.cd()

# Make kWeight table
kweightTable = makeKweightsTable(treedict, variables, binning, cuts, weights) 

# Make kWeights friend tree for simtree
makeKweightsFriendTree(kweightTable, simtree, variables, kwfilename)

# Add friend tree to simulation
simtree.AddFriend("kwTree",kwfilename)





##############################
# Show off the effect of our kWeights
##############################

if(makeplots) :
 
  # Draw kWeights
  c_2D_kWeights = ROOT.TCanvas("c_2D_kWeights")
  kweightTable.Draw("colz")
  c_2D_kWeights.SaveAs(outputdir+"kWeights.pdf")

  c1.cd()
  legendas = {} # make dict for persistency

  # Draw reweighed sim distributions in the same 1D histograms
  for i in range(2) :
    vari = "var{0}".format(i)
    var = variables[i]
    histname = "kweighedsim_1D_"+vari
   
    # Draw reweighed sim distribution
    simtree.Draw("{0}>>{1}({2},{3},{4})".format(var, histname, nbins, ranges[i][0], ranges[i][1]), 
      "({0})*({1})*kwTree.kweight".format(cuts["sim"], weights["sim"]) )

    # Set some properties
    histdict[ histname ] = ROOT.gDirectory.Get( histname )
    histdict[ histname ].SetTitle(histname)
    histdict[ histname ].GetXaxis().SetTitle(variables[i])
    histdict[ histname ].SetLineWidth(2)
    histdict[ histname ].SetLineStyle( styledict[  "kweighed" ] )
    histdict[ histname ].SetLineColor( colourdict[ "kweighed" ] )
  
    # Make legend
    legendas[vari] = ROOT.TLegend(0.76,0.77,0.9,0.9)
    legendas[vari].AddEntry( histdict["data_1D_"+vari],         "data",     "l")
    legendas[vari].AddEntry( histdict["sim_1D_"+vari ],         "sim",      "l")
    legendas[vari].AddEntry( histdict["kweighedsim_1D_"+vari],  "rew. sim", "l")
  
    # Draw and save
    cname = "c_1D_"+vari
    canvasdict[ cname ].cd()
    histdict[ histname ].DrawNormalized("histsame")
    legendas[vari].Draw("same")
    canvasdict[ cname ].Update()
    canvasdict[ cname ].SaveAs(outputdir+"kWeights_1D_"+vari+".pdf")

