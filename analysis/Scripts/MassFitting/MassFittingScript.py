import ROOT, os

#DIRECTORY CONTAINING THE "YEAR_MagPolarity" FOLDERS
directory = "binned_files/"

years = [2011,2012,2015,2016,2017,2018]
magPol = ["MagUp", "MagDown"]
mainDict = {}

def main():
	ROOT.gROOT.SetBatch(True) #STOP PRINTING
	
	for i in years:
		mainDict[i] = {}
		for j in magPol:
			mainDict[i][j] = {}
			for filename in os.listdir(directory + str(i) + "_" + j + "/bins/"):
				newDir = directory + str(i) + "_" + j + "/bins/"
				
				if filename.startswith("Lc"):
					MClocation = os.path.join(newDir,filename)
					Shape_fit("GaussCB", MClocation, filename, mainDict, i, j, "Lc", False, False)
					
				if filename.startswith("Xic"):
					MClocation = os.path.join(newDir,filename)
					Shape_fit("GaussCB", MClocation, filename, mainDict, i, j, "Xic", False, False)
	
	# WRITES THE .py FILE WITH DICT AND dictSearch FUNCTION
	dictF = open("./Dict_output/dictFile.py","w")
	dictF.write("mainDict = " + str(mainDict))
	dictF.write("\ndef dictSearch(year, magPol, filename):\n\tparamArray=[]\n\tfor i,j in mainDict[year][magPol][filename].items():\n\t\tparamArray.append(j)\n\treturn paramArray")
	dictF.close()
	
	#ASSEMBLES ALL PDFs INTO ONE, UNCOMMENT ONLY IF YOU HAVE PDFTK INSTALLED
	#cmd = "pdftk ./PDF_output/*.pdf cat output ./PDF_output/allFitsInOne.pdf"
	#os.system(cmd)


def Shape_fit(shape, MClocation, filename, mainDict, i, j, particle, Data=True, Pull=False):

	Bukin_xi_range =[0, -1, 1]
	Bukin_rho1_range = [0, -1, 1]
	Bukin_rho2_range = [0, -1, 1]
	#cb_alpha_range = [1, 0, 5]
	cb_alpha_range = [1.0,0.0,5.0]
	# was 1, 0, 7
	#cb_n_range = [1, 0, 15]
	cb_n_range = [1.0,0.0,5.0]
	# was 1, 0, 20
	gauss_normalisation_factor = 1

	if particle == "Lc":
		mass_range = [2240, 2340]
		#peak_range = [2288, 2280, 2290]
		peak_range = [2289,2260,2320]
		#was 2288, 2270, 2300
		normalisation_factor = 6
		gauss_normalisation_factor = 10
		exponential_normalisation_factor = 1
		#exponential_range = [0.001, -0.2, 0.2]
		exponential_range = [0.001, -0.5, 0.5]
		#width_range = [2, 0, 10]
		width_range = [6,4,20]
		# was 2, 0, 15
		#cb_width_range = [2, 0, 15]
		cb_width_range = [17,8,50]
		# was 2, 0, 20
		cb_normalisation_factor = 10


	if particle == "Xic":
		mass_range = [2420, 2520]
		#peak_range = [2469, 2460, 2480]
		peak_range = [2469, 2450, 2485]
		normalisation_factor = 1
		gauss_normalisation_factor = 2
		exponential_normalisation_factor = 1
		#exponential_range = [0.0, -1, 1]
		exponential_range = [-0.0002, -2, 2]
		#width_range = [8, 0, 20]
		width_range = [6, 0, 25]
		#cb_width_range = [6, 2, 20]
		cb_width_range = [6, 1, 25]
		cb_normalisation_factor = 5

	c1 = ROOT.TCanvas("c1")

	mcfile = ROOT.TFile(MClocation, "READONLY")
	mctree = mcfile.Get("DecayTree;1")
	mctree.SetName("MCtree")
	
	nbins = 300
	masshist = ROOT.TH1F("masshist","Histogram of Lc mass",nbins,mass_range[0],mass_range[1])

	for event in mctree:
		mass = event.lcplus_MM
		masshist.Fill(mass)
	
	mass = ROOT.RooRealVar("mass","Mass",mass_range[0],mass_range[1],"MeV/c^{2}")
