import ROOT, os, Imports, sys
from ROOT import TChain, TFile

def main():
	#a dictionary containing the details of the all the years' data according to joblog.txt
	folders_dict = {
		"115":["2016_MagDown", 186,"Xic"],
		"119":["2016_MagDown",527,"Lc"],
	} 
	
	# folders_dict = {
		# "43":["2011_MagDown", 907],
		# "45":["2011_MagUp", 817],
		# "46":["2012_MagUp",1342],
		# "42":["2012_MagDown",1155],
		# "119":["2016_MagDown",527,"Lc"],
		# "115":["2016_MagDown",186,"Xic"],
		# "91":["2017_MagDown",529,"Lc"],
		# "116":["2017_MagDown",257,"Xic"],
		# "117":["2018_MagDown",471,"Xic"],
		# "92":["2018_MagDown",656,"Lc"],
		# } 

	cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && piplus_ProbNNpi > 0.5 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000 && pplus_PIDp > 0 && kminus_PIDK > 0"
	PATH = "/dcache/bfys/jtjepkem/binned_files/"
	run = ""
	
	for element in folders_dict:
		if int(element) > 41 and int(element) < 47:
		   extra_variables = ["nTracks"]
		   run = 1
		else:
		   extra_variables = ["nSPDHits", "nTracks"]
		   particle = folders_dict[element][2]
		   
		name = folders_dict[element][0]
		subjobs = folders_dict[element][1]
		saving_directory = PATH + name + "_clusters/"
		if not os.path.exists(saving_directory):
		   os.makedirs(saving_directory)
		file_directory = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/" + element
			
		step = subjobs//20 #carry out the process in 20 clusters of datafiles to avoid memory overflow
		Max = step
		Min = 0

	# Loop used to apply global cuts on the data
		while (Max <= subjobs):
			if Max == Min:
				break
			strip_n_save(Min, Max, cuts, file_directory, saving_directory, extra_variables, particle)
			temp = Max
			if (Max+step > subjobs):
				Max = subjobs
			else:
				Max += step
			Min = temp

		clusters = os.listdir(saving_directory)

		final_chain = TChain("DecayTree")
		for element in clusters:
			final_chain.Add(saving_directory + element)

		
		if not os.path.exists(PATH + name + "/bins"):
		   os.makedirs(PATH + name + "/bins")
		saving_dir = PATH + name + "/bins/"
		split_in_bins_n_save(final_chain, saving_dir, run, particle) # split the datafile into mass-y-pt bins

		print ("process completed for " + name)



#### This function takes a ROOT file as an input, keeps the variables in useful_vars in the tree and throws the other ones away. The pruned tree is then returned. ###
def setBranch_funct (root_file, extra_variables):

	useful_vars = ["lcplus_MM", "lcplus_P", "lcplus_PT", "lcplus_ETA", "lcplus_RAPIDITY", "lcplus_TIP", "lcplus_IPCHI2_OWNPV", "lcplus_OWNPV_CHI2", "lcplus_TAU", "lcplus_L0HadronDecision_TOS", "pplus_M", "pplus_P", "pplus_PT", "pplus_RAPIDITY", "pplus_ETA", "pplus_ProbNNp", "piplus_M", "piplus_P", "piplus_PT", "piplus_RAPIDITY", "piplus_ETA", "piplus_ProbNNpi", "pplus_PIDp", "kminus_M", "kminus_P", "kminus_PT", "kminus_RAPIDITY", "kminus_ETA", "kminus_ProbNNk", "kminus_PIDK", "PVNTRACKS", ] # list of variables kept in the tree

	for extra_variable in extra_variables:
		if not (extra_variable == ""): #if extra_variable is something needed, then it will be added to the array
			useful_vars.append(extra_variable)

	tfile = root_file  #These 2 lines depend on the type of file fed into the function
	tfile.SetBranchStatus("*", False) #first deactivate all branches
	
	for element in useful_vars: # then reactivate the ones present in useful_vars
		tfile.SetBranchStatus(element, True)

	return tfile # return the pruned TTree


