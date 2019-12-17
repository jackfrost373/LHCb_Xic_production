import ROOT, os, math
from array import array
#/home/exultimathule/Code/HonoursProgramme/RatioPlotting

def ratioVy(combBinDict):
	years = [2011,2012,2015,2016,2017,2018]
	
	c1 = ROOT.TCanvas("c1", "Graph of ratio vs. rapidity",1000,900)
	mg = ROOT.TMultiGraph()

	dataDict = {}
	for year in years:
		dataDict[year] = {
			"x" : [],
			"y" : [],
			"ex" : [],
			"ey" : []
			}
		for yBin in combBinDict[year]["yBins"]:
			parsedY = yBin[1:].split("-")
			y = (float(parsedY[1])+float(parsedY[0]))/2
			dataDict[year]["x"].append(y)
			dataDict[year]["y"].append(combBinDict[year][yBin+"_Xic"]["yield_val"]/combBinDict[year][yBin+"_Lc"]["yield_val"])
			dataDict[year]["ex"].append(0)#(float(parsedY[1])-float(parsedY[0]))/2) #This is for the x errors
			dataDict[year]["ey"].append(math.sqrt((combBinDict[year][yBin+"_Xic"]["yield_err"]/combBinDict[year][yBin+"_Xic"]["yield_val"])**2 + (combBinDict[year][yBin+"_Lc"]["yield_err"]/combBinDict[year][yBin+"_Lc"]["yield_val"])**2))
	
	color = 0
	plotColor = [46,40,30,38,14,41]
	
	
	for year in years:
		x = array('f', dataDict[year]["x"])
		y = array('f', dataDict[year]["y"])
		ex = array('f', dataDict[year]["ex"])
		ey = array('f', dataDict[year]["ey"])
		nPoints = len(dataDict[year]["x"])
		gr = ROOT.TGraphErrors(nPoints,x,y,ex,ey)
		gr.SetTitle(str(year))
		gr.SetLineColor(plotColor[color])
		gr.SetLineWidth( 1 )
		gr.SetMarkerColor(plotColor[color])
		gr.SetMarkerStyle( 21 )
		mg.Add(gr)
		
		color+=1
	
	mg.SetTitle("Xic/Lc Ratio vs. Rapidity (y) per Year")
	mg.GetXaxis().SetTitle( 'Rapidity' )
	mg.GetXaxis().SetRangeUser(2.2,4.8)
	mg.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
	mg.GetYaxis().SetRangeUser(0.04,0.33)
	mg.Draw('AL*')
	c1.BuildLegend(.15,.8,.25,.6,"Years")
	c1.Update()		
	c1.Draw()
	c1.SaveAs("RatioVsRapidity.pdf")
	input("Press enter to quit...")

def ratioVpt(combBinDict):
	years = [2011,2012,2015,2016,2017,2018]
	
	c1 = ROOT.TCanvas("c1", "Graph of ratio vs. rapidity",1000,900)
	mg = ROOT.TMultiGraph()

	dataDict = {}
	for year in years:
		dataDict[year] = {
			"x" : [],
			"y" : [],
			"ex" : [],
			"ey" : []
			}
		for ptBin in combBinDict[year]["ptBins"]:
			parsedY = ptBin[2:].split("-")
			bin2 = float(parsedY[1][:-5])
			bin1 = float(parsedY[0])
			xerr = (bin2-bin1)/2
			y = (bin1+bin2)/2
			dataDict[year]["x"].append(y)
			dataDict[year]["y"].append(combBinDict[year][ptBin+"_Xic"]["yield_val"]/combBinDict[year][ptBin+"_Lc"]["yield_val"])
			dataDict[year]["ex"].append(0) #xerr) #This is for the x errors
			dataDict[year]["ey"].append(math.sqrt((combBinDict[year][ptBin+"_Xic"]["yield_err"]/combBinDict[year][ptBin+"_Xic"]["yield_val"])**2 + (combBinDict[year][ptBin+"_Lc"]["yield_err"]/combBinDict[year][ptBin+"_Lc"]["yield_val"])**2))
	
	color = 0
	plotColor = [46,40,30,38,14,41]
	
	
	for year in years:
		dataDict[year]["x"], dataDict[year]["y"], dataDict[year]["ex"], dataDict[year]["ey"] = zip(*sorted(zip(dataDict[year]["x"], dataDict[year]["y"], dataDict[year]["ex"], dataDict[year]["ey"])))
		x = array('f', dataDict[year]["x"])
		y = array('f', dataDict[year]["y"])
		ex = array('f', dataDict[year]["ex"])
		ey = array('f', dataDict[year]["ey"])
		nPoints = len(dataDict[year]["x"])
		gr = ROOT.TGraphErrors(nPoints,x,y,ex,ey)
		gr.SetTitle(str(year))
		gr.SetLineColor(plotColor[color])
		gr.SetLineWidth( 1 )
		gr.SetMarkerColor(plotColor[color])
		gr.SetMarkerStyle( 21 )
		mg.Add(gr)
		
		color+=1
	
	mg.SetTitle("Xic/Lc Ratio vs. Transverse Momentum (y) per Year")
	mg.GetXaxis().SetTitle( 'Transverse Momentum (MeV/c)' )
	mg.GetXaxis().SetRangeUser(3000,18000)
	mg.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
	mg.GetYaxis().SetRangeUser(0.01,0.33)
	mg.Draw('AL*')
	c1.BuildLegend(.15,.8,.25,.6,"Years")
	c1.Update()		
	c1.Draw()
	c1.SaveAs("RatioVsTransverseMomentum.pdf")
	input("Press enter to quit...")

