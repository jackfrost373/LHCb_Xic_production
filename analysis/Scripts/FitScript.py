#This script is used to fit all of the datafiles split into bins in a loop, by calling the Universal mass fit function on the data

import ROOT, os, math, Universal_fit_function
from ROOT import TChain, TFile
from Universal_fit_function import Shape_fit

user = "Nikhef"
#shape = "Bukin" # select the shape that you want to fit your data with
shape = input("please indicate the PDF (GaussCB, Bukin, Ipatia or Apolonios): ")
particles = ["Lc", "Xic"]

job = "2018_MagDown"
dir = "/dcache/bfys/scalo/"
directory = dir + job + "/"
os.mkdir("/dcache/bfys/scalo/" + job + "/graphs")


ybins = [ [2.0,2.5],[2.5,3.0], [3.0,3.5], [3.5,4.0]] # Rapidity bins

ptbins = [ [3000,4000],[4000,5000], [5000,6000], [6000,7000], [7000,8000], [8000,10000], [10000,20000]] # Transverse momentum bins modified

Lcyield ={}
Lcerror = {}
Xicyield ={}
Xicerror = {}

text = open(directory + "Output.txt", "w+") # This is the text file in which all of the interesting parameters from the fit are printed

# loop used to fit all the bins and print all of the interesting parameters of the fit
for particle in particles:
    for ybin in ybins:
        for ptbin in ptbins:
            location = (directory + "bins/" + particle + "_bin_y{0}-{1}_pt{2}-{3}.root".format(ybin[0],ybin[1],ptbin[0],ptbin[1]))
            file = ROOT.TFile(location, "READONLY")
            tree = file.Get("DecayTree")
            string = Shape_fit(shape, tree, particle, ybin, ptbin, job, Data = True, Pull = False)
            text.write(string)
            tlist = string.split()
            check = "y{0}-{1}_pt{2}-{3}".format(ybin[0],ybin[1],ptbin[0],ptbin[1])
            res = float(tlist[4])
            error = float(tlist[6])
            if particle == "Lc":
                Lcyield[check] = res
                Lcerror[check] = error
            elif particle == "Xic":
                Xicyield[check] = res
                Xicerror[check] = error
            file.Close()
                    
text.close()

f_text = open(directory + "Ratio_output.txt", "w+") # This is the text file in which the final dictonary with ratios and errors is printed

ratio_list = {}
yield_dict = {}
for element in Lcyield:
    
    num = Xicyield[element]
    den = Lcyield[element]
    ratio = num/den
    error_1 = Xicerror[element]
    error_2 = Lcerror[element]
    
    yield_dict[element] = [den, error_2, num, error_1]
    total_error =math.sqrt((error_1/num)**2 + (error_2/den)**2)*ratio
    ratio_list[element] = [ratio, total_error]


f_text.write(str(yield_dict))
f_text.close()
