
source /cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_87/gcc/4.9.3/x86_64-slc6/setup.sh
source /cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_87/ROOT/6.08.02/x86_64-slc6-gcc49-opt/bin/thisroot.sh
export RAPIDSIM_ROOT=`pwd`/RapidSim/build

./RapidSim/build/src/RapidSim.exe Lc2pKpi 100 

