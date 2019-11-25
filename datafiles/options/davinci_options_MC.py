
magnet = 'MagDown'
pythia = "Pythia8"
year = '2012'
eventtype = 25103006

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

restripversion = "" # empty = no restripping
if(eventtype == 25103006 and year == '2012') :
  restripversion = 'stripping21'

############################################################

# Find the right data file options from the database
#execfile('./options/mcdatabase.py') # for local running only.
#execfile('mcdatabase.py') # needs to be in ganga inputsandbox
exec(open("mcdatabase.py").read()) #python3, ganga v8.0.0
print("DaVinci - looking for files %s %s %s %s"%(eventtype,magnet,pythia,year))
datafile = getFileFromDB(eventtype, [magnet,pythia,year])
dddbtag = datafile[1]
conddbtag = datafile[2]


from Configurables import DaVinci, LHCbApp
from Configurables import DecayTreeTuple, TupleToolDecay
from DecayTreeTuple.Configuration import *


####################
## Define ntuples

# pions (test)
#tuple_pions = DecayTreeTuple( 'pions' )
#tuple_pions.Decay = '[pi+]CC'
#tuple_pions.Inputs = ["Phys/StdAllLoosePions/Particles"]
#tuple_pions.addTool(TupleToolDecay, name="Pi")
 
# (prompt) Lc -> p K pi 
stream = "AllStreams"
line1 = "LambdaCForPromptCharm"
tuple_Lc2pKpi = DecayTreeTuple( 'tuple_Lc2pKpi' )
tuple_Lc2pKpi.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream,line1)]
tuple_Lc2pKpi.Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC'
tuple_Lc2pKpi.addBranches({ 'lcplus' : '[Lambda_c+ -> p+ K- pi+]CC',
                            'pplus'  : '[Lambda_c+ -> ^p+ K- pi+]CC',
                            'kminus' : '[Lambda_c+ -> p+ ^K- pi+]CC',
                            'piplus' : '[Lambda_c+ -> p+ K- ^pi+]CC' })
#tuple_Lc2pKpi.setDescriptorTemplate('${lcplus}[Lambda_c+ -> ${pplus}p+ ${kminus}K- ${piplus}pi+]CC') # new quicker setup 
# add DecayTreeFitter tool to constrain origin to PV and refit kinematics
dtftool = tuple_Lc2pKpi.lcplus.addTupleTool('TupleToolDecayTreeFitter/PVConstrainedDTF')
dtftool.constrainToOriginVertex = True


# (detached) B -> (Lc -> p K pi) mu nu
#line = "SelLc2PKPiforCharmFromBSemi"
#tuple_b2Lc2pKpi = DecayTreeTuple( 'tuple_b2Lc2pKpi' )
#tuple_b2Lc2pKpi.Inputs = ['Phys/{0}/Particles'.format(line)]
#tuple_b2Lc2pKpi.Decay = '[ Beauty -> ^( Lambda_c+ -> ^p ^K- ^pi+ ) ^mu- ]CC'


tuples = [tuple_Lc2pKpi]

# Define common tuple tools
tupletools = []
tupletools.append("TupleToolKinematic")  # Mass and momenta
tupletools.append("TupleToolPid")        # PID info
tupletools.append("TupleToolANNPID")     # ProbNN for specific MC tunes
tupletools.append("TupleToolGeometry")   # ENDVERTEX, OWNPV, IP, FD, DIRA 
tupletools.append("TupleToolAngles")     # CosTheta, angle between daughter tracks
tupletools.append("TupleToolEventInfo")  # Runnr, eventnr, gpstime, magpol, BX
tupletools.append("TupleToolPropertime") # Proper lifetime TAU in ns 
tupletools.append("TupleToolTrackInfo")  # TRACK info
tupletools.append("TupleToolPrimaries")  # nPV, PV pos, PVnTracks
tupletools.append("TupleToolRecoStats")  # nPVs, nTracks, etc.
tupletools.append("TupleToolMCTruth")    # MC Truth information
tupletools.append("TupleToolMCBackgroundInfo") # BKGCAT information

