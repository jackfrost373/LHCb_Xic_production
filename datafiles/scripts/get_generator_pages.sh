
# OR just check out the index files online, e.g. http://lhcbdoc.web.cern.ch/lhcbdoc/STATISTICS/SIM08STAT/index.shtml

eventtype=26103090



echo "Searching for ${eventtype}"

curdir=`pwd`
tmpdir=/tmp/jdevries/genstats
mkdir -p $tmpdir
cd $tmpdir

# Download all gen. pages - perhaps run every once in a while.
#wget -np -r -R "index.html*"  -e robots=off http://lhcbdoc.web.cern.ch/lhcbdoc/STATISTICS/ 

#grep $eventtype lhcbdoc.web.cern.ch/lhcbdoc/STATISTICS/*/*/*
grep $eventtype -R .


cd $curdir
