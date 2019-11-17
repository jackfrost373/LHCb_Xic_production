#!/bin/bash

jobID=31

gangadir=/data/bfys/jdevries/gangadir/workspace/jdevries/LocalXML/${jobID}
cernboxdir=/eos/user/j/jadevrie/LcAnalysis_Simon/datafiles/ganga/

echo "Will copy job ${jobID} which has the following subjobs:"
du -lh --max-depth 1 $gangadir

#scp -rCv $gangadir lxplus:$cernboxdir 
rsync -vr --ignore-existing $gangadir lxplus:$cernboxdir

