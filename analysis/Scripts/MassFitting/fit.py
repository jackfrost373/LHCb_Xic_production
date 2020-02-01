import sys, getopt
import ROOT, os, MassfitLib as mf 
from fittingDict import fittingDict as singleFitDict
from CombinedBinFit_Dict import fittingDict as combinedFitDict
from yearTotalFit_Dict import fittingDict as yearFitDict
import os.path
import textwrap

#folder structure : 
#	/dcache/bfys/scalo/binned_files/2011_MagUp/bins/y_ptbins
#	/dcache/bfys/scalo/binned_files/2011_MagUp/bins/ybins
#	/dcache/bfys/scalo/binned_files/2011_MagUp/bins/ptbins
#	/dcache/bfys/scalo/binned_files/2011_MagUp/bins/LC_total.root

#filename structure : Lc_ybin_2.0-2.5_ptbin_3200-4000.root

#This is the base path without the particle location (until binned_files in our case)
BASE_PATH = "/home/exultimathule/Code/HonoursProgramme/MassFitScript/testDirectories/"
#BASE_PATH = "/dcache/bfys/scalo/binned_files/"

PDF_PATH_S = "PDF_output/Single/"
PDF_PATH_C = "PDF_output/Combined/"
PDF_PATH_Y = "PDF_output/Year/"

years = [2011,2012,2015,2016,2017,2018]
magPol = ["MagUp", "MagDown"]
pt_bin = ["3200-4000","4000-5000", "5000-6000", "6000-7000", "7000-8000", "8000-10000", "10000-20000"]
y_bin = ["2.0-2.5","2.5-3.0", "3.0-3.5", "3.5-4.0"]

def main(argv):
					
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH FOR ROOT
	
	try:
		opts, args = getopt.getopt(argv,"hm:y:o:p:r:t:")
	except getopt.GetoptError:
		print("The arguments are wrong")
		sys.exit(2)
	
	options = []
	arguments = []
	
	for opt,arg in opts:
		options.append(opt)
		arguments.append(arg)
	
	if "-h" in options:
		print(textwrap.dedent("""\
			
			Welcome to the fit.py script.
			Before running the script make sure you have two folders in the programme directory with the following structure:
				Dict_output/
				PDF_output/Single
				PDF_output/Combined
				PDF_output/Year
			These are for the output of the script and are necessary for a functionning run.

			The parameters are
				-m : mode (single, combined or year)
				-y : year (e.g. 2011) 
				-o : magnet polarity (up, down or both)
				-p : particle name (Xic, Lc or both)
				-r : rapidity (e.g. 2.5-3.0)
				-t : transverse momentum (e.g. 8000-10000)

			Important: the -o and -p are always used together, there is no option for using only one of the two (you can consider them as a single parameter...

			For modes -m:
				-"single" you can use any combination of -y -o -p -r -t 
				-"combined" you can use any combination of -y -o -p -r -t but you can never use both -r and -t together, which yould defeat the point of having combined bins
				-"year"you can use any combination of -y -o -p

			Running with no other parameter than -m makes the full fitting process. It also initializes the ditionnary file if you have not yet run the programme (important, the first time using this script requires initializing the dictionnaries by running with no parameter, e.g. "python fit.py -m single").
			"""))

		sys.exit()
		
	for m in range(len(options)):
		
		if options[m] == "-m":
			
			if arguments[m] == "single":
				
				if os.path.isfile("Dict_output/singleFit_DictFile.py"):
					from Dict_output.singleFit_DictFile import mainDict as singleDict
					
				
				del arguments[m]
				del options[m]
				
				# THE CODE THAT MAKES IT WORK FOR SINGLE BIN FILES

#####				
				if set(options) == set([]):
					# EVERYTHING HAS TO BE DONE
					mainDict = {}
	
					for i in years:
						mainDict[i] = {}
						for j in magPol:
							mainDict[i][j] = {}
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								mainDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
								
					
					# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(mainDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####					
				elif set(options) == set(["-y"]):
					# EVERYTHINg IN THAT YEAR
					year = int(arguments[0])#options.index("-y")]
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
						
					for i in magPol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + i + "/bins/y_ptbins/"):
							singleDict[year][i][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,i,filename,"single"),True,PDF_PATH_S)
							
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####
				elif set(options) == set(["-o","-p"]):
					# CHOOSE SPECIFIC MAGPOL AND PARTICLE AND DOES EVERYTHING
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					for i in years:
						for j in magpol:
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								parseName = filename.split('_')
								if particle == "both":
									singleDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
								elif parseName[0] == particle:
									singleDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
					
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####
				elif set(options) == set(["-y","-o","-p"]):
					
					# CHOOSE A YEAR, MAGPOL AND PARTICLE
					
					year = int(arguments[options.index("-y")])
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
						
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					for j in magpol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/y_ptbins/"):
							parseName = filename.split('_')
							if particle == "both":
								singleDict[year][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename),True,PDF_PATH_S)
							elif parseName[0] == particle:
								singleDict[year][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename),True,PDF_PATH_S)
				
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
				
				
#####
				elif set(options) == set(["-o","-p","-r"]):
					
					# CHOOSE A MAGPOL, PARTICLE AND RAPIDITY BIN
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					rapidity = arguments[options.index("-r")]
					if rapidity not in y_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for i in years:
						for j in magpol:
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								parseName = filename.split('_')
								if particle == "both" and parseName[2] == rapidity :
									singleDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
								elif parseName[0] == particle and parseName[2] == rapidity:
									singleDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
					
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
				
