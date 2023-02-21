#This script is used to plot series of comparison plots over multiple variables using the plot_comparison function as defined in the Imports script. The script generated may include some lines used as indications as to whether a possible cut could be applied and the canvasses are automatically saved in a desired location

import ROOT, os, Plot_comparison, Imports
from ROOT import TChain, TCanvas, TH1
from Imports import WORKING_DIR, TUPLE_PATH, RAW_TUPLE_PATH

#change the following string variable to select which particle you want to study
particle = "Xic"
#particle  = input("please indicate the particle (Lc or Xic): ")

#This string is a general name used for the canvas name
#name = "{0}_signal_vs_MC".format(particle)
name = input("please indicate the name that you would like your graphs to be saved with: ")

year = "2018"
MagPol="MagDown"
saveEntry="1"

#Here is a list of all the variables whose distribution needs to be compared
variables_to_plot = ["lcplus_P", "lcplus_OWNPV_CHI2", "pplus_ProbNNp", "kminus_ProbNNk", "piplus_ProbNNpi", "pplus_ETA","pplus_PT","pplus_P", "kminus_ETA","kminus_PT","kminus_P", "piplus_ETA", "piplus_PT" ,"piplus_P", "kminus_PIDK", "pplus_PIDp", "lcplus_IPCHI2_OWNPV", "lcplus_ETA", "lcplus_PT", "lcplus_TAU"]

#variables_to_plot = ["pplus_P","pplus_ETA","pplus_PT"]

#this dictionary should contain all of the variables that want to be plotted with a line. The key should be a string of the variable and its value should be the x value at which the line should be plotted
variables_to_plot_with_line = {}

fileloc=TUPLE_PATH+"/{0}_{1}/{2}_total.root".format(year,MagPol,particle)
print("Data file:" + fileloc)
f=ROOT.TFile.Open(fileloc,"READONLY")
tree1 = f.Get("DecayTree") # tree that will be plotted in red

#tree1 =  ROOT.TChain("tuple_Lc2pKpi/DecayTree")
#filedir=RAW_TUPLE_PATH + "/91"
#filename="Lc2pKpiTuple.root"
#for job in range (529):
#    tree1.Add("{0}/{1}/{2}".format(filedir, job, filename))


#fileloc=TUPLE_PATH + "/2017_MagDown/Lc_total.root"
#f=ROOT.TFile.Open(fileloc,"READONLY")
#tree1 = f.Get("DecayTree") # tree that will be plotted in blue 

#tree2 =  ROOT.TChain("tuple_Lc2pKpi/DecayTree")
#filedir=RAW_TUPLE_PATH+"/145"
#filename="MC_Lc2pKpiTuple_25103064.root"
#for job in range (181):
#    tree2.Add("{0}/{1}/{2}".format(filedir, job, filename))

for entry in Imports.MC_jobs_Dict:
    if Imports.MC_jobs_Dict[entry][0]==year:
        if Imports.MC_jobs_Dict[entry][1]==MagPol:
            if Imports.MC_jobs_Dict[entry][3]==particle:
                saveEntry=entry
                print ("found MC file which matches")
                tree2 =  ROOT.TChain("tuple_Lc2pKpi/DecayTree")
                filedir=Imports.RAW_TUPLE_PATH+entry
                filename="MC_Lc2pKpiTuple_{0}.root".format(Imports.MC_jobs_Dict[entry][4])
                for job in range (Imports.MC_jobs_Dict[entry][2]):
                    tree2.Add("{0}/{1}/{2}".format(filedir, job, filename))
                
entry=saveEntry
#directory = "/data/bfys/jdevries/LcAnalysis_plots/MCDataComp/{0}/{1}/".format(year, MagPol)
directory = "~/MCComp/"

print("Tree1 contains {0} and Tree2 contains {1}". format(tree1.GetEntries(), tree2.GetEntries()))
c1 = ROOT.TCanvas("c1")

masshist = ROOT.TH1F("masshist", "Histogram of L_{c}^{+} mass", 300, 2200, 2600)
masshist.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
masshist.GetYaxis().SetTitle("Number of events")

#define the cuts that you want to apply based on the specific comparison you want to make
#cuts1 = Imports.getDataCuts(2, trig=True )+ " && " + Imports.getSWeightsCuts(particle)
cuts2 = Imports.getMCCuts(particle, 2) + " && " + Imports.getDataCuts(2,trig=True) + " && " + Imports.getSWeightsCuts(particle)
cuts1 = Imports.getDataCuts(2, trig=True)+ " && " + Imports.getSWeightsCuts(particle)
#dummy histograms used for the legend. Ideally, they should be removed
histogram1 = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)
histogram2 = ROOT.TH1F("masshist", "Histogram of L_{c} mass", 300, 2200, 2600)

# TODO temporary workaround as Hlt2 variable is not in the data files somehow (wrong tupleprep?)
cuts1 = cuts1.replace("lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS","1")
cuts2 = cuts2.replace("lcplus_Hlt2CharmHadXicpToPpKmPipTurboDecision_TOS","1")
cuts1 = cuts1.replace("lcplus_Hlt2CharmHadLcpToPpKmPipTurboDecision_TOS","1")
cuts2 = cuts2.replace("lcplus_Hlt2CharmHadLcpToPpKmPipTurboDecision_TOS","1")


histogram1.SetLineColor(2) # red for tree1
histogram1.SetLineWidth(1)

histogram2.SetLineColor(9) # blue for tree2
histogram2.SetLineWidth(1)
#extralabel1=" "+particle+"Data "+year+" " +MagPol #label for tree1 in the Legend
extralabel1=" XiC MC (26103091) 2017 MagUp)"
extralabel2=" {0} MC ({1}) {2} {3})".format(particle, Imports.MC_jobs_Dict[entry][4],year,MagPol) #label for tree2 in the legend
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


