
magnet = 'MagDown'
pythia = "Pythia8"
year = '2017'
eventtype = 25103064

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

#eventtype = 25103064 # New created Lc
#eventtype = 26103091 # New created Xic - no longer used
#eventtype = 26103092 # New created Xic with new lifetime


restripversion = "" # empty = no restripping
if(eventtype == 25103006 and year == '2012') :
  restripversion = 'stripping21'

MDST = False
Turbo = False # False means simply use stripping output
lines = ["LambdaCForPromptCharm"]

if(year in ['2016','2017','2018'] and eventtype in [25203000, 26103090]) : 
  Turbo = True

if(eventtype == 25103064 or eventtype == 26103091 or eventtype == 26103092) : # new MC
  MDST = True
  if(year in ['2015','2016','2017','2018']) :
    Turbo = True # does not work: missing destination '/Event/AllStreams/MC/Particles' 
    lines = ["Hlt2CharmHad{0}pToPpKmPipTurbo".format(p) for p in ["Lc","Xic"] ] # does not work: contains 0 events?

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
tuple_Lc2pKpi = DecayTreeTuple( 'tuple_Lc2pKpi' )
tuple_Lc2pKpi.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream,line) for line in lines]
tuple_Lc2pKpi.Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC'
tuple_Lc2pKpi.addBranches({ 'lcplus' : '[Lambda_c+ -> p+ K- pi+]CC',
                            'pplus'  : '[Lambda_c+ -> ^p+ K- pi+]CC',
                            'kminus' : '[Lambda_c+ -> p+ ^K- pi+]CC',
                            'piplus' : '[Lambda_c+ -> p+ K- ^pi+]CC' })
#tuple_Lc2pKpi.setDescriptorTemplate('${lcplus}[Lambda_c+ -> ${pplus}p+ ${kminus}K- ${piplus}pi+]CC') # new setup, replaces Decay and addBranches 
# add DecayTreeFitter tool to constrain origin to PV and refit kinematics
dtftool = tuple_Lc2pKpi.lcplus.addTupleTool('TupleToolDecayTreeFitter/PVConstrainedDTF')
dtftool.constrainToOriginVertex = True


# Build combinations ourselves instead of depending on stripping output.
if(Turbo) :
  from PhysConf.Selections import AutomaticData
  Pions = AutomaticData('Phys/StdAllNoPIDsPions/Particles')
  Kaons = AutomaticData('Phys/StdAllLooseKaons/Particles')
  Protons = AutomaticData('Phys/StdAllLooseProtons/Particles')

  # Cuts should not be tighter than the Hlt2 Turbo line:
  #https://gitlab.cern.ch/lhcb/Hlt/blob/2018-patches/Hlt/Hlt2Lines/python/Hlt2Lines/CharmHad/Lines.py#L727
  #https://gitlab.cern.ch/lhcb/Hlt/blob/2018-patches/Hlt/Hlt2Lines/python/Hlt2Lines/CharmHad/Lines.py#L130
  from Configurables import CombineParticles
  Lc2pKpi_combiner = CombineParticles(
    'Lc2pKpi_combiner',
     DecayDescriptor='[Lambda_c+ -> p+ K- pi+]cc',
     DaughtersCuts={'p+' : '(PT > 200*MeV) & (P > 2000*MeV) & (MIPCHI2DV(PRIMARY) > 4)',
                    'K-' : '(PT > 200*MeV) & (P > 2000*MeV) & (MIPCHI2DV(PRIMARY) > 4)',
                    'pi+': '(PT > 200*MeV) & (P > 2000*MeV) & (MIPCHI2DV(PRIMARY) > 4)'},
     CombinationCut="( (ADAMASS('Lambda_c+') < 110*MeV) | (ADAMASS('Xi_c+') < 110*MeV) )",
     MotherCut="( (VFASPF(VCHI2/VDOF)< 10) & ( (ADMASS('Lambda_c+') < 80*MeV) | (ADMASS('Xi_c+') < 80*MeV) ) )"
  )

  from PhysConf.Selections import Selection, SelectionSequence
  Lc2pKpi_sel = Selection('Lc2pKpi_sel', Algorithm=Lc2pKpi_combiner, RequiredSelections=[Pions, Kaons, Protons] )
  Lc2pKpi_seq = SelectionSequence('Lc2pKpi_seq', TopSelection=Lc2pKpi_sel)
  DaVinci().UserAlgorithms += [ Lc2pKpi_seq.sequence() ]
  tuple_Lc2pKpi.Inputs = [ Lc2pKpi_sel.outputLocation() ]

