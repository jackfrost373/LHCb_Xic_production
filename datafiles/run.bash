#!/bin/bash

# make sure to setup the LHCb software with
#  . /cvmfs/lhcb.cern.ch/group_login.sh
# make sure to init your grid proxy with
# lhcb-proxy-init

# Set env for local running
LbLogin -c x86_64-slc6-gcc62-opt

# function to test if ganga and davinci are compatibally configured.
#function test_equal () {
#  davincitype=`grep "$1" options/davinci_options_MC.py`
#  gangatype=`grep "$1" options/ganga_options_MC.py`
#  if [ "$davincitype" == "$gangatype" ]; then 
#    return 1 
#  else 
#    echo "Error: mismatch between ganga and davinci MC options. Please check."
#    echo $davincitype
#    echo $gangatype
#    return 0 
#  fi
#}



# Run real data over grid. Please configure options first!
#ganga ./options/ganga_options.py 


# Mass submit real data over grid
#magnets=( "MagUp" "MagDown" )
#magnets=( "MagDown" )
#years=( "2011" "2012" "2015" "2016" "2017" "2018" )
#years=( "2016" "2017" "2018" )
#years=( "2017" )
#decays=( "Lc2pKpi" ) # takes both Lc and Xic from the stripping line
#decays=( "Lc2pKpi" "Xic2pKpi" ) # only needed for run2 Turbo, as it splits Lc and Xic into different streams
#decays=( "Xic2pKpi" ) 
#decays=( "Lb2LcMuX" "Xib2XicMuX" )
#for magnet in "${magnets[@]}"; do
#  for year in "${years[@]}"; do
#    for decay in "${decays[@]}"; do
#      sed -i "2s/.*/year = '${year}'/" ./options/davinci_options.py
#      sed -i "3s/.*/decay = '${decay}'/" ./options/davinci_options.py
#      sed -i "2s/.*/year = '${year}'/" ./options/ganga_options.py
#      sed -i "3s/.*/decay = '${decay}'/" ./options/ganga_options.py
#      sed -i "4s/.*/magnet = '${magnet}'/" ./options/ganga_options.py
#      ganga ./options/ganga_options.py
#    done
#  done
#done



# Run simulation over grid. Please ensure the same eventType, magnet, year and pythia version!
#test_equal "^eventtype = [0-9]*" 
#if [[ $? -eq 0 ]] ; then return 0 ; fi
#ganga ./options/ganga_options_MC.py 


# Mass submit simulation over grid
#magnets=( "MagUp" "MagDown" )
magnets=( "MagDown" )
#years=( "2016" "2017" "2018" )
#years=( "2016" "2017" )
years=( "2017" )
#eventtypes=( 25203000 26103090 ) #25203000 = new Lc, 26103090 = new Xic
#eventtypes=( 25103006 25103029 ) #25103006 = old Lc, 25103029 = old Xic
#eventtypes=( 25103006 )
#eventtypes=( 25103029 ) 
#eventtypes=( 25103064 ) # new Lc 2020
#eventtypes=( 26103091 ) # new Xic 2020
eventtypes-( 25103064 26103091 )
for magnet in "${magnets[@]}"; do
  for year in "${years[@]}"; do
    for eventtype in "${eventtypes[@]}"; do
      for file in ./options/davinci_options_MC.py ./options/ganga_options_MC.py ; do
        sed -i "2s/.*/magnet = '${magnet}'/" $file
        sed -i "4s/.*/year = '${year}'/" $file
        sed -i "5s/.*/eventtype = $eventtype/" $file
      done
      ganga ./options/ganga_options_MC.py
    done
  done
done





# Download local dst from the grid for testing. Look up the LFN from the Dirac bookkeeping.
#lhcb-proxy-init
#lb-run LHCbDirac dirac-dms-get-file /lhcb/LHCb/Collision17/CHARM.MDST/00071700/0000/00071700_00000137_1.charm.mdst
#lb-run LHCbDirac dirac-dms-get-file /lhcb/LHCb/Collision17/CHARMSPEC.MDST/00066595/0000/00066595_00000413_1.charmspec.mdst
#lb-run LHCbDirac dirac-dms-get-file /lhcb/LHCb/Collision17/CHARMCHARGED.MDST/00066595/0000/00066595_00000992_1.charmcharged.mdst
#lb-run LHCbDirac dirac-dms-get-file /lhcb/MC/2017/ALLSTREAMS.DST/00090974/0000/00090974_00000379_7.AllStreams.dst

# Inspect TES locations inside dst
#lb-run Bender/latest dst-dump -f -n 5000 ./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/00071700_00000137_1.charm.mdst
#lb-run Bender/latest dst-dump -f -n 100 -d 2016 LFN:/lhcb/MC/2016/ALLSTREAMS.DST/00091515/0000/00091515_00000038_7.AllStreams.dst


# Run over local dst to test ntuple production [data]
#LbLogin -c x86_64-centos7-gcc62-opt
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options.py /data/bfys/jdevries/dst/Collision17_MagDown_Reco17_Stripping29r2_CHARM/includeLocal.py | tee logs/davinciRun.log
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options.py ./data/Collision17_MagDown_Turbo04_CHARMSPEC/includeLocal.py | tee logs/davinciRun.log
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options.py ./data/Collision17_MagDown_Turbo04_CHARMMULTIBODY/includeLocal.py | tee logs/davinciRun.log
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options.py /data/bfys/jdevries/dst/Collision16_MagDown_Reco16_Stripping28r1_SEMILEPTONIC/includeLocal.py



# Run over local dst to test ntuple production [MC]
## for local MC: be sure to set eventtype in davinci options manually, and copy mcdatabase to current folder 
#LbLogin -c x86_64-centos7-gcc62-opt
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options_MC.py ./data/MC_2017_MagDown_Pythia8_Sim09f_Reco17_26103090_ALLSTREAMS/includeLocal.py
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options_MC.py ./data/MC_2017_MagDown_Pythia8_Sim09h_Reco17_Turbo04a_Stripping29r2_25103064/includeLocal.py
# if restripping: run with correct DaVinci version (see http://lhcbdoc.web.cern.ch/lhcbdoc/davinci/releases/ , https://twiki.cern.ch/twiki/bin/view/Main/ProcessingPasses )
#LbLogin -c x86_64-slc6-gcc48-opt
#lb-run DaVinci/v36r1p5 gaudirun.py ./options/davinci_options_MC.py ./data/MC_2012_MagDown_Pythia8_Sim08a_Reco14_25103006_ALLSTREAMS/includeLocal.py | tee logs/davinciMCRun.log

#mv *.root output/

# Inspect output ntuple
#lb-run ROOT root -l output/Lc2pKpiTuple.root

