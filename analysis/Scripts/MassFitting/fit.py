import sys, getopt

########################################################################################
#TO USE THIS PROGRAM OUTSIDE THE TERMINAL AND GETTING A LIST OF ROO Objects, YOU NEED TO 
#GIVE THE COMMAND-LINE ARGS AND OPTIONS ALREADY PARSED, AS SHOWN IN THE EXAMPLE BENEITH:
#import fit
#objList = fit.main(["-m", "single", "-y", "2012", "-o", "up", "-p", "Xic", "-r", "2.5-3.0", "-t", "8000-10000"])
########################################################################################

#Creating python path for the importing of the Imports.py module(has to be one directory behind)
# and the dictionnaries in Dict_output directory

sys.path.append('../') #This one is to be able to access Imports.py, one folder up from this script
sys.path.append('./')

import ROOT, os, MassfitLib as mf 
from GaussCB_single_fitting_Dict import fittingDict as GaussCB_singleFitDict
from GaussCB_CombinedFit_Dict import fittingDict as GaussCB_combinedFitDict
from GaussCB_year_TotalFit_Dict import fittingDict as GaussCB_yearFitDict
from Bukin_single_fitting_Dict import fittingDict as Bukin_singleFitDict
from Bukin_CombinedFit_Dict import fittingDict as Bukin_combinedFitDict
from Bukin_year_TotalFit_Dict import fittingDict as Bukin_yearFitDict

import os.path
import textwrap
import Imports
from Imports import TUPLE_PATH, OUTPUT_DICT_PATH, PLOT_PATH
#folder structure : 
#	/dcache/bfys/scalo/binned_files/2011_MagUp/bins/y_ptbins
#	/dcache/bfys/scalo/binned_files/2011_MagUp/bins/ybins
#	/dcache/bfys/scalo/binned_files/2011_MagUp/bins/ptbins
#	/dcache/bfys/scalo/binned_files/2011_MagUp/LC_total.root

#filename structure : Lc_ybin_2.0-2.5_ptbin_3200-4000.root

#This is the base path without the particle location (until binned_files in our case)
BASE_PATH = TUPLE_PATH

#Path for the outputting of the Dictionnaries. Need to make the second folder
Dict_PATH = OUTPUT_DICT_PATH + "Massfitting/"
sys.path.append(Dict_PATH)

#This is the PDF output base path. On local computer, just output into the same directory
# as the script, with the directory structure below. If on Stomboot, output into the other
#BASE_PDF_OUTPUT = "./"
BASE_PDF_OUTPUT = PLOT_PATH + "MassFitting/"

PDF_PATH_S = BASE_PDF_OUTPUT + "PDF_output/Single/"
PDF_PATH_C = BASE_PDF_OUTPUT + "PDF_output/Combined/"
PDF_PATH_Y = BASE_PDF_OUTPUT + "PDF_output/Year/"

#Creates the paths in case they don't exist
pathsArr = [Dict_PATH,PDF_PATH_S,PDF_PATH_C,PDF_PATH_Y]
for path in pathsArr:
	if not os.path.isdir(path):
		os.makedirs(path)


years = [2011,2012,2015,2016,2017,2018]
magPol = ["MagUp", "MagDown"]
shape = "GaussCB"

#Creation of the y and pt bin lists from the imports functions
pt_bin_temp = Imports.getPTbins()
pt_bin = []
for pt in pt_bin_temp:
	pt_bin.append("{}-{}".format(pt[0], pt[1]))
	
y_bin_temp = Imports.getYbins()
y_bin = []
for y in y_bin_temp:
	y_bin.append("{}-{}".format(y[0], y[1]))

