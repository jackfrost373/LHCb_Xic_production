def getMCCuts (particle, run):
    IDcuts = "abs(piplus_ID)==211 && abs(kminus_ID)==321 && abs(pplus_ID)==2212 && abs(lcplus_ID)==4122"
    if run == 2:
        IDcuts += " && lcplus_Hlt2CharmHad{0}pToPpKmPipTurboDecision_TOS == 1".format(particle)
    if particle == "Lc":
        #BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 50)"
        return IDcuts #+ "&&" + BKGCAT
    elif particle == "Xic":
        #BKGCAT = "(lcplus_BKGCAT == 0 || lcplus_BKGCAT == 10 || lcplus_BKGCAT == 50)"
        return IDcuts #+ "&&" + BKGCAT

def getDataCuts (run):
    cuts = "lcplus_P < 300000 && lcplus_OWNPV_CHI2 < 80 && pplus_ProbNNp > 0.5 && kminus_ProbNNk > 0.4 && piplus_ProbNNpi > 0.5 && pplus_P < 120000 && kminus_P < 115000 && piplus_P < 80000 && pplus_PIDp > 0 && kminus_PIDK > 0 && lcplus_L0HadronDecision_TOS == 1"
    if run == 1:
            trigger_cuts = "lcplus_Hlt1TrackAllL0Decision_TOS == 1 && lcplus_Hlt2CharmHadD2HHHDecision_TOS ==1"
    elif run == 2:
        trigger_cuts = "lcplus_Hlt1TrackMVADecision_TOS == 1"
    return cuts + " && " + trigger_cuts

def getBackgroundCuts(particle):
    if particle == "Lc":
        cuts = "(lcplus_MM > 2320 && lcplus_MM < 2350) || (lcplus_MM > 2220 && lcplus_MM < 2260)"
    elif particle == "Xic":
        cuts = "lcplus_MM > 2400 && lcplus_MM < 2450 || lcplus_MM > 2490"
    return cuts
    
def getPTbins():
    return [[3200,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,20000]]
    
def getYbins():
    return  [[2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]]


def getFoldersDict():
    folders_dict = {"42":["2012_MagDown", 1155], "43":["2011_MagDown", 907], "45":["2011_MagUp", 817], "46":["2012_MagUp", 1342], "91":["2017_MagDown_Lc", 529], "92":["2018_MagDown_Lc", 659], "115":["2016_MagDown_Xic", 186], "116":["2017_MagDown_Xic", 257], "117":["2018_MagDown_Xic", 471], "119":["2016_MagDown_Lc", 527]} 
    return folders_dict
