#This script is used to plot series of comparison plots over multiple variables using the plot_comparison function as defined in the Imports script. The script generated may include some lines used as indications as to whether a possible cut could be applied and the canvasses are automatically saved in a desired location
#Chris Pawley & Aleksandra Bołbot

#This section imports everything 
import ROOT, os, Plot_comparison, Imports, uproot, numpy, sklearn, hep_ml, hep_ml.reweight
from ROOT import TChain, TCanvas, TH1
from Imports import PLOT_PATH, TUPLE_PATH, RAW_TUPLE_PATH
from Plot_comparison import *
from hep_ml.reweight import GBReweighter
import matplotlib.pyplot as plt

#Change the following string variable to select which particle you want to study (Lc or Xic)
particle = "Xic"

#This string is a general name used for the canvas name
#name = "{0}_signal_vs_MC".format(particle)
name = input("please indicate the name that you would like your graphs to be saved with: ")

#Selection of year, magnet and ???
year = "2017"
MagPol="MagDown"
saveEntry="1"


#Here is a list of all the variables whose distribution needs to be compared
variables_to_plot = ["lcplus_P", "lcplus_PT", "lcplus_ETA", "nTracks"]

#This dictionary should contain all of the variables that want to be plotted with a line. The key should be a string of the variable and its value should be the x value at which the line should be plotted
variables_to_plot_with_line = {}

fileloc=TUPLE_PATH+"{0}_{1}/{2}_total.root".format(year,MagPol,particle)
print(fileloc)
f=ROOT.TFile.Open(fileloc,"READONLY")
tree1 = f.Get("DecayTree") # tree that will be plotted in red
tree1.AddFriend("dataNew","/data/bfys/cpawley/sWeights/2017_MagDown/Lc_total_sWeight_swTree.root")


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
                   

#Directory in which the final plots will be saved
entry = saveEntry
#directory = "/data/bfys/jdevries/LcAnalysis_plots/MCDataComp/{0}/{1}/".format(year, MagPol)
directory = "~/MCComp/"

print("Tree1 contains {0} and Tree2 contains {1}". format(tree1.GetEntries(), tree2.GetEntries()))
c1 = ROOT.TCanvas("c1")

masshist = ROOT.TH1F("masshist", "Histogram of L_{c}^{+} mass", 300, 2200, 2600)
masshist.GetXaxis().SetTitle("M(L_{c}^{+}) [MeV/c^{2}]")
masshist.GetYaxis().SetTitle("Number of events")

#Define the cuts that you want to apply based on the specific comparison you want to make
cuts1 = Imports.getDataCuts(2, trig=True)+ " && " + Imports.getSWeightsCuts(particle)
cuts2 = Imports.getMCCuts(particle, 2) + " && " + Imports.getDataCuts(2,trig=True) + " && " + Imports.getSWeightsCuts(particle)

#Dummy histograms for legend 
histoleg1 = ROOT.TH1F("histoleg1", "Histogram of L_{c} mass", 300, 2200, 2600)
histoleg2 = ROOT.TH1F("histoleg2", "Histogram of L_{c} mass", 300, 2200, 2600)

histoleg1.SetLineColor(2) # red for tree1
histoleg1.SetLineWidth(1)

histoleg2.SetLineColor(9) # blue for tree2
histoleg2.SetLineWidth(1)
extralabel1=" " + particle +"Data " + year + " " + MagPol #label for tree1 in the Legend
extralabel2=" {0} MC ({1}) {2} {3})".format(particle, Imports.MC_jobs_Dict[entry][4],year,MagPol) #label for tree2 in the legend
leg = ROOT.TLegend(0.7, 0.77, 0.89, 0.89)
leg.SetHeader("Legend")
leg.AddEntry(histoleg1, extralabel1, "l")
leg.AddEntry(histoleg2, extralabel2, "l")

#### GRADIENT BOOSTED REWEIGHTING ####

#Saving data variables in format accepred by the reweighter
#Data array
data_var1 = (tree1.AsMatrix(["lcplus_PT", "lcplus_ETA", "nTracks"]))
#data_var1 = data_var1.flatten()

#Data sWeights
data_sw = tree1.AsMatrix(["Actual_signalshape_Norm_sw"])
data_sw = data_sw.flatten()

#Some sanity check prints
print('Data sWeights matrix is ')
print(data_sw)
print('The dimentionality of the matrix is ')
print(numpy.ndim(data_sw))

#Saving MC variables in format accepred by the reweighter
#MC array
mc_var1 = tree2.AsMatrix(["lcplus_PT", "lcplus_ETA", "nTracks"])
#print(mc_var1.__type__())
print(numpy.array(mc_var1.tolist())[:,0])
#mc_var1 = mc_var1.flatten()

#This is where the reweighter is defined
gb = GBReweighter()

#Prepare reweighting formula by computing histograms
gb.fit(mc_var1, data_var1, target_weight = data_sw)

#Returns corrected weights. Result is computed as original_weight * reweighter_multipliers.
#Variable for new sWeights
mc_data_weights = gb.predict_weights(mc_var1)
#print('the corrected weights are')
#print(mc_data_weights)

#Plotting the comparison of the data sWeights, MC and newly reweighted MC
data_new = numpy.array(data_var1.tolist())[:,0]
#print(data_new)
mc_new = numpy.array(mc_var1.tolist())[:,0]
#print(mc_new)


plt.hist(mc_new, label = 'MC', bins = 100, alpha = 0.5 , edgecolor = "green", density = True)
plt.hist(mc_new, weights = mc_data_weights, label = 'MC rew', bins = 100, alpha = 0.5 , edgecolor = "red", density = True)
plt.hist(data_new, weights = data_sw, label='Data sW', bins = 100, alpha = 0.5, edgecolor = "blue", density = True)
plt.legend(loc='upper right')
plt.show()


#### FINAL PLOT COMPARISON OF MC AND DATA THAT WILL BE SAVED AS PDF IN THE DIRECTORY DEFINED AT THE BEGINNING ####
for variable in variables_to_plot:
    if variable == "lcplus_TAU":
        Plot_comparison.plot_comparison(variable,tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right", Override=True, xmin=0, xmax=2E-3)
    elif variable == "lcplus_OWNPV_CHI2":
        Plot_comparison.plot_comparison(variable,tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right", Override=True, xmin=0, xmax=90)
    elif variable == "lcplus_IPCHI2_OWNPV":
        Plot_comparison.plot_comparison(variable,tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right", Override=True, xmin=0, xmax=10)
    else:
        savehists = plot_comparison(variable, tree1=tree1, tree2=tree2, cuts1=cuts1, cuts2=cuts2, normalized=True, legendLocation="Right")
        print(savehists)
        
    savehists[1].DrawNormalized("H")
    savehists[0].DrawNormalized("SAMEH")

    leg.Draw("SAME")  
    if variable in variables_to_plot_with_line:
        point = variables_to_plot_with_line[variable]
        line = ROOT.TLine(point, 0, point, 0.08)
        line.SetLineColor(2)
        line.SetLineStyle(2)
        line.SetLineWidth(1)
        line.Draw("SAME")
    c1.Update()
    c1.Draw()
    graph_name = (name + variable +".pdf")
    filepath = directory
    fullpath = os.path.join(filepath, graph_name)
    c1.SaveAs(fullpath)