
# db of MC production files.
# Find MC production files with a certain eventtype using 
#  lb-dirac dirac-bookkeeping-decays-path 25103064

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
    print("No files found matching all identifiers {0}".format(identifiers))
    return 0

  if len(matchingfiles) > 1 :
    print("Multiple files matched the identifiers {0}. Please add criteria.".format(identifiers))
    for matchingfile in matchingfiles :
      print(" --> {0}".format(matchingfile[0]))
    return 0

  print("Using {0}".format(matchingfiles[0][0]))
  return matchingfiles[0]
      

# Xic_pKpi=TightCut
db[25103010] = [
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103010/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-md100', 28, 509500, 28256),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103010/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-mu100', 30, 521498, 28258),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103010/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-md100', 36, 519998, 28264),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103010/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-mu100', 33, 523499, 28266),
]

# Lc_pKpi=phsp,TightCut
db[25103006] = [
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103006/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-md100', 55, 1031796, 25017),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08a/Digi13/Trig0x409f0045/Reco14/Stripping20NoPrescalingFlagged/25103006/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-mu100', 57, 1028799, 25221),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14/Stripping20NoPrescalingFlagged/25103006/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-md100', 63, 1038997, 25225),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08a/Digi13/Trig0x409f0045/Reco14/Stripping20NoPrescalingFlagged/25103006/ALLSTREAMS.DST', 'Sim08-20130503-1', 'Sim08-20130503-1-vc-mu100', 62, 1027998, 25229),
]

# Xic_pKpi=phsp,TightCut,LifeTimePT,PPChange
db[25103036] = [
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103036/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 25, 515656, 51599),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103036/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 25, 515015, 51601),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103036/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 28, 647464, 51603),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103036/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 23, 532187, 51605),
]

# Lc_pKpi=DecProdCut
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

# fromB
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

# fromB
db[15164101] = [
('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim08e/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/15164101/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-mu100', 56, 1013912, 36758),
('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim08e/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/15164101/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-md100', 70, 1011198, 36760),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/15164101/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 126, 2015986, 36762),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/15164101/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 123, 2021588, 36764),
]

# fromB
db[16264060] = [
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-GenXiccPythia8/Sim09b/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/16264060/ALLSTREAMS.DST', 'dddb-20150928', 'sim-20160321-2-vc-md100', 43, 506197, 57177),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-GenXiccPythia8/Sim09b/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/16264060/ALLSTREAMS.DST', 'dddb-20150928', 'sim-20160321-2-vc-mu100', 45, 512111, 57185),
('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping28NoPrescalingFlagged/16264060/ALLSTREAMS.MDST', 'dddb-20150724', 'sim-20161124-2-vc-md100', 207, 508287, 61618),
('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping28NoPrescalingFlagged/16264060/ALLSTREAMS.MDST', 'dddb-20150724', 'sim-20161124-2-vc-mu100', 206, 507402, 61645),
('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-GenXiccPythia8/Sim09c/Trig0x6138160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/16264060/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20170721-2-vc-md100', 816, 2003712, 73643),
('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-GenXiccPythia8/Sim09c/Trig0x6138160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/16264060/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20170721-2-vc-mu100', 809, 2002246, 73645),
]

# Xic_pKpi=phsp,TightCut
db[25103046] = [
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103046/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 56, 1017367, 34483),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103046/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 58, 1016532, 34489),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103046/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 62, 1003768, 34495),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08e/Digi13/Trig0x409f0045/Reco14a/Stripping20NoPrescalingFlagged/25103046/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 65, 1028610, 34501),
('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia6/Sim08e/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/25103046/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-md100', 28, 532184, 34514),
('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia6/Sim08e/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/25103046/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-mu100', 28, 514504, 34518),
('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim08e/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/25103046/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-md100', 31, 521824, 34524),
('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim08e/Digi13/Trig0x40760037/Reco14a/Stripping20r1NoPrescalingFlagged/25103046/ALLSTREAMS.DST', 'dddb-20130929', 'sim-20130522-vc-mu100', 30, 527725, 34530),
]

# Xic_pKpi=TightCut,LifeTimePT
db[25103029] = [
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103029/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 26, 532929, 51066),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103029/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 27, 551509, 51068),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia6/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103029/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-mu100', 23, 529243, 51070),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia6/Sim08i/Digi13/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103029/ALLSTREAMS.DST', 'dddb-20130929-1', 'sim-20130522-1-vc-md100', 24, 553938, 51072),
]

# Lc_pKpi-res=LHCbAcceptance
db[25203000] = [
('/MC/2018/Beam6500GeV-2018-MagUp-Nu1.6-25ns-Pythia8/Sim09g/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/25203000/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20190430-vc-mu100', 787, 2004731, 91159),
('/MC/2018/Beam6500GeV-2018-MagDown-Nu1.6-25ns-Pythia8/Sim09g/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/25203000/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20190430-vc-md100', 780, 2000268, 91165),
('/MC/2017/Beam6500GeV-2017-MagUp-Nu1.6-25ns-Pythia8/Sim09g/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/25203000/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20190430-1-vc-mu100', 788, 2003842, 91327),
('/MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-Pythia8/Sim09g/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/25203000/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20190430-1-vc-md100', 792, 2007907, 91331),
('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8/Sim09g/Trig0x6139160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/25203000/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20170721-2-vc-mu100', 787, 2007242, 91513),
('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09g/Trig0x6139160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/25203000/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20170721-2-vc-md100', 788, 2009238, 91515),
]

