#!/bin/bash

# from https://twiki.cern.ch/twiki/bin/view/LHCb/DownloadAndBuild
# Note: if files are not staged, auto request is made but might take a while. Try running again in a few hours.

#export BKPATH='/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103029/ALLSTREAMS.DST'
BKPATH='/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09f/Trig0x6139160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/26103090/ALLSTREAMS.DST'

TMPDIR=/tmp/jdevries/makeGenStats



CURDIR=`pwd`

# get scripts
mkdir -p $TMPDIR
cd $TMPDIR
lb-run LHCbDirac/v9r2p9 git lb-clone-pkg -b v4r7p3 MCStatTools
cd MCStatTools/scripts

# get the prodID from the BK path
echo "${BKPATH}"
PRODID=$(lb-run LHCbDirac/prod dirac-bookkeeping-prod4path --BK "${BKPATH}" | grep "MCSimulation" | tr -dc '0-9')
echo "prodID = ${PRODID}"

# build the MC stat page
lb-run LHCbDirac/v9r2p9 ./DownloadAndBuildStat.py $PRODID 2>&1 | tee run-${PRODID}.log
# can add '-v debug' , or '-k' (compatibility for old numbers)

echo "STAT page written in ${TMPDIR}/MCStatTools/scripts/${PRODID}"
cd $CURDIR