#### This function requires a .root file as an input that in its structure has DecayTree immediately there without any intermediate structure. The TTree is divided into bins and these are saved in the saving_dir (which is a string of the saving directory) ####
def split_in_bins_n_save (root_file, saving_dir, run, mother_particle = "Lc"):

	ybins = Imports.getYbins() #Rapidity bins
    
	ptbins = Imports.getPTbins()

	if run == 1:
		particles = ["Lc", "Xic"]
	else:
		particles = []
		particles.append(mother_particle)
    
	if not os.path.exists(saving_dir + "ybins/"):
		os.mkdir(saving_dir + "ybins/")
	if not os.path.exists(saving_dir + "ptbins/"):
		os.mkdir(saving_dir + "ptbins/")
	if not os.path.exists(saving_dir + "y_ptbins/"):
		os.mkdir(saving_dir + "y_ptbins/")

	extra_variables = [""]
	tree = root_file
	for particle in particles:
		if particle == "Lc":
			mass_cuts = "lcplus_MM < 2375"
		if particle == "Xic":
			mass_cuts = "lcplus_MM > 2375"
		for ybin in ybins:
			ycuts = "lcplus_RAPIDITY >= {0} && lcplus_RAPIDITY < {1}".format(ybin[0], ybin[1])
			allcuts = " {0} && {1}".format(ycuts, mass_cuts)
			strip_n_save(0,0, allcuts, "", saving_dir + "ybins/" + particle + "_ybin_{0}-{1}.root".format(ybin[0], ybin[1]), extra_variables,particle, bins = True, tree = tree)
			for ptbin in ptbins:
				ptcuts = "lcplus_PT >= {0} && lcplus_PT < {1}".format(ptbin[0], ptbin[1])
				if (ybin[0] == 2.0):
					allcuts = " {0} && {1}".format(ptcuts, mass_cuts)
					strip_n_save(0,0, allcuts, "", saving_dir + "ptbins/" + particle + "_ptbin_{0}-{1}.root".format(ptbin[0], ptbin[1]), extra_variables, particle, bins = True,tree = tree)
				yptcut = ycuts + " && " + ptcuts
				allcuts = " {0} && {1}".format(yptcut, mass_cuts)
				strip_n_save(0,0, allcuts, "", saving_dir + "y_ptbins/" + particle + "_ybin_{0}-{1}_ptbin_{2}-{3}.root".format(ybin[0],ybin[1],ptbin[0],ptbin[1]), extra_variables, particle, bins = True, tree = tree)

#### Function that takes as inputs: min and max which are 2 integers that indicates from which subjob to which subjob the TChain ranges; cuts are the cuts applied to the TTrees; directory is the directory in which the subjobs are to be found and saving_directory is the directory in which the stripped files are then saved. ####
def strip_n_save (Min, Max, cuts, directory, saving_directory, extra_variables, particle, bins = False, tree = None):
    
	if not (bins):
		filename = "{0}2pKpiTuple.root".format(particle)
		alldata = TChain("tuple_{0}2pKpi/DecayTree".format(particle))
		extra_dir = ""
		for job in range(Min, Max) :
			if not os.path.exists("{0}/{1}{2}/{3}".format(directory,job,extra_dir,filename)):
				alldata.Add("{0}/{1}{2}/{3}".format(directory,job,extra_dir,filename))
    
    #Check if there are any issues with the data
		if (alldata.GetEntries() == 0):
			print("Error: entries = 0 for range " + str(Min) + "-" + str(Max))
			return
		if (alldata.GetEntries() == -1):
			print("Error: entries = -1 for range " + str(Min) + "-" + str(Max))
			return

		alldata = setBranch_funct(alldata, extra_variables)
		extra_string = particle + "_cluster_{0}-{1}.root".format(Min, Max)
	else:
		if not (tree == None):
			alldata = tree
		extra_string = ""

	wfile = TFile.Open(saving_directory + extra_string, "RECREATE")
	subtree = alldata.CopyTree( cuts )
	wfile.cd()
	subtree.Write()
	wfile.Close()
    
if __name__ == '__main__':
	main()

