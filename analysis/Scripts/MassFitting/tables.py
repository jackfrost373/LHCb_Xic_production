import ROOT, sys
sys.path.append('../')
from Imports import OUTPUT_DICT_PATH, TABLE_PATH
tablePath = TABLE_PATH
dictPath = OUTPUT_DICT_PATH + "Massfitting/"



def yearTables():

    sys.path.append(dictPath)

    # from BukincombinedFit_DictFile import mainDict as BukinCombined
    # from BukinsingleFit_DictFile import mainDict as BukinSingle
    from BukinyearFit_DictFile import mainDict as BukinYear
    # from GaussCBsingleFit_DictFile import mainDict as GaussSingle
    # from GaussCBcombinedFit_DictFile import mainDict as GaussCombined
    from GaussCByearFit_DictFile import mainDict as GaussYear

    LcTable = open(tablePath + "Year_Lc_yields_table.tex","w",encoding="utf-8")
    XicTable = open(tablePath + "Year_Xic_yields_table.tex","w",encoding="utf-8")

    LcTable.write("\\begin{tabular}{ c|c|c|c|c|c }\n \\hline \n Year & Polarity& GaussCB yield& Bukin yield&Difference& Relative difference\\\\ \n \\hline \n \\hline \n")
    XicTable.write("\\begin{tabular}{ c|c|c|c|c|c }\n \\hline \n Year & Polarity&GaussCB yield& Bukin yield&Difference& Relative difference\\\\ \n \\hline \n \\hline \n")

    for year in GaussYear:
        if GaussYear[year]=={}:
            continue
        for filename in GaussYear[year]["MagDown"]:

            particle = filename.split("_")[0]
            L = "{"+str(len(GaussYear[year]))+"}"
            Y = "{"+str(year)+"}"

            if particle == "Lc":
                LcTable.write(f"\\multirow{L}{{2em}}{Y}")
            elif particle == "Xic":
                XicTable.write(f"\\multirow{L}{{2em}}{Y}")
            for pol in GaussYear[year]:

                GaussValue = GaussYear[year][pol][filename]['yield_val']
                BukinValue = BukinYear[year][pol][filename]['yield_val']
                GaussYield = str(round(GaussValue))+" ± "+str(round(GaussYear[year][pol][filename]['yield_err']))
                BukinYield = str(round(BukinValue))+" ± "+str(round(BukinYear[year][pol][filename]['yield_err']))
                diff = round(BukinValue) - round(GaussValue)
                relDiff = diff/round(GaussValue)*100

                D  = str(round(diff))
                rD = str(round(relDiff,1))+"\\%"

                if particle == "Lc":
                    LcTable.write(f"&{pol}&{GaussYield}&{BukinYield}&{D}&{rD} \\\\ \n")
                elif particle == "Xic":
                    XicTable.write(f"&{pol}&{GaussYield}&{BukinYield}&{D}&{rD} \\\\ \n")

            if particle == "Lc":
                LcTable.write("\\hline \n")
            elif particle == "Xic":
                XicTable.write("\\hline \n")
    
    LcTable.write("\\end{tabular}")
    XicTable.write("\\end{tabular}")

def MCTables():

    mcDictPath = dictPath + "MC/"
    sys.path.append(mcDictPath)
    from Bukin_MC_DictFile import mainDict as BukinMC
    from GaussCB_MC_DictFile import mainDict as GaussMC

    MCTable = open(tablePath + "MC_Fitting_table.tex","w",encoding="utf-8")
    MCTable.write("\\begin{tabular}{ c|c|c|c|c|c|c|c }\n \\hline \n Year & Particle & Polarity& Total events& GaussCB yield & \\Delta & Bukin yield & \\Delta \\\\ \n \\hline \n \\hline \n")

    for year in GaussMC:
        if GaussMC[year] == {}:
            continue

        y = 0
        p = {"Lc" : 0, "Xic" : 0}

        for pol in GaussMC[year]:
            for name in GaussMC[year][pol]:
                y+=1
                if name.split("_")[1] in p:
                    p[name.split("_")[1]] += 1


        MCTable.write(f"\\multirow{{{y}}}{{2em}}{{{year}}} \n")

        for particle in ["Lc","Xic"]:
            if p[particle] == 0:
                continue

            MCTable.write(f"& \\multirow{{{p[particle]}}}{{2em}}{{{particle}}} ")

            i = 0
            for polarity in ["MagUp","MagDown"]:
                if not polarity in GaussMC[year]:
                    continue
                check = True
                for name in GaussMC[year][polarity]:
                    if name.split("_")[1]==particle:
                        check = False
                if check:
                    continue

                
                for name in GaussMC[year][polarity]:
                    if not particle == name.split("_")[1]:
                        continue
                    total = GaussMC[year][polarity][name]["nEvents"]
                    gauss = GaussMC[year][polarity][name]["yield_val"]
                    bukin = BukinMC[year][polarity][name]["yield_val"]

                    gaussYield = str(round(gauss))+" ± "+str(round(GaussMC[year][polarity][name]['yield_err'])) 
                    bukinYield = str(round(bukin))+" ± "+str(round(BukinMC[year][polarity][name]['yield_err']))
                    gaussDiff = f"{((round(gauss)-total)/total*100):.3f}\\%"
                    bukinDiff = f"{((round(bukin)-total)/total*100):.3f}\\%"

                    a = ["&","& &"] #this doesn't work when there is only DOWN OR UP
                     
                    MCTable.write(f"{a[i]}{polarity}&{total}&{gaussYield}&{gaussDiff}&{bukinYield}&{bukinDiff} \\\\ ")
                i +=1

            if particle == "Lc" and p["Xic"] > 0:
                line = "\\cline{2-8}"
            else: 
                line = "\\hline"
            
            MCTable.write("\n "+line+" \n ")
    
    MCTable.write("\\end{tabular}")



if __name__ == "__main__":
    yearTables()
    MCTables()