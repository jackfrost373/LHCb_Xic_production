import sys, getopt, ROOT, math, textwrap
from array import array
import Imports

Base_Path = "/data/bfys/jdevries/LcAnalysis_plots/"
Import_Path = Base_Path + "Dict_output"
sys.path.append(Import_Path)

#TO CHANGE DEPENDING ON WHERE THE DICTS ARE LOCATED!
from Massfitting.GaussCBcombinedFit_DictFile import mainDict as GaussCB_combinedDict
from Massfitting.GaussCByearFit_DictFile import mainDict as GaussCB_yearTotDict
from Massfitting.GaussCBsingleFit_DictFile import mainDict as GaussCB_singleDict

from Massfitting.BukincombinedFit_DictFile import mainDict as Bukin_combinedDict
from Massfitting.BukinyearFit_DictFile import mainDict as Bukin_yearTotDict
from Massfitting.BukinsingleFit_DictFile import mainDict as Bukin_singleDict


#CAN BE CHANGED TO OUTPUT THE 
GRAPH_PATH = Base_Path + "Yield_Ratios/Graphs/"
years = [2011,2012,2016,2017,2018]

color = 0
plotColor = [46,40,30,38,41]

#Creation of the y and pt bin lists from the imports functions
pt_bin_temp = Imports.getPTbins()
pt_arr = []			#format [3200,4000,5000,6000,7000,8000,10000,20000]
pt_arr_str = []		      #format ["3200-4000","4000-5000", ...]
		
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
G_y_dataDict = {}
G_pt_dataDict = {}
for year in years:
	G_y_dataDict[year] = {
		"x" : [],
		"y" : [],
		"ex" : [],
		"ey" : []
	}

	for points in y_arr_str:
		G_y_dataDict[year]['x'].append(0)
		G_y_dataDict[year]['y'].append(0)
		G_y_dataDict[year]['ex'].append(0)
		G_y_dataDict[year]['ey'].append(0)

	G_pt_dataDict[year] = {
		"x" : [],
		"y" : [],
		"ex" : [],
		"ey" : []
	}