triggerlist = ["Hlt1TrackAllL0Decision", "Hlt1TrackMVADecision",
 "Hlt2CharmHadD2HHHDecision", "Hlt2CharmHadLambdaC2KPPiDecision",
 "L0HadronDecision","L0MuonDecision","L0ElectronDecision"]

for tup in tuples:
    # add tools
    tup.ToolList =  tupletools[:]

    # add trigger and stripping decision info
    tistostool = tup.addTupleTool("TupleToolTISTOS")
    #tistostool = tup.addTupleTool("TupleToolTrigger")
    tistostool.VerboseL0   = True
    tistostool.VerboseHlt1 = True
    tistostool.VerboseHlt2 = True
    tistostool.TriggerList = triggerlist
    striptool = tup.addTupleTool("TupleToolStripping")
    striptool.TriggerList = ["Stripping{0}Decision".format(line1)]

    # add custom variables with functors
    hybridtool = tup.addTupleTool('LoKi::Hybrid::TupleTool')
    hybridtool.Variables = {'ETA' : '0.5 * log( (P+PZ)/(P-PZ) )' ,
                            'PHI' : 'atan2(PY,PX)',
                            'RAPIDITY' : '0.5 * log( (sqrt(P*P+M*M)+PZ)/(sqrt(P*P+M*M)-PZ) )',
                            'TIP' : '1e3 * (PX * (VFASPF(VY)-BPV(VY)) - PY * (VFASPF(VX)-BPV(VX))) / sqrt(PX*PX + PY*PY)'
                           }

    # refit PVs with exclusion of our tracks of interest
    tup.ReFitPVs = True

    # add ntuple to the list of running algorithms
    DaVinci().UserAlgorithms += [tup]

              

# Filter events for faster processing
from PhysConf.Filters import LoKi_Filters
if (restripversion == "") :
  fltrs = LoKi_Filters (
          STRIP_Code = "HLT_PASS_RE('Stripping{0}Decision')".format(line1)
          )
  DaVinci().EventPreFilters = fltrs.filters('Filters')



#DaVinci().RootInTES = "/Event/{0}".format(stream)
DaVinci().InputType="DST"
DaVinci().DataType = year
DaVinci().Simulation = True
DaVinci().Lumi = False
DaVinci().PrintFreq = 1000
DaVinci().EvtMax = -1
DaVinci().DDDBtag  = dddbtag 
DaVinci().CondDBtag = conddbtag

# output
fName = "MC_Lc2pKpiTuple_{0}".format(eventtype) 
#DaVinci().TupleFile = "output/{0}.root".format(fName)
#DaVinci().HistogramFile = 'output/{0}-histos.root'.format(fName)
DaVinci().TupleFile = "{0}.root".format(fName)
DaVinci().HistogramFile = '{0}-histos.root'.format(fName)



# restrip 
if not (restripversion == "") :

  # kill old stripping banks
  from Configurables import EventNodeKiller
  eventNodeKiller = EventNodeKiller('Stripkiller')
  eventNodeKiller.Nodes = [ '/Event/AllStreams', '/Event/Strip' ]

  from StrippingConf.Configuration import StrippingConf, StrippingStream
  from StrippingArchive import strippingArchive
  from StrippingArchive.Utils import buildStreams
  from StrippingSettings.Utils import strippingConfiguration

  # Note: can only  get stripping versions with certain DaVinci versions
  config  = strippingConfiguration(restripversion)
  archive = strippingArchive(restripversion)
  streams = buildStreams(stripping=config, archive=archive) 

  # get our stripping line from archive
  MyStream = StrippingStream("MyStream")
  MyLines = [ 'Stripping' + line1 ]
  for stream in streams: 
    for line in stream.lines:
      if line.name() in MyLines:
        MyStream.appendLines( [ line ] )  

  from Configurables import ProcStatusCheck
  filterBadEvents = ProcStatusCheck()
  sc = StrippingConf( Streams = [ MyStream ],
                      MaxCandidates = 2000,
                      AcceptBadEvents = False,
                      BadEventSelection = filterBadEvents )

  DaVinci().appendToMainSequence( [ eventNodeKiller, sc.sequence() ] )

  tuple_Lc2pKpi.Inputs = MyStream.outputLocations()



