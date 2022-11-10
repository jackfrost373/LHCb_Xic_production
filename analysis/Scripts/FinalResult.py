from math import sqrt
import sys,pprint
from Imports import TABLE_PATH, OUTPUT_DICT_PATH

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

if __name__ == "__main__":
    main()