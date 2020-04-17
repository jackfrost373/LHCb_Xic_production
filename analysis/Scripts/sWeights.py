#################
# Example of sWeight / sPlot using RooStats,
# as per https://arxiv.org/abs/physics/0402083
#################
import sys
sys.path.append('./MassFitting/')
import ROOT, Imports, getopt, os,fit
from Imports import *


#Which steps of the sWeights do we want to do?
getData        = True  # Load data.
makesWeights   = True  # Generate sWeights, write to workspace. Requires getData.
makeFriendTree = True  # create friend tree for simple future sweight plotting. Requires makesWeights.
plotVariable   = True  # make an sPlot using sWeights in RooDataSet from workspace.
testFriendTree = False  # test sWeights from friend tree to do an sPlot.

#Input dir is where the reduce tuples are, output is where we will make our plots and our friend trees
inputdir = "/dcache/bfys/scalo/binned_files/"
outputdir = "/data/bfys/cpawley/sWeights/"

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

def getVarfromList (name,list_to_search):
  #search a list for a var name - as used in Bs2mumu by JdV
  var=next((x for x in list_to_search if x.GetName()==name),None)
  return var

def main(argv):
  global outputdir
  fail=0
  #Stop ROOT printing graphs so much
  ROOT.gROOT.SetBatch(True)

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

    print (options, arguments)

    #Check inputs are viable/match what is possible
    #What happens when we don't enter parameters? maybe we need to look for length>0 first
  print ("Checking for parameter errors")
  mode=arguments[options.index("-m")]
  if (mode!="single" and mode!="combined" and mode!="year"):
    print ("Wrong looping mode input to sWeights...exiting...")
    sys.exit()

  year=int(arguments[options.index("-y")])
  if year not in years:
    print("Wrong year input to sWeights...exiting...")
    sys.exit()

  magpol=arguments[options.index("-o")]
  if (magpol=="Up"):
    magpol="MagUp"
  elif (magpol=="Down"):
    magpol="MagDown"
  else:
    print ("Wrong magnet polarity input to sWeights...exiting...")
    sys.exit()

  particle = arguments[options.index("-p")]
  if (particle!="Xic" and particle!="Lc" ):
    print("Wrong particle name input to sWeights...exiting...")
    sys.exit()
  
  for r in range(len(options)):
    if options[r]=="-r":
      rapidity=arguments[options.index("-r")]
      if rapidity not in y_bin:
        print("Wrong y bin input to sWeights...exiting...")
        sys.exit()

  for t in range(len(options)):
    if options[t]=="-t":
      pt=arguments[options.index("-t")]
      if pt not in pt_bin:
        print("Wrong Pt bin input to sWeights...exiting...")
        sys.exit()

#Check sufficient parameters entered


  if mode=="single":
    #all parameters need to be entered
    if set(options)!=set(["-y","-o","-p","-r","-t"]):
      print("Entered too few parameters in sWeights mode <single>...exiting...")
      sys.exit()
    elif mode=="combined":
    #one of r and t must be missing
      if set(options)!=set(["-y","-o","-p","-r"]) and set(options)!=set(["-y","-o","-p","-t"]):
        print("Entered too few parameters in sWeights mode <combined>...exiting...")
        sys.exit()
    elif mode=="year":
    #r and t must both be missing, all other params present
      if set(options)!=set(["-y","-o","-p"]):
        print("Entered too few parameters in sWeights mode <year>...exiting...")
        sys.exit()

  if(getData) :
