
# Before running on the grid, please ensure that:
# - davinci options file has no input file specified
# - davinci options file has the same event settings (magnet, pythia, year, eventtype)

magnet = "MagDown"
pythia = "Pythia8"
year = "2012"

# Select eventtype. Find details for eventtypes at http://lhcbdoc.web.cern.ch/lhcbdoc/decfiles/
#eventtype = 25103036 # Lc -> p K pi but with changed mass/momenta (from Xi_c decay).
#eventtype = 25103000 # Lc -> p K pi with DecProdCut
#eventtype = 25103006 # Lc -> p K pi with TightCut
#eventtype = 25103010 # Xic -> p K pi with TightCut
eventtype = 15264011 # Lb -> (Lc -> p K pi) pi with DecProdCut
#eventtype = 15164101 # Lb -> (Xi_c -> L pi) pi with DecProdCut



############################################################
 
# Find the right data file options from the database
execfile('./options/mcdatabase.py')
datafile = getFileFromDB(eventtype, [magnet,pythia,year])
dataloc = datafile[0]

jobname = "MC_Lc2pKpi_{0}_{1}_{2}_{3}".format(eventtype, magnet, pythia, year)
j = Job(name=jobname)
j.comment = "{0}_{1}_{2}_{3}".format(eventtype, magnet, pythia, year)
j.inputfiles = [ LocalFile('./options/mcdatabase.py') ] # for DaVinci db tags

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
j.application.options = ['./options/davinci_options_MC.py']
  
#j.backend = Local()
j.backend = Dirac()

j.outputfiles = [LocalFile('*.root'), LocalFile('stdout')]
#j.outputfiles = [DiracFile('*.root')] # stores on SE. Can download to local with j.outputfiles.get().

j.splitter = SplitByFiles(filesPerJob=1)
#j.do_auto_resubmit = True


# Get data to run over
print "Querying for data {0}".format(dataloc)
query = BKQuery(dataloc)

if not query: 
  print "Query resulted in nonetype, please check if location is correct."
  #j.remove()
else :
  j.inputdata = query.getDataset()

  j.submit()
  #queues.add(j.submit)

