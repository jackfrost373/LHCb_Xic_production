
year = '2017'
# when running ganga, make sure year matches the dst year

from Configurables import DaVinci, LHCbApp
from Configurables import DecayTreeTuple, TupleToolDecay
from DecayTreeTuple.Configuration import *


decay = "Lc2pKpi"
#decay = "Lc2pKpi_noipchi2"
#decay = "Lb2LcMuX"

events = -1   # for all. Default for ganga!
#events = 10000


####################
# Define settings according to decay

Turbo = False

if (decay == "Lc2pKpi") :
  # (prompt) Lc -> p K pi 
  striplines  = ["LambdaCForPromptCharm"]
  stream      = "Charm"
  decaystring = '${lcplus}[Lambda_c+ -> ${pplus}p+ ${kminus}K- ${piplus}pi+]CC'
  inputtype   = "MDST"

  if year in ["2016","2017","2018"] :
    Turbo = True
    stream = "Charmspec"
    striplines = ["Hlt2CharmHadLcpToPpKmPipTurbo", "Hlt2CharmHadXicpToPpKmPipTurbo"]

if (decay == "Lb2LcMuX") :
  striplines  = ["B2DMuNuX_Lc", "B2DMuNuX_Lc_FakeMuon"]
  stream      = "Semileptonic"
  decaystring = '${lambdab0}[Lambda_b0 -> ${lambdacplus}( Lambda_c+ -> ${kminus}K- ${pplus}p+ ${piplus}pi+ ) ${muplus}[mu+]cc ]CC'
  inputtype   = "DST"

if (decay == "Lc2pKpi_noipchi2") :
  # (prompt) Lc -> p K pi 
  striplines  = ["LambdaCLooseChi2IPForPromptCharm"]
  stream      = "Charm"
  decaystring = '${lcplus}[Lambda_c+ -> ${pplus}p+ ${kminus}K- ${piplus}pi+]CC'
  inputtype   = "MDST"


####################
## Define ntuples

mytuple = DecayTreeTuple( 'tuple_{0}'.format(decay) )
if(inputtype=="MDST") : mytuple.Inputs = ['Phys/{0}/Particles'.format(stripline) for stripline in striplines ]
if(Turbo)             : mytuple.Inputs = ['{0}/Particles'.format(stripline) for stripline in striplines ]
if(inputtype=="DST")  : mytuple.Inputs = ['/Event/{0}/Phys/{1}/Particles'.format(stream,stripline) for stripline in striplines ] 
mytuple.setDescriptorTemplate( decaystring )

# add DecayTreeFitter tool to constrain origin to PV and refit kinematics
if( "Lc2pKpi" in decay ) :
  dtftool = mytuple.lcplus.addTupleTool('TupleToolDecayTreeFitter/PVConstrainedDTF')
  dtftool.constrainToOriginVertex = True
if( decay == "Lb2LcMuX" ) :
  dtftool = mytuple.lambdab0.addTupleTool('TupleToolDecayTreeFitter/PVConstrainedDTF_Lb')
  dtftool.constrainToOriginVertex = True
  dtftool2 = mytuple.lambdacplus.addTupleTool('TupleToolDecayTreeFitter/PVConstrainedDTF_Lc')
  dtftool2.constrainToOriginVertex = True


tuples = [mytuple]

# Define common tuple tools
tupletools = []
tupletools.append("TupleToolKinematic")  # Mass and momenta
tupletools.append("TupleToolPid")        # PID info
tupletools.append("TupleToolANNPID")    # ProbNN for specific MC tunes
tupletools.append("TupleToolGeometry")   # ENDVERTEX, OWNPV, IP, FD, DIRA 
tupletools.append("TupleToolAngles")     # CosTheta, angle between daughter tracks
tupletools.append("TupleToolEventInfo")  # Runnr, eventnr, gpstime, magpol, BX
tupletools.append("TupleToolPropertime") # Proper lifetime TAU in ns 
tupletools.append("TupleToolTrackInfo")  # TRACK info
tupletools.append("TupleToolPrimaries")  # nPV, PV pos, PVnTracks
tupletools.append("TupleToolRecoStats")  # nPVs, nTracks, etc.

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
    #striptool = tup.addTupleTool("TupleToolStripping")
    #striptool.TriggerList = ["Stripping{0}Decision".format(stripline) for stripline in striplines]

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

              

# Filter events for faster processing. (Note the case for multiple lines)
if not Turbo : 
  from PhysConf.Filters import LoKi_Filters
  fltrs = LoKi_Filters (
          STRIP_Code = "HLT_PASS_RE('Stripping{0}.*Decision')".format(striplines[0])
          )
  DaVinci().EventPreFilters = fltrs.filters('Filters')


if(inputtype=="MDST") : DaVinci().RootInTES = "/Event/{0}".format(stream)
if(Turbo)             : DaVinci().RootInTES = "/Event/{0}/Turbo".format(stream)
DaVinci().InputType = inputtype
DaVinci().DataType = year
DaVinci().Simulation = False
DaVinci().Lumi = True
DaVinci().PrintFreq = 1000
DaVinci().EvtMax = events
DaVinci().Turbo = Turbo
#DaVinci().DDDBtag   = "dddb-20170721-3"         # Gauss-2016 (sim09b)
#DaVinci().CondDBtag = "sim-20170721-2-vc-md100" # Gauss-2016 (sim09b)
#DaVinci().appendToMainSequence(tuples)

# output
fName = "{0}Tuple".format(decay) 
#DaVinci().TupleFile = "output/{0}.root".format(fName)
#DaVinci().HistogramFile = 'output/{0}-histos.root'.format(fName)
DaVinci().TupleFile = "{0}.root".format(fName)
DaVinci().HistogramFile = '{0}-histos.root'.format(fName)

