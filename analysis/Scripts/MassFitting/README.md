# Mass fitting
## MassfitLib.py
**Requires the fittingDict.py file in the same directory to function correctly**
**shapefit(shape,fittingDict,fullPath) function**

This function takes as parameters the shape (for the moment only "GaussCB" is available), the fitting dictionary that is found in the fittingDict.py file and the full path for the root file that contains the data to fit. It requires a foder called PDF_output in the area where the function is used as a .pdf file of the drawn fit will be created into a folder called like this. 

The functions also return a dictionnary containing the important information from the fitting process. The keys are: 

*"yield_val", "yield_err", "chi2ndf", "gauss_mean_val", "gauss_mean_err", "gauss_width_val", "gauss_width_err", "CB_width_val", "CB_width_err", "CB_alpha_val", "CB_alpha_err", "CB_n_val", "CB_n_err"*

Here is an example of use inside a Python shell:

```bash
>>> from MassfitLib import shapefit
>>> from fittingDict import fittingDict
>>> dic = shapefit("GaussCB",fittingDict,"/home/user/Code/HonoursProgramme/MassFitScript/dataDirectories/2011_MagDown/bins/Lc_splitfile_y2.5-3.0_pt3000-4000.root")
>>> print(dic)
```

**pathFinder(basePath, year, magPol, filename)**

The basePath parameter is a path string that points to the folder containing the data directories (from the above example, that would be /home/user/Code/HonoursProgramme/MassFitScript/dataDirectories/). The other parameters are just to find the right file.

This function then returns the full path of the file. Is made to be used in the shapefit function as the fullpath variable.

## autoFitScript.py
This script gives a good example of how to use the above functions, as it runs automatically through all the repositories with the structure YEAR_MagPolarity/bins/event.root. It outputs .pdf files of the drawn fits and a python file containing a dictionnary with all the parameters for the fitted PDFs.

The structure of the dictionnary is as follows
```
mainDict[YEAR]["MagPol"]["Event"]["Parameters"]
```
with the parameter keys being 

*"yield_val", "yield_err", "chi2ndf", "gauss_mean_val", "gauss_mean_err", "gauss_width_val", "gauss_width_err", "CB_width_val", "CB_width_err", "CB_alpha_val", "CB_alpha_err", "CB_n_val", "CB_n_err"*

The .py file also has a inbuilt function called dictSearch(year, magPol, filename), which returns an array containing all the parameters in the same order as above (can be easily modified to return an array with tuples containing the name of param and value).

When using the dictionary and function just import both into your script with
"from dictFile import mainDict, dictSearch"

It is important to have the following folders in the **same** directory as the main script:

* Dict_output 
* PDF_output

## fittingDict.py
This is a file containing a library necessary to make the fits of all above functions. It contains the default values for fitting the Gauss, Crystal Ball and Exponential curves to real data, as well as values that have been found for specific data sets that didn't get fitted correctly with the defauld values