def main(argv):
	global shape				
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH FOR ROOT
	
	try:
		opts, args = getopt.getopt(argv,"hm:y:o:p:r:t:s:")
	except getopt.GetoptError:
		print("The arguments are wrong")
		sys.exit(2)
	
	options = []
	arguments = []
	objList = []
	
        
	for opt,arg in opts:
		options.append(opt)
		arguments.append(arg)
	print(options)
	print(arguments)
	if "-h" in options:
		print(textwrap.dedent("""\
			
			Welcome to the fit.py script.
			If not already present, the programme will create directories with the following structure:
				Dict_output/
				PDF_output/Single
				PDF_output/Combined
				PDF_output/Year
			These are for the output of the script and are necessary for a functionning run.

			The parameters are
				-s : shape (GaussCB or Bukin) (default: GaussCB)
				-m : mode (single, combined or year)
				-y : year (e.g. 2011) 
				-o : magnet polarity (up, down or both)
				-p : particle name (Xic, Lc or both)
				-r : rapidity (e.g. 2.5-3.0)
				-t : transverse momentum (e.g. 8000-10000)

			Important: If desired the -s argument always has to be specifed after the -m argument and before any other arguments. 

			Important: the -o and -p are always used together, there is no option for using only one of the two (you can consider them as a single parameter...

			For modes -m:
				-"single" you can use any combination of -s -y -o -p -r -t 
				-"combined" you can use any combination of -s -y -o -p -r -t but you can never use both -r and -t together, which yould defeat the point of having combined bins
				-"year"you can use any combination of -s -y -o -p

			Running with no other parameter than -m makes the full fitting process and uses default GaussCB fit shape. It also initializes the ditionnary file if you have not yet run the programme (important, the first time using this script requires initializing the dictionnaries by running with no parameter, e.g. "python fit.py -m single").
			"""))

		sys.exit()
	#look for s in options (like m) if there -> use String as shape, != do nothing	
#look everywhere and replace gaussCB with shape (find & replace)
#define dict file depending on shape
#replace everyhwere where its coded to the right dict
	

	for m in range(len(options)):

		if options[m] == "-s":
			print("shape opt")
			if arguments[m] == "Bukin":
				shape = "Bukin"
			elif arguments[m] == "GaussCB":
				shape = "GaussCB"
			else:
				print("Wrong fit shape entered. Please try again!")
				sys.exit()

			print("del shape")
			del arguments[m]
			del options[m]

		if options[m] == "-m":
			
			if arguments[m] == "single":
				print("single")
				
				if os.path.isfile(Dict_PATH + shape + "singleFit_DictFile.py"):
					if shape == "GaussCB":
						from GaussCBsingleFit_DictFile import mainDict as singleDict
					else: from BukinsingleFit_DictFile import mainDict as singleDict
			
				
				del arguments[m]
				del options[m]
				print("end  {0}".format( options))
				
				# THE CODE THAT MAKES IT WORK FOR SINGLE BIN FILES

#####
				singleFitDict = GaussCB_singleFitDict
				if shape == "Bukin":
					singleFitDict = Bukin_singleFitDict
				

				if set(options) == set([]):
					# EVERYTHING HAS TO BE DONE
					print("Options are empty. Everything has to be done")
					mainDict = {}

					for i in years:
						print(years)
						mainDict[i] = {}
						for j in magPol:
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							mainDict[i][j] = {}
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								mainDict[i][j][filename], objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)
								
					
					# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(mainDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
#####

