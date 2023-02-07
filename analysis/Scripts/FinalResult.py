from math import sqrt
import sys,pprint
from Imports import TABLE_PATH, OUTPUT_DICT_PATH,getYbins,getPTbins

effDictPath = OUTPUT_DICT_PATH + "Efficiencies/"
massFittingDictPath = OUTPUT_DICT_PATH + "Massfitting/"

for dir in [effDictPath,massFittingDictPath,"Efficiencies/"]:
    sys.path.append(dir)

from Total_eff_Dict import effDict
from efficiencies import ratio


def main():
    # from BukinyearFit_DictFile import mainDict as bukinDict
    from GaussCByearFit_DictFile import mainDict as gaussDict

    result = {}

    for year in effDict:
        
        # if year == "2017": #temp fix
        #     continue
        
        intYear = int(year)

        if not intYear in gaussDict:
            continue

        for polarity in effDict[year]:
            
            if not polarity in gaussDict[intYear]:
                continue
            
            for particle in effDict[year][polarity]:
                
                if particle == "ratio":
                    continue

                Key = {"Lc":"Lc_total.root","Xic":"Xic_total.root"}

                if not Key[particle] in gaussDict[intYear][polarity]:
                    continue

                if not year in result:
                    result[year]={}
                if not polarity in result[year]:
                    result[year][polarity]={}
                if not particle in result[year][polarity]:
                    result[year][polarity][particle]={}
                
                gaussYield = gaussDict[intYear][polarity][Key[particle]]["yield_val"]
                gaussErr = gaussDict[intYear][polarity][Key[particle]]["yield_err"]
                # bukinYield = bukinDict[year][polarity][Key[particle]]["yield_val"]
                # bukinErr = bukinDict[year][polarity][Key[particle]]["yield_err"]
                
                eff = effDict[year][polarity][particle]["val"]
                effErr = effDict[year][polarity][particle]["err"]

                #SECONDARIES RESULTS HERE
                #
                #
                #

                result[year][polarity][particle]["val"]=gaussYield/eff

                #do we also need to add other errors here?
                # right now includes uncertainty in yield and uncertainty in efficiency
                result[year][polarity][particle]["err"]=(
                    sqrt(
                        (gaussErr/gaussYield)**2
                        +(effErr/eff)**2
                    )
                    * result[year][polarity][particle]["val"]
                )
    result = ratio(result)
    table(result)
    prettyDict = pprint.pformat(result)
    dictF = open(OUTPUT_DICT_PATH + "FinalResult.py","w")
    dictF.write("resultDict = " + str(prettyDict))
    dictF.close()

