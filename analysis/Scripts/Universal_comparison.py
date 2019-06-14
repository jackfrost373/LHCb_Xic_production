#This script is used to plot series of comparison plots over multiple variables using the plot_comparison function as defined in the Imports script. The script generated may include some lines used as indications as to whether a possible cut could be applied and the canvasses are automatically saved in a desired location

import ROOT, os, Imports
from ROOT import TChain, TCanvas, TH1

#select the user in order to have the right directory for saving the plots
#user = "Simon"
user = input("please indicate the user (Simon, Chris or Nikhef): ")

#change the following string variable to select which particle you want to study

#particle = "Xic"
particle  = input("please indicate the particle (Lc or Xic): ")

#This string is a general name used for the canvas name
#name = "Xic_vs_MC"
name = input("please indicate the name that you would like your graphs to be saved with: ")

#Here is a list of all the variables whose distribution needs to be compared
variables_to_plot = ["lcplus_P", "lcplus_OWNPV_CHI2", "pplus_ProbNNp", "kminus_ProbNNk", "piplus_ProbNNpi", "pplus_P", "kminus_P", "piplus_P", "kminus_PIDK", "pplus_PIDp", "lcplus_IPCHI2_OWNPV", "lcplus_ETA", "lcplus_PT", "lcplus_TAU", "lcplus_PVConstrainedDTF_chi2"]

#this dictionary should contain all of the variables that want to be plotted with a line. The key should be a string of the variable and its value should be the x value at which the line should be plotted
variables_to_plot_with_line = {}

#import the trees which need to be plotted by using the relative Imports functions
Imports.datatree()
Imports.Xic_MC_datatree_1()

tree1 = Imports.tree # tree that will be plotted in red
tree2 = Imports.Xic_MC_tree_1 # tree that will be plotted in blue

directory = Imports.getDirectory(user)

c1 = ROOT.TCanvas("c1")

masshist = ROOT.TH1F("masshist", "Histogram of L_{c}^{+} mass", 300, 2200, 2600)
masshist.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
masshist.GetYaxis().SetTitle("Number of events")

#define the cuts that you want to apply based on the specific comparison you want to make
cuts1 = Imports.getBackgroundCuts(particle)
cuts2 = Imports.getMCCuts(particle)

#dummy histograms used for the legend. Ideally, they should be removed
histogram1 = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)
histogram2 = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)

histogram1.SetLineColor(2) # red for tree1
histogram1.SetLineWidth(1)

histogram2.SetLineColor(9) # blue for tree2
histogram2.SetLineWidth(1)
extralabel1="Xic Full Background" #label for tree1 in the Legend
extralabel2="Xic MC" #label for tree2 in the Legend
leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
leg.SetHeader("Legend")
leg.AddEntry(histogram1, extralabel1, "l")
leg.AddEntry(histogram2, extralabel2, "l")

for variable in variables_to_plot:

    Imports.plot_comparison(variable, tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right")
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


