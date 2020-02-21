import ROOT, sys, os
from ROOT import TChain
from Imports import getMCCuts

jobs = raw_input("Give the job number on which you want to chain every subjob together and get the number of entries:")

parsJob = jobs.split(',')

for job in parsJob:

        if (int(job) >= 95 and int(job) <= 108):
                run = 2
        else:
             	run = 1

        XicCuts = getMCCuts("Xic",run)
        LcCuts = getMCCuts("Lc",run)
        print(XicCuts)

        tree = TChain("tuple_Lc2pKpi/DecayTree")
        PATH = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga/" + job
        for subdir, dirs, files in os.walk(PATH):
                for file in files:
                        if "-histos" not in file:
                                #print subdir
                                tree.Add(os.path.join(subdir,file))

        if(run == 2):
                XicTree = tree.CopyTree(XicCuts)
                LcTree = tree.CopyTree(LcCuts)
                print("The nb of entries for job " + job + " is " + str(XicTree.GetEntries()+LcTree.GetEntries()))
        else:
             	print("The nb of entries for job " + job + " is " + str(tree.GetEntries()))

