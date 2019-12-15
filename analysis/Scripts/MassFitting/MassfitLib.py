import ROOT, os

#This is a function that returns the wanted path to use in the below Shape_fit_fullPath
#as the fullPath variable. BasePath variable is the place you store the folders name in the style year_MagPol
#For the other variables, it is just easy to make arrays containing the years an magPols
#of interest and loop over them (see MainProgram.py for an example)
def pathFinder(basePath, year, magPol, filename):
	if basePath[-1] != '/':
		fullPath = basePath + '/' + str(year) + "_" + magPol + "/bins/" + filename
	else :
		fullPath = basePath + str(year) + "_" + magPol + "/bins/" + filename
		
	return fullPath

#You just need to give the full path of the data file, the function will parse the important 
#information from it it is important that the data file is arranged in a structure like this:
#   .../year_MagPol/bins/file.root
def shapeFit(shape,fittingDict,fullPath, PDF = True):
	
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH

	parsePath = fullPath.split('/')
	filename = parsePath[-1]
	parseFName =  filename.split('_')
	parseFolder = parsePath[-3].split('_')
	year = parseFolder[0]
	magPol = parseFolder[1]
	particle = parseFName[0]

	fullname = year + "_" + magPol + "_" + filename

	mcfile = ROOT.TFile(fullPath, "READONLY")
	mctree = mcfile.Get("DecayTree")
	mctree.SetName("MCtree")
	
	return fit(mctree, shape, fittingDict, fullname, particle, PDF)
	
#wantedBin represents the type to combine ("both", "y" or "pt")
#This script passes through all the folders and depending on the chosen wantedBin param
#will combine the the bins in each year separately (MagUp and MagDown are donetogether)
def combYPTbinShapeFit(year,shape,fittingDict,path, wantedBin = "both", PDF = True):
	paramDict = {}
	magPol = ["MagUp", "MagDown"]
	
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH

	y = []
	pt = []
	for pol in magPol:
		for filename in os.listdir(path + str(year) + "_" + pol + "/bins/"):
			parseName = filename.split('_')
			if parseName[2] not in y:
				y.append(parseName[2])
			if parseName[3] not in pt:
				pt.append(parseName[3])
				
	paramDict["yBins"] = y
	paramDict["ptBins"] = pt

	if(wantedBin == "both" or wantedBin == "y"):	
		for binY in y:		
			treeYlc = ROOT.TChain("DecayTree")
			treeYxic = ROOT.TChain("DecayTree")
			added = 0
			for pol in magPol:
				for filename in os.listdir(path + str(year) + "_" + pol + "/bins/"):
					parseName = filename.split('_')
					if (parseName[0] == "Lc" and parseName[2] == binY):
						treeYlc.Add(path + str(year) + "_" + pol + "/bins/" + filename)
						added += 1
			if added > 0:
				paramDict[binY + "_Lc"] = fit(treeYlc, shape, fittingDict, "Combined_" + "Lc" + '_' + str(year) + '_' + binY, "Lc")
			
			added = 0
			for pol in magPol:
				for filename in os.listdir(path + str(year) + "_" + pol + "/bins/"):
					parseName = filename.split('_')
					if (parseName[0] == "Xic" and parseName[2] == binY):
						treeYxic.Add(path + str(year) + "_" + pol + "/bins/" + filename)
						added += 1
			if added > 0:
				paramDict[binY + "_Xic"] = fit(treeYxic, shape, fittingDict, "Combined_" + "Xic" + '_' + str(year) + '_' + binY, "Xic")
				
	if(wantedBin == "both" or wantedBin == "pt"):
		for binPT in pt:
			treePTlc = ROOT.TChain("DecayTree")
			treePTxic = ROOT.TChain("DecayTree")
			added = 0
			for pol in magPol:
				for filename in os.listdir(path + str(year) + "_" + pol + "/bins/"):
					parseName = filename.split('_')
					if (parseName[0] == "Lc" and parseName[3] == binPT):
						treePTlc.Add(path + str(year) + "_" + pol + "/bins/" + filename)
						added += 1
			if added > 0:
				paramDict[binPT + "_Lc"] = fit(treePTlc, shape, fittingDict, "Combined_" + "Lc" + '_' + str(year) + '_' + binPT, "Lc")
			
			added = 0
			for pol in magPol:
				for filename in os.listdir(path + str(year) + "_" + pol + "/bins/"):
					parseName = filename.split('_')
					if (parseName[0] == "Xic" and parseName[3] == binPT):
						treePTxic.Add(path + str(year) + "_" + pol + "/bins/" + filename)
						added += 1
			if added > 0:
				paramDict[binPT + "_Xic"] = fit(treePTxic, shape, fittingDict, "Combined_" + "Xic" + '_' + str(year) + '_' + binPT, "Xic")

	return paramDict

