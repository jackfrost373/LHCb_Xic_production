#!/bin/bash

# be sure to run bin/thisroot.sh or lb-run ROOT bash before execution!
# This script works perfectly on stoomboot (Nikhef) or lxplus (CERN). 
#  OSX or Ubuntu 16 LTS seem to have some dependency issues..

#LbLogin -c x86_64-centos7-gcc6-opt
source /cvmfs/sft.cern.ch/lcg/views/setupViews.sh LCG_96 x86_64-centos7-gcc8-opt

# lb-run ROOT bash

/bin/rm -rf ostap

git clone git://github.com/OstapHEP/ostap.git
cd ostap
mkdir build
cd build

cmake .. 
make -j8
make install
cd ../..

. ostap/install/thisostap.sh


