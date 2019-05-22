import ROOT, os, Imports
from ROOT import TCanvas, TH1

#definition of the function that defines the shape and fits. The arguments are as follows:
#shape: it is a string used to indicate which particular signal shape is wanted to fit the data
#file is the tree file (.root format) containing the data that is used
#particle is a string which indicates which of the 2 particles the data corresponds to. Based on this choice, parameters are chosen such as the location of the mass peak and the width of the shape, etc...
#ybin and ptbin are simply a list of 2 elements used to name the output files
#Data is a boolean variable which is used to determine whether the data contained in the file is actual data or if it is Monte Carlo. If it is actual data (i.e. if Data == True), then an exponential shape is added to module the background
#Pull is a boolean variable. If Pull == True, an additional pull plot is added in the figure plotted. Otherwise, no pull plot is added
def Shape_fit(shape, file, particle, ybin, ptbin, Data=True, Pull=False, user):

    #here is a list of the parameters used to define the shapes. A difference is made between Lc and Xic. This difference was found necessary while carrying out tests. All the parameters starting with "Bukin" are used for the Bukin shape. The ones starting with "cb" are used for the crystal ball, the ones starting with "gauss" for the gaussian, the ones starting with "exponential" are used for the exponential background shape and the rest are other general parameters
    directory = Imports.getDirectory(user)
    
    Bukin_xi_range =[0, -1, 1]
    Bukin_rho1_range = [0, -1, 1]
    Bukin_rho2_range = [0, -1, 1]
    #cb_alpha_range = [1, 0, 5]
    cb_alpha_range = [1, 0, 7]
    #cb_n_range = [1, 0, 15]
    cb_n_range = [1, 0, 20]
    gauss_normalisation_factor = 1
    
    if particle == "Lc":
        mass_range = [2240, 2340]
        #peak_range = [2288, 2280, 2290]
        peak_range = [2288, 2270, 2300]
        normalisation_factor = 6
        gauss_normalisation_factor = 10
        exponential_normalisation_factor = 1
        #exponential_range = [0.001, -0.2, 0.2]
        exponential_range = [0.001, -0.5, 0.5]
        #width_range = [2, 0, 10]
        width_range = [2, 0, 15]
        #cb_width_range = [2, 0, 15]
        cb_width_range = [2, 0, 20]
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
        width_range = [8, 0, 25]
        #cb_width_range = [6, 2, 20]
        cb_width_range = [6, 1, 25]
        cb_normalisation_factor = 5


    tree = file


    c1 = ROOT.TCanvas("c1")
    
    #These are dummy histograms uniquely used for the legend. Ideally, these should be removed.

    histogram1 = ROOT.TH1F("histogram1", "hist 1", 300, 2240, 2340)
    histogram2 = ROOT.TH1F("histogram2", "hist 1", 300, 2240, 2340)
    histogram1.SetLineColor(8)
    histogram1.SetLineStyle(2)
    histogram2.SetLineColor(46)
    histogram2.SetLineStyle(2)
    masshist = ROOT.TH1F("masshist", "Histogram of" + particle[:-1] + "_{c} mass", 300, mass_range[0], mass_range[1])
    masshist.GetXaxis().SetTitle("M(" + particle[:-1] + "_{c}^{+}) [MeV/c^{2}]")
    masshist.GetYaxis().SetTitle("Number of events")
    #this is the RooRealVariable for the mass, the independent variable if you will
    mass= ROOT.RooRealVar("mass","Mass",mass_range[0],mass_range[1],"MeV/c^{2}")
    #here is where the number of bins for the histogram is defined
    nbins = 300
    varname = "lcplus_MM"
    #here is where the data from the tree is drawn using the special function tree.Draw(). The drawing of the data depends on the number of bins and the mass range chosen
    tree.Draw(varname+">>masshist("+str(nbins)+","+str(mass_range[0])+","+str(mass_range[1])+")")
    masshist = ROOT.gDirectory.Get("masshist")

    masshist.SetLineColor(4)
    masshist.SetLineWidth(3)

    masshist.Draw()
    
    #Here is where the different fit shapes are implemented with their various parameters

    if shape == "GaussCB":
        #a RooRealVar allows you to fluctuate between a lower and an upper boundary, starting from an initial value which is the first numerical element given to it (e.g. peak_range[0])
        gauss_mean  = ROOT.RooRealVar("gauss_mean","Mean",peak_range[0], peak_range[1], peak_range[2])
        gauss_width = ROOT.RooRealVar("gauss_width","Width",width_range[0], width_range[1], width_range[2])
        myGauss     = ROOT.RooGaussian("myGauss","Gaussian", mass, gauss_mean, gauss_width)

        cb_width = ROOT.RooRealVar("cb_width","CB Width", cb_width_range[0], cb_width_range[1], cb_width_range[2])
        cb_alpha = ROOT.RooRealVar("cb_alpha","Exp.const",cb_alpha_range[0], cb_alpha_range[1], cb_alpha_range[2])
        cb_n = ROOT.RooRealVar("cb_n","Exp.crossover",cb_n_range[0], cb_n_range[1], cb_n_range[2])
        myCB        = ROOT.RooCBShape("myCB","Crystal Ball", mass, gauss_mean, cb_width, cb_alpha, cb_n)
        
        
        gauss_Norm  = ROOT.RooRealVar("gauss_Norm","Gauss Yield", tree.GetEntries()/nbins * 3, 0, tree.GetEntries() * 2)
        cb_Norm     = ROOT.RooRealVar("cb_Norm","CB Yield", tree.GetEntries()/nbins * 3/cb_normalisation_factor, 0, tree.GetEntries() * 2)
        
        #Using RooAddPfd multiple shapes can be added together to form the overall signal shape
        Actual_signalshape = ROOT.RooAddPdf ("Actual_signalshape", "Shape of the interesting events", ROOT.RooArgList(myGauss, myCB), ROOT.RooArgList(gauss_Norm, cb_Norm))
        Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", tree.GetEntries()/nbins * 3/gauss_normalisation_factor, 0, tree.GetEntries() * 2)

    elif shape == "Bukin":
    
        Bukin_Xp = ROOT.RooRealVar("Bukin_Xp", "Peak position", peak_range[0], peak_range[1], peak_range[2])
        Bukin_Sigp = ROOT.RooRealVar("Bukin_Sigp", "Peak width", width_range[0], width_range[1], width_range[2])
        Bukin_xi = ROOT.RooRealVar("Bukin_xi", "Peak asymmetry parameter", Bukin_xi_range[0], Bukin_xi_range[1], Bukin_xi_range[2])
        Bukin_rho1 = ROOT.RooRealVar("Bukin_rho1", "Parameter of the left tail", Bukin_rho1_range[0], Bukin_rho1_range[1], Bukin_rho1_range[2])
        Bukin_rho2 = ROOT.RooRealVar("Bukin_rho2", "Parameter of the right tail", Bukin_rho2_range[0], Bukin_rho2_range[1], Bukin_rho2_range[2])

        Bukin_PDF = ROOT.RooBukinPdf("Bukin_PDF", "Bukin shape", mass, Bukin_Xp, Bukin_Sigp, Bukin_xi, Bukin_rho1, Bukin_rho2)

        Bukin_Norm = ROOT.RooRealVar("Bukin_Norm", "Bukin Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 2)
        #RooExtendPdf is used to include the normalisation to the desired shape
        Actual_signalshape = ROOT.RooExtendPdf("Actual_signalshape", "Signal shape", Bukin_PDF, Bukin_Norm)
        Actual_signalshape_Norm = ROOT.RooRealVar("Actual_signalshape_Norm","Signal Yield", tree.GetEntries()/nbins * 3/normalisation_factor, 0, tree.GetEntries() * 3)

    if Data == True:
        #Here is where the background shape is defined and added to the overall shape to fit the data
        
        exponential = ROOT.RooRealVar("exponential","C", exponential_range[0], exponential_range[1], exponential_range[2])
        myexponential = ROOT.RooExponential("myexponential","Exponential", mass, exponential)

        exponential_Norm  = ROOT.RooRealVar("exponential_Norm","Exponential Yield", tree.GetEntries()/nbins * 3/exponential_normalisation_factor, 0, tree.GetEntries() * 2)

        signalshape = ROOT.RooAddPdf("signalshape","Signal shape", ROOT.RooArgList(Actual_signalshape, myexponential), ROOT.RooArgList(Actual_signalshape_Norm, exponential_Norm) )

        masshist_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), masshist)

    elif Data == False:
        #If it is not data, the overall shape is given only by the signal shape which modules real data

        signalshape = Actual_signalshape


    masshist_RooFit = ROOT.RooDataHist("masshist_RooFit","masshist RooFit", ROOT.RooArgList(mass), masshist)

