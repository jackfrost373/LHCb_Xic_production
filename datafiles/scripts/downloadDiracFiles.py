
import os

#TODO: redo 40, 41 (to 329), 42 (total)
#joblist = [39,40,41,42,43, 45,46,47,48,49,50]
joblist = [47,48,49,50]

basedir = "/dcache/bfys/jdevries/ntuples/LcAnalysis/ganga"


for jobi in joblist :
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

      f = subjob.outputfiles.get(DiracFile)[1]
      print("Downloading Diracfile for job {0} - sj {1}".format(jobi, subjobi))

      downloadsubjobdir = "{0}/{1}".format(downloadjobdir,subjobi)
      if not os.path.isdir(downloadsubjobdir) : os.makedirs(downloadsubjobdir)
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
  print(" nSuccess: {0} ({1:.1f} %".format(nSuccess, float(nSuccess)/len(job.subjobs)*100))
  print(" nFailed: {0} ({1:.1f} %".format(nFailed, float(nFailed)/len(job.subjobs)*100))
  print(" nNotCompleted: {0} ({1:.1f} %".format(nNotCompleted, float(nNotCompleted)/len(job.subjobs)*100))
  print("********************************\n")

