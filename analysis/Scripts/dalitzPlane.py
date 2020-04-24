#################
# Dalitz plot / sPlot
# Requires sweights script and Imports.py
#################


import ROOT, sys, getopt, os
import Imports



# Define what type of plot you want
dataType = "MC" #dataType = MC (monte carlo), or = data
particle = "Lc" # valid types :- Xic or Lc (For MC studies)
# Define if you want to add sWeights
addsWeights = True

#Input dir is where the reduce tuples are, output is where we will make our plots and our friend trees are in sweightdir
inputdir = "/dcache/bfys/scalo/binned_files/"
sweightsdir = "/data/bfys/cpawley/sWeights/"
outputdir = "/data/bfys/cpawley/dalitz/"


#Years, Mag pol and part. types hardcoded
years = [2011,2012,2015,2016,2017,2018]
magPol= ["MagUp","MagDown"]
particle_types=["Lc","Xic"]

#y and pt bins may vary - so we import them
y_bin_temp = Imports.getYbins()
y_bin=[]
for y in y_bin_temp:
  y_bin.append("{}-{}".format(y[0],y[1]))

pt_bin_temp = Imports.getPTbins() 
pt_bin=[]
for pt in pt_bin_temp:
  pt_bin.append("{}-{}".format(pt[0],pt[1]))

def invariantMass(p1, p2) :
  # build invariant mass string
    m1  = p1+"_M" ; ptot1 = p1+"_P" ; px1 = p1+"_PX" ; py1 = p1+"_PY" ; pz1 = p1+"_PZ"
    m2  = p2+"_M" ; ptot2 = p2+"_P" ; px2 = p2+"_PX" ; py2 = p2+"_PY" ; pz2 = p2+"_PZ"
    E1 = "sqrt({0}**2 + {1}**2)".format(m1,ptot1)
    E2 = "sqrt({0}**2 + {1}**2)".format(m2,ptot2)
    pvecdot = "({0}*{1} + {2}*{3} + {4}*{5})".format(px1,px2, py1,py2, pz1,pz2)
    M2 = "({0}**2 + {1}**2 + 2*{2}*{3} - 2*{4})".format(m1,m2,E1,E2,pvecdot)
    #print (M2)
    return (M2.replace("piplus_M","139.57").replace("kminus_M","493.68").replace("pplus_M","938.27")) #Returns Masses as numbers in MeV

def main(argv):
  global outputdir
  global sweightsdir
  #Stop ROOT printing graphs so much
  ROOT.gROOT.SetBatch(True)
  #Define masses (missing from our nTuples)
  #piplus_M=139.57#MeV
  #kminus_M=493.68#MeV
  #pplus_M=938.27#MeV

  


  ## parse the arguments from command line into arrays for us to check:
  print ("Starting to parse the command line input")
  try:
    opts,args=getopt.getopt(argv,"hm:y:o:p:r:t:")
  except getopt.GetoptError:
    print("Incorrect Arguements used in sWeights")
    sys.exit(2)

  options=[]
  arguments=[]

  for opt,arg in opts:
    options.append(opt)
    arguments.append(arg)


    #Check inputs are viable/match what is possible
    #What happens when we don't enter parameters? maybe we need to look for length>0 first
  print ("Checking for parameter errors")
  mode=arguments[options.index("-m")]
  print (mode)
  if (mode!="single" and mode!="combined" and mode!="year"):
    print ("Wrong looping mode input to Dalitz...exiting...")
    sys.exit()
  
  year=int(arguments[options.index("-y")])
  if year not in years:
    print("Wrong year input to Dalitz...exiting...")
    sys.exit()

  magpol=arguments[options.index("-o")]
  if (magpol=="Up"):
    magpol="MagUp"
  elif (magpol=="Down"):
    magpol="MagDown"
  else:
    print ("Wrong magnet polarity input to Dalitz...exiting...")
    sys.exit()

  particle = arguments[options.index("-p")]
  if (particle!="Xic" and particle!="Lc" ):
    print("Wrong particle name input to Dalitz...exiting...")
    sys.exit()
  
  for r in range(len(options)):
    if options[r]=="-r":
      rapidity=arguments[options.index("-r")]
      if rapidity not in y_bin:
        print("Wrong y bin input to Dalitz...exiting...")
        sys.exit()

  for t in range(len(options)):
    if options[t]=="-t":
      pt=arguments[options.index("-t")]
      if pt not in pt_bin:
        print("Wrong Pt bin input to Dalitz...exiting...")
        sys.exit()