def table(dict):
    csvF = open(TABLE_PATH + "FinalResult_table.tex","w")
    csvF.write("\\begin{tabular}{ll|c|c|c|c|c|c|}\n")
    csvF.write("\\cline{3-6}\n")
    csvF.write("& & \\multicolumn{2}{c|}{$\Lambda_c$} & \multicolumn{2}{c|}{$\\Xi_c$} \\\\ \\cline{3-8}\n")
    csvF.write("& & Yield & Err. & Yield & Err. & Ratio & Ratio Err. \\\\ \\cline{1-8}\n")

    for year in dict:

        # if year == "2017": #temp fix as 2017 data only has one polarity for Xic
        #     dict[year]["MagUp"]["Xic"]={}
        #     dict[year]["MagUp"]["ratio"]={}
        #     dict[year]["MagUp"]["Xic"]["val"]=0
        #     dict[year]["MagUp"]["Xic"]["err"]=0
        #     dict[year]["MagUp"]["ratio"]["val"]=0
        #     dict[year]["MagUp"]["ratio"]["err"]=0

        # if not "MagUp" in dict[year]:
            # dict[year]["MagUp"]={}
            # dict[year]["MagUp"]["Lc"]={}
            # dict[year]["MagUp"]["Xic"]={}
            # dict[year]["MagUp"]["ratio"]={}
            # dict[year]["MagUp"]["Lc"]["val"]=0
            # dict[year]["MagUp"]["Lc"]["err"]=0
            # dict[year]["MagUp"]["Xic"]["val"]=0
            # dict[year]["MagUp"]["Xic"]["err"]=0
            # dict[year]["MagUp"]["ratio"]["val"]=0
            # dict[year]["MagUp"]["ratio"]["err"]=0




        for polarity in dict[year]:
            if not "ratio"in dict[year][polarity]:
                dict[year][polarity]["ratio"]={"val":0,"err":0}

        csvF.write("\multicolumn{{1}}{{|l|}}{{\multirow{{2}}{{*}}{}}} & \multicolumn{{1}}{{|l|}}{} & {:.3e} & {:.3e} & {:.3e} & {:.3e} & {:.3f} & {:.3f} \\\\\n".format("{" + str(year) + "}", "{MagDown}",dict[year]["MagDown"]["Lc"]["val"],dict[year]["MagDown"]["Lc"]["err"],dict[year]["MagDown"]["Xic"]["val"],dict[year]["MagDown"]["Xic"]["err"],dict[year]["MagDown"]["ratio"]["val"],dict[year]["MagDown"]["ratio"]["err"]))
        if not "MagUp" in dict[year]:
            csvF.write("\multicolumn{1}{|l|}{} & \multicolumn{1}{|l|}{MagUp} & NA & NA & NA & NA & NA & NA \\\\ \\hline\n")
        else:
            csvF.write("\multicolumn{{1}}{{|l|}}{{}} & \multicolumn{{1}}{{|l|}}{} & {:.3e} & {:.3e} & {:.3e} & {:.3e} & {:.3f} & {:.3f} \\\\ \\hline\n".format("{MagUp}",dict[year]["MagUp"]["Lc"]["val"],dict[year]["MagUp"]["Lc"]["err"],dict[year]["MagUp"]["Xic"]["val"],dict[year]["MagUp"]["Xic"]["err"],dict[year]["MagUp"]["ratio"]["val"],dict[year]["MagUp"]["ratio"]["err"]))
    
    csvF.write("\end{tabular}")
    csvF.close()

def combinedBinning():
    from GaussCBcombinedFit_DictFile import mainDict as gaussCombinedDict

    result = {}

    for year in effDict:
        
        # if year == "2017": #temp fix
        #     continue
        
        intYear = int(year)

        if not intYear in gaussCombinedDict:
            continue

        for polarity in effDict[year]:
            
            if not polarity in gaussCombinedDict[intYear]:
                continue
            
            for key in gaussCombinedDict[intYear][polarity]:
                words = key.split("_")
                particle = words[0]
                binType = words[1].replace("bin","")
                binValues = words[2].replace(".root","")

                if not year in result:
                    result[year]={}
                if not polarity in result[year]:
                    result[year][polarity]={}
                if not binType in result[year][polarity]:
                    result[year][polarity][binType]={}
                if not binValues in result[year][polarity][binType]:
                    result[year][polarity][binType][binValues]={}
                if not particle in result[year][polarity][binType][binValues]:
                    result[year][polarity][binType][binValues][particle]={}
                

                
                gaussYield = gaussCombinedDict[intYear][polarity][key]["yield_val"]
                gaussErr = gaussCombinedDict[intYear][polarity][key]["yield_err"]
                
                eff = effDict[year][polarity][particle]["val"]
                effErr = effDict[year][polarity][particle]["err"]

                #SECONDARIES RESULTS HERE
                #
                #
                #

                result[year][polarity][binType][binValues][particle]["val"]=gaussYield/eff

                #do we also need to add other errors here?
                # right now includes uncertainty in yield and uncertainty in efficiency
                result[year][polarity][binType][binValues][particle]["err"]=(
                    sqrt(
                        (gaussErr/gaussYield)**2
                        +(effErr/eff)**2
                    )
                    * result[year][polarity][binType][binValues][particle]["val"]
                )
            
    result = combinedBinningRatio(result)
    combinedBinningRatioTable(result)
    prettyDict = pprint.pformat(result)
    dictF = open(OUTPUT_DICT_PATH + "Combined_FinalResult.py","w")
    dictF.write("resultDict = " + str(prettyDict))
    dictF.close()