#generate a frame and plot data and shape on it without fitting
    frame = mass.frame()
    masshist_RooFit.plotOn(frame)
    signalshape.plotOn(frame)
    frame.Draw()
#Fit the data using the desired shape
    fitresult = signalshape.fitTo(masshist_RooFit)
    frame = mass.frame()
    masshist_RooFit.plotOn(frame)

    if Data == True:
        #Plot the data component of the shape and the background one separately to see more clearly
        signalshape.plotOn(frame, ROOT.RooFit.Components("Actual_signalshape"), ROOT.RooFit.LineColor(8), ROOT.RooFit.LineStyle(2))
        signalshape.plotOn(frame, ROOT.RooFit.Components("myexponential"), ROOT.RooFit.LineColor(46), ROOT.RooFit.LineStyle(2))

    signalshape.plotOn(frame)
    frame.SetTitle(shape + " mass fit of " + particle)
    frame.GetYaxis().SetTitle("Number of events")
    frame.Draw()
    fitresult = signalshape.fitTo(masshist_RooFit)

#Get the interesting parameters resulting from the fit
    signal_yield = Actual_signalshape_Norm.getValV() #this is the number of interesting events
    signal_error = Actual_signalshape_Norm.getError() #error on that number
    chi2ndf = frame.chiSquare() #chi2/ndf is used to determine the quality of the fit

