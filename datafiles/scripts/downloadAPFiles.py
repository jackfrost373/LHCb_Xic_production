
import os, json, subprocess, sys

basedir = "/dcache/bfys/cpawley/ntuples/LcAnalysis/ganga"

jsonfile = "analysisproduction.json"

name_jobs = ["My_2017_MagDown_turbo_job"] # this nane has to match analysis production database

jobs = [1] # this array makes a fake "ganga-style" job (must be as big as the above array)

with open(jsonfile) as file:
  dict = json.load(file)

job_count = 0

for job in name_jobs:

  ganga_job = jobs [job_count]

  result = subprocess.run (['xrdfs root://eoslhcb.cern.ch/ ls /{0}'.format(dict[job].split("//")[2].replace('*.root',''))],shell=True, stdout=subprocess.PIPE)

  files_to_download = result.stdout.decode(sys.stdout.encoding)

  subjob = 1
  
  for file in files_to_download.split('\n'):
    if len(file)>0:
      if not os.path.isdir(os.path.join(basedir,str(ganga_job),str(subjob))) : os.makedirs(os.path.join(basedir,str(ganga_job),str(subjob)))
      print("Trying to get file {0} and placing it in {1}/{2}/{3}".format(file.split('lhcb/LHCb')[1], basedir,ganga_job, subjob))
      os.system('lb-dirac dirac-dms-get-file /lhcb/LHCb{0} -D {1}/{2}/{3}'.format (file.split('lhcb/LHCb')[1], basedir, ganga_job, subjob ))
      
      folder = (r"{0}/{1}/{2}".format(basedir, ganga_job, subjob))
      for file_name in os.listdir(folder):
        os.rename(folder+"/"+file_name , folder + "/{0}".format("Lc2pKpiTuple.root"))
    subjob += 1
  
  job_count += 1
