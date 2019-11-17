
magnet = 'MagDown'
pythia = "Pythia8"
year = '2016'
eventtype = 25203000

# Before running on the grid, please ensure that:
# - davinci options file has no input file specified
# - davinci options file has the same event settings (magnet, pythia, year, eventtype)


# Select eventtype. Find details for eventtypes at http://lhcbdoc.web.cern.ch/lhcbdoc/decfiles/
#eventtype = 25103000 # Lc -> p K pi with DecProdCut
#eventtype = 25103006 # Lc -> p K pi with TightCut

#eventtype = 25103010 # Xic -> p K pi with TightCut, but Lc used, with corrected mass 2468.
#eventtype = 25103029 # Xic -> p K pi with TightCut, uses more loose tau and pt cuts. Lc will be used. Is v2 of 25103036? [DEFAULT XIC]
#eventtype = 25103036 # Xic -> p K pi with Tightcut, but with Lc used as decay with corrected mass 2468. changed lifetime/pt as well.
#eventtype = 25103046 # Xic -> p K pi with Tightcut, Lc is used to mimic Xic, 'Xic partner for 25103006'.
#eventtype = 25203000 # NEW Lc -> pKpi with Dalitz
#eventtype = 26103090 # NEW Xic -> pKpi without using Lc as proxy

#eventtype = 15264011 # Lb -> (Lc -> p K pi) pi with DecProdCut
#eventtype = 15164101 # Lb -> (Xi_c -> L pi) pi with DecProdCut
#eventtype = 16264060 # Xibc -> (Xi_c -> p K pi) pi, Xibc lifetime = 0.4ps, DecProdCut, DaugInLhcb 


############################################################
 
# Find the right data file options from the database
#execfile('./options/mcdatabase.py')  # python2
exec(open("./options/mcdatabase.py").read()) #python3, ganga v8.0.0
print("Ganga   - using options for %s %s %s %s"%(eventtype,magnet,pythia,year))
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

j.splitter = SplitByFiles(filesPerJob=3)
#j.do_auto_resubmit = True


# Get data to run over
print("Querying for data {0}".format(dataloc))
query = BKQuery(dataloc)

if not query: 
  print("Query resulted in nonetype, please check if location is correct.")
  #j.remove()
else :
  j.inputdata = query.getDataset()

  j.submit()
  #queues.add(j.submit)

