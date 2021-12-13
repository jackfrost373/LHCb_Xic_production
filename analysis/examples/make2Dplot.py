
import ROOT
from array import array
ROOT.gStyle.SetOptStat(0)


# edges of the 2D bins
xbinedges = [0, 2, 5, 6, 8, 12]
ybinedges = [0, 1, 3, 4, 6]


nbinsx = len(xbinedges)-1
nbinsy = len(ybinedges)-1

# set up data dictionary used to fill histogram
mydata = {}
for i in range(nbinsx) :
  mydata[i] = {}
  for j in range(nbinsy) :
    mydata[i][j] = 0.


# mydata is filled as mydata[bin_number_x][bin_number_y] = ...
mydata[1][1] = 2
mydata[2][3] = 5
# etc...



# make the 2D hist with custom bin sizes
xbinedges_arr = array('f',xbinedges)
ybinedges_arr = array('f',ybinedges)

hist = ROOT.TH2F("2dhist", "2dhist", nbinsx, xbinedges_arr, nbinsy, ybinedges_arr)

# fill histogram with data
for i in range(nbinsx) :
  for j in range(nbinsy) :
    hist.SetBinContent( i+1, j+1, mydata[i][j] )

# Draw
hist.GetXaxis().SetTitle("xVar [units]")
hist.GetYaxis().SetTitle("yVar [units]")
c1 = ROOT.TCanvas("c1")
hist.Draw("COLZ")
c1.Update()
c1.SaveAs("my2dhist.jpg")


