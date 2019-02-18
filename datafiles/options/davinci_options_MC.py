
# define data type
magnet = "MagDown"
pythia = "Pythia8"
year = "2012"

# Select eventtype. Find details for eventtypes at http://lhcbdoc.web.cern.ch/lhcbdoc/decfiles/
#eventtype = 25103000 # Lc -> p K pi with DecProdCut
eventtype = 25103006 # Lc -> p K pi with TightCut

#eventtype = 25103010 # Xic -> p K pi with TightCut, but Lc used, with corrected mass 2468.
#eventtype = 25103029 # Xic -> p K pi with TightCut, uses more loose tau and pt cuts. Lc will be used. Is v2 of 25103036?
#eventtype = 25103036 # Xic -> p K pi with Tightcut, but with Lc used as decay with corrected mass 2468. changed lifetime/pt as well.
#eventtype = 25103046 # Xic -> p K pi with Tightcut, Lc is used to mimic Xic, 'Xic partner for 25103006'.

#eventtype = 15264011 # Lb -> (Lc -> p K pi) pi with DecProdCut
#eventtype = 15164101 # Lb -> (Xi_c -> L pi) pi with DecProdCut
#eventtype = 16264060 # Xibc -> (Xi_c -> p K pi) pi, Xibc lifetime = 0.4ps, DecProdCut, DaugInLhcb 


############################################################

# Find the right data file options from the database
#execfile('./options/mcdatabase.py') # for local running only.
execfile('mcdatabase.py') # needs to be in ganga inputsandbox
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
#tuple_Lc2pKpi.Decay = '[Lambda_c+ -> ^p+ ^K- ^pi+]CC'
tuple_Lc2pKpi.setDescriptorTemplate('${lcplus}[Lambda_c+ -> ${pplus}p+ ${kminus}K- ${pplus}pi+]CC')  # keep 'wrong' naming for consistency
#tuple_Lc2pKpi.setDescriptorTemplate('${lcplus}[Lambda_c+ -> ${pplus}p+ ${kminus}K- ${piplus}pi+]CC') # correct naming
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
tupletools.append("TupleToolMCTruth")    # MC Truth information
tupletools.append("TupleToolMCBackgroundInfo") # BKGCAT information

triggerlist = ["Hlt1TrackAllL0Decision", "Hlt1TrackMVADecision",
 "Hlt2CharmHadD2HHHDecision",
 "L0HadronDecision","L0MuonDecision"]

for tup in tuples:
    # add tools
    tup.ToolList =  tupletools[:]

    # add trigger and stripping decision info
    tistostool = tup.addTupleTool("TupleToolTISTOS")
    tistostool.FillL0 = True 
    tistostool.FillHlt1 = True
    tistostool.FillHlt2 = True
    tistostool.TriggerList = triggerlist
    striptool = tup.addTupleTool("TupleToolStripping")
    striptool.TriggerList = ["Stripping{0}Decision".format(line1)]

    # add custom variables with functors
    hybridtool = tup.addTupleTool('LoKi::Hybrid::TupleTool')
    hybridtool.Variables = {'ETA' : '0.5 * log( (P+PZ)/(P-PZ) )' ,
                            'PHI' : 'atan2(PY,PX)',
                            'RAPIDITY' : '0.5 * log( (sqrt(P^2+M^2)+PZ)/(sqrt(P^2+M^2)-PZ) )'}

    
    # refit PVs with exclusion of our tracks of interest
    tup.ReFitPVs = True

    # add ntuple to the list of running algorithms
    DaVinci().UserAlgorithms += [tup]

              

# Filter events for faster processing
from PhysConf.Filters import LoKi_Filters
fltrs = LoKi_Filters (
        STRIP_Code = "HLT_PASS_RE('Stripping{0}Decision')".format(line1)
        )
DaVinci().EventPreFilters = fltrs.filters('Filters')


#stream = "AllStreams"
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

