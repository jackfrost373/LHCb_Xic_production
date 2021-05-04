import ROOT
from ROOT import TChain, TFile

def plot_comparison(varname, tree1, tree2, bins=100, cuts1 = "1==1", cuts2 = "1==1", extralabel1="", extralabel2="", normalized=True, legendLocation="Right", Yaxis_range_1=0, Yaxis_range_2=1000, Override = False, xmin=0, xmax=0) :

    print("Plotting comparison of {0} between trees {1} and {2}".format(varname, tree1.GetName(), tree2.GetName()))
    print("- Using cuts1: {0}".format(cuts1))
    print("- Using cuts2: {0}".format(cuts2))

    name1 = tree1.GetName() + str(extralabel1)
    name2 = tree2.GetName() + str(extralabel2)

    ROOT.gStyle.SetOptStat(0)

    fileloc="/data/bfys/cpawley/sWeights/2017_MagDown/Xic_total_sWeight_swTree.root"
    f=ROOT.TFile.Open(fileloc,"READONLY")
    tree3 = f.Get("dataNew")


    if Override == False:
        xmin = tree1.GetMinimum(varname)
        xmax = tree1.GetMaximum(varname)
        if tree2.GetMinimum(varname) < xmin:
            xmin = tree2.GetMinimum(varname)
        if tree2.GetMaximum(varname) > xmax:
            xmax = tree2.GetMaximum(varname)
    tree1.AddFriend("dataNew","/data/bfys/cpawley/sWeights/2017_MagDown/Xic_total_sWeight_swTree.root")
    tree1.Draw(varname+">>histogram1("+str(bins)+","+str(xmin)+","+str(xmax)+")", cuts1, "dataNew.sw_sig")
    print("Sanity check, friend tree contains{0} entries, and the data file contains {1} entries".format(tree3.GetEntries(), tree1.GetEntries(cuts1)))
    #tree1.Draw(varname+">>histogram1("+str(bins)+","+str(xmin)+","+str(xmax)+")", cuts1)
    tree2.Draw(varname+">>histogram2("+str(bins)+","+str(xmin)+","+str(xmax)+")", cuts2)
    histogram1 = ROOT.gDirectory.Get("histogram1")
    histogram2 = ROOT.gDirectory.Get("histogram2")

    histogram1.SetTitle(varname)
    histogram1.GetXaxis().SetTitle(varname)
    histogram1.SetLineColor(2) # red
    histogram1.SetLineWidth(1)
    histogram2.SetTitle(varname)
    histogram2.SetLineColor(9) # blue
    histogram2.SetLineWidth(1)


    # allow normalized drawing but check which to draw first
    if(normalized) :
        if ((histogram1.GetMaximum()/histogram1.GetEntries())<(histogram2.GetMaximum()/histogram2.GetEntries())):
            histogram2.DrawNormalized()
            histogram1.DrawNormalized("same")
        else:
            histogram1.DrawNormalized()
            histogram2.DrawNormalized("same")
    else :
        histogram2.Draw()
        histogram1.Draw("same")

#the legend needs to be fixed so that it can be removed from the scripts that use this function
    if(legendLocation=="Right") :
        leg = ROOT.TLegend(0.11 + 0.59, 0.77, 0.3 + 0.59, 0.89)
        leg.SetHeader("Legend")
        leg.AddEntry(histogram1, "Upper band background", "l")
        leg.AddEntry(histogram2, "Monte Carlo simulation", "l")
        leg.Draw("same")
                         
    return