B_y_dataDict = {}
B_pt_dataDict = {}
for year in years:
	B_y_dataDict[year] = {
		"x" : [],
		"y" : [],
		"ex" : [],
		"ey" : []
	}

	for points in y_arr_str:
		B_y_dataDict[year]['x'].append(0)
		B_y_dataDict[year]['y'].append(0)
		B_y_dataDict[year]['ex'].append(0)
		B_y_dataDict[year]['ey'].append(0)

	B_pt_dataDict[year] = {
		"x" : [],
		"y" : [],
		"ex" : [],
		"ey" : []
	}

	for points in pt_arr_str: #initializes the dataset to zero everywhere
		G_pt_dataDict[year]['x'].append(0) # => "x" : [0,0,0,0,0,0,0] as theres 7 pt bins
		G_pt_dataDict[year]['y'].append(0)
		G_pt_dataDict[year]['ex'].append(0)
		G_pt_dataDict[year]['ey'].append(0)

	for points in pt_arr_str:
		B_pt_dataDict[year]['x'].append(0)
		B_pt_dataDict[year]['y'].append(0)
		B_pt_dataDict[year]['ex'].append(0)
		B_pt_dataDict[year]['ey'].append(0)
    
	for pol in GaussCB_combinedDict[year]:
		i = 0
		for file in sorted(GaussCB_combinedDict[year][pol]):
			if ("ybin" in file) and ("Xic" in file):
				y = (float(file[:-5].split('_')[-1].split('-')[0])+float(file[:-5].split('_')[-1].split('-')[1]))/2
				y_err = (float(file[:-5].split('_')[-1].split('-')[1])-float(file[:-5].split('_')[-1].split('-')[0]))/2
				ratio = GaussCB_combinedDict[year][pol][file]["yield_val"]/GaussCB_combinedDict[year][pol]['Lc'+file[3:]]["yield_val"]
				ratio_err = math.sqrt((GaussCB_combinedDict[year][pol][file]["yield_err"]/GaussCB_combinedDict[year][pol][file]["yield_val"])**2 + (GaussCB_combinedDict[year][pol]['Lc'+file[3:]]["yield_err"]/GaussCB_combinedDict[year][pol]['Lc'+file[3:]]["yield_val"])**2)

				G_y_dataDict[year]["x"][i] = y
				G_y_dataDict[year]["y"][i] += ratio
				G_y_dataDict[year]["ex"][i] = y_err

				if G_y_dataDict[year]["ey"][i] == 0:
					G_y_dataDict[year]["ey"][i] += ratio_err
				else:
					G_y_dataDict[year]["ey"][i] = math.sqrt(G_y_dataDict[year]["ey"][i]**2 + ratio_err**2)

				i+=1

	for pol in Bukin_combinedDict[year]:
		i = 0
		for file in sorted(Bukin_combinedDict[year][pol]):
			if ("ybin" in file) and ("Xic" in file):
				y = (float(file[:-5].split('_')[-1].split('-')[0])+float(file[:-5].split('_')[-1].split('-')[1]))/2
				y_err = (float(file[:-5].split('_')[-1].split('-')[1])-float(file[:-5].split('_')[-1].split('-')[0]))/2
				ratio = Bukin_combinedDict[year][pol][file]["yield_val"]/Bukin_combinedDict[year][pol]['Lc'+file[3:]]["yield_val"]
				ratio_err = math.sqrt((Bukin_combinedDict[year][pol][file]["yield_err"]/Bukin_combinedDict[year][pol][file]["yield_val"])**2 + (Bukin_combinedDict[year][pol]['Lc'+file[3:]]["yield_err"]/Bukin_combinedDict[year][pol]['Lc'+file[3:]]["yield_val"])**2)

				B_y_dataDict[year]["x"][i] = y
				B_y_dataDict[year]["y"][i] += ratio
				B_y_dataDict[year]["ex"][i] = y_err
				if B_y_dataDict[year]["ey"][i] == 0:
					B_y_dataDict[year]["ey"][i] += ratio_err
				else:
					B_y_dataDict[year]["ey"][i] = math.sqrt(B_y_dataDict[year]["ey"][i]**2 + ratio_err**2)

				i+=1
#####

	for pol in GaussCB_combinedDict[year]:
		i = 0
		for file in sorted(GaussCB_combinedDict[year][pol]):
			if ("ptbin" in file) and ("Xic" in file):
				pt = (float(file[:-5].split('_')[-1].split('-')[0])+float(file[:-5].split('_')[-1].split('-')[1]))/2
				pt_err = (float(file[:-5].split('_')[-1].split('-')[1])-float(file[:-5].split('_')[-1].split('-')[0]))/2
				ratio = GaussCB_combinedDict[year][pol][file]["yield_val"]/GaussCB_combinedDict[year][pol]['Lc'+file[3:]]["yield_val"]
				ratio_err = math.sqrt((GaussCB_combinedDict[year][pol][file]["yield_err"]/GaussCB_combinedDict[year][pol][file]["yield_val"])**2 + (GaussCB_combinedDict[year][pol]['Lc'+file[3:]]["yield_err"]/GaussCB_combinedDict[year][pol]['Lc'+file[3:]]["yield_val"])**2)

				G_pt_dataDict[year]["x"][i] = pt
				G_pt_dataDict[year]["y"][i] += ratio
				G_pt_dataDict[year]["ex"][i] = pt_err
				G_pt_dataDict[year]["ey"][i] += ratio_err

				i+=1

	for pol in Bukin_combinedDict[year]:
		i = 0
		for file in sorted(Bukin_combinedDict[year][pol]):
			if ("ptbin" in file) and ("Xic" in file):
				pt = (float(file[:-5].split('_')[-1].split('-')[0])+float(file[:-5].split('_')[-1].split('-')[1]))/2
				pt_err = (float(file[:-5].split('_')[-1].split('-')[1])-float(file[:-5].split('_')[-1].split('-')[0]))/2
				ratio = Bukin_combinedDict[year][pol][file]["yield_val"]/Bukin_combinedDict[year][pol]['Lc'+file[3:]]["yield_val"]
				ratio_err = math.sqrt((Bukin_combinedDict[year][pol][file]["yield_err"]/Bukin_combinedDict[year][pol][file]["yield_val"])**2 + (Bukin_combinedDict[year][pol]['Lc'+file[3:]]["yield_err"]/Bukin_combinedDict[year][pol]['Lc'+file[3:]]["yield_val"])**2)

				B_pt_dataDict[year]["x"][i] = pt
				B_pt_dataDict[year]["y"][i] += ratio
				B_pt_dataDict[year]["ex"][i] = pt_err
				B_pt_dataDict[year]["ey"][i] += ratio_err

				i+=1



