
import os, json, subprocess, sys

basedir = "/dcache/bfys/cpawley/ntuples/LcAnalysis/ganga"

jsonfile = "analysisproduction.json"

name_jobs = ["My_2017_MagDown_turbo_job"] #this nane has to match analysis production database

jobs = [1] #this array makes a fake "ganga-style" job (must be as big as the above array)

with open(jsonfile) as file:
  dict = json.load(file)

job_count = 0

for job in name_jobs:

  ganga_job = jobs [job_count]

  #to do - parse the URL from the JSON file!

  result = subprocess.run (['xrdfs root://eoslhcb.cern.ch/ ls /{0}'.format(dict[job].split("//")[2].replace('*.root',''))],shell=True, stdout=subprocess.PIPE)

  files_to_download = result.stdout.decode(sys.stdout.encoding)

  subjob = 1
  
  for file in files_to_download.split('\n'):
    if len(file)>0:
      if not os.path.isdir(os.path.join(basedir,str(ganga_job),str(subjob))) : os.makedirs(os.path.join(basedir,str(ganga_job),str(subjob)))
      print("Trying to get file {0} and placing it in {1}/{2}/{3}".format(file.split('lhcb/LHCb')[1], basedir,ganga_job, subjob))
      subprocess.run (['lb-dirac dirac-dms-get-file /lhcb/LHCb{0} -D {1}/{2}/{3}'.format (file.split('lhcb/LHCb')[1], basedir, ganga_job, subjob )])
      subprocess.run (['cd {0}/{1}/{2} | mv *.root Lc2pKpiTuple.root'.format(basedir, ganga_job, subjob)])
    subjob += 1
  
  job_count += 1

'''
for jobi in joblist :
  print("******************\n* Doing job {0}\n*******************".format(jobi))
  downloadjobdir = "{0}/{1}".format(basedir,jobi) 
  job = jobs(jobi)

  nSuccess = 0
  nFailed = 0
  nNotCompleted = 0

  #for subjob in job.subjobs.select(status='completed') :
  for subjobi in range(len(job.subjobs)) :
    subjob = job.subjobs(subjobi)
    if(subjob.status=="completed") :
      #lfn = subjob.backend.getOutputDataLFNs()[1].lfn

      flist = subjob.outputfiles.get(DiracFile)
      print("Downloading Diracfile for job {0} - sj {1}".format(jobi, subjobi))

      downloadsubjobdir = "{0}/{1}".format(downloadjobdir,subjobi)
      if not os.path.isdir(downloadsubjobdir) : os.makedirs(downloadsubjobdir)

      for f in flist :
        if("histos" in f.namePattern) : continue
        f.localDir = downloadsubjobdir
        try :
          f.get()
          nSuccess += 1
        #except GangaDiracError :
        except :
          print("Caught GangaDiracError --> failed to get file")
          nFailed += 1

    else :
      nNotCompleted += 1


  print("\n********************************")
  print(" Report for Job {0}: ".format(jobi))
  print(" nSuccess: {0} ({1:.1f} %)".format(nSuccess, float(nSuccess)/len(job.subjobs)*100))
  print(" nFailed: {0} ({1:.1f} %)".format(nFailed, float(nFailed)/len(job.subjobs)*100))
  print(" nNotCompleted: {0} ({1:.1f} %)".format(nNotCompleted, float(nNotCompleted)/len(job.subjobs)*100))
  print("********************************\n")



  # resubmit failed jobs
  if not (nSuccess == len(job.subjobs)) : 
    print("Resubmitting subjobs with the 'failed' status...")
    job.subjobs.select(status='failed').resubmit()
'''