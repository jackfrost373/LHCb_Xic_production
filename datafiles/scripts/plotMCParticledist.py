
import ROOT
f = ROOT.TFile.Open("./output/MC_Lc2pKpiTuple_25103006.root")

trec = f.Get("tuple_Lc2pKpi/DecayTree")
tmc  = f.Get("mctuple_Lc2pKpi/MCDecayTree")

totcuts = "lcplus_TRUEPT > 3000 && lcplus_TRUETAU > 0.0003 && piplus_TRUEPT > 300 && pplus_TRUEPT > 300 && kminus_TRUEPT > 300"
varias = [ 
         #["Lc_truePT","lcplus_TRUEPT",20,8000, totcuts],
         #["Lc_trueP","sqrt(lcplus_TRUEP_X**2 + lcplus_TRUEP_Y**2 + lcplus_TRUEP_Z**2)", 20, 70000,totcuts],
         #["Lc_trueTAU","lcplus_TRUETAU",0.0001, 0.0010, totcuts],
         ["pi_truePT","piplus_TRUEPT",20,3000, totcuts],
         ["p_truePT","pplus_TRUEPT",20,3000, totcuts],
         ["K_truePT","kminus_TRUEPT",20,3000,totcuts],
         #["pi_trueP","sqrt(piplus_TRUEP_X**2 + piplus_TRUEP_Y**2 + piplus_TRUEP_Z**2)", 20, 30000,totcuts],
         #["p_trueP","sqrt(pplus_TRUEP_X**2 + pplus_TRUEP_Y**2 + pplus_TRUEP_Z**2)", 20, 30000,totcuts],
         #["K_trueP","sqrt(kminus_TRUEP_X**2 + kminus_TRUEP_Y**2 + kminus_TRUEP_Z**2)", 20, 30000,totcuts],
         ]

c1 = ROOT.TCanvas("c1")

for var in varias :
  trec.Draw("{0} >> hrec(50,{1},{2})".format(var[1],var[2],var[3]), var[4])
  tmc.Draw( "{0} >> hmc(50,{1},{2})".format(var[1],var[2],var[3]), var[4])
  hmc  = ROOT.gDirectory.Get("hmc")
  hrec = ROOT.gDirectory.Get("hrec")

  hmc.SetLineColor(2)
  hmc.GetXaxis().SetTitle(var[0])
  hmc.DrawNormalized()
  hrec.DrawNormalized("same")
  print("MC  entries: {0} / {1}".format(hmc.GetEntries(), tmc.GetEntries()))
  print("rec entries: {0} / {1}".format(hrec.GetEntries(), trec.GetEntries()))
  c1.Update()

  c1.SaveAs("{0}.pdf".format(var[0]))

  raw_input("press enter to continue")