#get the data
    if mode=="single":
      print ("I am working on "+str(year)+" "+magpol+" "+particle+" "+rapidity+" "+pt)
      filestring=str(year)+"_"+magpol+"/bins/y_ptbins/"+particle+"_y_bin_"+rapidity+"_ptbin_"+pt+".root"
      outputdir += str(year)+"_"+magpol+"/bins/y_ptbins/"
      outputname=particle+"_y_bin_"+rapidity+"_ptbin_"+pt
    elif mode=="combined":
      for r in range(len(options)):
        if options[r]=="-r":
          print ("I am working on "+str(year)+" "+magpol+" "+particle+" "+rapidity)
          filestring=str(year)+"_"+magpol+"/bins/ybins/"+particle+"_ybin_"+rapidity+".root"
          outputdir +=  str(year)+"_"+magpol+"/bins/ybins/"
          outputname=particle+"_y_bin_"+rapidity
        elif r==len(options):
          print ("I am working on "+str(year)+" "+magpol+" "+particle+" "+pt)
          filestring=str(year)+"_"+magpol+"/bins/ptbins/"+particle+"_ptbin_"+pt+".root"
          outputdir +=  str (year)+"_"+magpol+"/bins/ptbins/"
          outputname=particle+"_ptbin_"+pt    
    elif mode=="year":
      print ("I am working on "+str(year)+" "+magpol+" "+particle+" Total")
      filestring=str(year)+"_"+magpol+"/"+particle+"_total.root"
      outputdir += str(year)+"_"+magpol+"/"
      outputname=particle+"_total"
    f = ROOT.TFile.Open(inputdir+filestring, "READONLY")
    tree = f.Get("DecayTree")
    cuts = "1==1"
    parsefile=(outputdir.split("/"))
    if not os.path.exists(outputdir):
      os.makedirs(outputdir)
              
    if particle == "Lc":
          
      mass = ROOT.RooRealVar("lcplus_MM","Lc_mass",2240,2340,"MeV/c^{2}")
      #todo: check number of entries, inclusive or exclusive???
      momentum = ROOT.RooRealVar("lcplus_P","Lc_P",5000,200000,"MeV/c")
      lifetime = ROOT.RooRealVar("lcplus_TAU","Lc_tau",0,0.007,"ns")
              
    elif particle == "Xic":
                       
      mass= ROOT.RooRealVar("lcplus_MM","XiC_mass", 2420,2520,"MeC/c^{2}")
      momentum= ROOT.RooRealVar("lcplus_P","XiC_P",5000,200000,"MeV/c")
      lifetime= ROOT.RooRealVar("lcplus_TAU","XiC_tau",0,0.007,"ns")
                       
    else: print ("I did not find the right particle, this is a problem")

  if(makesWeights) :

         # build the fit model
    print ("Building the fit model...")
    if magpol == "MagDown":
      mag="down"
    elif magpol == "MagUp":
      mag="up"
      
    if mode == "single":
        fit.main(["-m", "single","-y", year, "-o", mag, "-p", particle, "-r", rapidity, "-t", pt])
      
    elif mode == "combined":
      for r in range(len(options)):
        if options[r]=="-r":
          fit.main(["-m", "combined","-y", year,"-o", mag, "-p", particle,"-r", rapidity])
        elif (r==len(options)):
          fit.main(["-m", "combined","-y", year,"-o", mag, "-p", particle,"-t", pt])
    elif mode == "year":
        fit.main(["-m", "year", "-y", year, "-o", mag,"-p", particle])
    print("opening model file")    
    f1=ROOT.TFile.Open("MassFitting/model.root","READONLY")
    w=f1.Get("w")
    model=w.pdf("fullshape")
    data=w.data("masshist_RooFit")
    sig_norm=w.var("Actual_signalshape_Norm")
    bkg_norm=w.var("exponential_Norm")
    
    # Create sPlot object. This will instantiate 'sig_norm_sw' and 'bkg_norm_sw' vars in the data. 
    
    print ("Starting sWeights")
    sData = ROOT.RooStats.SPlot("sData", "an SPlot", data, model, ROOT.RooArgList(sig_norm,bkg_norm) )
    print ("sWeights is done")
      # Check sWeights - does not work in the current implimentation.
    if(False) :
      print("")
      print("sWeight sanity check:")
      print("sig Yield is {0}, from sWeights it is {1}".format(sig_norm.getVal(), sData.GetYieldFromSWeight("L_Actual_signalshape_Norm")))
      print("big Yield is {0}, from sWeights it is {1}".format(bkg_norm.getVal(), sData.GetYieldFromSWeight("L_exponential_Norm")))
      print("First 10 events:")
      for i in range(10) :
        print(" {0}: sigWeight = {1}, bkgWeight = {2}, totWeight = {3}".format(
        i, sData.GetSWeight(i,"sig_norm"), sData.GetSWeight(i,"bkg_norm"), sData.GetSumOfEventSWeight(i)))
    
  if(makeFriendTree) :
          # Make a new TTree that contains the sWeights for every event.
          # Makes use of the previously defined data and sData objects.

          print ("creating TTree and writing to file for sWeights...")
                  
          fileFriendTree = ROOT.TFile.Open("{0}{1}_sWeight_swTree.root".format(outputdir,outputname),"RECREATE")
          #fileFriendTree = ROOT.TFile.Open("Test_sWeight_swTree.root","RECREATE")
          newData = sData.GetSDataSet()
          dataNew = ROOT.RooDataSet("dataNew","dataNew",newData,newData.get())
          friendTree = dataNew.GetClonedTree()
          friendTree.Write()
          fileFriendTree.Close()
          print (".....TTree created with sWeights...")


  if(plotVariable) :

          # Plot sWeighted variable distribution from RooDataSet.
          
          #variable = "lcplus_P"
          variable = "lcplus_MM"

          # load sWeights from file (note: we will use 'data' as above, since we have just made it 
          # (i.e. we never expect to run plot without first getData) - thus it is commended out.

          fileFriendTree = ROOT.TFile.Open("{0}/{1}_sWeight_swTree.root".format(outputdir,outputname),("READONLY"))
          Friendtree = fileFriendTree.Get("dataNew")
          cuts = "1==1"

          Actual_signalshape_Norm_sw=ROOT.RooRealVar("Actual_signalshape_Norm_sw","signal",-5,5)
          exponential_Norm_sw=ROOT.RooRealVar("exponential_Norm_sw","background",-5,5)
        
          data = ROOT.RooDataSet("data","data set", Friendtree, ROOT.RooArgSet(mass,momentum,lifetime, Actual_signalshape_Norm_sw, exponential_Norm_sw), cuts)
          
          data_sig = ROOT.RooDataSet("data_sig", "sWeighed signal data", data, data.get(), "1==1", "Actual_signalshape_Norm_sw")
          data_bkg = ROOT.RooDataSet("data_bkg", "sWeighed bkgrnd data", data, data.get(), "1==1", "exponential_Norm_sw")
          
          c2 = ROOT.TCanvas("c2","c2")

          frame = mass.frame()
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
          c2.SaveAs("{0}_sPlot_{1}.pdf".format(outputdir+outputname,variable))
          #c2.SaveAs("Test_sPlot.pdf")
  if(testFriendTree) :

          # Make an sPlot using the sWeights from the friendTree, without RooFit / RooStats functionality.
          # Can be used to plot any variable in the original TTree.

          #[var,nbins,xmin,xmax] = ["lcplus_P",100,5000,200000]
          [var,nbins,xmin,xmax] = ["lcplus_TAU",100,0,0.007]

          # Load original TTree
          
          f = ROOT.TFile.Open(inputdir+name+"/bins/"+particle_type+"_bin"+y_bin+pt_bin+".root", "READONLY")
          tree = f.Get("DecayTree")
             
          # cuts should match those applied when creating the sWeight TTree --> should have same #entries!
          #  Note: limited range of RooRealVars in RooDataSet (used to create sWeights) also cuts events.
          datacuts = "1==1"
          datacuts += " && lcplus_MM >= 2240 && lcplus_MM <= 2340 && lcplus_P >= 5000 && lcplus_P <= 200000 && lcplus_TAU >= 0 && lcplus_TAU <= 0.007"
     
          print("beginning CopyTree")
          wfile = ROOT.TFile.Open(outputdir+name+"/cuttree.root","RECREATE")
          cuttree = tree.CopyTree(datacuts)

          print("cutTree nEvents = {0}".format(cuttree.GetEntries()))

          # add sWeight tree as friend. Should match #entries!
          cuttree.AddFriend("swTree","{0}/{1}_sWeight_swTree.root".format(outputdir+name,particle_type+y_bin+pt_bin))

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
          c4.SaveAs("{0}/{1}_sPlot_swTree_{2}.pdf".format(outputdir+name,particle_type+y_bin+pt_bin,var))
  return 
if __name__=="__main__":
  main(sys.argv[1:])
