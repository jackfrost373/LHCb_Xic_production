import ROOT, os
from ROOT import TChain, TCanvas, TH1

directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/"
#directory = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/"
#/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/64/25/output
job = "88"
ID = "25103006" #Lc: 25203000 Xic: 26103090
n_subjobs = 25
excludedjobs = []

Lc_MC_filedir = directory + job
Lc_MC_filename = "MC_Lc2pKpiTuple_" + ID + ".root"

Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree")

for job in range(n_subjobs) :
    if not job in excludedjobs :
        Lc_MC_tree.Add("{0}/{1}/{2}".format(Lc_MC_filedir,job,Lc_MC_filename))

N = float(Lc_MC_tree.GetEntries("lcplus_L0HadronDecision_TOS==1 && lcplus_Hlt1TrackAllL0Decision_TOS==1"))
#N = 2005446.0

        
print("The number of events in the uncut TChain is: " + str(N))

#cuts = "lcplus_L0HadronDecision_TOS==1 && lcplus_Hlt2CharmHadD2HHHDecision_TOS == 1 && lcplus_Hlt1TrackAllL0Decision_TOS==1"
#cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000"
cuts = "lcplus_L0HadronDecision_TOS==1 && lcplus_Hlt1TrackAllL0Decision_TOS==1 && lcplus_Hlt2CharmHadD2HHHDecision_TOS==1"

print("The number of events in the cut TChain are: " + str(Lc_MC_tree.GetEntries(cuts)))

k = float(Lc_MC_tree.GetEntries(cuts))

eff = float(k/N)

print("The efficiency is: " + str(eff))

binom_error =float( (1/N)*((k*(1-(k/N)))**(0.5))) #formula to calculate the binomial error given a total number of events N and a number k of events passing the selection

#print (str(binom_error))

print("Efficiency for the selection " + cuts + " is: " + str(eff) + " +/-" + str(binom_error))


