import ROOT, os

#The year and the magPol are just there to make the pdf files name clearer and avoid duplicate names
def Shape_fit(shape, fileLocation, year, magPol, filename, particle, fittingDict):
	
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH

	fullname = str(year) + "_" + magPol + "_" + filename
	
	if fileLocation[-1] != '/':
		fullPath = fileLocation + '/' + filename
	else:
		fullPath = fileLocation + filename
	
	if shape == "GaussCB":
		if fullname in fittingDict["GaussCB"][particle]:
			mass_range = fittingDict["GaussCB"][particle]["fullname"]["mass_range"]
			peak_range = fittingDict["GaussCB"][particle]["fullname"]["peak_range"]
			
			normalisation_factor = fittingDict["GaussCB"][particle]["fullname"]["normalisation_factor"]
			gauss_normalisation_factor = fittingDict["GaussCB"][particle]["fullname"]["gauss_normalisation_factor"]
			exponential_normalisation_factor = fittingDict["GaussCB"][particle]["fullname"]["exponential_normalisation_factor"]
			
			exponential_range = fittingDict["GaussCB"][particle]["fullname"]["exponential_range"]
			
			width_range = fittingDict["GaussCB"][particle]["fullname"]["width_range"]
			
			cb_width_range = fittingDict["GaussCB"][particle]["fullname"]["cb_width_range"]
			cb_alpha_range = fittingDict["GaussCB"][particle]["fullname"]["cb_alpha_range"]
			cb_n_range = fittingDict["GaussCB"][particle]["fullname"]["cb_n_range"]
			cb_normalisation_factor = fittingDict["GaussCB"][particle]["fullname"]["cb_normalisation_factor"]
		else:
			mass_range = fittingDict["GaussCB"][particle]["general"]["mass_range"]
			peak_range = fittingDict["GaussCB"][particle]["general"]["peak_range"]
			
			normalisation_factor = fittingDict["GaussCB"][particle]["general"]["normalisation_factor"]
			gauss_normalisation_factor = fittingDict["GaussCB"][particle]["general"]["gauss_normalisation_factor"]
			exponential_normalisation_factor = fittingDict["GaussCB"][particle]["general"]["exponential_normalisation_factor"]
			
			exponential_range = fittingDict["GaussCB"][particle]["general"]["exponential_range"]
			
			width_range = fittingDict["GaussCB"][particle]["general"]["width_range"]
			
			cb_width_range = fittingDict["GaussCB"][particle]["general"]["cb_width_range"]
			cb_alpha_range = fittingDict["GaussCB"][particle]["general"]["cb_alpha_range"]
			cb_n_range = fittingDict["GaussCB"][particle]["general"]["cb_n_range"]
			cb_normalisation_factor = fittingDict["GaussCB"][particle]["general"]["cb_normalisation_factor"]

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

	mcfile = ROOT.TFile(fullPath, "READONLY")
	mctree = mcfile.Get("DecayTree")
	mctree.SetName("MCtree")
	
	nbins = 150
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
		
		exponential = ROOT.RooRealVar("exponential","C", exponential_range[0], exponential_range[1], exponential_range[2])
		myexponential = ROOT.RooExponential("myexponential","Exponential", mass, exponential)
		exponential_Norm  = ROOT.RooRealVar("exponential_Norm","Exponential Yield", mctree.GetEntries()/nbins * 3/exponential_normalisation_factor, 0, mctree.GetEntries() * 2)

		gauss_Norm  = ROOT.RooRealVar("gauss_Norm","Gauss Yield", mctree.GetEntries()/nbins * 3, 0, mctree.GetEntries() * 2)
		cb_Norm     = ROOT.RooRealVar("cb_Norm","CB Yield", mctree.GetEntries()/nbins * 3/cb_normalisation_factor, 0, mctree.GetEntries() * 2)
		
		Actual_signalshape = ROOT.RooAddPdf ("Actual_signalshape", "Shape of the interesting events", ROOT.RooArgList(myGauss, myCB), ROOT.RooArgList(gauss_Norm, cb_Norm))
		Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", mctree.GetEntries()/nbins * 3/normalisation_factor, 0, mctree.GetEntries() * 3)

		signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

	
	masshist_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), masshist)

	#Fit the data using the desired shape
	fitresult = signalshape.fitTo(masshist_RooFit)
	frame = mass.frame()
	masshist_RooFit.plotOn(frame)
	signalshape.plotOn(frame)
	
	#Get the parameters resulting from the fit
	signal_yield = gauss_Norm.getValV() + cb_Norm.getValV() 
	signal_error = gauss_Norm.getError() + cb_Norm.getError()
	chi2ndf = frame.chiSquare()
	
	#signalshape.paramOn(frame, ROOT.RooFit.Layout(0.56,0.9,0.9))
	frame.SetTitle(fullname + " - chi2ndf : " + str(chi2ndf))

	pullhist = frame.pullHist()
	
	#Plot the data component of the shape and the background one separately to see more clearly
	signalshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"),ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(2))
	signalshape.plotOn(frame, ROOT.RooFit.Components("myexponential"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))

	frame.Draw()
	
	if shape == "Bukin":
		mainDict = {
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
		mainDict = {
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
	strName = "./PDF_output/"+ str(year) + "_" + magPol + "_" + filename + ".pdf"
	c1.SaveAs(strName)
	
	return mainDict