#####
				if set(options) == set(["-y"]):
					# EVERYTHING IN THAT YEAR
					year = int(arguments[options.index("-y")])#options.index("-y")]
					if year not in years:
						print("The year you entered is incorrect, please check again.")
						sys.exit()

					for i in magPol:
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + i):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + i + "/bins/y_ptbins/"):
							singleDict[year][i][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,i,filename,"single"),True,PDF_PATH_S,True)
							
					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape, year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								parseName = filename.split('_')
								if particle == "both":
									singleDict[i][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)
								elif parseName[0] == particle:
									singleDict[i][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)
                  
					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape, year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + j):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/y_ptbins/"):
							parseName = filename.split('_')
							if particle == "both":
								singleDict[year][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"single"),True,PDF_PATH_S,True)
							elif parseName[0] == particle:
								singleDict[year][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"single"),True,PDF_PATH_S,True)
				
					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								parseName = filename.split('_')
								if particle == "both" and parseName[2] == rapidity :
									singleDict[i][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)
								elif parseName[0] == particle and parseName[2] == rapidity:
									singleDict[i][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)

					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								parseName = filename.split('_')
								if particle == "both" and parseName[-1][:-5] == pt :
									singleDict[i][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)
								elif parseName[0] == particle and parseName[-1][:-5] == pt:
									singleDict[i][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)

					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/y_ptbins/"):
								parseName = filename.split('_')
								if particle == "both" and parseName[-1][:-5] == pt and parseName[2] == rapidity:
									singleDict[i][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)
								elif parseName[0] == particle and parseName[-1][:-5] == pt and parseName[2] == rapidity:
									singleDict[i][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"single"),True,PDF_PATH_S,True)
					
					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + j):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/y_ptbins/"):
							parseName = filename.split('_')
							if particle == "both" and parseName[2] == rapidity :
								singleDict[year][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"single"),True,PDF_PATH_S,True)
							elif parseName[0] == particle and parseName[2] == rapidity:
								singleDict[year][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"single"),True,PDF_PATH_S,True)

					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + j):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/y_ptbins/"):
							parseName = filename.split('_')
							if particle == "both" and parseName[-1][:-5] == pt :
								singleDict[year][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"single"),True,PDF_PATH_S,True)
							elif parseName[0] == particle and parseName[-1][:-5] == pt:
								singleDict[year][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"single"),True,PDF_PATH_S,True)
					
					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + j):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/y_ptbins/"):
							parseName = filename.split('_')
							if particle == "both" and parseName[-1][:-5] == pt and parseName[2] == rapidity:
								singleDict[year][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"single"),True,PDF_PATH_S,True)
							elif parseName[0] == particle and parseName[-1][:-5] == pt and parseName[2] == rapidity:
								singleDict[year][j][filename] , objList = mf.shapeFit(shape, singleFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"single"),True,PDF_PATH_S,True)

					dictF = open(Dict_PATH + shape + "singleFit_DictFile.py","w")
					dictF.write("mainDict = " + str(singleDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
					
				return objList
				
				
###############################################################################################################################################################
				
			elif arguments[m] == "combined":
				# THE CODE THAT MAKES IT WORK FOR COMBINED BIN FILES
				
				if os.path.isfile(Dict_PATH + shape + "combinedFit_DictFile.py"):
					if shape == "GaussCB":
						from GaussCBcombinedFit_DictFile import mainDict as combinedDict
					else: from BukincombinedFit_DictFile import mainDict as combinedDict
					
				
				del arguments[m]
				del options[m]
				
				# THE CODE THAT MAKES IT WORK FOR SINGLE BIN FILES

#####				
				combinedFitDict = GaussCB_combinedFitDict
				if shape == "Bukin":
					combinedFitDict = Bukin_combinedFitDict

#####

				if set(options) == set([]):
					# EVERYTHING HAS TO BE DONE
					mainDict = {}
	
					for i in years:
						mainDict[i] = {}
						for j in magPol:
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							mainDict[i][j] = {}
							
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ptbins/"):
								mainDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C,True)
							
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ybins/"):
								mainDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename, "y_combined"),True,PDF_PATH_C,True)

					# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
					dictF = open(Dict_PATH + shape + "combinedFit_DictFile.py","w")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + i):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + i + "/bins/ptbins/"):
							combinedDict[year][i][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,i,filename,"pt_combined"),True,PDF_PATH_C,True)
						for filename in os.listdir(BASE_PATH + str(year) + "_" + i + "/bins/ybins/"):
							combinedDict[year][i][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,i,filename,"y_combined"),True,PDF_PATH_C,True)

					dictF = open(Dict_PATH + shape + "combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ptbins/"):
								parseName = filename.split('_')
								if particle == "both":
									combinedDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C,True)
								elif parseName[0] == particle:
									combinedDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C,True)
									
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ybins/"):
								parseName = filename.split('_')
								if particle == "both":
									combinedDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"y_combined"),True,PDF_PATH_C,True)
								elif parseName[0] == particle:
									combinedDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"y_combined"),True,PDF_PATH_C,True)
					
					
					dictF = open(Dict_PATH + shape + "combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + j):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/ptbins/"):
							parseName = filename.split('_')
							if particle == "both":
								combinedDict[year][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"pt_combined"),True,PDF_PATH_C,True)
							elif parseName[0] == particle:
								combinedDict[year][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"pt_combined"),True,PDF_PATH_C,True)

						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/ybins/"):
							parseName = filename.split('_')
							if particle == "both":
								combinedDict[year][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"y_combined"),True,PDF_PATH_C,True)
							elif parseName[0] == particle:
								combinedDict[year][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"y_combined"),True,PDF_PATH_C,True)
				
					dictF = open(Dict_PATH + shape + "combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ybins/"):
								parseName = filename.split('_')
								
								if particle == "both" and parseName[-1][:-5] == rapidity :
									combinedDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"y_combined"),True,PDF_PATH_C,True)
								elif parseName[0] == particle and parseName[-1][:-5] == rapidity:
									combinedDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"y_combined"),True,PDF_PATH_C,True)
									
					dictF = open(Dict_PATH + shape + "combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/bins/ptbins/"):
								parseName = filename.split('_')
								if particle == "both" and parseName[-1][:-5] == pt :
									combinedDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C,True)
								elif parseName[0] == particle and parseName[-1][:-5] == pt:
									combinedDict[i][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"pt_combined"),True,PDF_PATH_C,True)

					dictF = open(Dict_PATH + shape + "combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + j):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/ybins/"):
							parseName = filename.split('_')
							
							if particle == "both" and parseName[-1][:-5] == rapidity :
								combinedDict[year][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"y_combined"),True,PDF_PATH_C,True)
							elif parseName[0] == particle and parseName[-1][:-5] == rapidity:
								combinedDict[year][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"y_combined"),True,PDF_PATH_C,True)
							
					dictF = open(Dict_PATH + shape + "combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + j):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/bins/ptbins/"):
							parseName = filename.split('_')
							if particle == "both" and parseName[-1][:-5] == pt :
								combinedDict[year][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"pt_combined"),True,PDF_PATH_C,True)
							elif parseName[0] == particle and parseName[-1][:-5] == pt:
								combinedDict[year][j][filename] , objList = mf.shapeFit(shape, combinedFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"pt_combined"),True,PDF_PATH_C,True)

					dictF = open(Dict_PATH + shape + "combinedFit_DictFile.py","w")
					dictF.write("mainDict = " + str(combinedDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()
				
				return objList
				
				
###########################################################################################################################################################################################

			elif arguments[m] == "year":
				
				# THE CODE THAT MAKES IT WORK FOR TOTAL YEAR FILES
				
				if os.path.isfile(Dict_PATH + shape + "yearFit_DictFile.py"):
					if shape == "GaussCB":
						from GaussCByearFit_DictFile import mainDict as yearDict
					else: from BukinyearFit_DictFile import mainDict as yearDict
					
				
				
				del arguments[m]
				del options[m]
				
				# THE CODE THAT MAKES IT WORK FOR SINGLE BIN FILES

#####				
				yearFitDict = GaussCB_yearFitDict
				if shape == "Bukin":
					yearFitDict = Bukin_yearFitDict
#####

				if set(options) == set([]):
					# EVERYTHING HAS TO BE DONE
					mainDict = {}

					for i in years:
						mainDict[i] = {}
						for j in magPol:
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							mainDict[i][j] = {}
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/"):
								if filename != "bins":
									mainDict[i][j][filename] , objList = mf.shapeFit(shape, yearFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"year"),True,PDF_PATH_Y,True)

					# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
					dictF = open(Dict_PATH + shape + "yearFit_DictFile.py","w")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + i):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + i + "/"):
							if filename != "bins":
								yearDict[year][i][filename] , objList = mf.shapeFit(shape, yearFitDict, mf.pathFinder(BASE_PATH,year,i,filename,"year"),True,PDF_PATH_Y,True)

					dictF = open(Dict_PATH + shape + "yearFit_DictFile.py","w")
					dictF.write("mainDict = " + str(yearDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
							if not os.path.isdir(BASE_PATH + "/" + str(i) + "_" + j):
								continue
							for filename in os.listdir(BASE_PATH + str(i) + "_" + j + "/"):
								if filename != "bins":
									parseName = filename.split('_')
									if particle == "both":
										yearDict[i][j][filename] , objList = mf.shapeFit(shape, yearFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"year"),True,PDF_PATH_Y,True)
									elif parseName[0] == particle:
										yearDict[i][j][filename] , objList = mf.shapeFit(shape, yearFitDict, mf.pathFinder(BASE_PATH,i,j,filename,"year"),True,PDF_PATH_Y,True)

					dictF = open(Dict_PATH + shape + "yearFit_DictFile.py","w")
					dictF.write("mainDict = " + str(yearDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
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
						if not os.path.isdir(BASE_PATH + "/" + str(year) + "_" + j):
							continue
						for filename in os.listdir(BASE_PATH + str(year) + "_" + j + "/"):
							if filename != "bins":
								parseName = filename.split('_')
								if particle == "both":
									yearDict[year][j][filename] , objList = mf.shapeFit(shape, yearFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"year"),True,PDF_PATH_Y,True)
								elif parseName[0] == particle:
									yearDict[year][j][filename] , objList = mf.shapeFit(shape, yearFitDict, mf.pathFinder(BASE_PATH,year,j,filename,"year"),True,PDF_PATH_Y,True)
								
					dictF = open(Dict_PATH + shape + "yearFit_DictFile.py","w")
					dictF.write("mainDict = " + str(yearDict))
					dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
					dictF.close()

				return objList
					
					
#########################################################################################################################################################################################################
			else:
				print("Please enter a correct string after the -m argument. For more help type -h.")
				sys.exit()


if __name__ == "__main__":
	main(sys.argv[1:])
