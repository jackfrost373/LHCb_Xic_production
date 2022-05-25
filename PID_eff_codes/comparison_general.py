import ROOT
from ROOT import TChain
import os
import fnmatch


kinvars = ["P", "ETA", "nTracks"]
drawvars = {"P":[0.0, 140000], "ETA":[0.0, 6], "nTracks":[0.0, 600]}
particles = ["pplus","kminus", "piplus"]
particles_short ={
  "pplus" : "P",
  "kminus" : "K",
  "piplus" : "Pi",
}
magnitudes = ["MagDown"]
PID_cuts = {
  "pplus" : "ProbNNp > 0.5 && DLLp > 0_",
  "kminus" : "ProbNNK > 0.4 && DLLK > 0_",
  "piplus" : "ProbNNpi > 0.5_",
}
years = ["2017"]
yeardict = { 
  "2015" : "Turbo15",
  "2016" : "Turbo16",
  "2017" : "Turbo17",
  }


def make_comparison_graph_plot(particle, year, magnitude, kinvar, PID_cut):

  c1 = ROOT.TCanvas('c1', f'{kinvar} of {particle}')

  PIDfolder = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v7r0/"
  PIDfilename = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_BHH_Binning_P_ETA_nTracks_Brunel.root"
  PIDfile = ROOT.TFile.Open(PIDfolder + PIDfilename)
  PIDhistbeforecut_name = f"TotalHist_{particles_short[particle]}_MC15TuneV1_{PID_cut}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
  PIDhistbeforecut = PIDfile.Get(PIDhistbeforecut_name)

  if kinvar=='P':
    X = PIDhistbeforecut.ProjectionX('X')
  if kinvar=='ETA':
    X = PIDhistbeforecut.ProjectionY('X')  
  if kinvar=='nTracks':
    X = PIDhistbeforecut.ProjectionZ('X')

  filedir = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/102"
  subjobs = next(os.walk(filedir))[1]
  filename = "MC_Lc2pKpiTuple_26103090.root"
  excludedjobs = []

  tree = TChain("tuple_Lc2pKpi/DecayTree")

  for job in subjobs:
    if not job in excludedjobs :
      print("- Adding subjobs {0}".format(job))
      tree.Add("{0}/{1}/{2}".format(filedir,job,filename))

  axesbins = X.GetXaxis().GetXbins()
  myhistogram_Lc = ROOT.TH1F('myhistogram_Lc',f'Comparison of {particle} in {kinvar} space phase', axesbins.GetSize()-1, axesbins.GetArray())
  if kinvar in ["P", "ETA"]:
    tree.Draw(f"{particle}_{kinvar}>>+myhistogram_Lc")
  if kinvar == "nTracks":
    tree.Draw(f"{kinvar}>>+myhistogram_Lc")
  filedir = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/16"
  subjobs = next(os.walk(filedir))[1]
  filename = "MC_Lc2pKpiTuple_26103092.root"
  excludedjobs = []

  tree = TChain("tuple_Lc2pKpi/DecayTree")

  for job in subjobs:
    if not job in excludedjobs :
      print("- Adding subjobs {0}".format(job))
      tree.Add("{0}/{1}/{2}".format(filedir,job,filename))

  myhistogram_Xic = ROOT.TH1F('myhistogram_Xic',f'Comparison of {particle} in {kinvar} space phase', axesbins.GetSize()-1, axesbins.GetArray())
  if kinvar in ["P", "ETA"]:
    tree.Draw(f"{particle}_{kinvar}>>+myhistogram_Xic")
  if kinvar == "nTracks":
    tree.Draw(f"{kinvar}>>+myhistogram_Xic")

  myhistogram_Lc.SetLineColor(30)
  myhistogram_Lc.SetLineWidth(4)
  myhistogram_Lc.GetXaxis().SetTitle(f'{kinvar}_{particle}')
  myhistogram_Lc.GetYaxis().SetTitle('Number of events')
  myhistogram_Lc.SetStats(0)
  myhistogram_Lc.GetXaxis().SetRangeUser( *drawvars[kinvar] )
  X.SetLineColor(38)
  X.SetLineWidth(4)
  myhistogram_Xic.SetLineColor(45)
  myhistogram_Xic.SetLineWidth(4)
  myhistogram_Xic.SetStats(0)
  myhistogram_Lc.DrawNormalized('E1')
  myhistogram_Xic.DrawNormalized('E1 same')
  X.DrawNormalized('E1 same')

  legend = ROOT.TLegend( 0.7, 0.67, 0.89, 0.86)
  legend.AddEntry(myhistogram_Lc, 'Lc MC data')
  legend.AddEntry(myhistogram_Xic, 'Xic MC data')
  legend.AddEntry( X, 'PID-unbiased data')
  legend.SetLineWidth(0)
  legend.Draw('same')
  print(f"Drawing {kinvar} of [{particle}")

  c1.SaveAs(f'{kinvar}_{particle}_Lc_Xic_PIDcalib_{year}.pdf')

for year in years:
  for magnitude in magnitudes:
    for particle in particles:
      for kinvar in kinvars:
        make_comparison_graph_plot(year=year, magnitude=magnitude, particle=particle, kinvar=kinvar, PID_cut=PID_cuts[particle])