#if(Turbo and year in ["2015","2016"]) : tuple_Lc2pKpi.InputPrimaryVertices = '/Event/Turbo/Primary'



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
 "Hlt2CharmHadLcpToPpKmPipTurboDecision", "Hlt2CharmHadXicpToPpKmPipTurboDecision",
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
    striptool.TriggerList = ["Stripping{0}Decision".format(line) for line in lines]

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


# MCParticle ntuple
from Configurables import MCDecayTreeTuple
mctuple = MCDecayTreeTuple( 'mctuple_Lc2pKpi' )
mctuple.Decay = '[Lambda_c+ => ^p+ ^K- ^pi+]CC'
mctuple.Branches = { 'lcplus' : '[Lambda_c+ => p+ K- pi+]CC',
                     'pplus'  : '[Lambda_c+ => ^p+ K- pi+]CC',
                     'kminus' : '[Lambda_c+ => p+ ^K- pi+]CC',
                     'piplus' : '[Lambda_c+ => p+ K- ^pi+]CC' }
#mctuple.ToolList = ["MCTupleToolKinematic"]
mctuple.ToolList = ['TupleToolRecoStats', 'MCTupleToolAngles', 'MCTupleToolHierarchy', 
                    'MCTupleToolKinematic', 'MCTupleToolPrimaries', 'MCTupleToolReconstructed', 
                    "MCTupleToolInteractions" ]
DaVinci().UserAlgorithms += [mctuple]





# Filter events for faster processing
#from PhysConf.Filters import LoKi_Filters
#if (restripversion == "" and Turbo == False) :
#  fltrs = LoKi_Filters (
#      STRIP_Code = "HLT_PASS_RE('Stripping{0}Decision')".format(lines[0]) # note: only for one line!
#          )
#  DaVinci().EventPreFilters = fltrs.filters('Filters')



DaVinci().InputType="DST"
DaVinci().DataType = year
DaVinci().Simulation = True
DaVinci().Lumi = False
DaVinci().PrintFreq = 1000
DaVinci().EvtMax = -1
DaVinci().DDDBtag  = dddbtag 
DaVinci().CondDBtag = conddbtag

if(MDST) :
  DaVinci().RootInTES = "/Event/{0}".format(stream)
  DaVinci().InputType="MDST"
  

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
  MyLines = [ 'Stripping' + lines[0] ]  # note: only for one line!
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



'''
# Fix MC truth for Turbo (https://twiki.cern.ch/twiki/bin/view/LHCb/MakeNTupleFromTurbo#Monte_Carlo_truth)
if(Turbo) :
  from TeslaTools import TeslaTruthUtils

  # Location of the truth tables for PersistReco objects
  if (year in ["2017","2018"]) :
    relations = TeslaTruthUtils.getRelLocs() + [TeslaTruthUtils.getRelLoc(''), 'Relations/Hlt2/Protos/Charged' ]
  if (year in ["2015","2016"]) :
    relations = [TeslaTruthUtils.getRelLoc(hlt2_line + '/')]

  mc_tools = [
        'MCTupleToolKinematic',
        # ...and any other tools you'd like to use
  ]
  for dtt in tuples :
    TeslaTruthUtils.makeTruth(dtt, relations, mc_tools)
'''

