import ROOT
from ROOT import TChain, TFile

def plot_comparison(varname, tree1, tree2, bins=100, cuts1 = "1==1", cuts2 = "1==1", extralabel1="", extralabel2="", normalized=True, legendLocation="Right", Yaxis_range_1=0, Yaxis_range_2=1000, Override = False, xmin=0, xmax=0) :

    print("Plotting comparison of {0} between trees {1} and {2}".format(varname, tree1.GetName(), tree2.GetName()))
    print("- Using cuts1: {0}".format(cuts1))
    print("- Using cuts2: {0}".format(cuts2))

    name1 = tree1.GetName() + str(extralabel1)
    name2 = tree2.GetName() + str(extralabel2)

    ROOT.gStyle.SetOptStat(0)

    fileloc="/data/bfys/cpawley/sWeights/2017_MagDown/Lc_total_sWeight_swTree.root"
    f=ROOT.TFile.Open(fileloc,"READONLY")
    tree3 = f.Get("dataNew")

    if Override == False:
        xmin = tree1.GetMinimum(varname)
        xmax = tree1.GetMaximum(varname)
        if tree2.GetMinimum(varname) < xmin:
            xmin = tree2.GetMinimum(varname)
        if tree2.GetMaximum(varname) > xmax:
            xmax = tree2.GetMaximum(varname)

    tree1.Draw(varname+">>histogram1("+str(bins)+","+str(xmin)+","+str(xmax)+")", "("+ cuts1 +")* dataNew.Actual_signalshape_Norm_sw")
    print("Sanity check, friend tree contains{0} entries, and the data file contains {1} entries".format(tree3.GetEntries(), tree1.GetEntries(cuts1)))
    tree2.Draw(varname+">>histogram2("+str(bins)+","+str(xmin)+","+str(xmax)+")", cuts2)
    histogram1 = ROOT.gDirectory.Get("histogram1")
    histogram2 = ROOT.gDirectory.Get("histogram2")
    histogram3 = ROOT.gDirectory.Get("histogram3")

    #Histogram 1
    histogram1.SetTitle(varname)
    histogram1.GetXaxis().SetTitle(varname)
    histogram1.SetLineColor(2) # red
    histogram1.SetLineWidth(1)

    #Histogram 2
    histogram2.SetTitle(varname)
    histogram2.SetLineColor(9) # blue
    histogram2.SetLineWidth(1)

    histogram1.Print()
    histogram2.Print()

    histogram1.SetDirectory(0)
    histogram2.SetDirectory(0)
    newList = [histogram1, histogram2]

    print(newList)

    #histogram1.Draw()
    #histogram2.Draw("same")

    #c2 = ROOT.TCanvas("c2")
    #histogram1.DrawNormalized("H")
    #histogram2.DrawNormalized("SAMEH")
    #c2.Update()
    #c2.SaveAs("sWeight_TEST2.pdf")
    return [histogram1, histogram2]