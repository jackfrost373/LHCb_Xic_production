from ROOT import TChain, TCanvas, TH1, TFile
import sys

sys.path.append('../')

import ROOT, os, Imports, getopt
from Imports import TUPLE_PATH, RAW_TUPLE_PATH, TABLE_PATH, OUTPUT_DICT_PATH, MC_jobs_Dict
import pprint

dict_path = OUTPUT_DICT_PATH + "Efficiencies/"
table_path = TABLE_PATH + "Efficiencies/"

ybins = Imports.getYbins()
ptbins = Imports.getPTbins()

def latexTable(dict, years, type):
	csvF = open(table_path + type + "_Eff_Values.tex","w")
	csvF.write("\\begin{tabular}{ll|c|c|c|c|c|c|}\n")
	csvF.write("\\cline{3-6}\n")
	csvF.write("& & \\multicolumn{2}{c|}{$\Xi_c$} & \multicolumn{2}{c|}{$\\Lambda_c$} \\\\ \\cline{3-8}\n")
	csvF.write("& & Efficiency & Err. & Efficiency & Err. & Ratio & Ratio Err. \\\\ \\cline{1-8}\n")

	for year in years:
		csvF.write("\multicolumn{{1}}{{|l|}}{{\multirow{{2}}{{*}}{}}} & \multicolumn{{1}}{{|l|}}{} & {:.3e} & {:.3e} & {:.3e} & {:.3e} & {:.3f} & {} \\\\\n".format("{" + str(year) + "}", "{MagDown}",dict["Lc_{}_MagDown".format(year)]["val"],dict["Lc_{}_MagDown".format(year)]["err"],dict["Xic_{}_MagDown".format(year)]["val"],dict["Xic_{}_MagDown".format(year)]["err"],dict["Xic_{}_MagDown".format(year)]["val"]/dict["Lc_{}_MagDown".format(year)]["val"],"Todo"))
		csvF.write("\multicolumn{{1}}{{|l|}}{{}} & \multicolumn{{1}}{{|l|}}{} & {:.3e} & {:.3e} & {:.3e} & {:.3e} & {:.3f} & {} \\\\ \\cline{{1-8}}\n".format("{MagUp}",dict["Lc_{}_MagUp".format(year)]["val"],dict["Lc_{}_MagUp".format(year)]["err"],dict["Xic_{}_MagUp".format(year)]["val"],dict["Xic_{}_MagUp".format(year)]["err"],dict["Xic_{}_MagUp".format(year)]["val"]/dict["Lc_{}_MagUp".format(year)]["val"],"Todo"))

	csvF.write("\end{tabular}")
	csvF.close()