def main(argv):
	
	ROOT.gROOT.SetBatch(True) #STOP SHOWING THE GRAPH FOR ROOT
	
	try:
		opts, args = getopt.getopt(argv,"habcdefgi")
	except getopt.GetoptError:
		print("The arguments are wrong")
		sys.exit(2)
	
	options = []
	arguments = []
	
	for opt,arg in opts:
		options.append(opt)
		arguments.append(arg)
		
	if not options:
		options = ["-a","-b","-c","-d","-e", "-f", "-g", "-i"]
	
	if "-h" in options:
		print(textwrap.dedent("""\
			
			Welcome to the plot.py script.
			
			You need to have a directory/folder called "./Graphs/" in the same directory as you run the script, as the PDF files will be saved there.
			You can always change the script variable GRAPH_PATH to change this.
			Be sure to also have the dictionnary files in "./Dict_output/", as well as the Imports.py library in the same directory as script.
			
			The parameters are
				-h : help
				-a : GaussCB 2D histograms of each y vs. each pt (one for each year)
				-b : Bukin 2D histograms of each y vs. each pt (one for each year)
				-c : GaussCB ratio vs. pt (a line for each year)
				-d : Bukin ratio vs. pt (a line for each year)
				-e : GaussCB ratio vs. y (a line for each year)
				-f : Bukin ratio vs. y (a line for each year)
				-g : ratio vs. years 

				-i : yield vs. year

			Running with no parameter will output all the graphs at once.
			"""))

		sys.exit()
		
	
	for opt in options:
		if opt == "-a": #GaussCB 2D histograms of each y vs. each pt
			for year in years:
				cA_G = ROOT.TCanvas( 'cA_G', 'Dynamic Filling Example', 200, 10, 700, 500 )
				G_pt_y_ratio = ROOT.TH2F("GaussCB Yield Ratios","y vs.Pt vs. Xic/Lc Ratio;Transverse Momentum (MeV/c);Rapidity (y)",len(pt_arr_str),array('f',pt_arr),len(y_arr_str),array('f',y_arr))
				G_pt_y_ratio.SetStats(0)
				
				for pol in GaussCB_singleDict[year]:
					for files in GaussCB_singleDict[year][pol]:
						if ("Xic" in files):
							G_ratio = GaussCB_singleDict[year][pol][files]["yield_val"]/GaussCB_singleDict[year][pol]['Lc'+files[3:]]["yield_val"]
							G_y = (float(files[:-5].split('_')[2].split('-')[0])+float(files[:-5].split('_')[2].split('-')[1]))/2
							G_pt = (float(files[:-5].split('_')[4].split('-')[0])+float(files[:-5].split('_')[4].split('-')[1]))/2
							G_pt_y_ratio.Fill(G_pt,G_y,G_ratio)
							
				G_pt_y_ratio.Draw("Colz")
				cA_G.Draw()
				cA_G.SaveAs(GRAPH_PATH +"GaussCB_"+ str(year)+"_pt_y_Ratio_2D.pdf")
				del cA_G, G_pt_y_ratio

		elif opt == "-b": #Bukin 2D histograms of each y vs. each pt
			for year in years:  
				cA_B = ROOT.TCanvas( 'cA_B', 'Dynamic Filling Example', 200, 10, 700, 500 )
				B_pt_y_ratio = ROOT.TH2F("Bukin Yield Ratios","y vs.Pt vs. Xic/Lc Ratio;Transverse Momentum (MeV/c);Rapidity (y)",len(pt_arr_str),array('f',pt_arr),len(y_arr_str),array('f',y_arr))
				B_pt_y_ratio.SetStats(0)
				
				for pol in Bukin_singleDict[year]:
					for files in Bukin_singleDict[year][pol]:
						if ("Xic" in files):
							B_ratio = Bukin_singleDict[year][pol][files]["yield_val"]/Bukin_singleDict[year][pol]['Lc'+files[3:]]["yield_val"]
							B_y = (float(files[:-5].split('_')[2].split('-')[0])+float(files[:-5].split('_')[2].split('-')[1]))/2
							B_pt = (float(files[:-5].split('_')[4].split('-')[0])+float(files[:-5].split('_')[4].split('-')[1]))/2
							B_pt_y_ratio.Fill(B_pt,B_y,B_ratio)
							
				B_pt_y_ratio.Draw("Colz")
				cA_B.Draw()
				cA_B.SaveAs(GRAPH_PATH +"Bukin_"+ str(year)+"_pt_y_Ratio_2D.pdf")
				del cA_B, B_pt_y_ratio
			
