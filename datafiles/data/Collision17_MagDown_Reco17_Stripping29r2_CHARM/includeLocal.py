
# input
from Gaudi.Configuration import *
from GaudiConf import IOHelper
IOHelper('ROOT').inputFiles(['PFN:./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/00071700_00000137_1.charm.mdst'], clear=True)


# output
from Configurables import DaVinci
fName = "charm_29r2" 
DaVinci().TupleFile = "output/{0}.root".format(fName)
DaVinci().HistogramFile = 'output/{0}-histos.root'.format(fName)
