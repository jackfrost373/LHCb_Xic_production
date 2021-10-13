import ROOT, sys, os
from ROOT import TChain
from Imports import getMCCuts, getDataCuts

XicMassRange = [2380, 2560]
LcMassRange = [2200, 2380]
nbin = 100

GRAPHS = True

if(GRAPHS == True):
	c1 = ROOT.TCanvas("c1","c1",1200,700)

jobs = raw_input("Give the job numbers (separated by a coma) on which you want to chain every subjob together and get the number of entries:")

parsJob = jobs.split(',')

for job in parsJob:

        if (int(job) >= 95 and int(job) <= 108):
            run = 2

            XicMCCuts = "{0} && {1}".format(getMCCuts("Xic",run), "lcplus_MM > 2375")
            XicDataCuts = getDataCuts(run)

            LcMCCuts = "{0} && {1}".format(getMCCuts("Lc",run), "lcplus_MM < 2375")
            LcDataCuts = getDataCuts(run)

        else:
            run = 1
		
            XicDataCuts = "{0} && {1}".format(getDataCuts(run), "lcplus_MM > 2375")
            LcDataCuts = "{0} && {1}".format(getDataCuts(run), "lcplus_MM < 2375")

        tree = TChain("tuple_Lc2pKpi/DecayTree")
        PATH = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/" + job
        for subdir, dirs, files in os.walk(PATH):
                for file in files:
                        if "-histos" not in file:
                                #print subdir
                                tree.Add(os.path.join(subdir,file))

        if(run == 2):
            XicTree = tree.CopyTree(XicMCCuts)
            XicTree = XicTree.CopyTree(XicDataCuts)

            LcTree = tree.CopyTree(LcMCCuts)
            LcTree = LcTree.CopyTree(LcDataCuts)

            print("The nb of entries for job " + job + " is (Xic: " + str(XicTree.GetEntries()) + ";Lc: " + str(LcTree.GetEntries())+ ")")		
        if(GRAPHS == True):
            XicMasshist = ROOT.TH1F("XicMasshist","Histogram of Xic mass, job: "+ job ,nbin,XicMassRange[0],XicMassRange[1])
            LcMasshist = ROOT.TH1F("LcMasshist","Histogram of Lc mass, job: "+ job ,nbin,LcMassRange[0],LcMassRange[1])

            LcTree.Draw("lcplus_MM>>LcMasshist")
            c1.SaveAs(job + "_Lc_MC.pdf")
            XicTree.Draw("lcplus_MM>>XicMasshist")
            c1.SaveAs(job + "_Xic_MC.pdf")

        del XicMasshist
        del LcMasshist
       
    elif(run == 1):
        XicTree = tree.CopyTree(XicDataCuts)
        LcTree = tree.CopyTree(LcDataCuts)
		
        print("The nb of entries for job " + job + " is (Xic: " + str(XicTree.GetEntries()) + ";Lc: " + str(LcTree.GetEntries())+ ")")

        if(GRAPHS == True):
            XicMasshist = ROOT.TH1F("XicMasshist","Histogram of Xic mass, job: "+ job ,nbin,XicMassRange[0],XicMassRange[1])
            LcMasshist = ROOT.TH1F("LcMasshist","Histogram of Lc mass, job: "+ job ,nbin,LcMassRange[0],LcMassRange[1])

            LcTree.Draw("lcplus_MM>>LcMasshist")
            c1.SaveAs(job + "_Lc_MC.pdf")
            XicTree.Draw("lcplus_MM>>XicMasshist")
            c1.SaveAs(job + "_Xic_MC.pdf")

        del XicMasshist
        del LcMasshist