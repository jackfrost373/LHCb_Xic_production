import ROOT, os, MassfitLib as mf 
from fittingDict import fittingDict

#STOOMBOOT 
#path = "/dcache/bfys/scalo/binned_files/"
path = "/home/exultimathule/Code/HonoursProgramme/MassFitScript/testDirectories/"

#STOOMBOOT 
#PDFpath = "~/PDF_output/"
#DictPath = "~/Dict_output/"
PDFpath = "/home/exultimathule/Code/HonoursProgramme/MassFitScript/PDF_output/"
DictPath = "/home/exultimathule/Code/HonoursProgramme/MassFitScript/Dict_output/"

years = [2011,2012,2015,2016,2017,2018]
magPol = ["MagUp", "MagDown"]
mainDict = {}

def main():
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH
	
	for i in years:
		mainDict[i] = {}
		for j in magPol:
			mainDict[i][j] = {}
			for filename in os.listdir(path + str(i) + "_" + j + "/bins/"):
				mainDict[i][j][filename] = mf.shapeFit("GaussCB", fittingDict, mf.pathFinder(path,i,j,filename),True,PDFpath)
				
	
	# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
	dictF = open(DictPath + "autoFit_DictFile.py","w")
	dictF.write("mainDict = " + str(mainDict))
	dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
	dictF.close()
	
	#ASSEMBLES ALL PDFs INTO ONE, UNCOMMENT ONLY IF YOU HAVE PDFTK INSTALLED
	#cmd = "pdftk {0}*.pdf cat output {0}allFitsInOne.pdf".format(PDFpath)
	#os.system(cmd)

if __name__ == '__main__':
    main()
