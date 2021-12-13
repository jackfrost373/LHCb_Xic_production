#This script is used to plot series of comparison plots over multiple variables using the plot_comparison function as defined in the Imports script. The script generated may include some lines used as indications as to whether a possible cut could be applied and the canvasses are automatically saved in a desired location

import ROOT, os, Plot_comparison, Imports
from ROOT import TChain, TCanvas, TH1

#select the user in order to have the right directory for saving the plots
user = "Nikhef"


#change the following string variable to select which particle you want to study

particle = "Xic"
#particle  = input("please indicate the particle (Lc or Xic): ")

#This string is a general name used for the canvas name
name = "Xic_Comp_"
#name = input("please indicate the name that you would like your graphs to be saved with: ")

#Here is a list of all the variables whose distribution needs to be compared
variables_to_plot = [ 'lcplus_RAPIDITY', 
                      'piplus_RAPIDITY',
                      'pplus_RAPIDITY',
                      'kminus_RAPIDITY',
                      'lcplus_ENDVERTEX_CHI2',
                      "lcplus_ENDVERTEX_NDOF",
                      'lcplus_IPCHI2_OWNPV',
                      'pplus_OWNPV_CHI2',
                      "pplus_P", 
                      "pplus_PT",
                      "kminus_P", 
                      "kminus_PT",
                      "piplus_P", 
                      "piplus_PT",
                      "kminus_PIDK", 
                      "kminus_PIDp",
                      "piplus_PIDK", 
                      "piplus_PIDp",
                      "pplus_PIDK", 
                      "pplus_PIDp",
                      'kminus_OWNPV_CHI2',
                      'piplus_OWNPV_CHI2',
                      'lcplus_IP_OWNPV',
                      'piplus_ProbNNpi',
                      'pplus_ProbNNp',
                      'kminus_ProbNNk',
                      "pplus_MC15TuneV1_ProbNNp",
                      "pplus_MC15TuneV1_ProbNNk",
                      "pplus_MC15TuneV1_ProbNNpi",
                      "pplus_MC15TuneV1_ProbNNghost",
                      "kminus_MC15TuneV1_ProbNNp",
                      "kminus_MC15TuneV1_ProbNNk",
                      "kminus_MC15TuneV1_ProbNNpi",
                      "kminus_MC15TuneV1_ProbNNghost",
                      "piplus_MC15TuneV1_ProbNNp",
                      "piplus_MC15TuneV1_ProbNNk",
                      "piplus_MC15TuneV1_ProbNNpi",
                      "piplus_MC15TuneV1_ProbNNghost"]

#variables_to_plot = ["pplus_P"]

#this dictionary should contain all of the variables that want to be plotted with a line. The key should be a string of the variable and its value should be the x value at which the line should be plotted
variables_to_plot_with_line = {}

#fileloc="/dcache/bfys/jtjepkem/binned_files/2017_MagDown/Xic_total.root"
#f=ROOT.TFile.Open(fileloc,"READONLY")
#tree1 = f.Get("DecayTree") # tree that will be plotted in red

tree1 =  ROOT.TChain("tuple_Xic2pKpi/DecayTree")
filedir="/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/115"
filename="Xic2pKpiTuple.root"
for job in range (185):
    tree1.Add("{0}/{1}/{2}".format(filedir, job, filename))


#fileloc="/dcache/bfys/jtjepkem/binned_files/2016_MagDown/Lc_total.root"
#f=ROOT.TFile.Open(fileloc,"READONLY")
#tree2 = f.Get("DecayTree") # tree that will be plotted in blue 

#tree2 =  ROOT.TChain("tuple_Lc2pKpi/DecayTree")
#filedir="/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/91"
#filename="Lc2pKpiTuple.root"
#for job in range (519):
#    tree2.Add("{0}/{1}/{2}".format(filedir, job, filename))

tree2 =  ROOT.TChain("tuple_Lc2pKpi/DecayTree")
filedir="/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/108"
filename="MC_Lc2pKpiTuple_26103090.root"
for job in range (282):
    tree2.Add("{0}/{1}/{2}".format(filedir, job, filename))

#directory = Imports.getDirectory(user)
directory = "~/Documents"
print("Tree1 contains {0} and Tree2 contains {1}". format(tree1.GetEntries(), tree2.GetEntries()))
c1 = ROOT.TCanvas("c1")

masshist = ROOT.TH1F("masshist", "Histogram of L_{c}^{+} mass", 300, 2200, 2600)
masshist.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
masshist.GetYaxis().SetTitle("Number of events")

#define the cuts that you want to apply based on the specific comparison you want to make
#cuts1 = ("pplus_P<120000 && lcplus_MM>2375 && lcplus_L0HadronDecision_TOS && lcplus_Hlt1TrackMVADecision_TOS==1 && lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS==1")
cuts2 = "abs(piplus_ID)==211 && abs(kminus_ID)==321 && abs(pplus_ID)==2212 && abs(lcplus_ID)==4122"
cuts2 = cuts2 + ("&&lcplus_MM>2440 && lcplus_MM<2490 && lcplus_L0Global_TOS==1 && lcplus_Hlt1TrackMVADecision_TOS==1 && lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS == 1")
cuts1 = "lcplus_MM>2440 && lcplus_MM<2490&&lcplus_L0Global_TOS == 1 && lcplus_Hlt1TrackMVADecision_TOS == 1"

#dummy histograms used for the legend. Ideally, they should be removed
histogram1 = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)
histogram2 = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)

histogram1.SetLineColor(2) # red for tree1
histogram1.SetLineWidth(1)

histogram2.SetLineColor(9) # blue for tree2
histogram2.SetLineWidth(1)
extralabel1="Data" #label for tree1 in the Legend
extralabel2="MC (26103090)" #label for tree2 in the Legend
leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
leg.SetHeader("Legend")
leg.AddEntry(histogram1, extralabel1, "l")
leg.AddEntry(histogram2, extralabel2, "l")

for variable in variables_to_plot:
    if variable == "lcplus_TAU":
        Plot_comparison.plot_comparison(variable,tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right", Override=True, xmin=0, xmax=2E-3)
    elif variable == "lcplus_OWNPV_CHI2":
        Plot_comparison.plot_comparison(variable,tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right", Override=True, xmin=0, xmax=90)
    elif variable == "lcplus_IPCHI2_OWNPV":
        Plot_comparison.plot_comparison(variable,tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right", Override=True, xmin=0, xmax=10)
    else:
        Plot_comparison.plot_comparison(variable, tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right")
    leg.Draw()
    if variable in variables_to_plot_with_line:
        point = variables_to_plot_with_line[variable]
        line = ROOT.TLine(point, 0, point, 0.08)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw("same")
    c1.Update()
    c1.Draw()
    graph_name = (name + variable +".pdf")
    filepath = directory
    fullpath = os.path.join(filepath, graph_name)
    c1.SaveAs(fullpath)


