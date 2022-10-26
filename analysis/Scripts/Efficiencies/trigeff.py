import sys
import ROOT, os,  Imports
from ROOT import TChain, TH1
from Imports import RAW_TUPLE_PATH

directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/"

cuts_L0 = "lcplus_L0HadronDecision_TOS==1"
cuts_Hlt1 = " && lcplus_Hlt1TrackAllL0Decision_TOS==1"
cuts_Hlt2 = " && lcplus_Hlt2CharmHadD2HHHDecision_TOS==1"

years = ["2012","2016","2017","2018"]
turboyears = ["2016","2017","2018"]
MagPol = ["MagDown", "MagUp"]
particles = ["Lc", "Xic"]

trigEffDict = {}
f = open("trigDict.txt","w")

tempfileDir = "/dcache/bfys/jhemink/test2.root"

for year in years:

    if not year in trigEffDict:
        trigEffDict[year] = {}

    for polarity in MagPol:

        if not polarity in trigEffDict[year]:
            trigEffDict[year][polarity] = {}
        
        for particle in particles:

            if not particle in trigEffDict[year][polarity]:
                trigEffDict[year][polarity][particle] = {}
            
            for entry in Imports.MC_jobs_Dict:
                if Imports.MC_jobs_Dict[entry][0]==year:
                    if Imports.MC_jobs_Dict[entry][1]==polarity:
                        if Imports.MC_jobs_Dict[entry][3]==particle:

                            tempFile = ROOT.TFile.Open(tempfileDir,"RECREATE")

                            tree =  ROOT.TChain("tuple_Lc2pKpi/DecayTree")
                            filedir = Imports.RAW_TUPLE_PATH + entry
                            filename = "MC_Lc2pKpiTuple_{0}.root".format(Imports.MC_jobs_Dict[entry][4])
                            for job in range (Imports.MC_jobs_Dict[entry][2]):
                                tree.Add("{0}/{1}/{2}".format(filedir, job, filename))
                            if year in turboyears:
                                cuts_Hlt1 = " && lcplus_Hlt1TrackMVADecision_TOS == 1" #turbo cuts
                                cuts_Hlt2 = " && lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS == 1" #turbo cuts
                            else:
                                cuts_Hlt1 = " && lcplus_Hlt1TrackAllL0Decision_TOS==1"
                                cuts_Hlt2 = " && lcplus_Hlt2CharmHadD2HHHDecision_TOS==1"
                            
                            k = float(tree.GetEntries(cuts_L0))
                            N = float(tree.GetEntries(""))
                            if N ==0:
                                continue
                            eff = float(k/N)
                            #print("L0 efficiency for " + str(particle) + " is " + str(eff) + " +/- " + str(binom_error) + ", " + str(year)+ ", " + str(polarity))

                            N2 = float(tree.GetEntries(cuts_L0))
                            k2 = float(tree.GetEntries(cuts_L0 + cuts_Hlt1))
                            eff2 = float((k2/N2)) 
                            #print("Hlt1 efficiency given L0 for " + str(particle) + " is " + str(eff2) + " +/- " + str(binom_error))

                            N3 = float(tree.GetEntries(cuts_L0 + cuts_Hlt1)) 
                            k3 = float(tree.GetEntries(cuts_L0 + cuts_Hlt1 + cuts_Hlt2))
                            eff_final = float((k3)/N3)
                            #print("Hlt2 efficiency given Hlt1 and L0 for  " + str(particle) + " is " + str(eff_final) + " +/- " + str(binom_error))

                            total_efficiency = float(eff*eff2*eff_final)
                            binom_error = float(((1/N)*((k3*(1-(k3/N)))**(0.5))))
                            #binomial error= ((1/N)*((k*(1-(k/N)))**(0.5))), where k is the number of entries with applied cuts, and N is the number of entries without the cuts.
                            #print("Total efficiency for  " + str(particle) + " is "+ str(total_efficiency) + " +/- " + str(total_error))

                            trigEffDict[year][polarity][particle]["val"] = total_efficiency
                            trigEffDict[year][polarity][particle]["err"] = binom_error
                            
                            f.write( str(trigEffDict))
os.remove(tempfileDir)
f.close()