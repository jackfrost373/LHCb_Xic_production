
LbLogin -c x86_64-centos7-gcc62-opt

lb-dev Urania/v7r0

cd UraniaDev_v7r0

git lb-use Urania

git lb-checkout Urania/master PIDCalib/PIDPerfTools

git lb-checkout Urania/master PIDCalib/PIDPerfScripts

git lb-checkout Urania/master cmake

make configure

make install