def main(argv):

	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH FOR ROOT

	try:
		opts, args = getopt.getopt(argv,"hstp")
	except getopt.GetoptError:
		print("The arguments are wrong")
		sys.exit(2)

	options = []
	arguments = []

	for opt,arg in opts:
		options.append(opt)
		arguments.append(arg)

	if not options:
		options = ["-s","-t","-p"]

	if "-h" in options:
		print(textwrap.dedent("""\

			Welcome to the efficiencies.py script.

			The parameters are
				-h : help
				-s : Selection
				-t : Trigger
				-p : PID

			Running with no parameter will output all the data at once.
			"""))

		sys.exit()


	for opt in options:

		if opt == "-s":

			selecEffDict = {}
			years = []

			print("\nCreation of the selection efficiency files")

			n = len(MC_jobs_Dict)
			i = 0

			for job in MC_jobs_Dict:
				#FOR THE PROGRESSION BAR
				if i < n:
					j = (i + 1) / n
					sys.stdout.write('\r')
					sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
					sys.stdout.flush()
					i += 1
				if job == "NA":
					continue

				particle = MC_jobs_Dict[job][3]
				year = MC_jobs_Dict[job][0]
				pol = MC_jobs_Dict[job][1]
				subjobs = MC_jobs_Dict[job][2]
				identifier = MC_jobs_Dict[job][4]

				if year not in years:
					years.append(year)

				filename = "MC_Lc2pKpiTuple_" + identifier + ".root"

				if int(year) <= 2012:
					run = 1
					cuts = Imports.getDataCuts(run)
				else:
					run = 2
					cuts = Imports.getDataCuts(run)

				Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree") # !!! QUESTION : NOT BETTER ISTEAD OF CHAIN; JUST GETENTRIES FROM EACH ONE BY ONE, ONCE WITHOUT CUT AND ONCE WITH?

				for subjob in os.listdir(RAW_TUPLE_PATH + job):
					Lc_MC_tree.Add(RAW_TUPLE_PATH + job + "/" + subjob + "/" + filename)

				N= float(Lc_MC_tree.GetEntries()) #WHY DID SIMON USE A HARDCODED NUMBER OF ENTRIES??
				#k = float(Lc_MC_tree.GetEntries(cuts + " && " + turbo)) SIMON VERSION
				k = float(Lc_MC_tree.GetEntries(cuts))
				eff = float(k/N)
				binom_error = (1/N)*((k*(1-k/N))**(0.5))

				selecEffDict[particle + "_" + str(year) + "_" + pol] = {'val': eff, 'err': binom_error}


			print("\nSelection efficiency calculations are done!")

			latexTable(selecEffDict,years,"Selection")

			prettyEffDict = pprint.pformat(selecEffDict)
			dictF = open(dict_path + "Selection_Eff_Dict.py","w")
			dictF.write("selDict = " + str(prettyEffDict))
			dictF.close()

		elif opt == "-t":

			print("\nCreation of the trigger efficiency files")

			trigEffDict = {}
			years = []

			n = len(MC_jobs_Dict)
			i = 0

			for job in MC_jobs_Dict:
				#FOR THE PROGRESSION BAR
				if i < n:
					j = (i + 1) / n
					sys.stdout.write('\r')
					sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
					sys.stdout.flush()
					i += 1
				if job == "NA":
					continue

				particle = MC_jobs_Dict[job][3]
				year = MC_jobs_Dict[job][0]
				pol = MC_jobs_Dict[job][1]
				subjobs = MC_jobs_Dict[job][2]
				identifier = MC_jobs_Dict[job][4]

				if year not in years:
					years.append(year)

				filename = "MC_Lc2pKpiTuple_" + identifier + ".root"

				if int(year) <= 2012:
					run = 1
					cuts = "lcplus_L0HadronDecision_TOS == 1 && lcplus_Hlt1TrackAllL0Decision_TOS == 1"
					turbo = "lcplus_Hlt2CharmHadD2HHHDecision_TOS==1"
				else:
					run = 2
					cuts = Imports.getDataCuts(run)
					turbo = "lcplus_Hlt1TrackMVADecision_TOS==1"

				#WHAT DO I NEED FOR TRIGGER CUTS?!!

				Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree") # !!! QUESTION : NOT BETTER ISTEAD OF CHAIN; JUST GETENTRIES FROM EACH ONE BY ONE, ONCE WITHOUT CUT AND ONCE WITH?

				for subjob in os.listdir(RAW_TUPLE_PATH + job):
					Lc_MC_tree.Add(RAW_TUPLE_PATH + job + "/" + subjob + "/" + filename)

				N=float(Lc_MC_tree.GetEntries( turbo + " && lcplus_L0HadronDecision_TOS==1"))
				k = float(Lc_MC_tree.GetEntries(cuts + " && " + turbo ))
				eff = float(k/N)
				binom_error = (1/N)*((k*(1-k/N))**(0.5))

				trigEffDict[particle + "_" + str(year) + "_" + pol] = {'val': eff, 'err': binom_error}

			print("\nTrigger efficiency calculations are done!")

			latexTable(trigEffDict,years,"Trigger")

			prettyEffDict = pprint.pformat(trigEffDict)
			dictF = open(dict_path + "Trigger_Eff_Dict.py","w")
			dictF.write("trigDict = " + str(prettyEffDict))
			dictF.close()


		elif opt == "-p":
			pass

		else:
			sys.exit()



if __name__ == "__main__":
   main(sys.argv[1:])
