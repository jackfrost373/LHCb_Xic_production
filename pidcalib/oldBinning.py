"""This file is an example of a user-defined binning scheme file, which """ \
"""can be passed as an argument to the multi-track calibration scripts.
The methods for constructing binning schema are defined in """ \
"""$PIDPERFSCRIPTSROOT/python/PIDPerfScripts/binning.py."""

from PIDPerfScripts.Binning import *
from PIDPerfScripts.Definitions import *

# example binning scheme using for K/pi/p
for trType in GetRICHPIDPartTypes() :
    # momentum
    AddBinScheme(trType, 'P', 'BsMuMu_BDTCalib', 5000, 200000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 9300) # R1 Kaon threshold
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 15600) # R2 Kaon threshold
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 17675)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 20000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 23000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 26000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 29650)
    AddUniformBins(trType, 'P', 'BsMuMu_BDTCalib', 14, 30000, 100000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 125000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib', 150000)



    # eta
    AddBinScheme(trType, 'ETA', 'BsMuMu_BDTCalib', 1.5, 5)
    AddUniformBins(trType, 'ETA', 'BsMuMu_BDTCalib', 3, 2.5, 4)

    # nTracks
    AddBinScheme(trType, 'nTracks', 'BsMuMu_BDTCalib', 0, 800)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib', 50)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib', 100)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib', 200)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib', 400)

# SECOND BINNING SCHEME USED FOR BDT/RESOLUTION CALIBRATION BsMuMu
for trType in GetRICHPIDPartTypes() :
    # momentum
    AddBinScheme(trType, 'P', 'BsMuMu_BDTCalib2', 5000, 200000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 9300) # R1 Kaon threshold
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 12000) 
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 15600) # R2 Kaon threshold
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 17675)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 20000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 21500)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 23000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 24500)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 26000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 27500)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 29650)
    AddUniformBins(trType, 'P', 'BsMuMu_BDTCalib2', 28, 30000, 100000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 110000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 125000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 135000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 150000)
    AddBinBoundary(trType, 'P', 'BsMuMu_BDTCalib2', 170000)


    # eta
    AddBinScheme(trType, 'ETA', 'BsMuMu_BDTCalib2', 1.5, 5)
    AddUniformBins(trType, 'ETA', 'BsMuMu_BDTCalib2', 7, 1.5, 5)

    # nTracks
    AddBinScheme(trType, 'nTracks', 'BsMuMu_BDTCalib2', 0, 800)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib2', 50)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib2', 75)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib2', 100)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib2', 150)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib2', 200)
    AddBinBoundary(trType, 'nTracks', 'BsMuMu_BDTCalib2', 400)



# BINNING SCHEME FROM BHH ANALYSIS
for trType in GetRICHPIDPartTypes() :
    # momentum
    AddBinScheme(trType, 'P', 'BHH_Binning', 0, 500000)
    AddUniformBins(trType, 'P', 'BHH_Binning', 2,      0, 10000 )
    AddUniformBins(trType, 'P', 'BHH_Binning', 45, 10000, 100000)
    AddUniformBins(trType, 'P', 'BHH_Binning', 20,100000, 150000)
    AddUniformBins(trType, 'P', 'BHH_Binning',  4,150000, 500000)

    # eta
    AddBinScheme(trType, 'ETA', 'BHH_Binning', 1., 6)
    AddUniformBins(trType, 'ETA', 'BHH_Binning', 10, 1., 6)

    # nTracks
    AddBinScheme(trType, 'nTracks', 'BHH_Binning', 0, 600)
    AddBinBoundary(trType, 'nTracks', 'BHH_Binning', 100)
    AddBinBoundary(trType, 'nTracks', 'BHH_Binning', 200)
    AddBinBoundary(trType, 'nTracks', 'BHH_Binning', 300)
    AddBinBoundary(trType, 'nTracks', 'BHH_Binning', 400)
    
    AddBinScheme(trType, 'nTracks_Brunel', 'BHH_Binning', 0, 600)
    AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning', 100)
    AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning', 200)
    AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning', 300)
    AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning', 400)




