# Calculate PID efficiency of b2hh sample using the PIDCalib PerfHists
#  This is a self-written alternative to pidcalib's PerformMultiTrackCalib.

import ROOT as R
from python import bdkpi_reduce 
from math import sqrt
import re


tupleloc = "/eos/lhcb/user/j/jadevrie/tuples/b2mumu/bdkpi/"


# variables to draw sWeighed distributions for, and their range
#drawvars = [["muplus_P", [0,100000]], ["muplus_eta", [1.5,5.0]], ["nTracks",[0,500]]]
drawvars = []



############################################

particles = ["muplus","muminus"]

yeardict = { 
  "2011" : "Strip20r1",
  "2012" : "Strip20",
  "2015" : "Turbo15",
  "2016" : "Turbo16",
  "2017" : "Turbo17",
  "2018" : "Turbo18"
  }



def getPIDcuts(decay, cutvalue=5) :
  # defines PID cuts for b2hh
  if( decay=="KK" ) : return "(muplus_PIDK >  {0} && muminus_PIDK >  {0})".format(cutvalue)
  if( decay=="KPi") : return "(muplus_PIDK >  {0} && muminus_PIDK < -{0})".format(cutvalue)
  if( decay=="PiK") : return "(muplus_PIDK < -{0} && muminus_PIDK >  {0})".format(cutvalue)
  if( decay=="PiPi"): return "(muplus_PIDK < -{0} && muminus_PIDK < -{0})".format(cutvalue)
  return "(1==1)"

def setParameterFromOptions(PARNAME, optionstring, default=0) :
  # parse parameter value from options: "PID17" --> gets 17
  if(PARNAME in optionstring) : 
    param = re.findall( r'(?:{0})([0-9]+)'.format(PARNAME), optionstring )[0]
    print("==> OPTIONS: setting {0} to {1}".format(PARNAME,param))
    return param
  else : 
    return default

def masshypovar(decay, year="2016") :
  # B mass under different daughter mass hypothesis. Need for run1.
  # Edit: no longer required.
  #if("2011" in year or "2012" in year) :
  #  if(decay) == "KPi" : [massplus, massmin] = [m_kaon, m_pion]
  #  if(decay) == "PiK" : [massplus, massmin] = [m_pion, m_kaon]
  #  if(decay) == "KK"  : [massplus, massmin] = [m_kaon, m_kaon]
  #  Eplus   = "sqrt({0}**2 +  muplus_P**2)".format(massplus)
  #  Emin    = "sqrt({0}**2 + muminus_P**2)".format(massmin)
  #  Pvecdot = "({0}_PX*{1}_PX + {0}_PY*{1}_PY + {0}_PZ*{1}_PZ)".format("muplus","muminus")
  #  minv = "sqrt({0}**2 + {1}**2 + 2*{2}*{3} - 2*{4})".format(massplus,massmin,Eplus,Emin,Pvecdot) 
  #  return minv
  #else :
  #  return "B_M"+decay
  return "B_M"+decay

def drawWeighedDistributions(tree, var="B_MKPi", weightlist=["1"], window=[5100,5600],nbins=100,colors=[1,9,8,46]) :
  cDraw = R.TCanvas("cDraw_{0}".format(var))
  histos = []
  for i in range(len(weightlist)) :
    weight = weightlist[i]
    tree.Draw("{0}>>drawweighed_{1}({2},{3},{4})".format(var,weight,nbins,window[0],window[1]),weight)
    histos += [ R.gDirectory.Get("drawweighed_{0}".format(weight)) ]
    histos[i].SetLineColor(colors[i])
  histos[0].Draw()
  for histo in histos :
    histo.Draw("same")
  cDraw.Update()
  cDraw.SaveAs("output/sWeighed_{0}.pdf".format(var))
  return[cDraw,histos]




