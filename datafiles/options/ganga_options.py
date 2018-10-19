
# Before running on the grid, please ensure that:
# - davinci options file has no input file specified
# - options file has no subfolder in output files specified


name = "Lc2pKpi"
year = "17"
magnet = "MagDown"
reco = "17"
stripping = "29r2"

eventtype = "90000000" # real data
streamsuffix = "CHARM.MDST"


j = Job(name="{0}_20{1}_{2}_reco{3}_stripping{4}".format(name,year,magnet,reco,stripping))
j.comment = "20{0}_{1}_reco{2}_stripping{3}".format(year,magnet,reco,stripping)

# Set up the required application to run
app = "DaVinci"
version = "v44r5"
projectpath = "/project/bfys/jdevries/cmtuser"
from os import path
if not path.isdir("{0}/{1}Dev_{2}".format(projectpath,app,version)) :
  prepareGaudiExec('DaVinci','v44r5', myPath=projectpath)
myApp = GaudiExec()
j.application = GaudiExec()
j.application.directory = "{0}/{1}Dev_{2}".format(projectpath,app,version) 
j.application.options = ['./options/davinci_options.py']
  
#j.backend = Local()
j.backend = Dirac()

j.outputfiles = [LocalFile('*.root'), LocalFile('stdout')]
#j.outputfiles = [DiracFile('*.root')] # stores on SE. Can download to local with j.outputfiles.get().

j.splitter = SplitByFiles(filesPerJob=5)
#j.do_auto_resubmit = True


# Get data to run over
#j.application.readInputData('./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/Collision17_MagDown_Reco17_Stripping29r2_CHARM_full_mdst.py')
dataloc = '/LHCb/Collision{0}/Beam6500GeV-VeloClosed-{1}/Real Data/Reco{2}/Stripping{3}/{4}/{5}'.format(year,magnet,reco,stripping,eventtype,streamsuffix)
print "Querying for data {0}".format(dataloc)
query = BKQuery(dataloc)

if not query: 
  print "Query resulted in nonetype, please check if location is correct."
  #j.remove()
else :
  j.inputdata = query.getDataset()

  j.submit()
  #queues.add(j.submit)

