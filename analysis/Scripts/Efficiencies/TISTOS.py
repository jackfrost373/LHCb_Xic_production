#################
# Doing the TISTOS method for efficiency of the trigger using sWeighted data,
# as per LHCB-PUB-2014-039
#################

import sys

sys.path.append('./')

import ROOT, getopt, os
from Imports import SWEIGHTS_PATH, DATA_jobs_Dict, getDataCuts

#Input dir is where the original ntuples are, sWeights contains our friend trees
inputdir = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga"
sweightsdir = SWEIGHTS_PATH

#Years, Mag pol and part. types hardcoded
years = [2011,2012,2015,2016,2017,2018]
magPol= ["MagUp","MagDown"]
particle_types=["Lc","Xic"]

def main(argv):
 
  ## parse the arguments from command line into arrays for us to check:
  try:
    opts,args=getopt.getopt(argv,"y:o:p:")
  except getopt.GetoptError:
    print("Incorrect Arguements used in TISTOS")
    sys.exit(2)
  options=[]
  arguments=[]
  for opt,arg in opts:
    options.append(opt)
    arguments.append(arg)
    #Check inputs are viable/match what is possible
    #What happens when we don't enter parameters? maybe we need to look for length>0 first
  print ("Checking for parameter errors")
  
  particle = arguments[options.index("-p")]
  if (particle!="Xic" and particle!="Lc" ):
    print("Wrong particle name input to TISTOS...exiting...")
    sys.exit()

  year=int(arguments[options.index("-y")])
  if year not in years:
    print("Wrong year input to TISTOS...exiting...")
    sys.exit()
  if (year==2011 or year==2012):
    run=1
    particle_id=particle
  else:
    run=2
    particle_id="Lc"

  magpol=arguments[options.index("-o")]
  if (magpol=="Up"):
    magpol="MagUp"
  elif (magpol=="Down"):
    magpol="MagDown"
  else:
    print ("Wrong magnet polarity input to TISTOS...exiting...")
    sys.exit()

  
  
#Check sufficient parameters entered

  if set(options)!=set(["-y","-o","-p"]):
    print("Entered too few parameters in TISTOS...exiting...")
    sys.exit()

#getthedata

  print("Getting the data")
  for element in DATA_jobs_Dict:
    if (DATA_jobs_Dict[element][0]=='{0}_{1}'.format(year,magpol)):
      filename=("{0}2pKpiTuple.root".format(particle_id))
      cutTotalTree=ROOT.TChain('DecayTree'.format(particle_id))
      for job in range(DATA_jobs_Dict[element][1]):
        if os.path.exists("{0}/{1}/{2}/{3}".format(inputdir,element,job,filename)):
          temp_tree=ROOT.TChain('tuple_{0}2pKpi/DecayTree'.format(particle_id))
          temp_tree.Add("{0}/{1}/{2}/{3}".format(inputdir,element,job,filename))
          cut_temp_tree=temp_tree.CopyTree(getDataCuts(run))
          wfile=ROOT.TFile.Open("temp.root","RECREATE")
          wfile.cd()
          cut_temp_tree.Write()
          wfile.Close()
          cutTotalTree.Add("temp.root")
  
  print ("The total number of entries in this nTuple is {0}".format(cutTotalTree.GetEntries()))
  

  wfile=ROOT.TFile.Open("/data/bfys/cpawley/efficiencies/TISTOS.root", "RECREATE")
  wfile.cd()
  cutTotalTree.Write()
  wfile.Close()
  os.remove("temp.root")


  print ("The total number of entries in this nTuple is {0}".format(cutTotalTree.GetEntries()))
  return

if __name__ == "__main__":
  main(sys.argv[1:])
