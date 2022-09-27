TUPLE_PATH = "/dcache/bfys/jtjepkem/binned_files/"
TUPLE_PATH_NOTRIG = "/dcache/bfys/jtjepkem/binned_files_noTrig/"
RAW_TUPLE_PATH = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/"

PLOT_PATH = "/data/bfys/cpawley/LcAnalysis_plots/"
TABLE_PATH = PLOT_PATH + "Tables/"
OUTPUT_DICT_PATH = PLOT_PATH + "Dict_output/"

#Important! When we decide the fate of Turbo/Stripping/ etc. These HLT2 checks must be tidied up

def getMCCuts(particle, run):
	IDcuts = "abs(piplus_TRUEID)==211 && abs(kminus_TRUEID)==321 && abs(pplus_TRUEID)==2212"# && abs(lcplus_TRUEID)==4122" 
	if run == 2:
		IDcuts += " && lcplus_Hlt2CharmHad{0}pToPpKmPipTurboDecision_TOS == 1 ".format(particle)
		#IDcuts += " && lcplus_Hlt2CharmHadD2HHHDecision_TOS == 1"
	if particle == "Lc":
		#BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 50)"
		return IDcuts #+ "&&" + BKGCAT
	elif particle == "Xic":
		#BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 10 || lcplus_BKGCAT == 50)"
		return IDcuts #+ "&&" + BKGCAT

def getDataCuts(run, trig = True):
	cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && piplus_ProbNNpi > 0.5 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000 && pplus_PIDp > 0 && kminus_PIDK > 0"
	
	if run == 1:
		if trig:
			trigger_cuts = "lcplus_L0HadronDecision_TOS == 1 && lcplus_Hlt1TrackAllL0Decision_TOS == 1 && lcplus_Hlt2CharmHadD2HHHDecision_TOS == 1"
		else:
			trigger_cuts = ""
	elif run == 2:
		if trig:
			trigger_cuts = "lcplus_L0HadronDecision_TOS == 1 && lcplus_Hlt1TrackMVADecision_TOS == 1 && (lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS == 1 || lcplus_Hlt2CharmHadLcpToPpKmPipTurboDecision_TOS == 1) "
			#trigger_cuts = "lcplus_L0HadronDecision_TOS == 1 && lcplus_Hlt1TrackAllL0Decision_TOS == 1 && lcplus_Hlt2CharmHadD2HHHDecision_TOS == 1"
		else:
			trigger_cuts = ""
	
	if trigger_cuts == "":	
		return cuts
	else:
		return cuts + " && " + trigger_cuts

def getBackgroundCuts(particle):
	if particle == "Lc":
		cuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)"
	elif particle == "Xic":
		cuts = "lcplus_MM > 2400 && lcplus_MM < 2450 || lcplus_MM > 2490"
	return cuts

def getSWeightsCuts(particle):
	if particle == "Lc":
		cuts = "lcplus_MM>=2240 && lcplus_MM<=2340"
	elif particle == "Xic":
		cuts = "lcplus_MM>=2420 && lcplus_MM<=2520"
	return cuts

def getPTbins():
	return [[3200,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,20000]]

def getYbins():
	return  [[2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]]

#the dictionnary values are to be uncommented once the jobs are gotten off the grid
DATA_jobs_Dict = {
	"43":["2011_MagDown", 907],
	"45":["2011_MagUp", 817],
	"46":["2012_MagUp",1342],
	"42":["2012_MagDown",1155],
	#"NA":["2016_MagDown",],
	"163":["2017_MagDown",1875],
	#"NA":["2018_MagDown",],
	}

MC_jobs_Dict = {
	"NA":["2011","MagDown", 907,"Lc",""],
	"NA":["2011","MagDown", 907,"Xic",""],
	"NA":["2011","MagUp", 817,"Lc",""],
	"NA":["2011","MagUp", 817,"Xic",""],

	"88":["2012","MagDown", 25,"Lc","25103006"],
	"123":["2012","MagDown", 15,"Xic","25103029"],
	"87":["2012","MagUp", 25,"Lc","25103006"],
	"122":["2012","MagUp", 17,"Xic","25103029"],

	"107":["2016","MagDown", 290,"Lc","25203000"],
	"108":["2016","MagDown", 282,"Xic","26103090"],
	"105":["2016","MagUp", 281,"Lc","25203000"],
	"106":["2016","MagUp", 286,"Xic","26103090"],

	"145":["2017","MagDown", 285,"Lc","25103064"],
	"150":["2017","MagDown", 181,"Xic","26103091"], #data apears to be missing
	"144":["2017","MagUp", 284,"Lc","25103064"],
	"NA":["2017","MagUp", 181,"Xic","26103091"],

	"103":["2018","MagDown", 279,"Lc","25203000"],
	"16":["2018","MagDown", 357,"Xic","26103092"],
	"97":["2018","MagUp", 283,"Lc","25203000"],
	"98":["2018","MagUp", 278,"Xic","26103090"],
}

#this needs changing - job 150 is MagDown only (used as a proxy for MagUp)

def getMC(year,polarity, particle,cuts=True):
	from ROOT import TChain
	import os
	excludedJobs = [
		"NA",
		# "150",
		# "103",
		# "16",
		# "97",
		# "98"
	]
	if year > 2012:
		run =2
	else: 
		run =1
	year = str(year)
	MC_tree = TChain("tuple_Lc2pKpi/DecayTree")

	for job in MC_jobs_Dict:
		if job in excludedJobs:
			continue

		par = MC_jobs_Dict[job][3]
		y = MC_jobs_Dict[job][0]
		pol = MC_jobs_Dict[job][1]
		subjobs = MC_jobs_Dict[job][2]	
		identifier = MC_jobs_Dict[job][4]
		filename = "MC_Lc2pKpiTuple_" + identifier + ".root"

		if not y == year:
			continue
		if not pol == polarity:
			continue
		if not particle == par:
			continue
		
		print(f"adding job {job}")
		for subjob in os.listdir(RAW_TUPLE_PATH + job):
			if job == "150":
				if not os.path.exists(RAW_TUPLE_PATH + job + "/" + subjob + "/" + filename): #temp fix
					continue
			MC_tree.Add(RAW_TUPLE_PATH + job + "/" + subjob + "/" + filename)
	if MC_tree.GetEntries() == 0:
		return MC_tree
	
	if cuts:	
		MC_tree = MC_tree.CopyTree(getMCCuts(particle,run))

	return MC_tree
		


