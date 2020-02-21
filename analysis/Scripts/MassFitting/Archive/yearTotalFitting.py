import ROOT, os, MassfitLib as mf 
from yearTotalFit_Dict import fittingDict

#STOOMBOOT 
#path = "/dcache/bfys/scalo/binned_files/"
path = "/home/exultimathule/Code/HonoursProgramme/MassFitScript/testDirectories/"

#STOOMBOOT 
#PDFpath = "~/PDF_output/"
#DictPath = "~/Dict_output/"
PDFpath = "/home/exultimathule/Code/HonoursProgramme/MassFitScript/PDF_output/"
DictPath = "/home/exultimathule/Code/HonoursProgramme/MassFitScript/Dict_output/"

mainDict = {}
years = [2011,2012,2015,2016,2017,2018]

for year in years:
	mainDict[year] = mf.yearTotalShapeFit(year,"GaussCB",fittingDict,path, PDFpath)

dictF = open(DictPath + "yearTotal_DictFile.py","w")
dictF.write("mainDict = " + str(mainDict))
dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
dictF.close()

#ASSEMBLES ALL PDFs INTO ONE, UNCOMMENT ONLY IF YOU HAVE PDFTK INSTALLED
#cmd = "pdftk {0}*.pdf cat output {0}allFitsInOne.pdf".format(PDFpath)
#os.system(cmd)