#Here is where the different fit shapes are implemented with their various parameters

	if shape == "GaussCB":
		gauss_mean  = ROOT.RooRealVar("gauss_mean","Mean",peak_range[0], peak_range[1], peak_range[2])
		gauss_width = ROOT.RooRealVar("gauss_width","Width",width_range[0], width_range[1], width_range[2])
		myGauss     = ROOT.RooGaussian("myGauss","Gaussian", mass, gauss_mean, gauss_width)

		cb_width    = ROOT.RooRealVar("cb_width","CB Width",cb_width_range[0], cb_width_range[1], cb_width_range[2])
		cb_alpha    = ROOT.RooRealVar("cb_alpha","Exp.const",cb_alpha_range[0], cb_alpha_range[1], cb_alpha_range[2])
		cb_n        = ROOT.RooRealVar("cb_n","Exp.crossover",cb_n_range[0], cb_n_range[1], cb_n_range[2])

		myCB        = ROOT.RooCBShape("myCB","Crystal Ball", mass, gauss_mean, cb_width, cb_alpha, cb_n)

		if particle == "Lc":
			gauss_Norm  = ROOT.RooRealVar("gauss_Norm","Gauss Yield", mctree.GetEntries()/nbins * 6, 0, mctree.GetEntries() * 4)
			cb_Norm     = ROOT.RooRealVar("cb_Norm","CB Yield", mctree.GetEntries()/nbins * 6, 0, mctree.GetEntries() * 4)
		elif particle == "Xic":
			gauss_Norm  = ROOT.RooRealVar("gauss_Norm","Gauss Yield", mctree.GetEntries()/nbins * 3, 0, mctree.GetEntries() * 2)
			cb_Norm     = ROOT.RooRealVar("cb_Norm","CB Yield", mctree.GetEntries()/nbins * 3, 0, mctree.GetEntries() * 2)
			
		Actual_signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(myGauss,myCB), ROOT.RooArgList(gauss_Norm, cb_Norm) )


	elif shape == "Bukin":

		Bukin_Xp = ROOT.RooRealVar("Bukin_Xp", "Peak position", peak_range[0], peak_range[1], peak_range[2])
		Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width", width_range[0], width_range[1], width_range[2])
		Bukin_xi = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter", Bukin_xi_range[0], Bukin_xi_range[1], Bukin_xi_range[2])
		Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail", Bukin_rho1_range[0], Bukin_rho1_range[1], Bukin_rho1_range[2])
		Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", Bukin_rho2_range[0], Bukin_rho2_range[1], Bukin_rho2_range[2])

		Bukin_PDF = ROOT.RooBukinPdf("Bukin_PDF", "Bukin shape", mass, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)

		Bukin_Norm = ROOT.RooRealVar("Bukin_Norm", "Bukin Yield", mctree.GetEntries()/nbins * 3/normalisation_factor, 0, mctree.GetEntries() * 2)
		#RooExtendPdf is used to include the normalisation to the desired shape
		Actual_signalshape = ROOT.RooExtendPdf("Actual_signalshape", "Signal shape", Bukin_PDF, Bukin_Norm)
		Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", mctree.GetEntries()/nbins * 3/normalisation_factor, 0, mctree.GetEntries() * 3)

	if Data == True:
		#Here is where the background shape is defined and added to the overall shape to fit the data

		exponential = ROOT.RooRealVar("exponential","C", exponential_range[0], exponential_range[1], exponential_range[2])
		myexponential = ROOT.RooExponential("myexponential","Exponential", mass, exponential)

		exponential_Norm  = ROOT.RooRealVar("exponential_Norm","Exponential Yield", mctree.GetEntries()/nbins * 3/exponential_normalisation_factor, 0, mctree.GetEntries() * 2)

		signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

		masshist_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), masshist)

	elif Data == False:
		#If it is not data, the overall shape is given only by the signal shape which modules real data
		signalshape = Actual_signalshape
		masshist_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), masshist)

	


