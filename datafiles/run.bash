
# Run real data over grid. Please configure options first!
#ganga ./options/ganga_options.py | tee logs/gangaRun.log 

# Run simulation over grid. Please configure options first!
ganga ./options/ganga_options_MC.py | tee logs/gangaRun_MC.log 


# Download local dst from the grid for testing. Look up the LFN from the Dirac bookkeeping.
#lhcb-proxy-init
#lb-run LHCbDirac dirac-dms-get-file /lhcb/LHCb/Collision17/CHARM.MDST/00071700/0000/00071700_00000137_1.charm.mdst

# Inspect TES locations inside dst
#lb-run Bender/latest dst-dump -f -n 5000 ./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/00071700_00000137_1.charm.mdst

# Run over local dst to produce ntuples
#lb-run DaVinci/v44r5 gaudirun.py ./options/davinci_options.py ./data/Collision17_MagDown_Reco17_Stripping29r2_CHARM/includeLocal.py | tee logs/davinciRun.log

# Inspect output ntuple
#lb-run ROOT root -l output/charm_29r2.root