#####
			
		elif opt == "-c": #GaussCB ratio vs. pt
			
			cB_G = ROOT.TCanvas("cB_G", "GaussCB Graph of ratio vs. rapidity")
			mgB_G = ROOT.TMultiGraph()


			color = 0
			plotColor = [46,40,30,38,41]

			for year in years:
				#This below was to sort the order
				G_pt_dataDict[year]["x"], G_pt_dataDict[year]["y"], G_pt_dataDict[year]["ex"], G_pt_dataDict[year]["ey"] = zip(*sorted(zip(G_pt_dataDict[year]["x"], G_pt_dataDict[year]["y"], G_pt_dataDict[year]["ex"], G_pt_dataDict[year]["ey"])))
				G_x = array('f', G_pt_dataDict[year]["x"])
				G_y = array('f', G_pt_dataDict[year]["y"])
				G_ex = array('f', G_pt_dataDict[year]["ex"])
				G_ey = array('f', G_pt_dataDict[year]["ey"])
				G_nPoints = len(G_pt_dataDict[year]["x"])
				G_grB = ROOT.TGraphErrors(G_nPoints,G_x,G_y,G_ex,G_ey)
				G_grB.SetTitle(str(year))
				G_grB.SetLineColor(plotColor[color])
				G_grB.SetLineWidth( 1 )
				G_grB.SetMarkerColor(plotColor[color])
				G_grB.SetMarkerStyle( 21 )
				mgB_G.Add(G_grB)

				color+=1
			

			mgB_G.SetTitle("GaussCB Xic/Lc Ratio vs. Transverse Momentum per Year")
			mgB_G.GetXaxis().SetTitle( 'Transverse Momentum (MeV/c)' )
			mgB_G.GetXaxis().SetRangeUser(3000,18000)
			mgB_G.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
			mgB_G.GetYaxis().SetRangeUser(0.01,0.62)
			mgB_G.Draw('AL*')
			cB_G.BuildLegend(.75,.8,.85,.6,"Years")
			cB_G.Update()
			cB_G.Draw()
			cB_G.SaveAs(GRAPH_PATH +"GaussCB_"+ "ratioVpt.pdf")
			
			
