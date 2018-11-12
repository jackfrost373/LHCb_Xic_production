
# db of MC production files.
# Find MC production files with a certain eventtype using ./scripts/get_bookkeeping_info 25103036

db = {}

def getFileFromDB(eventtype, identifiers) :
  files = db[eventtype]
  matchingfiles = []
  for ifile in files :
    ifilename = ifile[0]
    addFile = 1
    for identifier in identifiers :
      if not identifier in ifilename :
        addFile = 0
    if (addFile == 1) :
      matchingfiles += [ifile]

  if len(matchingfiles) == 0 :
    print "No files found matching all identifiers {0}".format(identifiers)
    return 0

  if len(matchingfiles) > 1 :
    print ("Multiple files matched the identifiers {0}. Please add criteria.".format(identifiers))
    for matchingfile in matchingfiles :
      print " --> {0}".format(matchingfile[0])
    return 0

  print "Using {0}".format(matchingfiles[0][0])
  return matchingfiles[0]
      


db[25103010] = [
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103010/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-md100', 28, 509500, 28256),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103010/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-mu100', 30, 521498, 28258),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103010/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-md100', 36, 519998, 28264),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103010/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-mu100', 33, 523499, 28266),
]

db[25103006] = [
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103006/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-md100', 55, 1031796, 25017),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14/Stripping20NoPrescalingFlagged/25103006/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-mu100', 57, 1028799, 25221),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14/Stripping20NoPrescalingFlagged/25103006/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-md100', 63, 1038997, 25225),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14/Stripping20NoPrescalingFlagged/25103006/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-mu100', 62, 1027998, 25229),
]

db[25103036] = [
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103036/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 25, 515656, 51599),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103036/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 25, 515015, 51601),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103036/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 28, 647464, 51603),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103036/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 23, 532187, 51605),
]

db[25103000] = [
#('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim08f/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-mu100', 63, 1013135, 42125),
#('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim08f/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-md100', 63, 1035449, 42127),
('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim08h/Digi13/Trig0x40760037/Reco14c/Stripping20r1NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-mu100', 97, 1630353, 47879),
('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim08h/Digi13/Trig0x40760037/Reco14c/Stripping20r1NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-md100', 96, 1641984, 47891),
#('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 10, 129431, 35722),
#('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 9, 132115, 35736),
#('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 9, 128496, 35750),
#('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 8, 127628, 35768),
#('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08h/Digi13/Trig0x409f0045/Reco14c/Stripping20NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 23, 269341, 46765),
#('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08h/Digi13/Trig0x409f0045/Reco14c/Stripping20NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 17, 288683, 46767),
#('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08h/Digi13/Trig0x409f0045/Reco14c/Stripping20NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 17, 281286, 46769),
#('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08h/Digi13/Trig0x409f0045/Reco14c/Stripping20NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 14, 252790, 46771),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim09b/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20150928', 'sim-20160321-2-vc-mu100', 580, 1600644, 61813),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim09b/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20150928', 'sim-20160321-2-vc-md100', 577, 1602034, 61815),
#('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20150724', 'sim-20161124-2-vc-md100', 471, 1188135, 59810),
#('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20150724', 'sim-20161124-2-vc-mu100', 457, 1148411, 59812),
('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping28NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20150724', 'sim-20161124-2-vc-mu100', 805, 2008582, 61396),
('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping28NoPrescalingFlagged/25103000/ALLSTREAMS.DST', 'dddb-20150724', 'sim-20161124-2-vc-md100', 803, 2016565, 61410),
]

db[15264011] = [
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08g/Digi13/Trig0x409f0045/Reco14c/Stripping20NoPrescalingFlagged/15264011/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 28, 554352, 44482),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08g/Digi13/Trig0x409f0045/Reco14c/Stripping20NoPrescalingFlagged/15264011/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 28, 557907, 44488),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08g/Digi13/Trig0x409f0045/Reco14c/Stripping20NoPrescalingFlagged/15264011/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 26, 518421, 44496),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08g/Digi13/Trig0x409f0045/Reco14c/Stripping20NoPrescalingFlagged/15264011/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 30, 517375, 44500),
('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim08g/Digi13/Trig0x40760037/Reco14c/Stripping20r1NoPrescalingFlagged/15264011/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-mu100', 21, 264677, 44512),
('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim08g/Digi13/Trig0x40760037/Reco14c/Stripping20r1NoPrescalingFlagged/15264011/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-md100', 20, 258256, 44518),
('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia6/Sim08g/Digi13/Trig0x40760037/Reco14c/Stripping20r1NoPrescalingFlagged/15264011/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-mu100', 17, 251954, 44524),
('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia6/Sim08g/Digi13/Trig0x40760037/Reco14c/Stripping20r1NoPrescalingFlagged/15264011/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-md100', 17, 259582, 44530),
]

db[15164101] = [
('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim08e/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/15164101/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-mu100', 56, 1013912, 36758),
('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim08e/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/15164101/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-md100', 70, 1011198, 36760),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/15164101/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 126, 2015986, 36762),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/15164101/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 123, 2021588, 36764),
]

db[16264060] = [
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-GenXiccPythia8/Sim09b/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/16264060/ALLSTREAMS.DST', 'dddb-20150928', 'sim-20160321-2-vc-md100', 43, 506197, 57177),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-GenXiccPythia8/Sim09b/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/16264060/ALLSTREAMS.DST', 'dddb-20150928', 'sim-20160321-2-vc-mu100', 45, 512111, 57185),
('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping28NoPrescalingFlagged/16264060/ALLSTREAMS.MDST', 'dddb-20150724', 'sim-20161124-2-vc-md100', 207, 508287, 61618),
('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping28NoPrescalingFlagged/16264060/ALLSTREAMS.MDST', 'dddb-20150724', 'sim-20161124-2-vc-mu100', 206, 507402, 61645),
('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim09c/Trig0x6138160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/16264060/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20170721-2-vc-md100', 816, 2003712, 73643),
('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim09c/Trig0x6138160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/16264060/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20170721-2-vc-mu100', 809, 2002246, 73645),
]