def calcPIDefficiency( year, mag, decay="KPi", bdtbin=0, tupleloc=tupleloc,
    pidbinvars = ["P","ETA","nTracks_Brunel"], b2hhbinvars = ["P","eta","nTracks"], optionstring="",
    ignoreB2hhStatErr = False, correctKinematics = True, binningscheme=""
    ) :

  assert(len(pidbinvars) == len(b2hhbinvars))
  assert(decay in ["KPi","PiK","KK"])
  assert(mag in ["Up","Down"])
  if(pidbinvars[2]=="nTracks_Brunel" and year in ["2011","2012"]) :
    print("Warning: Setting nTracks_Brunel to nTracks for non-turbo data")
    pidbinvars[2]="nTracks"
  if(pidbinvars[2]=="nTracks" and year in ["2015","2016","2017","2018"]) :
    print("Warning: Setting nTracks to nTracks_Brunel for turbo data")
    pidbinvars[2]="nTracks_Brunel"

  
  pidcut    = float( setParameterFromOptions("PID", optionstring, 5) )
  windowmin = float( setParameterFromOptions("XMIN", optionstring, 5100) )
  window = [windowmin, 5600.]

  simulation = False
  if ("_MC" in optionstring) : simulation = True

  pidcuts = { "K"  : "K_DLLK > {0:.1f}".format(float(pidcut)),
              "Pi" : "Pi_DLLK < -{0:.1f}".format(float(pidcut)) }
  
  print("\n*************************************************")
  print("Calculating PID efficiency for {0} {1} {2}, BDTbin {3}, PIDcut {4} ({5})".format(year,mag,decay,bdtbin,pidcut,optionstring))
  print("  (binning vars: {0} --> {1})".format(pidbinvars, b2hhbinvars))

  # get PIDCalib perfhists 
  perfhistFiles = {}
  perfhists = {}
  for particle in ["K", "Pi"] :
    perfhistfilename = "./pidcalib/UraniaDev_v7r0/PerfHists_{0}_{1}_Mag{2}{3}_{4}_{5}_{6}.root".format(
      particle,yeardict[year], mag, binningscheme, *pidbinvars)
    print("Opening {0}".format(perfhistfilename))
    perfhistFiles[particle] = R.TFile.Open(perfhistfilename)
    perfhists[particle] = perfhistFiles[particle].Get("{0}_All".format(pidcuts[particle]))
    #perfhists[particle].Sumw2() # already created.
    if(perfhists[particle]) == None : print(" Error: Cannot find histogram {0}_All".format(pidcuts[particle]))

  
  # Obtain binning used by PIDCalib
  ndims = len(pidbinvars)
  axesbins = {}
  if(ndims>0) : axesbins[0] = perfhists["K"].GetXaxis().GetXbins()
  if(ndims>1) : axesbins[1] = perfhists["K"].GetYaxis().GetXbins()
  if(ndims>2) : axesbins[2] = perfhists["K"].GetZaxis().GetXbins()
 
  axesbins_python = {}
  print("Found PIDCalib binning:")
  for i in range(ndims) :
    axesbins_python[i] = [ axesbins[i][j] for j in range(axesbins[i].GetSize()) ]
    print(" {0} : {1}".format(pidbinvars[i], axesbins_python[i]))

  nbinranges = []
  for i in range(ndims) :
    nbinranges += [1] # first bin, without underflow
    nbinranges += [ axesbins[i].GetSize() -1 ]


  # get b2hh tree
  files = []
  if("Up"   in mag) : files += bdkpi_reduce.getCutFiles(year,"up",   baseloc=tupleloc, optionstring=optionstring)
  if("Down" in mag) : files += bdkpi_reduce.getCutFiles(year,"down", baseloc=tupleloc, optionstring=optionstring)
  treeload = R.TChain("DecayTree")
  for f in files : 
    print("- Adding {0}".format(f))
    treeload.Add(f)

 
 # define cuts: should be identical to sWeight production, in order to have same #entries
  if not simulation :
    cuts_pid  = getPIDcuts(decay, cutvalue=pidcut)#.replace(">",">=").replace("<","<=")
    cuts_bdt  = R.c_BDTbin_dict[year][bdtbin]#.replace(">",">=").replace("<","<=")
    cuts_mass = "{0} > {1} && {0} < {2}".format(masshypovar(decay,year), window[0], window[1])
    cuts_b2hh = "( ({0}) && ({1}) && ({2}) )".format(cuts_pid, cuts_bdt, cuts_mass)
  if simulation : 
    cuts_bdt  = R.c_BDTbin_dict[year][bdtbin]#.replace(">",">=").replace("<","<=")
    cuts_b2hh = cuts_bdt 
    # add MCMatching?
  
  dummyfile = R.TFile.Open("/tmp/dummy.root","RECREATE")
  tree = treeload.CopyTree(cuts_b2hh)
  print("\nnEntries in b2hh after cuts: {0}".format(tree.GetEntries()))


  # add sWeights
  if not simulation :
    swfilename = "{0}/b2hh_sWeights/sWeight_{1}_{2}_{3}_bdtbin{4}{5}.root".format(tupleloc,year,mag.lower(),decay,bdtbin,optionstring)
    print("adding sWeight tree: {0}".format(swfilename))
    tree.AddFriend("swTree",swfilename)
    if decay in ["KPi","PiK"] : weight = "swTree.sw_n_bd"
    if decay in ["KK"]        : weight = "swTree.sw_n_bs"
  if simulation :
    weight = "1."

  if not simulation : 
    # Draw weighed 1D distributions for given variables
    drawweights = ["1","swTree.sw_n_bd","swTree.sw_n_bs","swTree.sw_n_comb"]
    for i in drawvars :
      [drawvar, drawwindow] = i
      [cDraw,cDrawHistos] = drawWeighedDistributions(tree, drawvar, drawweights, drawwindow)


  # define decay-specific parameters 
  if(decay=="KPi") : b2hh_particlemap = { "muplus" : "K" , "muminus" : "Pi" } 
  if(decay=="PiK") : b2hh_particlemap = { "muplus" : "Pi", "muminus" : "K"  } 
  if(decay=="KK")  : b2hh_particlemap = { "muplus" : "K",  "muminus" : "K"  } 

  
  # draw b2hh histogram in same binning as PIDCalib perfhists
  print("Drawing b2hh histograms")
  c1 = R.TCanvas("c1")
  b2hhHists = {}
  for particle in particles :
    histname = "b2hhHist_{0}".format(particle)
    if(ndims>0) : var0 = "{0}_{1}".format(particle,b2hhbinvars[0])
    if(ndims>1) : var1 = "{0}_{1}".format(particle,b2hhbinvars[1])
    if(ndims>2) : var2 = "{0}_{1}".format(particle,b2hhbinvars[2])
    if(ndims>2 and ("nTracks" in b2hhbinvars[2] or "SPD" in b2hhbinvars[2])) : var2 = b2hhbinvars[2]

    if(ndims==1) : 
      b2hhHists[particle] = R.TH1F(histname,histname, axesbins[0].GetSize()-1, axesbins[0].GetArray())
      tree.Draw("{0}>>+{1}".format(var0,histname), 
                "{0}".format(weight))
    if(ndims==2) :
      b2hhHists[particle] = R.TH2F(histname,histname, axesbins[0].GetSize()-1, axesbins[0].GetArray(), 
                                                      axesbins[1].GetSize()-1, axesbins[1].GetArray())
      tree.Draw("{0}:{1}>>+{2}".format(var1,var0,histname), 
                "{0}".format(weight))
    if(ndims==3) :
      b2hhHists[particle] = R.TH3F(histname,histname, axesbins[0].GetSize()-1, axesbins[0].GetArray(), 
                                                      axesbins[1].GetSize()-1, axesbins[1].GetArray(), 
                                                      axesbins[2].GetSize()-1, axesbins[2].GetArray())
      tree.Draw("{0}:{1}:{2}>>+{3}".format(var2,var1,var0,histname), 
                "{0}".format(weight))

    if(ndims>0) : b2hhHists[particle].GetXaxis().SetTitle( var0 ) 
    if(ndims>1) : b2hhHists[particle].GetYaxis().SetTitle( var1 ) 
    if(ndims>2) : b2hhHists[particle].GetZaxis().SetTitle( var2 ) 


  if(ignoreB2hhStatErr) :
    # ignore stat errors on the b2hh sample, since already counted in yield 
    print("Setting b2hh stat errors to 0")
    for particle in particles :
      histo = b2hhHists[particle]
      for binx in range(1,histo.GetNbinsX()+1) :
        for biny in range(1,histo.GetNbinsY()+1) :
          for binz in range(1,histo.GetNbinsZ()+1) :
            ibin = histo.GetBin(binx,biny,binz)
            b2hhHists[particle].SetBinError(ibin, 0.)



  
  if(correctKinematics) :
    # apply 1/PID efficiencies as weights, to correct kinematics due to the PID cut itself.
    print("Applying 1/PIDeff as additional weights to correct kinematics")
    for particle in particles :
      #beforehist = b2hhHists[particle].ProjectionX().Clone("beforehist")
      #b2hhHists[particle].Divide( perfhists[ b2hh_particlemap[particle] ] )
      #afterhist = b2hhHists[particle].ProjectionX().Clone("afterhist")

      # To get the errors right, we have to do this bin-by-bin instead.
      weighthist = R.TH1F("weighthist","weighthist",25,0,1) # for visualizing weight distribution
      histo = b2hhHists[particle]
      perfhist = perfhists[ b2hh_particlemap[particle] ]
      for binx in range(1,histo.GetNbinsX()+1) :
        for biny in range(1,histo.GetNbinsY()+1) :
          for binz in range(1,histo.GetNbinsZ()+1) :
            ibin = histo.GetBin(binx,biny,binz)
            b2hh_val = histo.GetBinContent(ibin)
            b2hh_err = histo.GetBinError(ibin)
            pid_val  = perfhist.GetBinContent(ibin)
            pid_err  = perfhist.GetBinError(ibin)
            if(pid_val < 0.05) : pid_val = 0.05 # cutoff to avoid large weights
            weighthist.Fill(pid_val, b2hh_val)
            if not pid_val == 0 : newval = b2hh_val / pid_val
            else : newval = 0.
            newerr = 0.
            if not b2hh_val == 0 : newerr += (b2hh_err/b2hh_val)**2
            if not pid_val  == 0 : newerr += (pid_err /pid_val )**2
            newerr = sqrt( newerr ) * newval ## TODO is this correct? gives the same total error!
            b2hhHists[particle].SetBinContent(ibin, newval)
            b2hhHists[particle].SetBinError(ibin, newerr)
      weighthist.SetTitle("PID eff distribution ; PID eff ; Count")
      #cweight = R.TCanvas("cweight","cweight")
      #weighthist.Draw("H")
      #cweight.Update()
      #cweight.SaveAs("weighthist{0}.pdf".format(particle))
  
  
  
  if(False) :
    # do a naive bin-by-bin loop, to see if it matches the faster 'Integrate' result below
    print("Performing naive check:")
    for particle in particles :
      efftotal = 0.
      errtotal = 0.
      ntotal = 0.
      histo = b2hhHists[particle]
      perfhist = perfhists[ b2hh_particlemap[particle] ]
      for binx in range(1,histo.GetNbinsX()+1) :
        for biny in range(1,histo.GetNbinsY()+1) :
          for binz in range(1,histo.GetNbinsZ()+1) :
            ibin = histo.GetBin(binx,biny,binz)
            #print(" ibin location XYZ: {0}, {1}, {2}".format( histo.GetXaxis().GetBinCenter(binx), 
            #  histo.GetYaxis().GetBinCenter(biny), histo.GetZaxis().GetBinCenter(binz) ))
            b2hh_val = histo.GetBinContent(ibin)
            b2hh_err = histo.GetBinError(ibin)
            pid_val  = perfhist.GetBinContent(ibin)
            pid_err  = perfhist.GetBinError(ibin)
            efftotal += b2hh_val * pid_val
            errtotal += b2hh_err * pid_val + pid_err * b2hh_val
            ntotal += b2hh_val
            #print("Bin: {0},{1},{2} - eff = {3:.3f} ; val = {4:.3f} --> TOT={5:.3f}".format(binx,biny,binz,pid_val, b2hh_val, efftotal/ntotal))
      result = efftotal / ntotal
      reserr = errtotal / ntotal
      print(" --> bin-looped result for {0}: {1} +- {2}".format(particle,result, reserr))
    



  # Multiply to obtain total efficiency
  effs = {}
  for particle in particles :
    b2hhHist = b2hhHists[particle]
    #b2hhHist.Sumw2() # is already created
    ntotal = b2hhHist.Integral(*nbinranges)
    
    b2hhHist.Multiply( perfhists[ b2hh_particlemap[particle] ] )
    efftotal_error = R.Double(0)
    efftotal = b2hhHist.IntegralAndError(*(nbinranges + [efftotal_error]))
    efftotal = efftotal / ntotal
    efftotal_error = efftotal_error / ntotal
    print("PID eff {0}  \t= {1:.4f} +- {2:.4f}".format(particle, efftotal, efftotal_error))
    effs[particle] = [efftotal, efftotal_error]

  # compute total eff, assuming full correlation for the error
  totaleff = effs["muplus"][0] * effs["muminus"][0]
  totaleff_error = (effs["muplus"][1] / effs["muplus"][0] + effs["muminus"][1] / effs["muminus"][0]) * totaleff
  print("Total {0} eff   \t= {1:.4f} +- {2:.4f}".format(decay, totaleff, totaleff_error))
  return [totaleff, totaleff_error]
