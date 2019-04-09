#!/bin/bash

# function to test if ganga and davinci are compatibally configured.
function test_equal () {
  davincitype=`grep "$1" options/davinci_options_MC.py`
  gangatype=`grep "$1" options/ganga_options_MC.py`
  if [ "$davincitype" == "$gangatype" ]; then 
    return 1 
  else 
    echo "Error: mismatch between ganga and davinci MC options. Please check."
    echo $davincitype
    echo $gangatype
    return 0 
  fi
}



# Run simulation over grid. Please ensure the same eventType, magnet, year and pythia version!
#test_equal "^eventtype = [0-9]*" 
#if [[ $? -eq 0 ]] ; then return 0 ; fi
#ganga ./options/ganga_options_MC.py | tee logs/gangaRun_MC.log



# Run real data over grid. Please configure options first!
ganga ./options/ganga_options.py | tee logs/gangaRun.log 


# Download local dst from the grid for testing. Look up the LFN from the Dirac bookkeeping.
#lhcb-proxy-init
#lb-run LHCbDirac dirac-dms-get-file /lhcb/LHCb/Collision17/CHARM.MDST/00071700/0000/00071700_00000137_1.charm.mdst

# Inspect TES locations inside dst
#lb-run Bender/latest dst-dump -f -n 5000 ./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/00071700_00000137_1.charm.mdst


# Run over local dst to test ntuple production [data]
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options.py /data/bfys/jdevries/dst/Collision17_MagDown_Reco17_Stripping29r2_CHARM/includeLocal.py | tee logs/davinciRun.log
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options.py /data/bfys/jdevries/dst/Collision16_MagDown_Reco16_Stripping28r1_SEMILEPTONIC/includeLocal.py


# Run over local dst to test ntuple production [MC]
## for local MC: be sure to set eventtype to 25103006 and change dir of mcdatabase 
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options_MC.py ./data/MC_2012_MagDown_Pythia8_Sim08a_Reco14_25103006_ALLSTREAMS/includeLocal.py | tee logs/davinciMCRun.log

#mv *.root output/

# Inspect output ntuple
#lb-run ROOT root -l output/Lc2pKpiTuple.root

