
subjobs = 2
filedir = "../datafiles/ganga/4"
filename = "charm_29r2_g.root"
excludedjobs = []

from ROOT import TChain

tree = TChain("tuple_Lc2pKpi/DecayTree")

for job in range(subjobs) :
  if not job in excludedjobs :
    print "- Adding subjob {0}".format(job)
    tree.Add("{0}/{1}/output/{2}".format(filedir,job,filename))

tree.Draw("lcplus_M")


