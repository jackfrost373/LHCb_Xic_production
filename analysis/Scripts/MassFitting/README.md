# Mass fitting
## fit.py

This information can be found by using 
```
python fit.py -h
```

Before running the script make sure you have two folders in the programme directory with the following structure:
-	Dict_output/
-	PDF_output/Single
-	PDF_output/Combined
-	PDF_output/Year
These are for the output of the script and are necessary for a functionning run.

The parameters are
-	s : shape (GaussCB or Bukin)
-	m : mode (single, combined or year)
-	y : year (e.g. 2011) 
-	o : magnet polarity (up, down or both)
-	p : particle name (Xic, Lc or both)
-	r : rapidity (e.g. 2.5-3.0)
-	t : transverse momentum (e.g. 8000-10000)

Important: the -s argument always has to be specified first after the -m argument. No -s argument is given will result in default fit shape GaussCB.

Important: the -o and -p are always used together, there is no option for using only one of the two (you can consider them as a single parameter...

For modes -m:
-	"single" you can use any combination of -s -y -o -p -r -t 
-	"combined" you can use any combination of -s -y -o -p -r -t but you can never use both -r and -t together, which yould defeat the point of having combined bins
-	"year"you can use any combination of -s -y -o -p

Running with no other parameter than -m makes the full fitting process with default GaussCB fit shape. It also initializes the ditionnary file if you have not yet run the programme (important, the first time using this script requires initializing the dictionnaries by running with no parameter, e.g. "python fit.py -m single").

The main function of this script returns an list of two lists, one containing the fitting variables and the other containing all of the fitting shapes as they were for the final plotting. This means you can use the main function inside other programs.To use this program like this, outside of the normal terminal setting you will have to give the main function a list with the command line arguments, like you can see in the example below: 

```
import fit
objList = fit.main(["-m", "single", "-s", "Bukin",  "-y", "2012", "-o", "up", "-p", "Xic", "-r", "2.5-3.0", "-t", "8000-10000"])
```

## MassfitLib.py
**Requires the fittingDict.py file in the same directory to function correctly**
**shapefit(shape,fittingDict,fullPath) function**

This function takes as parameters the shape, the fitting dictionary that is found in the fittingDict.py file and the full path for the root file that contains the data to fit. It requires a foder called PDF_output in the area where the function is used as a .pdf file of the drawn fit will be created into a folder called like this. 

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

**combYPTbinShapeFit(shape,fittingDict,path, wantedBin = "both", PDF = True)**

This function loops through each year and depending on the value of the wantedBin parameter ("y", "pt" or "both"), it will make fits for the combined bins and output a PDF as well as a dictionnary with the fitting data.

**yearTotalShapeFit(year,shape,fittingDict,path, PDFpath = "./PDF_output/", PDF = True)**

Chains all of the data together per year (adding the two polarities) for each particles and output a PDF as well as a dictionnary with the fitting data.
