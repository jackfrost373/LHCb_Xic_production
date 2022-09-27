import ROOT,sys,os

sys.path.append('../') #This one is to be able to access Imports.py, one folder up from this script
sys.path.append('./')


from GaussCB_year_TotalFit_Dict import fittingDict as GaussCB_yearFitDict
from Bukin_year_TotalFit_Dict import fittingDict as Bukin_yearFitDict
from Imports import TUPLE_PATH, OUTPUT_DICT_PATH, PLOT_PATH,getMC,getMCCuts

def main():
	pdfpath = PLOT_PATH + "MassFitting/MC/PDF_output/Year/"
	dictpath = OUTPUT_DICT_PATH + "Massfitting/MC/"
	GaussDict ={}
	BukinDict ={}
	ROOT.gROOT.SetBatch(True)
	for year in [2011,2012,2016,2017,2018]:
		for particle in ["Lc","Xic"]:
			for mag in ["MagDown","MagUp"]:
				file = ROOT.TFile.Open("/dcache/bfys/jhemink/test.root","RECREATE")
				mctree = getMC(year = year,particle = particle,polarity = mag,cuts = True)
				if year > 2012:
					run =2
				else: 
					run =1
				if mctree.GetEntries() == 0:
					continue
				
				if not year in GaussDict:
					GaussDict[year]={}
					BukinDict[year]={}
				if not mag in GaussDict[year]:
					GaussDict[year][mag]={}
					BukinDict[year][mag]={}

				GaussDict[year][mag][f"MC_{particle}"], objList = fit(mctree,"GaussCB",GaussCB_yearFitDict,f"{year}_{mag}_{particle}_total.root",particle,True,pdfpath)
				BukinDict[year][mag][f"MC_{particle}"], objList = fit(mctree,"Bukin",Bukin_yearFitDict,f"{year}_{mag}_{particle}_total.root",particle,True,pdfpath)
				
				file.Close()
				
	dictF = open(dictpath + "GaussCB_MC_DictFile.py","w")
	dictF.write("mainDict = " + str(GaussDict))
	dictF.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
	dictF.close()
	dictG = open(dictpath + "Bukin_MC_DictFile.py","w")
	dictG.write("mainDict = " + str(BukinDict))
	dictG.write("\ndef dictSearch(shape,year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[shape][year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
	dictG.close()
	
	os.remove("/dcache/bfys/jhemink/test.root")




def fit(mctree, shape, fittingDict, fullname, particle, PDF, PDFpath, fitComp = True,strategy = 1):
	splitfullname = fullname.split('.root')
	shortfullname = splitfullname[0]

	# return lists for persistency in memory
	varlist = []
	shapelist = []

	nEntries = mctree.GetEntries()
	
	if shape == "GaussCB":		
		if fullname in fittingDict["GaussCB"][particle]:
			mass_range = fittingDict["GaussCB"][particle][fullname]["mass_range"]
			peak_range = fittingDict["GaussCB"][particle][fullname]["peak_range"]
			
			normalisation_factor = fittingDict["GaussCB"][particle][fullname]["normalisation_factor"]
			exponential_normalisation_factor = fittingDict["GaussCB"][particle][fullname]["exponential_normalisation_factor"]
			
			exponential_range = fittingDict["GaussCB"][particle][fullname]["exponential_range"]
			
			width_range = fittingDict["GaussCB"][particle][fullname]["width_range"]
			
			cb_width_range = fittingDict["GaussCB"][particle][fullname]["cb_width_range"]
			cb_alpha_range = fittingDict["GaussCB"][particle][fullname]["cb_alpha_range"]
			cb_n_range = fittingDict["GaussCB"][particle][fullname]["cb_n_range"]
			
		else:
			mass_range = fittingDict["GaussCB"][particle]["general"]["mass_range"]
			peak_range = fittingDict["GaussCB"][particle]["general"]["peak_range"]
			
			normalisation_factor = fittingDict["GaussCB"][particle]["general"]["normalisation_factor"]
			exponential_normalisation_factor = fittingDict["GaussCB"][particle]["general"]["exponential_normalisation_factor"]
			
			exponential_range = fittingDict["GaussCB"][particle]["general"]["exponential_range"]
			
			width_range = fittingDict["GaussCB"][particle]["general"]["width_range"]
			
			cb_width_range = fittingDict["GaussCB"][particle]["general"]["cb_width_range"]
			cb_alpha_range = fittingDict["GaussCB"][particle]["general"]["cb_alpha_range"]
			cb_n_range = fittingDict["GaussCB"][particle]["general"]["cb_n_range"]

	if shape=="Bukin":
		if fullname in fittingDict["Bukin"][particle]:
			mass_range = fittingDict["Bukin"][particle][fullname]["mass_range"]
			peak_range = fittingDict["Bukin"][particle][fullname]["peak_range"]

			normalisation_factor = fittingDict["Bukin"][particle][fullname]["normalisation_factor"]
			exponential_normalisation_factor = fittingDict["Bukin"][particle][fullname]["exponential_normalisation_factor"]

			exponential_range = fittingDict["Bukin"][particle][fullname]["exponential_range"]

			Bukin_Xp_range = fittingDict["Bukin"][particle][fullname]["Bukin_Xp_range"]
			Bukin_Sigp_range = fittingDict["Bukin"][particle][fullname]["Bukin_Sigp_range"]
			Bukin_xi_range = fittingDict["Bukin"][particle][fullname]["Bukin_xi_range"]
			Bukin_rho1_range = fittingDict["Bukin"][particle][fullname]["Bukin_rho1_range"]
			Bukin_rho2_range = fittingDict["Bukin"][particle][fullname]["Bukin_rho2_range"]
			

		else:
			mass_range = fittingDict["Bukin"][particle]["general"]["mass_range"]
			peak_range = fittingDict["Bukin"][particle]["general"]["peak_range"]

			normalisation_factor = fittingDict["Bukin"][particle]["general"]["normalisation_factor"]
			exponential_normalisation_factor = fittingDict["Bukin"][particle]["general"]["exponential_normalisation_factor"]

			exponential_range = fittingDict["Bukin"][particle]["general"]["exponential_range"]
			
			Bukin_Xp_range = fittingDict["Bukin"][particle]["general"]["Bukin_Xp_range"]
			Bukin_Sigp_range = fittingDict["Bukin"][particle]["general"]["Bukin_Sigp_range"]
			Bukin_xi_range = fittingDict["Bukin"][particle]["general"]["Bukin_xi_range"]
			Bukin_rho1_range = fittingDict["Bukin"][particle]["general"]["Bukin_rho1_range"]
			Bukin_rho2_range = fittingDict["Bukin"][particle]["general"]["Bukin_rho2_range"]

	exponential_range = [0,0,0]

	print(mass_range)


	c1 = ROOT.TCanvas("c1","c1",1200,700)
	pullpad1 = ROOT.TPad("pullpad1", "",0.0,0.25,1.0,1.0)
	pullpad2 = ROOT.TPad("pullpad2", "",0.0,0.0,1.0,0.25)
	pullpad1.SetTopMargin(0.05)
	pullpad1.SetBottomMargin(0)
	pullpad1.SetLeftMargin(0.12)
	pullpad1.SetRightMargin(0.05)
	pullpad2.SetTopMargin(0)
	pullpad2.SetBottomMargin(0.25)
	pullpad2.SetLeftMargin(0.12)
	pullpad2.SetRightMargin(0.05)
	pullpad1.cd()
	
	nbins = 100
	masshist = ROOT.TH1F("masshist","Histogram of Lc mass",nbins,mass_range[0],mass_range[1])
	mctree.Draw("lcplus_MM>>mymasshist")
	masshist = ROOT.gDirectory.Get("mymasshist")
	
	mass = ROOT.RooRealVar("lcplus_MM","Mass",mass_range[0],mass_range[1],"MeV/c^{2}")


	#Here is where the different fit shapes are implemented with their various parameters
	if shape == "GaussCB":
		gauss_mean  = ROOT.RooRealVar("gauss_mean","Mean",peak_range[0], peak_range[1], peak_range[2])
		gauss_width = ROOT.RooRealVar("gauss_width","Width",width_range[0], width_range[1], width_range[2])
		myGauss	    = ROOT.RooGaussian("myGauss","Gaussian", mass, gauss_mean, gauss_width)
		shapelist+=[myGauss]
		cb_width    = ROOT.RooRealVar("cb_width","CB Width",cb_width_range[0], cb_width_range[1], cb_width_range[2])
		cb_alpha    = ROOT.RooRealVar("cb_alpha","Exp.const",cb_alpha_range[0], cb_alpha_range[1], cb_alpha_range[2])
		cb_n	    = ROOT.RooRealVar("cb_n","Exp.crossover",cb_n_range[0], cb_n_range[1], cb_n_range[2])
		myCB	    = ROOT.RooCBShape("myCB","Crystal Ball", mass, gauss_mean, cb_width, cb_alpha, cb_n)
		shapelist+=[myCB]
		exponential = ROOT.RooRealVar("exponential","C", exponential_range[0], exponential_range[1], exponential_range[2])
		exponential_Norm  = ROOT.RooRealVar("exponential_Norm","Exponential Yield", 0, 0, 0)
		myexponential = ROOT.RooExponential("myexponential","Exponential", mass, exponential)
		shapelist+=[myexponential]
		combined_Norm = ROOT.RooRealVar("combined_Norm","Normalization for gaussCB", 0.5,0,1)

		Actual_signalshape = ROOT.RooAddPdf ("Actual_signalshape", "Shape of the interesting events", myGauss, myCB, combined_Norm)
		shapelist+=[Actual_signalshape]
		Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", nEntries/2, nEntries/50, nEntries*1.25)

		fullshape = ROOT.RooAddPdf("fullshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

	if shape == "Bukin":
		Bukin_Xp = ROOT.RooRealVar("Bukin_Xp", "Peak position",Bukin_Xp_range[0],Bukin_Xp_range[1],Bukin_Xp_range[2])
		Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width",Bukin_Sigp_range[0],Bukin_Sigp_range[1],Bukin_Sigp_range[2])
		Bukin_xi = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter",Bukin_xi_range[0],Bukin_xi_range[1],Bukin_xi_range[2])
		Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail",Bukin_rho1_range[0],Bukin_rho1_range[1],Bukin_rho1_range[2])
		Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", Bukin_rho2_range[0],Bukin_rho2_range[1],Bukin_rho2_range[2])
		
		exponential = ROOT.RooRealVar("exponential","C",exponential_range[0],exponential_range[1],exponential_range[2])
		myexponential = ROOT.RooExponential("myexponential","Exponential", mass, exponential)
		exponential_Norm = ROOT.RooRealVar("exponential Norm", "exponential Yield", 0, 0, 0)
		
		Bukin_PDF = ROOT.RooBukinPdf("Actual_signalshape", "Bukin shape", mass, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)

		Actual_signalshape_Norm = ROOT.RooRealVar("actual_signalshape_Norm", "Signal Yield", nEntries, nEntries/10, nEntries*2)
		
		fullshape = ROOT.RooAddPdf("signalshape", "Signal Shape", ROOT.RooArgList(Bukin_PDF, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

	masshist_RooFit = ROOT.RooDataSet("masshist_RooFit","masshist RooFit", mctree , ROOT.RooArgSet(mass))

	#Fit the data using the desired shape
	fullshape.fitTo(masshist_RooFit,ROOT.RooFit.Strategy(strategy))
	frame = mass.frame()
	masshist_RooFit.plotOn(frame)
	fullshape.plotOn(frame)
	
	
	#Important, if we use other variables/ define other shapes we need to ensure we return the non-yield vars as constants
	if shape == "GaussCB":
		for var in [gauss_mean, gauss_width, cb_width, cb_alpha, cb_n, exponential, combined_Norm]:
			var.setConstant(ROOT.kTRUE)
		varlist += [gauss_mean, gauss_width, cb_width, cb_alpha, cb_n, exponential, exponential_Norm, combined_Norm, Actual_signalshape_Norm]
		shapelist = [fullshape] + shapelist

	elif shape == "Bukin":
		for var in [Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2, exponential]:
			var.setConstant(ROOT.kTRUE)
		varlist += [Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2, exponential, exponential_Norm, Actual_signalshape_Norm]
		shapelist = [fullshape] + shapelist
	#Get the parameters resulting from the fit
	
		
	w=ROOT.RooWorkspace("w")
	# getattr(w,'import')(masshist_RooFit)	
	# getattr(w,'import')(fullshape)
	# w.writeToFile("MassFitting/MC_{0}_model.root".format(shortfullname))

	signal_yield = Actual_signalshape_Norm.getValV()
	signal_error = Actual_signalshape_Norm.getError()
	chi2ndf = frame.chiSquare()

	#Show parameters on graph
	fullshape.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.56,0.9,0.9))

	frame.SetTitle("MC_" + fullname + f" events: {round(signal_yield)} / {nEntries} " )

	pullhist = frame.pullHist()
	
	#Plot the data component of the shape and the background one separately to see more clearly
	fullshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"),ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(2))
	fullshape.plotOn(frame, ROOT.RooFit.Components("myexponential"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
	
	if fitComp == True:
		if shape =="GaussCB":
			fullshape.plotOn(frame, ROOT.RooFit.Components("myGauss"),ROOT.RooFit.LineColor(7), ROOT.RooFit.LineStyle(2),ROOT.RooFit.LineWidth(1))
			fullshape.plotOn(frame, ROOT.RooFit.Components("myCB"),ROOT.RooFit.LineColor(40), ROOT.RooFit.LineStyle(2),ROOT.RooFit.LineWidth(1))

	

	frame.Draw()

	if shape == "GaussCB":
		mainDict = {
			"Shape" : shape,
			"yield_val" : signal_yield,
			"yield_err" : signal_error,
			"chi2ndf" : chi2ndf,
			"nEvents" : nEntries,
			# "gauss_mean_val" : gauss_mean.getValV(),
			# "gauss_mean_err" : gauss_mean.getError(),
			# "gauss_width_val" : gauss_width.getValV(),
			# "gauss_width_err" : gauss_width.getError(),
			# "CB_width_val" : cb_width.getValV(),
			# "CB_width_err" : cb_width.getError(),
			# "CB_alpha_val" : cb_alpha.getValV(),
			# "CB_alpha_err" : cb_alpha.getError(),
			# "CB_n_val" : cb_n.getValV(),
			# "CB_n_err" : cb_n.getError()
		}
	if shape == "Bukin":
		mainDict = {
			"Shape" : shape,
			"yield_val" : signal_yield,
			"yield_err" : signal_error,
			"chi2ndf" : chi2ndf,
			"nEvents" : nEntries,
		}
	
	pullpad2.cd()
	framepull = mass.frame()
	framepull.addPlotable(pullhist)
	framepull.SetTitle("")
	framepull.GetYaxis().SetTitle("Pull")
	framepull.GetYaxis().SetTitleOffset(0.4)
	framepull.GetYaxis().SetTitleSize(0.1)
	framepull.GetYaxis().SetLabelSize(0.1)
	framepull.GetXaxis().SetTitleSize(0.1)
	framepull.GetXaxis().SetLabelSize(0.1)
	framepull.Draw()

	c1.cd()
	pullpad1.Draw()
	pullpad2.Draw()
	c1.Update()
	c1.Draw()

	#PDF CREATION#
	if PDF == True:
		strName = PDFpath + shape + "_MC_" + fullname + ".pdf"
		c1.SaveAs(strName)	
	
	masshist.Delete()
	ROOT.gDirectory.Delete("mymasshist")
	
	return mainDict, [varlist,shapelist]

if __name__ == "__main__":
	main()