def combinedBinningRatio(dict):
    ptBins = getPTbinsString()
    yBins = getYbinsString()
    for year in ["2011","2012","2016","2017","2018"]:
        if not year in dict:
            dict[year] = {}
        for pol in ["MagDown","MagUp"]:
            if not pol in dict[year]:
                dict[year][pol]={"pt":{},"y":{}}
            for binType in dict[year][pol]:
                for binValues in getBinsString(binType):
                    if not binValues in dict[year][pol][binType]:
                        dict[year][pol][binType][binValues]={}
                    if not("Xic" in dict[year][pol][binType][binValues] and "Lc" in dict[year][pol][binType][binValues]):
                        dict[year][pol][binType][binValues]["ratio"] = {"val":999,"err":999}
                        continue
                    
                    if not "ratio" in dict[year][pol][binType][binValues]:
                        dict[year][pol][binType][binValues]["ratio"]={}

                    dict[year][pol][binType][binValues]["ratio"]["val"]= dict[year][pol][binType][binValues]["Xic"]["val"]/dict[year][pol][binType][binValues]["Lc"]["val"]
                    dict[year][pol][binType][binValues]["ratio"]["err"] = (
                        sqrt(
                            (dict[year][pol][binType][binValues]["Xic"]["err"]/dict[year][pol][binType][binValues]["Xic"]["val"])**2
                            + (dict[year][pol][binType][binValues]["Lc"]["err"]/dict[year][pol][binType][binValues]["Lc"]["val"])**2
                        )
                        * dict[year][pol][binType][binValues]["ratio"]["val"]
                    )
    return dict

def combinedBinningRatioTable(dict):
    binTypeString = {"pt": "P_t","y":"\\gamma"}
    for pol in ["MagDown","MagUp"]:
        table = open(TABLE_PATH + pol + "_Combined_Ratios_table.tex","w",encoding = "utf-8")
        
        table.write("\\begin{tabular}{|c|c|c|c|c|c|c|} \n \\hline \n \\multicolumn{2}{|c|}{Bin}")
        for year in ["2011","2012","2016","2017","2018"]:
            table.write(f"&{year}")
        
        table.write("\\\\ \n \\hline")

        for binType in dict[year][pol]:
            nBins = "{"+ str(len(dict[year][pol][binType])) + "}"

            table.write("\\multirow"+nBins+"{*}{"+binTypeString[binType]+"}")

            for binValues in getBinsString(binType):

                table.write(f"& {binValues}")

                for year in ["2011","2012","2016","2017","2018"]:
                    val = dict[year][pol][binType][binValues]["ratio"]["val"]
                    err = dict[year][pol][binType][binValues]["ratio"]["err"]

                    if val == 999:
                        string = "NA"
                    else:
                        string = f"{val:.2e}"  #±{err:.2e}"

                    table.write(f"& {string}")
                
                table.write("\\\\ \\cline{2-7} \n")
            table.write("\\hline \n")

        table.write("\\end{tabular}")
        table.close()
def getBinsString(binType):
    if binType == "pt":
        return getPTbinsString()
    elif binType == "y":
        return getYbinsString()
    return None
def getPTbinsString():
    return bins2String(getPTbins())
def getYbinsString():
    return bins2String(getYbins())
def bins2String(bins):
    return [f"{bin[0]}-{bin[1]}" for bin in bins]


                


if __name__ == "__main__":
    combinedBinning()