from ROOT import TChain, TCanvas, TH1, TFile
import ROOT, os, Imports, sys, getopt
from Imports import TUPLE_PATH, RAW_TUPLE_PATH, MC_jobs_Dict

ybins = Imports.getYbins()
ptbins = Imports.getPTbins()

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
			
			f_text = open("Selection_Eff_output.txt", "w+")
			
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
				
				filename = "MC_Lc2pKpiTuple_" + identifier + ".root"
				
				if int(year) <= 2012:
					run = 1
					cuts = Imports.getDataCuts(run)
				else:
					run = 2
					cuts = Imports.getDataCuts(run)
				
				# # APPARENTLY THAT THE ONLY CUTS THAT SIMON WAS LOOKING AT ---- !!!QUESTION!!!
				# cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 &&  pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000"
				
				# #turbo = "lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS==1"
				# turbo = "lcplus_Hlt2CharmHadD2HHHDecision_TOS == 1"
 
				Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree") # !!! QUESTION : NOT BETTER ISTEAD OF CHAIN; JUST GETENTRIES FROM EACH ONE BY ONE, ONCE WITHOUT CUT AND ONCE WITH?
						
				for subjob in os.listdir(RAW_TUPLE_PATH + job):
					Lc_MC_tree.Add(RAW_TUPLE_PATH + job + "/" + subjob + "/" + filename)
					
				N= float(Lc_MC_tree.GetEntries()) #WHY DID SIMON USE A HARDCODED NUMBER OF ENTRIES??
				#k = float(Lc_MC_tree.GetEntries(cuts + " && " + turbo)) SIMON VERSION
				k = float(Lc_MC_tree.GetEntries(cuts))
				eff = float(k/N)
				binom_error = (1/N)*((k*(1-k/N))**(0.5))
				string = "Particle: " + particle + " year: " + str(year) + pol + " efficiency for the selection: " + cuts + " is: " + str(eff) + " +/- " + str(binom_error) + "\n"
				f_text.write(string)
			
			print("\nSelection efficiency calculations are done!")
			f_text.close()
			
		elif opt == "-t":
			
			f_text = open("Trigger_Eff_output.txt", "w+")
			
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
				string = "Particle: " + particle + " year: " +str(year) + MagPol +" efficiency for the selection " + cuts + " is: " + str(eff) + " +/- " + str(binom_error) + "\n"
				f_text.write(string)
			
			print("\nTrigger efficiency calculations are done!")
			f_text.close()
			
			


			
		elif opt == "-p":
			pass
			
		else:
			sys.exit()
	
	

if __name__ == "__main__":
   main(sys.argv[1:])