#Check sufficient parameters entered


  if mode=="single":
    #all parameters need to be entered
    if set(options)!=set(["-y","-o","-p","-r","-t"]):
      print("Entered too few parameters in Dalitz  mode <single>...exiting...")
      sys.exit()
    elif mode=="combined":
    #one of r and t must be missing
      if set(options)!=set(["-y","-o","-p","-r"]) and set(options)!=set(["-y","-o","-p","-t"]):
        print("Entered too few parameters in Dalitz  mode <combined>...exiting...")
        sys.exit()
    elif mode=="year":
    #r and t must both be missing, all other params present
      if set(options)!=set(["-y","-o","-p"]):
        print("Entered too few parameters in Dalitz mode <year>...exiting...")
        sys.exit()

  if(True) :
    if mode=="single":
      print ("I am working on "+str(year)+" "+magpol+" "+particle+" "+rapidity+" "+pt)
      filestring=str(year)+"_"+magpol+"/bins/y_ptbins/"+particle+"_y_bin_"+rapidity+"_ptbin_"+pt+".root"
      outputdir +=  str(year)+"_"+magpol+"/bins/y_ptbins/"
      sweightsdir +=  str (year)+"_"+magpol+"/bins/y_ptbins/"
      outputname=particle+"_y_bin_"+rapidity+"_ptbin_"+pt
    elif mode=="combined":
      for r in range(len(options)):
        if options[r]=="-r":
          print ("I am working on "+str(year)+" "+magpol+" "+particle+" "+rapidity)
          filestring=str(year)+"_"+magpol+"/bins/ybins/"+particle+"_ybin_"+rapidity+".root"
          outputdir +=  str(year)+"_"+magpol+"/bins/ybins/"
          sweightsdir +=  str(year)+"_"+magpol+"/bins/ybins/"
          outputname=particle+"_y_bin_"+rapidity
        elif r==len(options):
          print ("I am working on "+str(year)+" "+magpol+" "+particle+" "+pt)
          filestring=str(year)+"_"+magpol+"/bins/ptbins/"+particle+"_ptbin_"+pt+".root"
          outputdir +=  str (year)+"_"+magpol+"/bins/ptbins/"
          sweightsdir +=  str (year)+"_"+magpol+"/bins/ptbins/"
          outputname=particle+"_ptbin_"+pt
    elif mode=="year":
      print ("I am working on "+str(year)+" "+magpol+" "+particle+" Total")
      filestring=str(year)+"_"+magpol+"/"+particle+"_total.root"
      outputdir += str(year)+"_"+magpol+"/"
      sweightsdir +=  str(year)+"_"+magpol+"/"
      outputname=particle+"_total"
    print ("loading tree from "+inputdir+filestring)
    f = ROOT.TFile.Open(inputdir+filestring, "READONLY")
    tree = f.Get("DecayTree")
    cuts = "1==1"

    if not os.path.exists(outputdir):
      os.makedirs(outputdir)


#elif dataType == "MC": #Todo: check both trees for updates from ganga?
#  cuts = getMCCuts(particle)
#  addsWeights = False  #double check to ensure sWeights never used for MC files
#  if particle == "Xic":
#    Xic_MC_datatree_1()
#    tree = Xic_MC_tree_1 #Todo: check tree 1 or 2 or both?
#  if particle == "Lc":
#    Lc_MC_datatree()
#    tree = Lc_MC_tree


  if(addsWeights) :
    print ("adding sWeights")
    # If we made an sWeight friend tree: add it, and use sWeights. Make sure same cuts (--> #entries) as swTree!
    wfile = ROOT.TFile.Open("{0}dalitz_temp.root".format(outputdir),"RECREATE")
    swcuts = "lcplus_MM >= 2240 && lcplus_MM <= 2340 "#&& lcplus_P >= 5000 && lcplus_P <= 200000 && lcplus_TAU >= 0 && lcplus_TAU <= 0.007"
    #swcuts = "1==1"
    tree.Print()
    cuttree = tree.CopyTree(swcuts)
    cuttree.Print()
    print("cutTree nEvents = {0}".format(cuttree.GetEntries()))
    cuttree.AddFriend("dataNew","{0}_sWeight_swTree.root".format(sweightsdir+outputname))
    weightvar = "dataNew.L_Actual_signalshape_Norm"
    print ("finished adding sWeights")
  else :
    cuttree = tree
    weightvar = "1"
    


  
  

  print ("building invarient mass strings")
  m2_pK  = invariantMass("piplus","kminus")
  m2_Kpi = invariantMass("kminus","pplus")

  
  c1 = ROOT.TCanvas("c1","c1")
  ROOT.gStyle.SetOptStat(0)

  cuttree.Draw("{0}:{1}>>dalitzHist(100,300e3,2500e3,100,1800e3,5800e3)".format(m2_pK,m2_Kpi), "{0}*{1}".format(cuts,weightvar))
  dalitzHist = ROOT.gDirectory.Get("dalitzHist")
  dalitzHist.SetTitle("Dalitz plot of pK#pi")
  dalitzHist.GetYaxis().SetTitle("m^{2}_{pK} [MeV^{2}/c^{4}]")
  dalitzHist.GetXaxis().SetTitle("m^{2}_{K#pi} [MeV^{2}/c^{4}]")

  if(addsWeights) :
    # set negative sWeight bin contents to zero for color visibility
    dalitzHist.SetMinimum(0)
    dalitzHist.SetTitle("sWeighed Dalitz plot of pK#pi")

  dalitzHist.Draw("colz")
  c1.Update()
  c1.SaveAs("{0}_Dalitz.pdf".format(outputdir+outputname))



if (__name__ == "__main__") :
   main(sys.argv[1:])