#Fit the data using the desired shape
	fitresult = signalshape.fitTo(masshist_RooFit)
	frame = mass.frame()
	masshist_RooFit.plotOn(frame)
	signalshape.plotOn(frame)

	if Data == True:
	#Plot the data component of the shape and the background one separately to see more clearly
		signalshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2))
		signalshape.plotOn(frame, ROOT.RooFit.Components("myexponential"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
	elif shape == "GaussCB":
		signalshape.plotOn(frame, ROOT.RooFit.Components("myGauss"),ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2)) 
		signalshape.plotOn(frame, ROOT.RooFit.Components("myCB"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))
	
	signalshape.paramOn(frame, ROOT.RooFit.Layout(0.56,0.9,0.9))
	frame.SetTitle(str(i) + "_" + j + "_" + filename)
	frame.Draw()

	#Get the parameters resulting from the fit
	signal_yield = gauss_Norm.getValV() + cb_Norm.getValV() 
	signal_error = gauss_Norm.getError() + cb_Norm.getError()
	chi2ndf = frame.chiSquare()


	if shape == "Bukin":
		mainDict[i][j][filename]={
			"yield_val" : signal_yield,
			"yield_err" : signal_error,
			"chi2ndf" : chi2ndf,
			"Bukin_Xp_val" : Bukin_Xp.getValV(),
			"Bukin_Xp_err" : Bukin_Xp.getError(),
			"Bukin_Sigp_val" : Bukin_Sigp.getValV(),
			"Bukin_Sigp_err" : Bukin_Sigp.getError(),
			"Bukin_xi_val" : Bukin_xi.getValV(),
			"Bukin_xi_err" : Bukin_xi.getError(),
			"Bukin_rho1_val" : Bukin_rho1.getValV(),
			"Bukin_rho1_err" : Bukin_rho1.getError(),
			"Bukin_rho2_val" : Bukin_rho2.getValV(),
			"Bukin_rho2_err" : Bukin_rho2.getError()
		}

	if shape == "GaussCB":
		mainDict[i][j][filename]={
			"yield_val" : signal_yield,
			"yield_err" : signal_error,
			"chi2ndf" : chi2ndf,
			"gauss_mean_val" : gauss_mean.getValV(),
			"gauss_mean_err" : gauss_mean.getError(),
			"gauss_width_val" : gauss_width.getValV(),
			"gauss_width_err" : gauss_width.getError(),
			"CB_width_val" : cb_width.getValV(),
			"CB_width_err" : cb_width.getError(),
			"CB_alpha_val" : cb_alpha.getValV(),
			"CB_alpha_err" : cb_alpha.getError(),
			"CB_n_val" : cb_n.getValV(),
			"CB_n_err" : cb_n.getError()
		}

	if Pull == True:

		# Here is where the pull histogram is defined as well as the pads of the canvas

		pullhist = frame.pullHist()

		cpull = ROOT.TCanvas("cpull","cpull",600,700)
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
		frame.SetTitle(shape + "mass fit of " + particle)
		frame.Draw()

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

		cpull.cd()
		pullpad1.Draw()
		pullpad2.Draw()
		cpull.Update()
		cpull.Draw()

	#PDF CREATION#
	strName = "./PDF_output/"+ str(i) + "_" + j + "_" + filename + ".pdf"
	c1.SaveAs(strName)
  
######### JUST AS ARCHIVE OF THE PREVIOUS VERSION - TO BE DELETED AFTER DEVELOPMENT #############

# def graphing(MClocation, filename, mainDict, i, j):
	# c1 = ROOT.TCanvas("c1", filename,800,500)

	# mcfile = ROOT.TFile(MClocation, "READONLY")
	# mctree = mcfile.Get("DecayTree;1")
	# mctree.SetName("MCtree")

	# nbins = 200
	# massrange = [2240,2340] 
	# masshist = ROOT.TH1F("masshist","Histogram of Lc mass",nbins,massrange[0],massrange[1])

	# for event in mctree :
		# mass = event.lcplus_MM
		# masshist.Fill( mass )

	# #masshist.GetXaxis().SetTitle("M(B_{s}^{0}) [MeV/c^{2}]")
	# #masshist.GetYaxis().SetTitle("Number of events")


	# mass        = ROOT.RooRealVar("mass","Mass",massrange[0],massrange[1],"MeV/c^{2}")

	# gauss_mean  = ROOT.RooRealVar("gauss_mean","Mean",2289,2260,2320)
	# gauss_width = ROOT.RooRealVar("gauss_width","Width",6,4,20)
	# myGauss     = ROOT.RooGaussian("myGauss","Gaussian", mass, gauss_mean, gauss_width)

	# cb_width    = ROOT.RooRealVar("cb_width","CB Width",17,8,50)
	# cb_alpha    = ROOT.RooRealVar("cb_alpha","Exp.const",1.0,0.0,5.0)
	# cb_n        = ROOT.RooRealVar("cb_n","Exp.crossover",1.0,0.0,15.0)

	# myCB        = ROOT.RooCBShape("myCB","Crystal Ball", mass, gauss_mean, cb_width, cb_alpha, cb_n)

	# gauss_Norm  = ROOT.RooRealVar("gauss_Norm","Gauss Yield", mctree.GetEntries()/nbins * 6, 0, mctree.GetEntries() * 4)
	# cb_Norm     = ROOT.RooRealVar("cb_Norm","CB Yield", mctree.GetEntries()/nbins * 6, 0, mctree.GetEntries() * 4)

	# signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(myGauss,myCB), ROOT.RooArgList(gauss_Norm, cb_Norm) )

	# masshist_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), masshist)

	# fitresult = signalshape.fitTo(masshist_RooFit)

	# mainFrame = mass.frame()
	# masshist_RooFit.plotOn(mainFrame)
	# signalshape.plotOn(mainFrame)

	# signal_yield = gauss_Norm.getValV() + cb_Norm.getValV() 
	# signal_error = gauss_Norm.getError() + cb_Norm.getError() 

	# chi2ndf = mainFrame.chiSquare()

	# signalshape.plotOn(mainFrame, ROOT.RooFit.Components("myGauss"),ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2)) 

	# signalshape.plotOn(mainFrame, ROOT.RooFit.Components("myCB"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2)) 

	# print("N(Lc) = %.0f +- %.0f"%(signal_yield,signal_error))
	# print("chi2/ndf = " + str(chi2ndf))

	# signalshape.paramOn(mainFrame, ROOT.RooFit.Layout(0.56,0.9,0.9))
	
	# mainFrame.SetTitle(str(i) + "_" + j + "_" + filename)
	
	# #APPARENTLY NECESSARY FOR THE PDF GENERATION#
	# mainFrame.Draw()
	
	# #PDF CREATION#
	# strName = "./PDF_output/"+ str(i) + "_" + j + "_" + filename + ".pdf"
	# c1.SaveAs(strName)
	
	# #FOR THE OUTPUT OF ROOT FILE, UNCOMMENT ONLY IF THERE IS A FOLDER "ROOT_output" 
	# #f = ROOT.TFile("./ROOT_output/rootFileOutput.root","UPDATE")
	# #mainFrame.Write("mainFrame"+filename)
	# #f.Close()
		
	# #DICT CREATION#
	# mainDict[i][j][filename]={
		# "N(Lc)_yield" : signal_yield,
		# "N(Lc)_error" : signal_error,
		# "chi2/ndf" : chi2ndf,
		# "gauss_mean_val" : gauss_mean.getValV(),
		# "gauss_mean_err" : gauss_mean.getError(),
		# "gauss_width_val" : gauss_width.getValV(),
		# "gauss_width_err" : gauss_width.getError()
	# }
	

if __name__ == '__main__':
    main()
