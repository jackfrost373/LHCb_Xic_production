
# Before running on the grid, please ensure in the davinci options that:
# - it has no input file specified
# - it has no subfolder in output files specified
# - #events in options file is set to -1
# - the decay considered matches the input files ganga will look for


#name = "Lc2pKpi"
name = "Lc2pKpi_noipchi2"
streamsuffix = "CHARM.MDST"
#name = "Lb2LcMuX"
#streamsuffix = "SEMILEPTONIC.DST"

year = "17"  # Make sure the year matches the DaVinci options!
magnet = "MagDown"


#################################

yeardict = { 
    "18" : { "reco" : "18",  "stripping" : "34"  , "energy" : "6500" },
    "17" : { "reco" : "17",  "stripping" : "29r2", "energy" : "6500" },
    "16" : { "reco" : "16",  "stripping" : "28r1", "energy" : "6500" },
    "15" : { "reco" : "15a", "stripping" : "24r1", "energy" : "6500" },
    "12" : { "reco" : "14",  "stripping" : "21"  , "energy" : "4000" },
    "11" : { "reco" : "14",  "stripping" : "21r1", "energy" : "3500" } }

reco      = yeardict[year]["reco"]
stripping = yeardict[year]["stripping"]
energy    = yeardict[year]["energy"]


eventtype = "90000000" # real data

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

#j.outputfiles = [LocalFile('*.root'), LocalFile('stdout')]
j.outputfiles = [DiracFile('*.root')] # stores on SE. Can download to local with j.outputfiles.get().

j.splitter = SplitByFiles(filesPerJob=5, ignoremissing = True)
#j.do_auto_resubmit = True


# Get data to run over
#j.application.readInputData('./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/Collision17_MagDown_Reco17_Stripping29r2_CHARM_full_mdst.py')
dataloc = '/LHCb/Collision{0}/Beam{1}GeV-VeloClosed-{2}/Real Data/Reco{3}/Stripping{4}/{5}/{6}'.format(year,energy,magnet,reco,stripping,eventtype,streamsuffix)
print "Querying for data {0}".format(dataloc)
query = BKQuery(dataloc)

if not query: 
  print "Query resulted in nonetype, please check if location is correct."
  #j.remove()
else :
  j.inputdata = query.getDataset()

  j.submit()
  #queues.add(j.submit)

