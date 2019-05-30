import ROOT, os
from ROOT import TChain, TCanvas, TH1

ROOT.gStyle.SetOptStat(0)

def getMCCuts (particle):
    IDcuts = "abs(pplus1_ID)==211 && abs(kminus_ID)==321 && abs(pplus0_ID)==2212 && abs(lcplus_ID)==4122"
    if particle == "Lc":
        BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 50)"
        return IDcuts + "&&" + BKGCAT
    elif particle == "Xic":
        BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 10 || lcplus_BKGCAT == 50)"
        return IDcuts + "&&" + BKGCAT

def getDataCuts ():
    cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && piplus_ProbNNpi > 0.5 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000 && pplus_PIDp > 0 && kminus_PIDK > 0"
    return cuts

def getBackgroundCuts(particle):
    if particle == "Lc":
        cuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)"
    elif particle == "Xic":
        cuts = "lcplus_MM > 2400 && lcplus_MM < 2450 || lcplus_MM > 2490"
    return cuts

def plot_comparison(varname, tree1, tree2, bins=100, cuts1 = "1==1", cuts2 = "1==1", extralabel1="", extralabel2="", normalized=True, legendLocation="Right", Yaxis_range_1=0, Yaxis_range_2=1000, Override = False, xmin=0, xmax=0) :
    
    print("Plotting comparison of {0} between trees {1} and {2}".format(varname, tree1.GetName(), tree2.GetName()))
    print("- Using cuts1: {0}".format(cuts1))
    print("- Using cuts2: {0}".format(cuts2))

    name1 = tree1.GetName() + str(extralabel1)
    name2 = tree2.GetName() + str(extralabel2)
    
    ROOT.gStyle.SetOptStat(0)
    
    if Override == False:
        xmin = tree1.GetMinimum(varname)
        xmax = tree1.GetMaximum(varname)
        if tree2.GetMinimum(varname) < xmim:
            xmin = tree2.GetMinimum(varname)
        if tree2.GetMaximum(varname) > xmax:
            xmax = tree2.GetMaximum(varname)
    
    tree1.Draw(varname+">>histogram1("+str(bins)+","+str(xmin)+","+str(xmax)+")", cuts1)
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


    # allow normalized drawing
    if(normalized) :
        histogram2.DrawNormalized()
        histogram1.DrawNormalized("same")
    else :
        histogram2.Draw()
        histogram1.Draw("same")
    #the legend needs to be fixed so that it can be removed from the scripts that use this function
    if(legendLocation=="Right") :
        leg = ROOT.TLegend(0.11 + 0.59, 0.77, 0.3 + 0.59, 0.89)
        #leg = ROOT.TLegend(0.11,0.77,0.3,0.89)
        leg.SetHeader("Legend")
        leg.AddEntry(histogram1, "Upper band background", "l")
        leg.AddEntry(histogram2, "Monte Carlo simulation", "l")
        leg.Draw("same")

    #c1.Update()
    #c1.Draw()
                                            
    return

subjobs = 1843

#File dir for data, uncomment the version for each person
#Calo
#pwd="/Users/simoncalo/LHCb_data/datafiles/first_batch/ganga/"
#Pawley
pwd="/home/chris/Documents/LHCB/Data/"

def getDirectory(user):
    if user == "Simon":
        directory = "/Users/simoncalo/LHCb_data/datafiles/"
    elif user == "Chris":
        directory = "/home/chris/Documents/LHCB/Data/"
    elif user == "Jacco":
        directory = ""
    elif user == "Nikhef":
        directory = "/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/"
    return directory

#File dir for MC, uncomment the version(s) for each person
#Calo
#mcpwd="/Users/simoncalo/LHCb_data/datafiles/Lc_MC_datafiles_2/ganga/"
#ximcpwd="/Users/simoncalo/LHCb_data/datafiles/XIc_MC_datafiles_1/ganga/"
#ximc2pwd="/Users/simoncalo/LHCb_data/datafiles/XIc_MC_datafiles_2/ganga/"
#mcbmcpwd="/Users/simoncalo/LHCb_data/datafiles/MC_B->Lc_datafiles/ganga/"
#mctippwd="/Users/simoncalo/LHCb_data/datafiles/where/simon/puts/it/"
#mcbtippwd="/Users/simoncalo/LHCb_data/datafiles/where/simon/puts/it/"
#Pawley
mcbtippwd=mctippwd=mcpwd=ximcpwd=ximc2pwd=mcbmcpwd=pwd=directory