#Less acurate
def ratioVpt_allfiles(autoFitDict):
	years = [2011,2012,2015,2016,2017,2018]
	magPol = ["MagDown","MagUp"]
	ptBins = ['3000-4000', '4000-5000', '5000-6000', '6000-7000', '7000-8000', '8000-10000', '10000-20000']
	
	c1 = ROOT.TCanvas("c1", "Graph of ratio vs. rapidity",1000,900)
	mg = ROOT.TMultiGraph()

	dataDict = {}
	for year in years:
		dataDict[year] = {
			"x" : [3500, 4500, 5500, 6500, 7500, 8500, 15000],
			"ex" : [0,0,0,0,0,0,0],
			"yXc" : [0,0,0,0,0,0,0],
			"eyXc" : [0,0,0,0,0,0,0],
			"yLc" : [0,0,0,0,0,0,0],
			"eyLc" : [0,0,0,0,0,0,0]
			}
		for pol in magPol:
			i = 0
			for ptBin in ptBins:
				for key in autoFitDict[year][pol]:
					if ptBin in key:
						if "Xic" in key:
							dataDict[year]["yXc"][i] += autoFitDict[year][pol][key]["yield_val"]
							dataDict[year]["eyXc"][i] += autoFitDict[year][pol][key]["yield_err"]
						if "Lc" in key:
							dataDict[year]["yLc"][i] += autoFitDict[year][pol][key]["yield_val"]
							dataDict[year]["eyLc"][i] += autoFitDict[year][pol][key]["yield_err"]
				i+=1
	
	color = 0
	plotColor = [46,40,30,38,14,41]
	
	for year in years:
		yArr = []
		eyArr =[]
		for i in range(len(dataDict[year]["x"])):
			yArr.append(dataDict[year]["yXc"][i]/dataDict[year]["yLc"][i])
			eyArr.append(math.sqrt((dataDict[year]["eyXc"][i]/dataDict[year]["yXc"][i])**2+(dataDict[year]["eyLc"][i]/dataDict[year]["yLc"][i])**2))
			 
		x = array('f', dataDict[year]["x"])
		y = array('f', yArr)
		ex = array('f', dataDict[year]["ex"])
		ey = array('f', eyArr)
		nPoints = len(dataDict[year]["x"])
		gr = ROOT.TGraphErrors(nPoints,x,y,ex,ey)
		gr.SetTitle(str(year))
		gr.SetLineColor(plotColor[color])
		gr.SetLineWidth( 1 )
		gr.SetMarkerColor(plotColor[color])
		gr.SetMarkerStyle( 21 )
		mg.Add(gr)
		
		color+=1
	
	mg.SetTitle("Xic/Lc Ratio vs. Transverse Momentum (y) per Year")
	mg.GetXaxis().SetTitle( 'Transverse Momentum (MeV/c)' )
	mg.GetXaxis().SetRangeUser(3000,18000)
	mg.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
	#mg.GetYaxis().SetRangeUser(0.01,0.33)
	mg.Draw('AL*')
	c1.BuildLegend(.15,.8,.25,.6,"Years")
	c1.Update()		
	c1.Draw()
	c1.SaveAs("RatioVsTransverseMomentum_allFiles.pdf")
	input("Press enter to quit...")
	