#Assembles all files for a specific particle per year and fits it, and outputs a PDF file.
#returns a dictionary with the fitting parameters and yields
def yearTotalShapeFit(year,shape,fittingDict,path, PDF = True):
	paramDict = {}
	magPol = ["MagUp", "MagDown"]
	
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH
	
	treeLc = ROOT.TChain("DecayTree")
	treeXic = ROOT.TChain("DecayTree")
	
	for pol in magPol:
		for filename in os.listdir(path + str(year) + "_" + pol + "/bins/"):
			parseName = filename.split('_')
			if parseName[0] == "Xic":
				treeXic.Add(path + str(year) + "_" + pol + "/bins/" + filename)
	paramDict["Xic"] = fit(treeXic, shape, fittingDict, "Total" + "_" + str(year) + '_' + "Xic", "Xic")
	
	for pol in magPol:
		for filename in os.listdir(path + str(year) + "_" + pol + "/bins/"):
			parseName = filename.split('_')
			if parseName[0] == "Lc":
				treeLc.Add(path + str(year) + "_" + pol + "/bins/" + filename)
	paramDict["Lc"] = fit(treeLc, shape, fittingDict, "Total" + "_" + str(year) + '_' + "Lc", "Lc")
	
	return paramDict

		
	
	
def fit(mctree, shape, fittingDict, fullname, particle, PDF=True):
	
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

		combined_Norm = ROOT.RooRealVar("combined_Norm","Normalization for gaussCB", 0.5,0,1)
		
		Actual_signalshape = ROOT.RooAddPdf ("Actual_signalshape", "Shape of the interesting events", myGauss, myCB, combined_Norm)
		Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", mctree.GetEntries()/nbins * 3/normalisation_factor, 0, mctree.GetEntries() * 3)

		fullshape = ROOT.RooAddPdf("fullshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

	
	masshist_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), masshist)

	#Fit the data using the desired shape
	fitresult = fullshape.fitTo(masshist_RooFit)
	frame = mass.frame()
	masshist_RooFit.plotOn(frame)
	fullshape.plotOn(frame)
	
	#Get the parameters resulting from the fit
	signal_yield = Actual_signalshape_Norm.getValV()
	signal_error = Actual_signalshape_Norm.getError()
	chi2ndf = frame.chiSquare()
	
	#fullshape.paramOn(frame, ROOT.RooFit.Layout(0.56,0.9,0.9))
	frame.SetTitle(fullname + " - chi2ndf : " + str(chi2ndf))

	pullhist = frame.pullHist()
	
	#Plot the data component of the shape and the background one separately to see more clearly
	fullshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"),ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(2))
	fullshape.plotOn(frame, ROOT.RooFit.Components("myexponential"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))

	frame.Draw()

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
	if PDF == True:
		strName = "./PDF_output/"+ fullname + ".pdf"
		c1.SaveAs(strName)	
	
	masshist.Delete()
	ROOT.gDirectory.Delete("mymasshist")
	
	return mainDict
