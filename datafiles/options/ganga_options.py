
year = '2017'
magnet = 'MagDown'

# Before running on the grid, please ensure in the davinci options that:
# - it has no input file specified
# - it has no subfolder in output files specified
# - #events in options file is set to -1
# - the decay considered matches the input files ganga will look for

name = "Lc2pKpi"
#name = "Lc2pKpi_noipchi2"
streamsuffix = "CHARM.MDST"

#name = "Lb2LcMuX"
#streamsuffix = "SEMILEPTONIC.DST"

Turbo = True

#################################

yeardict = {}
yeardict["2011"] = { "recsel" : "Reco14/Stripping21r1" , "energy" : "3500" , "eventtype" : "90000000" }
yeardict["2012"] = { "recsel" : "Reco14/Stripping21"   , "energy" : "4000" , "eventtype" : "90000000" }
yeardict["2015"] = { "recsel" : "Reco15a/Stripping24r1", "energy" : "6500" , "eventtype" : "90000000" }
#yeardict["2016"] = { "recsel" : "Reco16/Stripping28r1" , "energy" : "6500" , "eventtype" : "90000000" }
#yeardict["2017"] = { "recsel" : "Reco17/Stripping29r2" , "energy" : "6500" , "eventtype" : "90000000" }
#yeardict["2018"] = { "recsel" : "Reco18/Stripping34"   , "energy" : "6500" , "eventtype" : "90000000" }
if(Turbo and streamsuffix == "CHARM.MDST") :
  #yeardict["2015"] = { "recsel" : "Turbo02",  "energy" : "6500" , "eventtype" : "94000000" , "suffix" : "TURBO.MDST" }
  yeardict["2016"] = { "recsel" : "Turbo03a", "energy" : "6500" , "eventtype" : "94000000" , "suffix" : "CHARMSPECPRESCALED.MDST" }
  yeardict["2017"] = { "recsel" : "Turbo04",  "energy" : "6500" , "eventtype" : "94000000" , "suffix" : "CHARMSPEC.MDST" }
  yeardict["2018"] = { "recsel" : "Turbo05",  "energy" : "6500" , "eventtype" : "94000000" , "suffix" : "CHARMSPEC.MDST" }

recsel    = yeardict[year]["recsel"]
energy    = yeardict[year]["energy"]
eventtype = yeardict[year]["eventtype"]
if( yeardict[year]["suffix"] ) : streamsuffix = yeardict[year]["suffix"]


j = Job(name="{0}_{1}_{2}_{3}".format(name,year,magnet,recsel))
j.comment = "{0}_{1}_{2}".format(year,magnet,recsel)

# Set up the required application to run
app = "DaVinci"
version = "v44r5"
projectpath = "/project/bfys/jdevries/cmtuser"
from os import path
if not path.isdir("{0}/{1}Dev_{2}".format(projectpath,app,version)) :
  prepareGaudiExec('DaVinci','v44r5', myPath=projectpath)
j.application = GaudiExec()
j.application.directory = "{0}/{1}Dev_{2}".format(projectpath,app,version) 
j.application.options = ['./options/davinci_options.py']
  
#j.backend = Local()
j.backend = Dirac()

#j.outputfiles = [LocalFile('*.root'), LocalFile('stdout')]
j.outputfiles = [DiracFile('*.root')] # stores on SE. Can download to local with j.outputfiles.get().

filesperjob = 5
if(Turbo) : filesperjob = 25
j.splitter = SplitByFiles(filesPerJob=filesperjob, ignoremissing = True)
#j.do_auto_resubmit = True


# Get data to run over
#j.application.readInputData('./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/Collision17_MagDown_Reco17_Stripping29r2_CHARM_full_mdst.py')
dataloc = '/LHCb/Collision{0}/Beam{1}GeV-VeloClosed-{2}/Real Data/{3}/{4}/{5}'.format(year[2:],energy,magnet,recsel,eventtype,streamsuffix)
print("Querying for data {0}".format(dataloc))
query = BKQuery(dataloc)

if not query: 
  print("Query resulted in nonetype, please check if location is correct.")
  #j.remove()
else :
  j.inputdata = query.getDataset()

  j.submit()
  #queues.add(j.submit)