def yieldVyear(yearTotDict):
	years = [2011,2012,2015,2016,2017,2018]
	XicYield = []
	XicYieldEr = []
	LcYield = []
	LcYieldEr = []
	
	c1 = ROOT.TCanvas("c1", "Graph of ratio vs. rapidity",1000,900)
	c1.SetLogy()
	mg = ROOT.TMultiGraph()
	
	for year in years:
		XicYield.append(yearTotDict[year]["Xic"]["yield_val"])
		XicYieldEr.append(yearTotDict[year]["Xic"]["yield_err"])
		LcYield.append(yearTotDict[year]["Lc"]["yield_val"])
		LcYieldEr.append(yearTotDict[year]["Lc"]["yield_err"])
	
	nPoints = len(years)
	x = array('f', years)
	ex = array('f', [0,0,0,0,0,0,0])
	yXi = array('f', XicYield)
	eyXi = array('f', XicYieldEr)
	yL = array('f', LcYield)
	eyL = array('f', LcYieldEr)
	
	gr1 = ROOT.TGraphErrors(nPoints,x,yXi,ex,eyXi)
	gr1.SetTitle("Xic")
	gr1.SetLineColor(40)
	gr1.SetLineWidth( 1 )
	gr1.SetMarkerColor(40)
	gr1.SetMarkerStyle( 21 )
	mg.Add(gr1)
	
	gr2 = ROOT.TGraphErrors(nPoints,x,yL,ex,eyL)
	gr2.SetTitle("Lc")
	gr2.SetLineColor(46)
	gr2.SetLineWidth( 1 )
	gr2.SetMarkerColor(46)
	gr2.SetMarkerStyle( 21 )
	mg.Add(gr2)
		
	mg.SetTitle("Xic and Lc Yield vs. Year")
	mg.GetXaxis().SetTitle( 'Year' )
	mg.GetYaxis().SetTitle( 'Xic,Lc Yields' )
	mg.GetXaxis().SetRangeUser(2009,2019)
	mg.GetYaxis().SetRangeUser(100000,100000000)
	mg.Draw('AL*')
	c1.BuildLegend(.15,.8,.25,.7,"Particles")
	c1.Update()		
	c1.Draw()
	c1.SaveAs("YieldVYear.pdf")
	input("Press enter to quit...")
		
def ratioVyear(yearTotDict):
	
	years = [2011,2012,2015,2016,2017,2018]
	ratio = []
	ratioErr = []
	
	c1 = ROOT.TCanvas("c1", "Graph of ratio vs. rapidity",1000,900)

	for year in years:
		ratio.append(yearTotDict[year]["Xic"]["yield_val"]/yearTotDict[year]["Lc"]["yield_val"])
		ratioErr.append((yearTotDict[year]["Xic"]["yield_err"]/yearTotDict[year]["Xic"]["yield_val"])**2+(yearTotDict[year]["Lc"]["yield_err"]/yearTotDict[year]["Lc"]["yield_val"])**2)
	
	nPoints = len(years)
	x = array('f', years)
	ex = array('f', [0,0,0,0,0,0,0])
	y = array('f', ratio)
	ey = array('f', ratioErr)
	
	gr = ROOT.TGraphErrors(nPoints,x,y,ex,ey)
	gr.SetTitle("Xic")
	gr.SetLineColor(40)
	gr.SetLineWidth( 1 )
	gr.SetMarkerColor(40)
	gr.SetMarkerStyle( 21 )
	
	gr.SetTitle("Xic/Lc Ratios vs. Year")
	gr.GetXaxis().SetTitle( 'Year' )
	gr.GetYaxis().SetTitle( 'Xic/Lc Ratios' )
	gr.GetXaxis().SetRangeUser(2009,2019)
	gr.Draw('AL*')
	leg = ROOT.TLegend(.15,.8,.40,.7,"Ratio")
	leg.AddEntry("gr","Xic/Lc Yield Ratio","AL*")
	leg.SetTextSize(0.03)
	leg.Draw()
	c1.Update()		
	c1.Draw()
	c1.SaveAs("RatioVYear.pdf")
	input("Press enter to quit...")
