import ROOT
from ROOT import TChain
from ctypes import c_double
import os
from prettytable import PrettyTable
import numpy as np

years = ["2017"]
yeardict = { 
  "2015" : "Turbo15",
  "2016" : "Turbo16",
  "2017" : "Turbo17",
  }
magnitudes = ["MagDown"]
binnings = ["non-BHH", "new-binning"]
binning_schemes = {
  "non-BHH" : "",
  "new-binning" : "Xic_Binning_",
}
mother_particles = ["Lc", "Xic"]
particles = ["pplus","kminus", "piplus"]
particles_short ={
  "pplus" : "P",
  "kminus" : "K",
  "piplus" : "Pi",
}
PID_cuts = {
  "pplus" : "ProbNNp > 0.5 && DLLp > 0_",
  "kminus" : "ProbNNK > 0.4 && DLLK > 0_",
  "piplus" : "ProbNNpi > 0.5_",
}

def make_comparison_graph_plot(year, magnitude, binning, mother_particle, particle):
  print(f'running with({year}, {magnitude}, {binning}, {mother_particle}, {particle})')
  c1 = ROOT.TCanvas('c1', f'{mother_particle}_{particle}')
  
  if binning=="non-BHH":
    PIDfolder = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v10r1/"
    PIDfilename = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_P_ETA_nTracks_Brunel.root"
    PIDfile = ROOT.TFile.Open(PIDfolder + PIDfilename)
    PIDhistbeforecut_name = f"TotalHist_{particles_short[particle]}_MC15TuneV1_{PID_cuts[particle]}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
    PIDhistbeforecut = PIDfile.Get(PIDhistbeforecut_name)
    PIDhistaftercut_name = f"PassedHist_{particles_short[particle]}_MC15TuneV1_{PID_cuts[particle]}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
    PIDhistaftercut = PIDfile.Get(PIDhistaftercut_name)

  if binning=="new-binning":
    PIDfolder = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v10r1/"
    PIDfilename = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_Xic_Binning_P_ETA_nTracks_Brunel.root"
    PIDfile = ROOT.TFile.Open(PIDfolder + PIDfilename)
    PIDhistbeforecut_name = f"TotalHist_{particles_short[particle]}_MC15TuneV1_{PID_cuts[particle]}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
    PIDhistbeforecut = PIDfile.Get(PIDhistbeforecut_name)
    PIDhistaftercut_name = f"PassedHist_{particles_short[particle]}_MC15TuneV1_{PID_cuts[particle]}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
    PIDhistaftercut = PIDfile.Get(PIDhistaftercut_name)

  X = PIDhistbeforecut.ProjectionX('X')
  Y = PIDhistbeforecut.ProjectionY('Y')
  Z = PIDhistbeforecut.ProjectionZ('Z')

  if mother_particle == 'Lc':
    filedir = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/145"
    filename = "MC_Lc2pKpiTuple_25103064.root"
  if mother_particle == 'Xic':
    filedir = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/16"
    filename = "MC_Lc2pKpiTuple_26103092.root"

  subjobs = next(os.walk(filedir))[1]
  excludedjobs = []
  tree = TChain("tuple_Lc2pKpi/DecayTree")

  for job in subjobs:
    if not job in excludedjobs :
      tree.Add("{0}/{1}/{2}".format(filedir,job,filename))

  myhistogram_mother_particle = {
    "Lc" : "myhistogram_Lc",
    "Xic" : "myhistogram_Xic",
  }
  myhistogram = myhistogram_mother_particle[mother_particle]
  axesbinsX = X.GetXaxis().GetXbins()
  axesbinsY = Y.GetXaxis().GetXbins()
  axesbinsZ = Z.GetXaxis().GetXbins()

  myhistogram = ROOT.TH3F('myhistogram',f'Total efficiency {particle}_{mother_particle}', axesbinsX.GetSize()-1, axesbinsX.GetArray(), axesbinsY.GetSize()-1, axesbinsY.GetArray(), axesbinsZ.GetSize()-1, axesbinsZ.GetArray())
  cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000"
  tree.Draw(f"nTracks:{particle}_ETA:{particle}_P>>+myhistogram", cuts)
  
  ratio = PIDhistaftercut.Clone()
  ratio.Divide(PIDhistbeforecut)

  nbinranges = []
  nbinranges += [1]
  nbinranges += [ axesbinsX.GetSize() -1 ]
  nbinranges += [1]
  nbinranges += [ axesbinsY.GetSize() -1 ]
  nbinranges += [1]
  nbinranges += [ axesbinsZ.GetSize() -1 ]

  efftotal_error = c_double(0.0)
  myhistogram.Sumw2()
  ntotal = myhistogram.Integral(*nbinranges)
  myhistogram.Multiply(ratio)
  print(ntotal)
  efftotal = myhistogram.IntegralAndError(*(nbinranges + [efftotal_error]))
  print(efftotal)
  ntotal = c_double(ntotal)
  efftotal = c_double(efftotal)

  efftotal = efftotal.value / ntotal.value
  efftotal_error = efftotal_error.value / ntotal.value
  print (f'("PID efficiency and an error of {mother_particle}_{particle} is {efftotal:.4f} +- {efftotal_error:.4f}")')
  return [year, magnitude, mother_particle, particle, f'{efftotal:.4f}', f'{efftotal_error:.4f}'], efftotal, efftotal_error

table_1 = PrettyTable(['Year', 'Magnitude', 'Mother_particle', 'Daughter_particle', 'Efficiency', 'Statistical error', 'Systematic_error'])
table_2 = PrettyTable(['Mother_particle', 'Efficiency', 'Statistical error', 'Systematic_error'])


for mother_particle in mother_particles:
  totaleff = 1
  totaleff_new_binning = 1
  totaleff_error = 0
  for year in years:
    for magnitude in magnitudes:
      for particle in particles:
        table_entry, efftotal, efftotal_error = make_comparison_graph_plot(year=year, magnitude=magnitude, binning='non-BHH', mother_particle=mother_particle, particle=particle)
        _, efftotal_new_binning,_ = make_comparison_graph_plot(year=year, magnitude=magnitude, binning='new-binning', mother_particle=mother_particle, particle=particle)
        table_entry.append(f'{abs(efftotal-efftotal_new_binning):.4f}')
        table_1.add_row(table_entry)
        totaleff = totaleff*efftotal
        totaleff_new_binning = totaleff_new_binning*efftotal_new_binning
        totaleff_error = efftotal_error/efftotal + totaleff_error
  totaleff_error = totaleff_error * totaleff
  table_2.add_row([mother_particle, f'{totaleff:.4f}', f'{totaleff_error:.4f}', f'{abs(totaleff-totaleff_new_binning):.4f}'])
print(table_1)
print(table_2)


  

  

