
# Example of new Lc MC file
# Details: /MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-Pythia8/Sim09h/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20190430-vc-mu100', 4042, 9978084, 108253)

# get one data file
#lb-run lhcbDirac dirac-dms-get-file /lhcb/MC/2017/ALLSTREAMS.MDST/00108253/0000/00108253_00000353_7.AllStreams.mdst

# dst-dump
#lb-run Bender/latest dst-dump -f -n 5000 -d 2017 00108253_00000353_7.AllStreams.mdst

