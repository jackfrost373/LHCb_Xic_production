
source /cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_87/gcc/4.9.3/x86_64-slc6/setup.sh
source /cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_87/ROOT/6.08.02/x86_64-slc6-gcc49-opt/bin/thisroot.sh
export RAPIDSIM_ROOT=`pwd`/RapidSim

# 10M takes about 1m30. 100M 15 minutes.

./RapidSim/build/src/RapidSim.exe Lc2pKpi 10000000 1 
./RapidSim/build/src/RapidSim.exe Lc2pKpi_tightcuts 10000000 1 

