import ROOT, os
from ROOT import TChain, TCanvas, TH1
import Imports

#directory = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/"
#directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/"
#job = "78"
ID = ""

ybins = Imports.getYbins()
ptbins = Imports.getPTbins()

#cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && piplus_ProbNNpi > 0.5 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000 && pplus_PIDp > 0 && kminus_PIDK > 0"
cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 &&  pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000"
#101:[285, 2017, "MagDown"]
#dictionary = {95:[284, 2017, "MagUp", 2003842], 96:[284, 2017, "MagUp", 2006193], 97:[283, 2018, "MagUp", 2004731], 98:[278, 2018, "MagUp", 2007066], 102:[281, 2017, "MagDown", 2002494], 103:[279, 2018, "MagDown", 2000268], 104:[277, 2018, "MagDown", 2005446], 105:[281, 2016, "MagUp", 2007242], 106:[286, 2016, "MagUp", 2006283], 107:[290, 2016, "MagDown", 2009238], 108:[282, 2016, "MagDown", 2052337]}
dictionary = {30:[27, 2012, "MagDown", 551509], 88:[25, 2012, "MagDown", 519998]}

f_text = open("/dcache/bfys/scalo/run1_Selection_Eff_output_v2.txt", "w+")

for job in dictionary:
    particle = ""
    #cuts = "lcplus_L0HadronDecision_TOS==1 && lcplus_Hlt1TrackAllL0Decision_TOS==1"
    n_subjobs = dictionary[job][0]
    year = dictionary[job][1]
    MagPol = dictionary[job][2]
    tot_entries = dictionary[job][3]
    if (job == 30):
        particle = "Xic"
        #ID = "26103090"
        ID = "25103029"
		#turbo = "lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS==1"
        turbo = "lcplus_Hlt2CharmHadD2HHHDecision_TOS == 1"
        directory = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/"
        Lc_MC_filename = "output/MC_Lc2pKpiTuple_" + ID + ".root"
	
    else:
        particle = "Lc"
        #ID = "25203000"
        ID = "25103006"
		#turbo = "lcplus_Hlt2CharmHadLcpToPpKmPipTurboDecision_TOS==1"
        turbo = "lcplus_Hlt2CharmHadD2HHHDecision_TOS==1"
        directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/"
        Lc_MC_filename = "MC_Lc2pKpiTuple_" + ID + ".root"
	
    #cuts+= " && " + turbo    
    Lc_MC_filedir = directory + str(job)
    #Lc_MC_filename = "MC_Lc2pKpiTuple_" + ID + ".root"

    Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree")
    
    for subjob in range(n_subjobs) :
        Lc_MC_tree.Add("{0}/{1}/{2}".format(Lc_MC_filedir,subjob,Lc_MC_filename))

#Binomial error calculation
    N= float(tot_entries)
    k = float(Lc_MC_tree.GetEntries(cuts + " && " + turbo))
    eff = float(k/N)
    binom_error = (1/N)*((k*(1-k/N))**(0.5))
    string = "Particle: " + particle + " year: " + str(year) + MagPol + " efficiency for the selection: " + cuts + " is: " + str(eff) + " +/- " + str(binom_error) + "\n"
    f_text.write(string)

	# for ybin in ybins:
		# for ptbin in ptbins:
			# yptcut = "lcplus_PT >= {0} && lcplus_PT < {1} && lcplus_RAPIDITY >= {2} && lcplus_RAPIDITY < {3}".format(ptbin[0], ptbin[1], ybin[0], ybin[1])
			# N = float(Lc_MC_tree.GetEntries(yptcut + " && " + turbo + " && lcplus_L0HadronDecision_TOS==1"))
			# N = tot_entries
			# if N==0.0:
				# continue
			# k = float(Lc_MC_tree.GetEntries(cuts + " && " + yptcut + " && " + turbo))
			# eff = float(k/N)
			# binom_error = (1/N)*((k*(1-k/N))**(0.5))
			# string = "Particle: " + particle + "year: " +str(year) + MagPol + " Bin " + str(ybin[0]) + "-" + str(ybin[1]) + " pt: " + str(ptbin[0]) + "-" + str(ptbin[1]) +" efficiency for the selection " + cuts + " is: " + str(eff) + " +/- " + str(binom_error) + "\n"
			# f_text.write(string)

f_text.close()





