# Mass fitting
## MainProgram.py
**Requires the fittingDict.py file in the same directory to function correctly**

For the moment it is only possible to do a GaussCB fit on the data. The script runs automatically through all the repositories with the structure YEAR_MagPolarity/bins/event.root and outputs a the .pdf file of the drawn fit and a .py file containing a dictionnary with all the parameters for the fitted PDFs (it is also possible to output a .root file containing all of the raw data).

The structure of the dictionnary is as follows
```
mainDict[YEAR]["MagPol"]["Event"]["Parameters"]
```
with the parameter keys being 

"yield_val", "yield_err", "chi2ndf", "gauss_mean_val", "gauss_mean_err", "gauss_width_val", "gauss_width_err", "CB_width_val", "CB_width_err", "CB_alpha_val", "CB_alpha_err", "CB_n_val", "CB_n_err"

The .py file also has a inbuilt function called dictSearch(year, magPol, filename), which returns an array containing all the parameters in the same order as above (can be easily modified to return an array with tuples containing the name of param and value).

When using the dictionary and function just import both into your script with
"from dictFile import mainDict, dictSearch"

It is important to have the following folders in the **same** directory as the main script:

* Dict_output 
* PDF_output 
* ROOT_output (optional, only if the .root output has been uncommented)

The main function of the program is based on Simons Shape_fit() script with some modifications. The Bukin fit doesn't work yet, and the pull histogram is not available yet. The GaussCB fit is not optimized for Xic mass fitting neither (see the output PDFs)


## MassfitLib
This library contains a function that will do a GaussCB fitting to a specified dataset found in a root file. It works almost similarly to the fitting part of the above program, and as such it requires an import of the dictionnary found in the fittingDict.py file.



