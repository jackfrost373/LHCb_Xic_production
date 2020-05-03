import sys, getopt, ROOT, math, textwrap
from array import array
import Imports

#TO CHANGE DEPENDING ON WHERE THE DICTS ARE LOCATED!
from Dict_output.combinedFit_DictFile import mainDict as combinedDict
from Dict_output.yearFit_DictFile import mainDict as yearTotDict
from Dict_output.singleFit_DictFile import mainDict as singleDict

#CAN BE CHANGED TO OUTPUT THE 
GRAPH_PATH = "./Graphs/"
years = [2011,2012,2016,2017,2018]

color = 0
plotColor = [46,40,30,38,41]

#Creation of the y and pt bin lists from the imports functions
pt_bin_temp = Imports.getPTbins()
pt_arr = []			#format [3200,4000,5000,6000,7000,8000,10000,20000]
pt_arr_str = []		#format ["3200-4000","4000-5000", ...]
firstLoop = True
for pt in pt_bin_temp:
	if firstLoop:
		pt_arr.append(pt[0])
		firstLoop = False
	pt_arr.append(pt[1])
	pt_arr_str.append("{}-{}".format(pt[0], pt[1]))
	
	
y_bin_temp = Imports.getYbins()
y_arr = []		#format: [2.0,2.5,3.0,3.5,4.0]
y_arr_str = []	#format: ["2.0-2.5","2.5-3.0", ...]
firstLoop = True
for y in y_bin_temp:
	if firstLoop:
		y_arr.append(y[0])
		firstLoop = False
	y_arr.append(y[1])
	y_arr_str.append("{}-{}".format(y[0], y[1]))
	

# CREATES THE DATASET FOR GRAPHING 
y_dataDict = {}
pt_dataDict = {}
for year in years:
	y_dataDict[year] = {
		"x" : [],
		"y" : [],
		"ex" : [],
		"ey" : []
	}

	for points in y_arr_str:
		y_dataDict[year]['x'].append(0)
		y_dataDict[year]['y'].append(0)
		y_dataDict[year]['ex'].append(0)
		y_dataDict[year]['ey'].append(0)

	pt_dataDict[year] = {
		"x" : [],
		"y" : [],
		"ex" : [],
		"ey" : []
	}
	for points in pt_arr_str: #initializes the dataset to zero everywhere
		pt_dataDict[year]['x'].append(0) # => "x" : [0,0,0,0,0,0,0] as theres 7 pt bins
		pt_dataDict[year]['y'].append(0)
		pt_dataDict[year]['ex'].append(0)
		pt_dataDict[year]['ey'].append(0)
    
	for pol in combinedDict[year]:
		i = 0
		for file in sorted(combinedDict[year][pol]):
			if ("ybin" in file) and ("Xic" in file):
				y = (float(file[:-5].split('_')[-1].split('-')[0])+float(file[:-5].split('_')[-1].split('-')[1]))/2
				y_err = (float(file[:-5].split('_')[-1].split('-')[1])-float(file[:-5].split('_')[-1].split('-')[0]))/2
				ratio = combinedDict[year][pol][file]["yield_val"]/combinedDict[year][pol]['Lc'+file[3:]]["yield_val"]
				ratio_err = math.sqrt((combinedDict[year][pol][file]["yield_err"]/combinedDict[year][pol][file]["yield_val"])**2 + (combinedDict[year][pol]['Lc'+file[3:]]["yield_err"]/combinedDict[year][pol]['Lc'+file[3:]]["yield_val"])**2)

				y_dataDict[year]["x"][i] = y
				y_dataDict[year]["y"][i] += ratio
				y_dataDict[year]["ex"][i] = y_err
				if y_dataDict[year]["ey"][i] == 0:
					y_dataDict[year]["ey"][i] += ratio_err
				else:
					y_dataDict[year]["ey"][i] = math.sqrt(y_dataDict[year]["ey"][i]**2 + ratio_err**2)

				i+=1
    
	for pol in combinedDict[year]:
		i = 0
		for file in sorted(combinedDict[year][pol]):
			if ("ptbin" in file) and ("Xic" in file):
				pt = (float(file[:-5].split('_')[-1].split('-')[0])+float(file[:-5].split('_')[-1].split('-')[1]))/2
				pt_err = (float(file[:-5].split('_')[-1].split('-')[1])-float(file[:-5].split('_')[-1].split('-')[0]))/2
				ratio = combinedDict[year][pol][file]["yield_val"]/combinedDict[year][pol]['Lc'+file[3:]]["yield_val"]
				ratio_err = math.sqrt((combinedDict[year][pol][file]["yield_err"]/combinedDict[year][pol][file]["yield_val"])**2 + (combinedDict[year][pol]['Lc'+file[3:]]["yield_err"]/combinedDict[year][pol]['Lc'+file[3:]]["yield_val"])**2)

				pt_dataDict[year]["x"][i] = pt
				pt_dataDict[year]["y"][i] += ratio
				pt_dataDict[year]["ex"][i] = pt_err
				pt_dataDict[year]["ey"][i] += ratio_err

				i+=1



