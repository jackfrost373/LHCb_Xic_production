import ROOT, sys
sys.path.append('../')
from Imports import OUTPUT_DICT_PATH, TABLE_PATH
from math import sqrt
tablePath = TABLE_PATH
dictPath = OUTPUT_DICT_PATH + "Massfitting/"



def yearTables():

    sys.path.append(dictPath)

    from BukinyearFit_DictFile import mainDict as BukinYear
    from GaussCByearFit_DictFile import mainDict as GaussYear

    LcTable = open(tablePath + "Year_Lc_yields_table.tex","w",encoding="utf-8")
    XicTable = open(tablePath + "Year_Xic_yields_table.tex","w",encoding="utf-8")

    LcTable.write("\\begin{table}[h]\n\\centering")
    XicTable.write("\\begin{table}[h]\n\\centering")

    LcTable.write("\\begin{tabular}{ c|c|c|c|c|c }\n \\hline \n Year & Polarity& GaussCB yield& Bukin yield&Difference& Rel. difference\\\\ \n \\hline \n \\hline \n")
    XicTable.write("\\begin{tabular}{ c|c|c|c|c|c }\n \\hline \n Year & Polarity&GaussCB yield& Bukin yield&Difference& Rel. difference\\\\ \n \\hline \n \\hline \n")

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

                D  = str(round(diff))+ " ± "+str(round(sqrt(round(GaussYear[year][pol][filename]['yield_err'])^2+round(BukinYear[year][pol][filename]['yield_err'])^2)))
                rD = str(round(relDiff,1))+"\\%"

                if particle == "Lc":
                    LcTable.write(f"&{pol}&{GaussYield}&{BukinYield}&{D}&{rD} \\\\ \n")
                elif particle == "Xic":
                    XicTable.write(f"&{pol}&{GaussYield}&{BukinYield}&{D}&{rD} \\\\ \n")

            if particle == "Lc":
                LcTable.write("\\hline \n")
            elif particle == "Xic":
                XicTable.write("\\hline \n")
    
    LcTable.write("\\end{tabular}\n\\caption{Lc yields compared to alternate fitshape}\n\\label{table:LcYieldCompare}\n\\end{table}")
    XicTable.write("\\end{tabular}\n\\caption{Xic yields compared to alternate fitshape}\n\\label{table:XicYieldCompare}\n\\end{table}")

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

def GaussYieldsTable():
    sys.path.append(dictPath)
    from GaussCByearFit_DictFile import mainDict as GaussYear

    table = open(tablePath + "GaussYields_table.tex","w",encoding="utf-8")

    table.write("\\begin{table}[h]\\centering\n")
    table.write("\\begin{tabular}{ll|c|c|c|c|}\n")
    table.write("\\cline{3-6}\n")
    table.write("& & \\multicolumn{2}{c|}{$\Lambda_c$} & \multicolumn{2}{c|}{$\\Xi_c$} \\\\ \\hline\n")
    table.write("\multicolumn{1}{|c|}{Year} & \multicolumn{1}{|c|}{Polarity} & Yield & Err. & Yield & Err.\\\\\n")

    for year in GaussYear:
        if GaussYear[year] == {}:
            continue
        
        table.write("\hline\n")
        table.write(f"\multicolumn{{1}}{{|c|}}{{\\multirow{{2}}{{*}}{{{year}}}}}")

        for polarity in ["MagDown","MagUp"]:
            if not polarity in GaussYear[year]:
                GaussYear[year][polarity] = {}

            if polarity == "MagUp":
                table.write("\multicolumn{1}{|c|}{}")

            if not "Lc_total.root" in GaussYear[year][polarity]:
                LcYield = "NA"
                LcErr = "NA"
            else:
                LcYield = round(GaussYear[year][polarity]["Lc_total.root"]["yield_val"])
                LcErr = round(GaussYear[year][polarity]["Lc_total.root"]["yield_err"])
            
            if not "Xic_total.root" in GaussYear[year][polarity]:
                XicYield = "NA"
                XicErr = "NA"
            else:
                XicYield = round(GaussYear[year][polarity]["Xic_total.root"]["yield_val"])
                XicErr = round(GaussYear[year][polarity]["Xic_total.root"]["yield_err"])

            table.write(f" & \multicolumn{{1}}{{|c|}}{{{polarity}}} & {LcYield} & {LcErr} & {XicYield} & {XicErr} \\\\ \n")

    table.write("\\hline\n\end{tabular}\\caption{Table of yields for each year depending on the magnet polarity and particle in question for GaussCB.}\n\\label{table:yield}\n\\end{table}")
    table.close()


if __name__ == "__main__":
    yearTables()
    # MCTables()
    GaussYieldsTable()
