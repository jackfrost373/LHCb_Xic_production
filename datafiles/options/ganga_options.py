
# Before running on the grid, please ensure that:
# - options file has no input file specified
# - options file has correct options w.r.t. datafiles
#   ( e.g. MC-related options such as datatype, lumi, sim, stream, tupletoolMC, evtMax=-1, conddb/dddb)  

import os

name = "Lc2pKpi"
year = "17"
magnet = "MagDown"
reco = "17"
stripping = "29r2"


j = Job(name="{0}_20{1}_{2}_reco{3}_stripping{4}".format(name,year,magnet,reco,stripping))

# Set up the required application to run
app = "DaVinci"
version = "v44r5"
path = "/project/bfys/jdevries/cmtuser"
if not os.path.isdir("{0}/{1}Dev_{2}".format(path,app,version)) :
  prepareGaudiExec('DaVinci','v44r5', myPath=path)
myApp = GaudiExec()
j.application = GaudiExec()
j.application.directory = "{0}/{1}Dev_{2}".format(path,app,version) 
j.application.options = ['./options/davinci_options.py']
  
#j.backend = Local()
j.backend = Dirac()

j.outputfiles = [LocalFile('*.root'), LocalFile('stdout')]
#j.outputfiles = [DiracFile('*.root')] # stores on SE. Can download to local with j.outputfiles.get().

j.splitter = SplitByFiles(filesPerJob=5)


# Get data to run over
#j.application.readInputData('./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/Collision17_MagDown_Reco17_Stripping29r2_CHARM_full_mdst.py')
dataloc = '/LHCb/Collision{0}/Beam6500GeV-VeloClosed-{1}/Real Data/Reco{2}/Stripping{3}/90000000/CHARM.MDST'.format(year,magnet,reco,stripping)
print "Querying for data {0}".format(dataloc)
query = BKQuery(dataloc)

if not query: 
  print "Query resulted in nonetype, please check if location is correct."
  #j.remove()
else :
  j.inputdata = query.getDataset()

  j.submit()
  #queues.add(j.submit)