#####
		elif opt == "-d": #Bukin ratio vs. pt


			cB_B = ROOT.TCanvas("cB_B", "Bukin Graph of ratio vs. rapidity")
			mgB_B = ROOT.TMultiGraph()

			color = 0
			plotColor = [46,40,30,38,41]

			for year in years:
				B_pt_dataDict[year]["x"], B_pt_dataDict[year]["y"], B_pt_dataDict[year]["ex"], B_pt_dataDict[year]["ey"] = zip(*sorted(zip(B_pt_dataDict[year]["x"], B_pt_dataDict[year]["y"], B_pt_dataDict[year]["ex"], B_pt_dataDict[year]["ey"])))
				B_x = array('f', B_pt_dataDict[year]["x"])
				B_y = array('f', B_pt_dataDict[year]["y"])
				B_ex = array('f', B_pt_dataDict[year]["ex"])
				B_ey = array('f', B_pt_dataDict[year]["ey"])
				B_nPoints = len(B_pt_dataDict[year]["x"])
				B_grB = ROOT.TGraphErrors(B_nPoints,B_x,G_y,B_ex,B_ey)
				B_grB.SetTitle(str(year))
				B_grB.SetLineColor(plotColor[color])
				B_grB.SetLineWidth( 1 )
				B_grB.SetMarkerColor(plotColor[color])
				B_grB.SetMarkerStyle( 21 )
				mgB_B.Add(B_grB)

				color+=1

			mgB_B.SetTitle("Bukin Xic/Lc Ratio vs. Transverse Momentum per Year")
			mgB_B.GetXaxis().SetTitle( 'Transverse Momentum (MeV/c)' )
			mgB_B.GetXaxis().SetRangeUser(3000,18000)
			mgB_B.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
			mgB_B.GetYaxis().SetRangeUser(0.01,0.62)
			mgB_B.Draw('AL*')
			cB_B.BuildLegend(.75,.8,.85,.6,"Years")
			cB_B.Update()
			cB_B.Draw()
			cB_B.SaveAs(GRAPH_PATH +"Bukin_"+ "ratioVpt.pdf")

		elif opt == "-e": #GaussCB ratio vs. y
			
			cC_G = ROOT.TCanvas("cC_G", "GaussCB Graph of ratio vs. rapidity")
			mgC_G = ROOT.TMultiGraph()

			color = 0
			plotColor = [46,40,30,38,41]

			for year in years:
				G_x = array('f', G_y_dataDict[year]["x"])
				G_y = array('f', G_y_dataDict[year]["y"])
				G_ex = array('f', G_y_dataDict[year]["ex"])
				G_ey = array('f', G_y_dataDict[year]["ey"])
				G_nPoints = len(G_y_dataDict[year]["x"])
				G_grC = ROOT.TGraphErrors(G_nPoints,G_x,G_y,G_ex,G_ey)
				G_grC.SetTitle(str(year))
				G_grC.SetLineColor(plotColor[color])
				G_grC.SetLineWidth( 1 )
				G_grC.SetMarkerColor(plotColor[color])
				G_grC.SetMarkerStyle( 21 )
				mgC_G.Add(G_grC)

				color+=1

			

			mgC_G.SetTitle("GaussCB Xic/Lc Ratio vs. Rapidity per Year")
			mgC_G.GetXaxis().SetTitle( 'Rapidity' )
			mgC_G.GetXaxis().SetRangeUser(2.0,4.8)
			mgC_G.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
			mgC_G.GetYaxis().SetRangeUser(0.04,0.35)
			mgC_G.Draw('AL*')
			cC_G.BuildLegend(.15,.8,.25,.6,"Years")
			cC_G.Update()
			cC_G.Draw()
			cC_G.SaveAs(GRAPH_PATH +"GaussCB_"+ "ratioVy.pdf")
			
		
		elif opt == "-f": 

			cC_B = ROOT.TCanvas("cC_B", "Bukin Graph of ratio vs. rapidity")
			mgC_B = ROOT.TMultiGraph()

			color = 0
			plotColor = [46,40,30,38,41]

			for year in years:
				B_x = array('f', B_y_dataDict[year]["x"])
				B_y = array('f', B_y_dataDict[year]["y"])
				B_ex = array('f', B_y_dataDict[year]["ex"])
				B_ey = array('f', B_y_dataDict[year]["ey"])
				B_nPoints = len(B_y_dataDict[year]["x"])
				B_grC = ROOT.TGraphErrors(B_nPoints,B_x,B_y,B_ex,B_ey)
				B_grC.SetTitle(str(year))
				B_grC.SetLineColor(plotColor[color])
				B_grC.SetLineWidth( 1 )
				B_grC.SetMarkerColor(plotColor[color])
				B_grC.SetMarkerStyle( 21 )
				mgC_B.Add(B_grC)

				color+=1

			mgC_B.SetTitle("Bukin Xic/Lc Ratio vs. Rapidity per Year")
			mgC_B.GetXaxis().SetTitle( 'Rapidity' )
			mgC_B.GetXaxis().SetRangeUser(2.0,4.8)
			mgC_B.GetYaxis().SetTitle( 'Xic/Lc Yield Ratio' )
			mgC_B.GetYaxis().SetRangeUser(0.04,0.35)
			mgC_B.Draw('AL*')
			cC_B.BuildLegend(.15,.8,.25,.6,"Years")
			cC_B.Update()
			cC_B.Draw()
			cC_B.SaveAs(GRAPH_PATH +"Bukin_"+ "ratioVy.pdf")

		elif opt == "-g": #ratio vs. years 
			
			G_ratio = []
			G_ratioErr = []
			B_ratio = []
			B_ratioErr = []

			cD = ROOT.TCanvas("cD", "Graph of Ratio vs. Year")
			mgG = ROOT.TMultiGraph()

			for year in years:
				if year == 2011 or year == 2012:
					G_ratio.append((GaussCB_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"]+GaussCB_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])/(GaussCB_yearTotDict[year]["MagUp"]["Lc_total.root"]["yield_val"]+GaussCB_yearTotDict[year]["MagDown"]["Lc_total.root"]["yield_val"]))
					G_ratioErr.append((GaussCB_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_err"]/GaussCB_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"])**2+(GaussCB_yearTotDict[year]["MagUp"]['Lc_total.root']["yield_err"]/GaussCB_yearTotDict[year]["MagUp"]['Lc_total.root']["yield_val"])**2)
					
					B_ratio.append((Bukin_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"]+Bukin_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])/(Bukin_yearTotDict[year]["MagUp"]["Lc_total.root"]["yield_val"]+Bukin_yearTotDict[year]["MagDown"]["Lc_total.root"]["yield_val"]))
					B_ratioErr.append((Bukin_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_err"]/Bukin_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"])**2+(Bukin_yearTotDict[year]["MagUp"]['Lc_total.root']["yield_err"]/Bukin_yearTotDict[year]["MagUp"]['Lc_total.root']["yield_val"])**2)
				else:
					G_ratio.append(GaussCB_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"]/GaussCB_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					G_ratioErr.append((GaussCB_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"]/GaussCB_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])**2+(GaussCB_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"]/GaussCB_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])**2)

					B_ratio.append(Bukin_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"]/Bukin_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					B_ratioErr.append((Bukin_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"]/Bukin_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])**2+(Bukin_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"]/Bukin_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])**2)

			G_nPoints = len(years)
			G_x = array('f', years)
			G_ex = array('f', [0,0,0,0,0,0,0])
			G_y = array('f', G_ratio)
			G_ey = array('f', G_ratioErr)

			G_grD = ROOT.TGraphErrors(G_nPoints,G_x,G_y,G_ex,G_ey)
			G_grD.SetTitle("GaussCB")
			G_grD.SetLineColor(2)
			G_grD.SetLineWidth( 1 )
			G_grD.SetMarkerColor(2)
			G_grD.SetMarkerStyle( 21 )

			mgG.Add(G_grD)


			B_nPoints = len(years)
			B_x = array('f', years)
			B_ex = array('f', [0,0,0,0,0,0,0])
			B_y = array('f', B_ratio)
			B_ey = array('f', B_ratioErr)

			B_grD = ROOT.TGraphErrors(B_nPoints,B_x,B_y,B_ex,B_ey)
			B_grD.SetTitle("Bukin")
			B_grD.SetLineColor(38)
			B_grD.SetLineWidth( 1 )
			B_grD.SetMarkerColor(38)
			B_grD.SetMarkerStyle( 21 )

			mgG.Add(B_grD)

			mgG.SetTitle("ratio vs years vs fit shape")
			mgG.GetXaxis().SetTitle( "Year" )
			mgG.GetYaxis().SetTitle( "Xic/Lc Ratios" )
			mgG.GetXaxis().SetRangeUser(2009, 2019)
			mgG.Draw("AL*")
			cD.BuildLegend(.15,.2,.25,.3, "fit shapes")
			cD.Update()
			cD.Draw()
			cD.SaveAs(GRAPH_PATH + "ratioVyear.pdf")
			
		elif opt == "-i": #yield vs. year
			Gauss_XicYield = []
			Gauss_XicYieldEr = []
			Gauss_LcYield = []
			Gauss_LcYieldEr = []
			Bukin_XicYield = []
			Bukin_XicYieldEr = []
			Bukin_LcYield = []
			Bukin_LcYieldEr = []

			cE = ROOT.TCanvas("cE", "Graph of Yield vs. year")
			cE.SetLogy()
			mgE = ROOT.TMultiGraph()

			for year in years:
				if year == 2011 or year == 2012:
					Gauss_XicYield.append(GaussCB_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"]+GaussCB_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])
					Gauss_XicYieldEr.append(math.sqrt((GaussCB_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_err"])**2+(GaussCB_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"])**2))
					Gauss_LcYield.append(GaussCB_yearTotDict[year]["MagUp"]['Lc_total.root']["yield_val"]+GaussCB_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					Gauss_LcYieldEr.append(math.sqrt(GaussCB_yearTotDict[year]["MagUp"]['Lc_total.root']["yield_err"]**2+GaussCB_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"]**2))

					Bukin_XicYield.append(Bukin_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_val"]+Bukin_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])
					Bukin_XicYieldEr.append(math.sqrt((Bukin_yearTotDict[year]["MagUp"]['Xic_total.root']["yield_err"])**2+(Bukin_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"])**2))
					Bukin_LcYield.append(Bukin_yearTotDict[year]["MagUp"]['Lc_total.root']["yield_val"]+Bukin_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					Bukin_LcYieldEr.append(math.sqrt(Bukin_yearTotDict[year]["MagUp"]['Lc_total.root']["yield_err"]**2+Bukin_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"]**2))
				
				else:
					Gauss_XicYield.append(GaussCB_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])
					Gauss_XicYieldEr.append(GaussCB_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"])
					Gauss_LcYield.append(GaussCB_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					Gauss_LcYieldEr.append(GaussCB_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"])

					Bukin_XicYield.append(Bukin_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_val"])
					Bukin_XicYieldEr.append(Bukin_yearTotDict[year]["MagDown"]['Xic_total.root']["yield_err"])
					Bukin_LcYield.append(Bukin_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_val"])
					Bukin_LcYieldEr.append(Bukin_yearTotDict[year]["MagDown"]['Lc_total.root']["yield_err"])
					
			nPoints = len(years)
			x = array('f', years)
			ex = array('f', [0,0,0,0,0,0,0])
			G_yXi = array('f', Gauss_XicYield)
			G_eyXi = array('f', Gauss_XicYieldEr)
			G_yL = array('f', Gauss_LcYield)
			G_eyL = array('f', Gauss_LcYieldEr)
			B_yXi = array('f', Bukin_XicYield)
			B_eyXi = array('f', Bukin_XicYieldEr)
			B_yL = array('f', Bukin_LcYield)
			B_eyL = array('f', Bukin_LcYieldEr)

			grE1 = ROOT.TGraphErrors(nPoints,x,G_yXi,ex,G_eyXi)
			grE1.SetTitle("Gauss_Xic")
			grE1.SetLineColor(40)
			grE1.SetLineWidth( 1 )
			grE1.SetMarkerColor(40)
			grE1.SetMarkerStyle( 21 )
			mgE.Add(grE1)

			grE2 = ROOT.TGraphErrors(nPoints,x,G_yL,ex,G_eyL)
			grE2.SetTitle("Gauss_Lc")
			grE2.SetLineColor(46)
			grE2.SetLineWidth( 1 )
			grE2.SetMarkerColor(46)
			grE2.SetMarkerStyle( 21 )
			mgE.Add(grE2)

			grE3 = ROOT.TGraphErrors(nPoints,x,B_yXi,ex,B_eyXi)
			grE3.SetTitle("Bukin_Xic")
			grE3.SetLineColor(45)
			grE3.SetLineWidth( 1 )
			grE3.SetMarkerColor(45)
			grE3.SetMarkerStyle( 21 )
			mgE.Add(grE3)
			
			grE4 = ROOT.TGraphErrors(nPoints,x,B_yL,ex,B_eyL)
			grE4.SetTitle("Bukin_Lc")
			grE4.SetLineColor(39)
			grE4.SetLineWidth( 1 )
			grE4.SetMarkerColor(39)
			grE4.SetMarkerStyle( 21 )
			mgE.Add(grE4)

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




