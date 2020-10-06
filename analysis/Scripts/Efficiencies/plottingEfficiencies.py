import sys, getopt, ROOT, math, textwrap

sys.path.append("../")

from array import array
import Imports
from Imports import PLOT_PATH, OUTPUT_DICT_PATH

sys.path.append(PLOT_PATH + "Dict_output/Efficiencies/")

years = [2012,2016,2017,2018]

from Trigger_Eff_Dict import trigDict
from Selection_Eff_Dict import selDict

def plotEff(Dict,title,range_yMin,range_yMax):

	cE = ROOT.TCanvas("cE", title)
	mgE = ROOT.TMultiGraph()

	Lc_md = []
	Lc_err_md = []
	Lc_mu = []
	Lc_err_mu = []

	Xic_md = []
	Xic_err_md = []
	Xic_mu = []
	Xic_err_mu = []

	for year in years:
		Lc_md.append(Dict["Lc_{}_MagDown".format(year)]["val"])
		Lc_err_md.append(Dict["Lc_{}_MagDown".format(year)]["val"])
		Lc_mu.append(Dict["Lc_{}_MagUp".format(year)]["val"])
		Lc_err_mu.append(Dict["Lc_{}_MagUp".format(year)]["val"])

		Xic_md.append(Dict["Xic_{}_MagDown".format(year)]["val"])
		Xic_err_md.append(Dict["Xic_{}_MagDown".format(year)]["val"])
		Xic_mu.append(Dict["Xic_{}_MagUp".format(year)]["val"])
		Xic_err_mu.append(Dict["Xic_{}_MagUp".format(year)]["val"])

	nPoints = len(years)
	x = array('f', years)
	ex = array('f', [0,0,0,0,0,0,0])

	yXi_md = array('f', Xic_md)
	eyXi_md = array('f', Xic_err_md)
	yL_md = array('f', Lc_md)
	eyL_md = array('f', Lc_err_md)

	yXi_mu = array('f', Xic_mu)
	eyXi_mu = array('f', Xic_err_mu)
	yL_mu = array('f', Lc_mu)
	eyL_mu = array('f', Lc_err_mu)

	grE1 = ROOT.TGraphErrors(nPoints,x,yXi_md,ex,eyXi_md)
	grE1.SetTitle("Xic_MD")
	grE1.SetLineColor(40)
	grE1.SetLineWidth( 1 )
	grE1.SetMarkerColor(40)
	grE1.SetMarkerStyle( 21 )
	mgE.Add(grE1)

	grE2 = ROOT.TGraphErrors(nPoints,x,yL_md,ex,eyL_md)
	grE2.SetTitle("Lc_MD")
	grE2.SetLineColor(46)
	grE2.SetLineWidth( 1 )
	grE2.SetMarkerColor(46)
	grE2.SetMarkerStyle( 21 )
	mgE.Add(grE2)

	grE3 = ROOT.TGraphErrors(nPoints,x,yXi_mu,ex,eyXi_mu)
	grE3.SetTitle("Xic_MU")
	grE3.SetLineColor(48)
	grE3.SetLineWidth( 1 )
	grE3.SetMarkerColor(48)
	grE3.SetMarkerStyle( 21 )
	mgE.Add(grE3)

	grE4 = ROOT.TGraphErrors(nPoints,x,yL_mu,ex,eyL_mu)
	grE4.SetTitle("Lc_MU")
	grE4.SetLineColor(50)
	grE4.SetLineWidth( 1 )
	grE4.SetMarkerColor(50)
	grE4.SetMarkerStyle( 21 )
	mgE.Add(grE4)

	mgE.SetTitle("Trigger Efficiencies vs. Year")
	mgE.GetXaxis().SetTitle( 'Year' )
	mgE.GetYaxis().SetTitle( 'Efficiency values' )
	mgE.GetXaxis().SetRangeUser(2009,2019)
	mgE.GetYaxis().SetRangeUser(range_yMin,range_yMax)
	mgE.Draw('AL*')
	cE.BuildLegend(.15,.8,.25,.7,"Particles")
	cE.Update()		
	cE.Draw()
	
	what = title.split()
	cE.SaveAs(PLOT_PATH + "Efficiencies/" + what[0] + "_Eff_Graph.pdf")

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
		options = ["-s","-t","-p"]
	
	for opt in options:
		if opt == "-s":
			plotEff(selDict,"Selection Efficiency vs. Year",-0.2,0.5)

		elif opt == "-t":
			plotEff(trigDict, "Trigger Efficiency vs. Year",-1,2)

		elif opt == "-p":
			print("Sorry PID is not yet implemented, exiting...")
			sys.exit()

		else:
			print("Option does not exist, exiting...")
			sys.exit()

if __name__ == "__main__":
	main(sys.argv[1:])
