#!/bin/bash

# be sure to run bin/thisroot.sh or lb-run ROOT bash before execution!
# This script works perfectly on stoomboot (Nikhef) or lxplus (CERN). 
#  OSX or Ubuntu 16 LTS seem to have some dependency issues..

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


