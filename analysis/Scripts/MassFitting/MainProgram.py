import ROOT, os, MassfitLib as mf 
from fittingDict import fittingDict

directory = "/home/exultimathule/Code/HonoursProgramme/LcAnalysis_Simon/analysis/Scripts/MassFitting/testDirectories/"
years = [2011,2012,2015,2016,2017,2018]
magPol = ["MagUp", "MagDown"]
mainDict = {}

def main():
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH
	
	for i in years:
		mainDict[i] = {}
		for j in magPol:
			mainDict[i][j] = {}
			for filename in os.listdir(directory + str(i) + "_" + j + "/bins/"):
				mf.shapeFit("GaussCB", fittingDict, mf.pathFinder(directory,i,j,filename))
				
	
	# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
	dictF = open("./Dict_output/dictFile.py","w")
	dictF.write("mainDict = " + str(mainDict))
	dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
	dictF.close()
	
	#ASSEMBLES ALL PDFs INTO ONE, UNCOMMENT ONLY IF YOU HAVE PDFTK INSTALLED
	#cmd = "pdftk ./PDF_output/*.pdf cat output ./PDF_output/allFitsInOne.pdf"
	#os.system(cmd)

if __name__ == '__main__':
    main()