# attempt at BHH with reduced bins
for trType in GetRICHPIDPartTypes() :

  AddBinScheme(  trType, 'P', 'BHH_Binning_run1run2', 3000, 500000)
  AddUniformBins(trType, 'P', 'BHH_Binning_run1run2',  2,   3000,  10000)
  AddUniformBins(trType, 'P', 'BHH_Binning_run1run2', 15,  10000,  20000)
  AddUniformBins(trType, 'P', 'BHH_Binning_run1run2', 15,  20000,  50000)
  AddUniformBins(trType, 'P', 'BHH_Binning_run1run2', 10,  50000, 100000)
  AddUniformBins(trType, 'P', 'BHH_Binning_run1run2',  5, 100000, 300000)
  AddUniformBins(trType, 'P', 'BHH_Binning_run1run2',  3, 300000, 500000)
  AddBinBoundary(trType, 'P', 'BHH_Binning_run1run2', 9300)  # R1 Kaon threshold
  AddBinBoundary(trType, 'P', 'BHH_Binning_run1run2', 15600) # R2 Kaon threshold
    
  AddBinScheme(trType,   'ETA', 'BHH_Binning_run1run2', 1.5, 5)
  AddUniformBins(trType, 'ETA', 'BHH_Binning_run1run2', 6, 1.5, 5)

  # nTracks
  AddBinScheme(trType,   'nTracks', 'BHH_Binning_run1run2', 0, 600)
  AddBinBoundary(trType, 'nTracks', 'BHH_Binning_run1run2', 100)
  AddBinBoundary(trType, 'nTracks', 'BHH_Binning_run1run2', 200)
  AddBinBoundary(trType, 'nTracks', 'BHH_Binning_run1run2', 300)
  
  AddBinScheme(trType,   'nTracks_Brunel', 'BHH_Binning_run1run2', 0, 600)
  AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning_run1run2', 100)
  AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning_run1run2', 200)
  AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning_run1run2', 300)


# attempt at BHH with drastically reduced bins
for trType in GetRICHPIDPartTypes() :

  AddBinScheme(  trType, 'P', 'BHH_Binning_reduced', 3000, 500000)
  AddUniformBins(trType, 'P', 'BHH_Binning_reduced',  2,   3000,  10000)
  AddUniformBins(trType, 'P', 'BHH_Binning_reduced',  5,  10000,  20000)
  AddUniformBins(trType, 'P', 'BHH_Binning_reduced',  5,  20000,  50000)
  AddUniformBins(trType, 'P', 'BHH_Binning_reduced',  4,  50000, 100000)
  AddUniformBins(trType, 'P', 'BHH_Binning_reduced',  4, 100000, 300000)
  AddUniformBins(trType, 'P', 'BHH_Binning_reduced',  2, 300000, 500000)
    
  AddBinScheme(trType,   'ETA', 'BHH_Binning_reduced', 1.5, 5)
  AddUniformBins(trType, 'ETA', 'BHH_Binning_reduced', 6, 1.5, 5)

  # nTracks
  AddBinScheme(trType,   'nTracks', 'BHH_Binning_reduced', 0, 600)
  AddBinBoundary(trType, 'nTracks', 'BHH_Binning_reduced', 100)
  AddBinBoundary(trType, 'nTracks', 'BHH_Binning_reduced', 200)
  AddBinBoundary(trType, 'nTracks', 'BHH_Binning_reduced', 300)
  AddBinBoundary(trType, 'nTracks', 'BHH_Binning_reduced', 400)
  
  AddBinScheme(trType,   'nTracks_Brunel', 'BHH_Binning_reduced', 0, 600)
  AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning_reduced', 100)
  AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning_reduced', 200)
  AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning_reduced', 300)
  AddBinBoundary(trType, 'nTracks_Brunel', 'BHH_Binning_reduced', 400)