#####
				elif set(options) == set(["-o","-p","-t"]):
					
					# CHOOSE A MAGPOL, PARTICLE AND TRANS MOMENTUM BIN
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					pt = arguments[options.index("-t")]
					if pt not in pt_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for i in years:
						for j in magpol:
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								parseName = filename.split('_')
								if particle == "both" and parseName[-1][:-5] == pt :
									singleDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
								elif parseName[0] == particle and parseName[-1][:-5] == pt:
									singleDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
					
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
					
#####
				elif set(options) == set(["-o","-p","-r","-t"]):
					
					# CHOOSE A MAGPOL, PARTICLE AND RAPIDITY AND TRANS MOM. BIN
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					pt = arguments[options.index("-t")]
					if pt not in pt_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
						
					rapidity = arguments[options.index("-r")]
					if rapidity not in y_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for i in years:
						for j in magpol:
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								parseName = filename.split('_')
								if particle == "both" and parseName[-1][:-5] == pt and parseName[2] == rapidity:
									singleDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
								elif parseName[0] == particle and parseName[-1][:-5] == pt and parseName[2] == rapidity:
									singleDict[i][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S)
					
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
#####
				
				elif set(options) == set(["-y","-o","-p","-r"]):
					
					# CHOOSE A YEAR, MAGPOL, PARTICLE AND RAPIDITY BIN
					
					year = int(arguments[options.index("-y")])
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					rapidity = arguments[options.index("-r")]
					if rapidity not in y_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for j in magpol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/y_ptbins/"):
							parseName = filename.split('_')
							if particle == "both" and parseName[2] == rapidity :
								singleDict[year][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename),True,PDF_PATH_S)
							elif parseName[0] == particle and parseName[2] == rapidity:
								singleDict[year][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename),True,PDF_PATH_S)
				
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
				
				
#####
				elif set(options) == set(["-y","-o","-p","-t"]):
					
					# CHOOSE A YEAR, MAGPOL, PARTICLE AND TRANS MOMENTUM BIN
					
					year = int(arguments[options.index("-y")])
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					pt = arguments[options.index("-t")]
					if pt not in pt_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for j in magpol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/y_ptbins/"):
							parseName = filename.split('_')
							if particle == "both" and parseName[-1][:-5] == pt :
								singleDict[year][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename),True,PDF_PATH_S)
							elif parseName[0] == particle and parseName[-1][:-5] == pt:
								singleDict[year][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename),True,PDF_PATH_S)
					
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####
				
				elif set(options) == set(["-y","-o","-p","-r","-t"]):
					
					# CHOOSE A YEAR, MAGPOL, PARTICLE AND RAPIDITY AND TRANS MOM. BIN
					
					year = int(arguments[options.index("-y")])
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					pt = arguments[options.index("-t")]
					if pt not in pt_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
						
					rapidity = arguments[options.index("-r")]
					if rapidity not in y_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for j in magpol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/y_ptbins/"):
							parseName = filename.split('_')
							if particle == "both" and parseName[-1][:-5] == pt and parseName[2] == rapidity:
								singleDict[year][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename),True,PDF_PATH_S)
							elif parseName[0] == particle and parseName[-1][:-5] == pt and parseName[2] == rapidity:
								singleDict[year][j][filename] = mf.shapeFit("GaussCB", singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename),True,PDF_PATH_S)
					
					dictF = open("Dict_output/singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
				sys.exit()
				
				
###############################################################################################################################################################
				
			elif arguments[m] == "combined":
				
				# THE CODE THAT MAKES IT WORK FOR COMBINED BIN FILES
				
				if os.path.isfile("Dict_output/combinedFit_DictFile.py"):
					from Dict_output.combinedFit_DictFile import mainDict as combinedDict
					
				
				del arguments[m]
				del options[m]
				
				# THE CODE THAT MAKES IT WORK FOR SINGLE BIN FILES

#####				
				if set(options) == set([]):
					# EVERYTHING HAS TO BE DONE
					mainDict = {}
	
					for i in years:
						mainDict[i] = {}
						for j in magPol:
							mainDict[i][j] = {}
							
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ptbins/"):
								mainDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C)
							
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ybins/"):
								mainDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename, "y_combined"),True,PDF_PATH_C)
								
					
					# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
					dictF = open("Dict_output/combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(mainDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####					
				elif set(options) == set(["-y"]):
					# EVERYTHINg IN THAT YEAR
					year = int(arguments[0])#options.index("-y")]
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
						
					for i in magPol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + i + "/bins/ptbins/"):
							combinedDict[year][i][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,i,filename,"pt_combined"),True,PDF_PATH_C)
						for filename in os.listdir(BASE_PATH + str(year) + "_" + i + "/bins/ybins/"):
							combinedDict[year][i][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,i,filename,"y_combined"),True,PDF_PATH_C)
								
					dictF = open("Dict_output/combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####
				elif set(options) == set(["-o","-p"]):
					# CHOOSE SPECIFIC MAGPOL AND PARTICLE AND DOES EVERYTHING
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					for i in years:
						for j in magpol:
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ptbins/"):
								parseName = filename.split('_')
								if particle == "both":
									combinedDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C)
								elif parseName[0] == particle:
									combinedDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C)
									
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ybins/"):
								parseName = filename.split('_')
								if particle == "both":
									combinedDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"y_combined"),True,PDF_PATH_C)
								elif parseName[0] == particle:
									combinedDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"y_combined"),True,PDF_PATH_C)
					
					
					dictF = open("Dict_output/combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####
				elif set(options) == set(["-y","-o","-p"]):
					
					# CHOOSE A YEAR, MAGPOL AND PARTICLE
					
					year = int(arguments[options.index("-y")])
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
						
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					for j in magpol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/ptbins/"):
							parseName = filename.split('_')
							if particle == "both":
								combinedDict[year][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"pt_combined"),True,PDF_PATH_C)
							elif parseName[0] == particle:
								combinedDict[year][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"pt_combined"),True,PDF_PATH_C)
								
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/ybins/"):
							parseName = filename.split('_')
							if particle == "both":
								combinedDict[year][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"y_combined"),True,PDF_PATH_C)
							elif parseName[0] == particle:
								combinedDict[year][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"y_combined"),True,PDF_PATH_C)
				
					dictF = open("Dict_output/combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
				
				
#####
				elif set(options) == set(["-o","-p","-r"]):
					
					# CHOOSE A MAGPOL, PARTICLE AND RAPIDITY BIN
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					rapidity = arguments[options.index("-r")]
					if rapidity not in y_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for i in years:
						for j in magpol:
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ybins/"):
								parseName = filename.split('_')
								
								if particle == "both" and parseName[-1][:-5] == rapidity :
									combinedDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"y_combined"),True,PDF_PATH_C)
								elif parseName[0] == particle and parseName[-1][:-5] == rapidity:
									combinedDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"y_combined"),True,PDF_PATH_C)
									
					
					dictF = open("Dict_output/combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
				
#####
				elif set(options) == set(["-o","-p","-t"]):
					
					# CHOOSE A MAGPOL, PARTICLE AND TRANS MOMENTUM BIN
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					pt = arguments[options.index("-t")]
					if pt not in pt_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for i in years:
						for j in magpol:
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ptbins/"):
								parseName = filename.split('_')
								if particle == "both" and parseName[-1][:-5] == pt :
									combinedDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C)
								elif parseName[0] == particle and parseName[-1][:-5] == pt:
									combinedDict[i][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C)
							
					
					dictF = open("Dict_output/combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
#####
				
				elif set(options) == set(["-y","-o","-p","-r"]):
					
					# CHOOSE A YEAR, MAGPOL, PARTICLE AND RAPIDITY BIN
					
					year = int(arguments[options.index("-y")])
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					rapidity = arguments[options.index("-r")]
					if rapidity not in y_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for j in magpol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/ybins/"):
							parseName = filename.split('_')
							
							if particle == "both" and parseName[-1][:-5] == rapidity :
								combinedDict[year][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"y_combined"),True,PDF_PATH_C)
							elif parseName[0] == particle and parseName[-1][:-5] == rapidity:
								combinedDict[year][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"y_combined"),True,PDF_PATH_C)
							
					dictF = open("Dict_output/combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
				
				
#####
				elif set(options) == set(["-y","-o","-p","-t"]):
					
					# CHOOSE A YEAR, MAGPOL, PARTICLE AND TRANS MOMENTUM BIN
					
					year = int(arguments[options.index("-y")])
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					pt = arguments[options.index("-t")]
					if pt not in pt_bin:
						print("You entered a wrong input as rapidity bin, please check again.")
						sys.exit()
					
					for j in magpol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/ptbins/"):
							parseName = filename.split('_')
							if particle == "both" and parseName[-1][:-5] == pt :
								combinedDict[year][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"pt_combined"),True,PDF_PATH_C)
							elif parseName[0] == particle and parseName[-1][:-5] == pt:
								combinedDict[year][j][filename] = mf.shapeFit("GaussCB", combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"pt_combined"),True,PDF_PATH_C)
						
					dictF = open("Dict_output/combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
				sys.exit()
				
				
###########################################################################################################################################################################################

			elif arguments[m] == "year":
				
				# THE CODE THAT MAKES IT WORK FOR TOTAL YEAR FILES
				
				if os.path.isfile("Dict_output/yearFit_DictFile.py"):
					from Dict_output.yearFit_DictFile import mainDict as yearDict
					
				
				del arguments[m]
				del options[m]
				
				# THE CODE THAT MAKES IT WORK FOR SINGLE BIN FILES

#####				
				if set(options) == set([]):
					# EVERYTHING HAS TO BE DONE
					mainDict = {}
	
					for i in years:
						mainDict[i] = {}
						for j in magPol:
							mainDict[i][j] = {}
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/"):
								if filename != "bins":
									mainDict[i][j][filename] = mf.shapeFit("GaussCB", yearFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"year"),True,PDF_PATH_Y)
								
					
					# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
					dictF = open("Dict_output/yearFit_DictFile.py","w")
					dictF.write("mainDict = " + str(mainDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####					
				elif set(options) == set(["-y"]):
					# EVERYTHINg IN THAT YEAR
					year = int(arguments[0])#options.index("-y")]
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
						
					for i in magPol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + i + "/"):
							if filename != "bins":
								yearDict[year][i][filename] = mf.shapeFit("GaussCB", yearFitDict, mf.pathFinder(BASE_PATH,year,i,filename,"year"),True,PDF_PATH_Y)
								
					dictF = open("Dict_output/yearFit_DictFile.py","w")
					dictF.write("mainDict = " + str(yearDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####
				elif set(options) == set(["-o","-p"]):
					# CHOOSE SPECIFIC MAGPOL AND PARTICLE AND DOES EVERYTHING
					
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					for i in years:
						for j in magpol:
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/"):
								if filename != "bins":
									parseName = filename.split('_')
									if particle == "both":
										yearDict[i][j][filename] = mf.shapeFit("GaussCB", yearFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"year"),True,PDF_PATH_Y)
									elif parseName[0] == particle:
										yearDict[i][j][filename] = mf.shapeFit("GaussCB", yearFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"year"),True,PDF_PATH_Y)
								
					
					dictF = open("Dict_output/yearFit_DictFile.py","w")
					dictF.write("mainDict = " + str(yearDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
					
#####
				elif set(options) == set(["-y","-o","-p"]):
					
					# CHOOSE A YEAR, MAGPOL AND PARTICLE
					
					year = int(arguments[options.index("-y")])
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()
						
					magpol = arguments[options.index("-o")]
					if magpol == "up":
						magpol = ["MagUp"]
					elif magpol == "down":
						magpol = ["MagDown"]
					elif magpol == "both":
						magpol = magPol
					else:
						print("You entered a wrong input as magnet polarity, please check again.")
						sys.exit()
					
					particle = arguments[options.index("-p")]
					if(particle != "Xic" and particle != "Lc" and particle != "both"):
						print("You entered a wrong input as particle name, please check again.")
						sys.exit()
					
					for j in magpol:
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/"):
							if filename != "bins":
								parseName = filename.split('_')
								if particle == "both":
									yearDict[year][j][filename] = mf.shapeFit("GaussCB", yearFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"year"),True,PDF_PATH_Y)
								elif parseName[0] == particle:
									yearDict[year][j][filename] = mf.shapeFit("GaussCB", yearFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"year"),True,PDF_PATH_Y)
								
					dictF = open("Dict_output/yearFit_DictFile.py","w")
					dictF.write("mainDict = " + str(yearDict))
					dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
				sys.exit()
					
					
#########################################################################################################################################################################################################
			else:
				print("Please enter a correct string after the -m argument. For more help type -h.")
				sys.exit()


if __name__ == "__main__":
   main(sys.argv[1:])
