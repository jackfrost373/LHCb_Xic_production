import ROOT
from array import array

MCfile_loc  = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/29/1/output/MC_Lc2pKpiTuple_25103006.root"   #From reweighing.py in examples
MCtreename = "tuple_Lc2pKpi/DecayTree"

variables = ["lcplus_P", "lcplus_ETA"]

binning = { "lcplus_P" : [5000, 20000, 30000, 35000, 40000, 45000, 50000, 60000, 70000, 80000, 100000, 150000, 200000, 300000, 450000] ,
          "lcplus_ETA" : [2.0, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 4.0, 4.5, 5.5] }

cuts = { "MC" : "1==1" }  # sim should include MCTruth

weights = { "MC" : "1==1"  # data should contain sweight (but add friendTree then!)
              }

## outputdir = "./output/"

makeplots = True
nbins = 100 # bins for regular drawing

# set some stuff
ROOT.gStyle.SetOptStat(0) # remove hist info box
if not makeplots : ROOT.gROOT.SetBatch(True) # prevent graphical output
ranges = [ [binning[variables[0]][0], binning[variables[0]][-1]],
           [binning[variables[1]][0], binning[variables[1]][-1]] ]

#Get Data
MCfile  = ROOT.TFile.Open(MCfile_loc)
MCtree  = MCfile.Get(MCtreename)

# Make global dictionaries for easy access/looping.
# This will also prevent objects from going out-of-scope when created in function calls.
treedict = { "MC"  : MCtree }
colourdict = { "MC"  : 28,        # 28=brown
               "kweighed" : 46 }   # 46=red
styledict  = { "MC"  : 1,         # 1=solid
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


c1 = ROOT.TCanvas() # Dummy canvas for TTree::Draw calls

if(makeplots) :
  
  print("Making histograms for plotting")

  # Make the 1D histograms
  for i in range(2) :
    vari = "var{0}".format(i)
    var = variables[i]
    for datatype in ["MC"] :
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
  for datatype in ["MC"] :
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
    histdict[  "MC_1D_"+vari ].DrawNormalized("same")
    canvasdict[ cname ].Update()

  # Draw the 2D histograms
  binedgelines = makeBinningLines(binning, variables)
  for datatype in ["MC"] :
    cname = "c_2D_"+datatype
    canvasdict[ cname ] = ROOT.TCanvas(cname)
    histdict[ datatype+"_2D" ].Draw("colz")
    for line in binedgelines : line.Draw("same")
    canvasdict[ cname ].Update()
    ## canvasdict[ cname ].SaveAs(outputdir+"kWeights_2D_"+datatype+".pdf")