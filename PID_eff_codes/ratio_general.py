import ROOT


years = ["2017"]
yeardict = { 
  "2015" : "Turbo15",
  "2016" : "Turbo16",
  "2017" : "Turbo17",
  }
magnitudes = ["MagDown"]

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
nonBHH_PID_cuts= {
  "pplus" : "ProbNNp > 0.5_",
  "kminus" : "ProbNNK > 0.4_",
  "piplus" : "ProbNNpi > 0.5_",
}
kinvars = ["P", "ETA", "nTracks"]

def make_comparison_graph_plot(year, magnitude, particle, PID_cut, kinvar, nonBHH_PID_cut):

  c1 = ROOT.TCanvas('c1', f'{kinvar} of {particle}')

  PIDfolder = "/project/bfys/jdevries/cmtuser/LHCb_Xic_production/pidcalib/UraniaDev_v7r0/"
  PIDfilename = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_BHH_Binning_P_ETA_nTracks_Brunel.root"
  PIDfilename2 = f"PerfHists_{particles_short[particle]}_{yeardict[year]}_{magnitude}_P_ETA_nTracks_Brunel.root"
  PIDfile = ROOT.TFile.Open(PIDfolder + PIDfilename)
  PIDfile2 = ROOT.TFile.Open(PIDfolder + PIDfilename2)
  PIDhistbeforecut_name = f"TotalHist_{particles_short[particle]}_MC15TuneV1_{PID_cut}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
  PIDhistbeforecut = PIDfile.Get(PIDhistbeforecut_name)
  PIDhistbeforecut_name2 = f"TotalHist_{particles_short[particle]}_MC15TuneV1_{nonBHH_PID_cut}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
  PIDhistbeforecut2 = PIDfile2.Get(PIDhistbeforecut_name2)
  PIDhistaftercut_name = f"PassedHist_{particles_short[particle]}_MC15TuneV1_{PID_cut}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
  PIDhistaftercut = PIDfile.Get(PIDhistaftercut_name)
  PIDhistaftercut_name2 = f"PassedHist_{particles_short[particle]}_MC15TuneV1_{nonBHH_PID_cut}All__{particles_short[particle]}_P_{particles_short[particle]}_Eta_nTracks_Brunel"
  PIDhistaftercut2 = PIDfile2.Get(PIDhistaftercut_name2)

  if kinvar=='P':
    X = PIDhistbeforecut.ProjectionX('X')
    XA = PIDhistaftercut.ProjectionX('XA')
    X2 = PIDhistbeforecut2.ProjectionX('X2')
    XA2 = PIDhistaftercut2.ProjectionX('XA2')
  if kinvar=='ETA':
    X = PIDhistbeforecut.ProjectionY('X')
    XA = PIDhistaftercut.ProjectionY('XA')
    X2 = PIDhistbeforecut2.ProjectionY('X2')
    XA2 = PIDhistaftercut2.ProjectionY('XA2')  
  if kinvar=='nTracks':
    X = PIDhistbeforecut.ProjectionZ('X')
    XA = PIDhistaftercut.ProjectionZ('XA')
    X2 = PIDhistbeforecut2.ProjectionZ('X2')
    XA2 = PIDhistaftercut2.ProjectionZ('XA2')

  ratio = XA.Clone()
  ratio.Divide(X) 
  ratio2 = XA2.Clone()
  ratio2.Divide(X2)
  ratio.GetXaxis().SetTitle(f'{kinvar}_{particle}')
  ratio.GetYaxis().SetTitle('Efficiency')
  ratio.SetLineColor(46)
  ratio.SetLineWidth(3)
  ratio2.SetLineColor(30)
  ratio2.SetLineWidth(3)
  ratio.SetTitle(f'Efficiency vs. {kinvar} histogram of {particle} particle')
  ratio.SetStats(0)
  ratio.GetYaxis().SetRangeUser( 0.0, 1 )
  ratio.Draw('E1')
  ratio2.Draw('E1 same')

  legend = ROOT.TLegend( 0.7, 0.67, 0.89, 0.86)
  legend.AddEntry(ratio, 'BHH_Binning')
  legend.AddEntry(ratio2, 'NON-BHH_Binning')
  legend.SetLineWidth(0)
  legend.Draw('same')
 
  c1.SaveAs(f'Efficiency_vs_{kinvar}_histogram_of_{particle}_comparison_{year}.pdf')
  
for year in years:
	for magnitude in magnitudes:
		for particle in particles:
			for kinvar in kinvars:
				make_comparison_graph_plot(year=year, magnitude=magnitude, particle=particle, kinvar=kinvar, PID_cut=PID_cuts[particle], nonBHH_PID_cut=nonBHH_PID_cuts[particle])