# Xic+_pKpi=phsp,DecProdCut
db[26103090] = [
#('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/26103090/ALLSTREAMS.DST', 'dddb-20150724', 'sim-20161124-2-vc-mu100', 467, 1166440, 62034),
#('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/26103090/ALLSTREAMS.DST', 'dddb-20150724', 'sim-20161124-2-vc-md100', 407, 1015240, 62040),
('/MC/2018/Beam6500GeV-2018-MagDown-Nu1.6-25ns-Pythia8/Sim09f/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/26103090/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20190128-vc-md100', 752, 2005446, 90970),
('/MC/2018/Beam6500GeV-2018-MagUp-Nu1.6-25ns-Pythia8/Sim09f/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/26103090/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20190128-vc-mu100', 752, 2007066, 90972),
('/MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-Pythia8/Sim09f/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/26103090/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20180411-vc-md100', 751, 2002494, 90974),
('/MC/2017/Beam6500GeV-2017-MagUp-Nu1.6-25ns-Pythia8/Sim09f/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/26103090/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20180411-vc-mu100', 754, 2006193, 90976),
('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09f/Trig0x6139160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/26103090/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20170721-2-vc-md100', 762, 2052337, 90978),
('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8/Sim09f/Trig0x6139160F/Reco16/Turbo03/Stripping28r1NoPrescalingFlagged/26103090/ALLSTREAMS.DST', 'dddb-20170721-3', 'sim-20170721-2-vc-mu100', 754, 2006283, 90980),
]

# Our new Lc request with tightcutsv2
db[25103064] = [
('/MC/2017/Beam6500GeV-2017-MagUp-Nu1.6-25ns-Pythia8/Sim09h/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20190430-1-vc-mu100', 4056, 10003317, 106119),
('/MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-Pythia8/Sim09h/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20190430-1-vc-md100', 4059, 10007458, 108253),
('/MC/2012/Beam4000GeV-2012-MagDown-Nu2.5-Pythia8/Sim09k/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-2', 'sim-20160321-2-vc-md100', 2902, 7121612, 128812),
('/MC/2012/Beam4000GeV-2012-MagUp-Nu2.5-Pythia8/Sim09k/Trig0x409f0045/Reco14c/Stripping21NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-2', 'sim-20160321-2-vc-mu100', 2857, 7006362, 128814),
('/MC/2011/Beam3500GeV-2011-MagDown-Nu2-Pythia8/Sim09k/Trig0x40760037/Reco14c/Stripping21r1NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-1', 'sim-20160614-1-vc-md100', 1094, 3036549, 128816),
('/MC/2011/Beam3500GeV-2011-MagUp-Nu2-Pythia8/Sim09k/Trig0x40760037/Reco14c/Stripping21r1NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-1', 'sim-20160614-1-vc-mu100', 1079, 3000757, 128818),
('/MC/2018/Beam6500GeV-2018-MagDown-Nu1.6-25ns-Pythia8/Sim09k/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20190430-vc-md100', 4068, 10011069, 130101),
('/MC/2018/Beam6500GeV-2018-MagUp-Nu1.6-25ns-Pythia8/Sim09k/Trig0x617d18a4/Reco18/Turbo05-WithTurcal/Stripping34NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20190430-vc-mu100', 4080, 10060619, 130103),
('/MC/2016/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09k/Trig0x6139160F/Reco16/Turbo03a/Stripping28r1NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20170721-2-vc-md100', 4410, 10869713, 130105),
('/MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8/Sim09k/Trig0x6139160F/Reco16/Turbo03a/Stripping28r1NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20170721-2-vc-mu100', 3415, 8398608, 130107),
('/MC/2015/Beam6500GeV-2015-MagDown-Nu1.6-25ns-Pythia8/Sim09k/Trig0x411400a2/Reco15a/Turbo02/Stripping24r1NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20161124-vc-md100', 907, 2232039, 130109),
('/MC/2015/Beam6500GeV-2015-MagUp-Nu1.6-25ns-Pythia8/Sim09k/Trig0x411400a2/Reco15a/Turbo02/Stripping24r1NoPrescalingFlagged/25103064/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20161124-vc-mu100', 1268, 3113322, 130111),
]

# Our new Xic request --> to be updated to new number.
db[26103091] = [
('/MC/2017/Beam6500GeV-2017-MagDown-Nu1.6-25ns-Pythia8/Sim09i/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/26103091/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20170721-2-vc-md100', 4120, 10009885, 109979),
('/MC/2017/Beam6500GeV-2017-MagUp-Nu1.6-25ns-Pythia8/Sim09i/Trig0x62661709/Reco17/Turbo04a-WithTurcal/Stripping29r2NoPrescalingFlagged/26103091/ALLSTREAMS.MDST', 'dddb-20170721-3', 'sim-20170721-2-vc-md100', 4123, 10018168, 109981),
]