#user = "Nikhef"
#if user = "Nikhef":
#    pwd = getDirectory(user)
#    subjobs= 1843

#filedir = pwd+"4_reduced"
filedire = pwd+"31"
#filename = "charm_29r2_g.root"
filename = "Lc2pKpiTuple.root"
excludedjobs = []


tree = TChain("tuple_Lc2pKpi/DecayTree")

def datatree():
    for job in range(subjobs) :
        #tree.Add("{0}/{1}/output/{2}".format(filedir,job,filename))
        tree.Add(filedir + "/" + str(job) + "/output/" + filename)
    return tree

Lc_MC_filedir = mcpwd+"15"
Lc_MC_filename = "MC_Lc2pKpiTuple_25103006.root"

Lc_MC_tree = TChain("tuple_Lc2pKpi/DecayTree")

def Lc_MC_datatree():
    for job in range(63) :
        if not job in excludedjobs :
            Lc_MC_tree.Add("{0}/{1}/output/{2}".format(Lc_MC_filedir,job,Lc_MC_filename))
    return Lc_MC_tree

Xic_MC_filedir_1 = ximcpwd+"17"
Xic_MC_filename_1 = "MC_Lc2pKpiTuple_25103029.root"

Xic_MC_tree_1 = TChain("tuple_Lc2pKpi/DecayTree")

def Xic_MC_datatree_1 ():
    for job in range(27) :
        if not job in excludedjobs :
            #print ("- Adding subjob {0}".format(job))
            Xic_MC_tree_1.Add("{0}/{1}/output/{2}".format(Xic_MC_filedir_1,job,Xic_MC_filename_1))

Xic_MC_filedir_2 = ximc2pwd+"18"
Xic_MC_filename_2 = "MC_Lc2pKpiTuple_25103036.root"

Xic_MC_tree_2 = TChain("tuple_Lc2pKpi/DecayTree")

def Xic_MC_datatree_2():
    for job in range(25) :
        if not job in excludedjobs :
            #print ("- Adding subjob {0}".format(job))
            Xic_MC_tree_2.Add("{0}/{1}/output/{2}".format(Xic_MC_filedir_2,job,Xic_MC_filename_2))

Lb_MC_filedir =mcbmcpwd+ "14"
Lb_MC_filename = "MC_Lc2pKpiTuple_15264011.root"

Lb_MC_tree = TChain("tuple_Lc2pKpi/DecayTree")

def Lb_MC_datatree():
    for job in range(26) :
        if not job in excludedjobs :
            Lb_MC_tree.Add("{0}/{1}/output/{2}".format(Lb_MC_filedir,job,Lb_MC_filename))


            
Lb_TIP_MC_filedir =mcbtippwd+ "23"
Lb_TIP_MC_filename = "MC_Lc2pKpiTuple_15264011.root"

Lb_TIP_MC_tree = TChain("tuple_Lc2pKpi/DecayTree")

def Lb_TIP_MC_datatree():
    for job in range(26) :
        if not job in excludedjobs :
            Lb_TIP_MC_tree.Add("{0}/{1}/output/{2}".format(Lb_TIP_MC_filedir,job,Lb_TIP_MC_filename))

Lc_TIP_MC_filedir = mctippwd+"22"
Lc_TIP_MC_filename = "MC_Lc2pKpiTuple_25103006.root"

Lc_TIP_MC_tree = TChain("tuple_Lc2pKpi/DecayTree")

def Lc_TIP_MC_datatree():
    for job in range(63) :
        if not job in excludedjobs :
            Lc_TIP_MC_tree.Add("{0}/{1}/output/{2}".format(Lc_TIP_MC_filedir,job,Lc_TIP_MC_filename))
    return Lc_TIP_MC_tree