#construnct the legend and the name of the graph
    leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
    #leg.SetHeader("Legend")
    leg.AddEntry( histogram1, "Signal shape", "l")
    leg.AddEntry(histogram2, "Background", "l")
    leg.Draw("same")
    graph_name = (particle + shape + "_Mass_Fit_y{0}-{1}_pt{2}-{3}.pdf".format(ybin[0],ybin[1],ptbin[0],ptbin[1]))
    filepath = (directory)
    fullpath = os.path.join(filepath, graph_name)
    c1.SaveAs(fullpath) # the canvas is saved into the location given by fullpath

#The following are used to obtain a string which indicates the values of the various free parameters used to construct the shape and the relative errors on those parameters which is then summed into the overall results string
    if shape == "Bukin":

        parameter_String = "Bukin Xp: {0} +/- {1}, Bukin Sigp: {2} +/- {3}, Bukin xi: {4} +/- {5}, Bukin rho1: {6} +/- {7}, Bukin rho2: {8} +/- {9} \n ".format(Bukin_Xp.getValV(),Bukin_Xp.getError(), Bukin_Sigp.getValV(), Bukin_Sigp.getError(), Bukin_xi.getValV(), Bukin_xi.getError(), Bukin_rho1.getValV(), Bukin_rho1.getError(), Bukin_rho2.getValV(), Bukin_rho2.getError())

    if shape == "GaussCB":
    
        parameter_String = shape + ": Gauss mean: {0} +/- {1}, Gauss width: {2} +/- {3}, CB width: {4} +/- {5}, CB alpha: {6} +/- {7}, CB n: {8} +/- {9} \n ".format(gauss_mean.getValV(),gauss_mean.getError(), gauss_width.getValV(), gauss_width.getError(), cb_width.getValV(), cb_width.getError(), cb_alpha.getValV(), cb_alpha.getError(), cb_n.getValV(), cb_n.getError())
#an overall result string is generated which includes all of the interesting information that can be obtained from the fitting process
    results = particle +  ": y:{0}-{1} pt:{2}-{3} : {4} +/- {5}  with Chi2/ndf = {6} \n parameter list: \n".format(ybin[0],ybin[1],ptbin[0],ptbin[1],signal_yield, signal_error, chi2ndf) + parameter_String
    
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
        leg.Draw("same")
        cpull.Update()
        cpull.Draw()


        graph_name = (particle + shape + "Pull_Mass_Fit_y{0}-{1}_pt{2}-{3}.pdf".format(ybin[0],ybin[1],ptbin[0],ptbin[1]))
        filepath = (directory)
        fullpath = os.path.join(filepath, graph_name)
        cpull.SaveAs(fullpath)


    
#the overall results string is the output of the function so that it can be printed into a text file and analysed later on
    
    return results

