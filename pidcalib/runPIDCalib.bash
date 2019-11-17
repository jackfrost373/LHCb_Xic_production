
# Create the PIDCalib PerfHists 


# First install Urania. Then, execute this first:
#cd UraniaDev_v7r0
#LbLogin -c x86_64-centos7-gcc62-opt
#lhcb-proxy-init
#./run bash --norc 



# Now you can run the PerfHists scripts:

#python PIDCalib/PIDPerfScripts/scripts/python/MultiTrack/MakePerfHistsRunRange.py "Turbo16" "MagUp" "K" "[DLLK > 0.0 && InMuonAcc==1, DLLK > 3.0 && InMuonAcc==1, DLLK > 5.0 && InMuonAcc==1, DLLK > 7.0 && InMuonAcc==1, DLLK > 10.0 && InMuonAcc==1]" "P" "ETA" "nTracks_Brunel"

#python PIDCalib/PIDPerfScripts/scripts/python/MultiTrack/MakePerfHistsRunRange.py "Turbo16" "MagUp" "Pi" "[DLLK < -0.0 && InMuonAcc==1, DLLK < -3.0 && InMuonAcc==1, DLLK < -5.0 && InMuonAcc==1, DLLK < -7.0 && InMuonAcc==1, DLLK < -10.0 && InMuonAcc==1]" "P" "ETA" "nTracks_Brunel"


#sample_array=("21r1" "21" "24r1" "28r1" "29r2" "34") # these are signal versions (not pidcalib)
#sample_array=("20r1" "20" "Turbo15" "Turbo16" "Turbo17" "Turbo18")
#sample_array=("20r1" "20")
sample_array=("Turbo15" "Turbo16" "Turbo17" "Turbo18")

#magnet_array=("MagUp" "MagDown")
#magnet_array=("MagUp")    
magnet_array=("MagDown")    

particle_array=( "K" "Pi" "P" )
#particle_array=( "P" )

precuts="1==1"

declare -A pidcuts
#pidcuts["K"]="[DLLK > 0.0, DLLK > 1.0, DLLK > 2.0, DLLK > 3.0, DLLK > 4.0, DLLK > 5.0, DLLK > 6.0, DLLK > 7.0, DLLK > 8.0, DLLK > 9.0, DLLK > 10.0]"
#pidcuts["Pi"]="[DLLK < -0.0, DLLK < -1.0, DLLK < -2.0, DLLK < -3.0, DLLK < -4.0, DLLK < -5.0, DLLK < -6.0, DLLK < -7.0, DLLK < -8.0, DLLK < -9.0, DLLK < -10.0]"

# for run1
#pidcuts["K"]="[MC12TuneV2_ProbNNK > 0.4 && DLLK > 0]"
#pidcuts["Pi"]="[MC12TuneV2_ProbNNpi > 0.5]"
#pidcuts["P"]="[MC12TuneV2_ProbNNp > 0.5 && DLLp > 0]"

# for run2
pidcuts["K"]="[MC15TuneV1_ProbNNK > 0.4 && DLLK > 0]"
pidcuts["Pi"]="[MC15TuneV1_ProbNNpi > 0.5]"
pidcuts["P"]="[MC15TuneV1_ProbNNp > 0.5 && DLLp > 0]"

varx="P"
vary="ETA"
varz="nTracks_Brunel"



for sample in "${sample_array[@]}"
do :
  for magnet in "${magnet_array[@]}"
  do :
    for particle in "${particle_array[@]}"
    do :
      varz2=$varz
      if [ $varz == "nTracks_Brunel" ]; then 
        if [ $sample == "20r1" ] ; then varz2="nTracks" ; fi
        if [ $sample == "20" ]   ; then varz2="nTracks" ; fi
      fi
      python PIDCalib/PIDPerfScripts/scripts/python/MultiTrack/MakePerfHistsRunRange.py "${sample}" "${magnet}" "${particle}"  "${pidcuts[$particle]}" "${varx}" "${vary}" "${varz2}" -c "${precuts}" --binSchemeFile="oldBinning.py" --schemeName="BHH_Binning" --allow-missing
    done
  done
done