'''
# DEFAULT PIDCALIB BINNING
for trType in GetRICHPIDPartTypes() :
    # momentum
    AddBinScheme(trType, 'P', 'DLLKpi', 3000, 100000)
    AddBinBoundary(trType, 'P', 'DLLKpi', 9300) # R1 Kaon threshold
    AddBinBoundary(trType, 'P', 'DLLKpi', 15600) # R2 Kaon threshold
    AddUniformBins(trType, 'P', 'DLLKpi', 15, 19000, 100000)
    
    # momentum
    AddBinScheme(trType, 'Brunel_P', 'DLLKpi', 3000, 100000)
    AddBinBoundary(trType, 'Brunel_P', 'DLLKpi', 9300) # R1 Kaon threshold
    AddBinBoundary(trType, 'Brunel_P', 'DLLKpi', 15600) # R2 Kaon threshold
    AddUniformBins(trType, 'Brunel_P', 'DLLKpi', 15, 19000, 100000)

    # eta
    AddBinScheme(trType, 'ETA', 'DLLKpi', 1.5, 5)
    AddUniformBins(trType, 'ETA', 'DLLKpi', 4, 1.5, 5)
    
    # eta
    AddBinScheme(trType, 'Brunel_ETA', 'DLLKpi', 1.5, 5)
    AddUniformBins(trType, 'Brunel_ETA', 'DLLKpi', 4, 1.5, 5)

    # nTracks
    AddBinScheme(trType, 'nTracks', 'DLLKpi', 0, 500)
    AddBinBoundary(trType, 'nTracks', 'DLLKpi', 50)
    AddBinBoundary(trType, 'nTracks', 'DLLKpi', 200)
    AddBinBoundary(trType, 'nTracks', 'DLLKpi', 300)
    
    # nTracks_Brunel (offline version)
    AddBinScheme(trType, 'nTracks_Brunel', 'DLLKpi', 0, 500)
    AddBinBoundary(trType, 'nTracks_Brunel', 'DLLKpi', 50)
    AddBinBoundary(trType, 'nTracks_Brunel', 'DLLKpi', 200)
    AddBinBoundary(trType, 'nTracks_Brunel', 'DLLKpi', 300)
'''

# BINNING SCHEME FOR LC XIC
for trType in GetRICHPIDPartTypes() :
    # momentum
    AddBinScheme(trType,   'P', 'Xic_Binning', 0, 500000)
    AddUniformBins(trType, 'P', 'Xic_Binning', 6,      0, 10000 )
    AddUniformBins(trType, 'P', 'Xic_Binning', 45, 10000, 100000)
    AddUniformBins(trType, 'P', 'Xic_Binning', 20,100000, 150000)
    AddUniformBins(trType, 'P', 'Xic_Binning',  4,150000, 500000)

    # eta
    AddBinScheme(trType, 'ETA', 'Xic_Binning', 1., 6)
    AddUniformBins(trType, 'ETA', 'Xic_Binning', 10, 1., 6)

    # nTracks
    AddBinScheme(trType, 'nTracks', 'Xic_Binning', 0, 600)
    AddBinBoundary(trType, 'nTracks', 'Xic_Binning', 100)
    AddBinBoundary(trType, 'nTracks', 'Xic_Binning', 200)
    AddBinBoundary(trType, 'nTracks', 'Xic_Binning', 300)
    AddBinBoundary(trType, 'nTracks', 'Xic_Binning', 400)
    
    AddBinScheme(trType, 'nTracks_Brunel', 'Xic_Binning', 0, 600)
    AddBinBoundary(trType, 'nTracks_Brunel', 'Xic_Binning', 100)
    AddBinBoundary(trType, 'nTracks_Brunel', 'Xic_Binning', 200)
    AddBinBoundary(trType, 'nTracks_Brunel', 'Xic_Binning', 300)
    AddBinBoundary(trType, 'nTracks_Brunel', 'Xic_Binning', 400)