def main(argv):
	
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH FOR ROOT
	
	try:
		opts, args = getopt.getopt(argv,"habcde")
	except getopt.GetoptError:
		print("The arguments are wrong")
		sys.exit(2)
	
	options = []
	arguments = []
	
	for opt,arg in opts:
		options.append(opt)
		arguments.append(arg)
		
	if not options:
		options = ["-a","-b","-c","-d","-e"]
	
	if "-h" in options:
		print(textwrap.dedent("""\
			
			Welcome to the plot.py script.
			
			You need to have a directory/folder called "./Graphs/" in the same directory as you run the script, as the PDF files will be saved there.
			You can always change the script variable GRAPH_PATH to change this.
			Be sure to also have the dictionnary files in "./Dict_output/", as well as the Imports.py library in the same directory as script.
			
			The parameters are
				-h : help
				-a : 2D histograms of each y vs. each pt (one for each year)
				-b : ratio vs. pt (a line for each year)
				-c : ratio vs. y (a line for each year)
				-d : ratio vs. years 
				-e : yield vs. year

			Running with no parameter will output all the graphs at once.
			"""))

		sys.exit()
		
	
	for opt in options:
		if opt == "-a": #2D histograms of each y vs. each pt
			for year in years:
				cA = ROOT.TCanvas( 'cA', 'Dynamic Filling Example', 200, 10, 700, 500 )
				pt_y_ratio = ROOT.TH2F("Yield Ratios","y vs.Pt vs. Xic/Lc Ratio;Transverse Momentum (MeV/c);Rapidity (y)",len(pt_arr_str),array('f',pt_arr),len(y_arr_str),array('f',y_arr))
				pt_y_ratio.SetStats(0)
				
				for pol in singleDict[year]:
					for files in singleDict[year][pol]:
						if ("Xic" in files):
							ratio = singleDict[year][pol][files]["yield_val"]/singleDict[year][pol]['Lc'+files[3:]]["yield_val"]
							y = (float(files[:-5].split('_')[2].split('-')[0])+float(files[:-5].split('_')[2].split('-')[1]))/2
							pt = (float(files[:-5].split('_')[4].split('-')[0])+float(files[:-5].split('_')[4].split('-')[1]))/2
							pt_y_ratio.Fill(pt,y,ratio)
							
				pt_y_ratio.Draw("Colz")
				cA.Draw()
				cA.SaveAs(GRAPH_PATH + str(year)+"_pt_y_Ratio_2D.pdf")
				del cA, pt_y_ratio
			
			
		elif opt == "-b": #ratio vs. pt
			
			cB = ROOT.TCanvas("cB", "Graph of ratio vs. rapidity")
			mgB = ROOT.TMultiGraph()

			color = 0
			plotColor = [46,40,30,38,41]

			for year in years:
				#This below was to sort the order
				pt_dataDict[year]["x"], pt_dataDict[year]["y"], pt_dataDict[year]["ex"], pt_dataDict[year]["ey"] = zip(*sorted(zip(pt_dataDict[year]["x"], pt_dataDict[year]["y"], pt_dataDict[year]["ex"], pt_dataDict[year]["ey"])))
				x = array('f', pt_dataDict[year]["x"])
				y = array('f', pt_dataDict[year]["y"])
				ex = array('f', pt_dataDict[year]["ex"])
				ey = array('f', pt_dataDict[year]["ey"])
				nPoints = len(pt_dataDict[year]["x"])
				grB = ROOT.TGraphErrors(nPoints,x,y,ex,ey)
				grB.SetTitle(str(year))
				grB.SetLineColor(plotColor[color])
				grB.SetLineWidth( 1 )
				grB.SetMarkerColor(plotColor[color])
				grB.SetMarkerStyle( 21 )
				mgB.Add(grB)

				color+=1

			mgB.SetTitle("Xic/Lc Ratio vs. Transverse Momentum per Year")
			mgB.GetXaxis().SetTitle( 'Transverse Momentum (MeV/c)' )
			mgB.GetXaxis().SetRangeUser(3000,18000)
			mgB.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
			mgB.GetYaxis().SetRangeUser(0.01,0.62)
			mgB.Draw('AL*')
			cB.BuildLegend(.75,.8,.85,.6,"Years")
			cB.Update()
			cB.Draw()
			cB.SaveAs(GRAPH_PATH + "ratioVpt.pdf")
			
		elif opt == "-c": #ratio vs. y
			
			cC = ROOT.TCanvas("cC", "Graph of ratio vs. rapidity")
			mgC = ROOT.TMultiGraph()

			color = 0
			plotColor = [46,40,30,38,41]

			for year in years:
				x = array('f', y_dataDict[year]["x"])
				y = array('f', y_dataDict[year]["y"])
				ex = array('f', y_dataDict[year]["ex"])
				ey = array('f', y_dataDict[year]["ey"])
				nPoints = len(y_dataDict[year]["x"])
				grC = ROOT.TGraphErrors(nPoints,x,y,ex,ey)
				grC.SetTitle(str(year))
				grC.SetLineColor(plotColor[color])
				grC.SetLineWidth( 1 )
				grC.SetMarkerColor(plotColor[color])
				grC.SetMarkerStyle( 21 )
				mgC.Add(grC)

				color+=1

			mgC.SetTitle("Xic/Lc Ratio vs. Rapidity per Year")
			mgC.GetXaxis().SetTitle( 'Rapidity' )
			mgC.GetXaxis().SetRangeUser(2.0,4.8)
			mgC.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
			mgC.GetYaxis().SetRangeUser(0.04,0.35)
			mgC.Draw('AL*')
			cC.BuildLegend(.15,.8,.25,.6,"Years")
			cC.Update()
			cC.Draw()
			cC.SaveAs(GRAPH_PATH + "ratioVy.pdf")
			
		elif opt == "-d": #ratio vs. years 
			
			ratio = []
			ratioErr = []

			cD = ROOT.TCanvas("cD", "Graph of Ratio vs. Year")

			for year in years:
				if year == 2011 or year == 2012:
					ratio.append((yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"]+yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])/(yearTotDict[year]["MagUp"]["Lc_total.root"]["yield_val"]+yearTotDict[year]["MagDown"]["Lc_total.root"]["yield_val"]))
					ratioErr.append((yearTotDict[year]["MagUp"]['Xic_total.root']["yield_err"]/yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"])**2+(yearTotDict[year]["MagUp"]['Lc_total.root']["yield_err"]/yearTotDict[year]["MagUp"]['Lc_total.root']["yield_val"])**2)
				else:
					ratio.append(yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"]/yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					ratioErr.append((yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"]/yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])**2+(yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"]/yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])**2)

			nPoints = len(years)
			x = array('f', years)
			ex = array('f', [0,0,0,0,0,0,0])
			y = array('f', ratio)
			ey = array('f', ratioErr)

			grD = ROOT.TGraphErrors(nPoints,x,y,ex,ey)
			grD.SetTitle("Xic")
			grD.SetLineColor(40)
			grD.SetLineWidth( 1 )
			grD.SetMarkerColor(40)
			grD.SetMarkerStyle( 21 )

			grD.SetTitle("Xic/Lc Ratios vs. Year")
			grD.GetXaxis().SetTitle( 'Year' )
			grD.GetYaxis().SetTitle( 'Xic/Lc Ratios' )
			grD.GetXaxis().SetRangeUser(2009,2019)
			grD.Draw('AL*')
			legD = ROOT.TLegend(.15,.4,.40,.3,"Ratio")
			legD.AddEntry("grD","Xic/Lc Yield Ratio","AL*")
			legD.SetTextSize(0.03)
			legD.Draw()
			cD.Draw()
			cD.SaveAs(GRAPH_PATH + "ratioVyear.pdf")
			
		elif opt == "-e": #yield vs. year
			XicYield = []
			XicYieldEr = []
			LcYield = []
			LcYieldEr = []

			cE = ROOT.TCanvas("cE", "Graph of Yield vs. year")
			cE.SetLogy()
			mgE = ROOT.TMultiGraph()

			for year in years:
				if year == 2011 or year == 2012:
					XicYield.append(yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"]+yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])
					XicYieldEr.append(math.sqrt((yearTotDict[year]["MagUp"]['Xic_total.root']["yield_err"])**2+(yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"])**2))
					LcYield.append(yearTotDict[year]["MagUp"]['Lc_total.root']["yield_val"]+yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					LcYieldEr.append(math.sqrt(yearTotDict[year]["MagUp"]['Lc_total.root']["yield_err"]**2+yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"]**2))
				else:
					XicYield.append(yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])
					XicYieldEr.append(yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"])
					LcYield.append(yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					LcYieldEr.append(yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"])
					
			nPoints = len(years)
			x = array('f', years)
			ex = array('f', [0,0,0,0,0,0,0])
			yXi = array('f', XicYield)
			eyXi = array('f', XicYieldEr)
			yL = array('f', LcYield)
			eyL = array('f', LcYieldEr)

			grE1 = ROOT.TGraphErrors(nPoints,x,yXi,ex,eyXi)
			grE1.SetTitle("Xic")
			grE1.SetLineColor(40)
			grE1.SetLineWidth( 1 )
			grE1.SetMarkerColor(40)
			grE1.SetMarkerStyle( 21 )
			mgE.Add(grE1)

			grE2 = ROOT.TGraphErrors(nPoints,x,yL,ex,eyL)
			grE2.SetTitle("Lc")
			grE2.SetLineColor(46)
			grE2.SetLineWidth( 1 )
			grE2.SetMarkerColor(46)
			grE2.SetMarkerStyle( 21 )
			mgE.Add(grE2)

			mgE.SetTitle("Xic and Lc Yield vs. Year")
			mgE.GetXaxis().SetTitle( 'Year' )
			mgE.GetYaxis().SetTitle( 'Xic,Lc Yields' )
			mgE.GetXaxis().SetRangeUser(2009,2019)
			mgE.GetYaxis().SetRangeUser(10000,100000000)
			mgE.Draw('AL*')
			cE.BuildLegend(.15,.8,.25,.7,"Particles")
			cE.Update()		
			cE.Draw()
			cE.SaveAs(GRAPH_PATH + "yieldVyear.pdf")
			
		else:
			sys.exit()
		


if __name__ == "__main__":
   main(sys.argv[1:])




