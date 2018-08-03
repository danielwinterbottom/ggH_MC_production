#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc530
if [ -r CMSSW_8_0_21/src ] ; then 
 echo release CMSSW_8_0_21 already exists
else
scram p CMSSW CMSSW_8_0_21
fi
cd CMSSW_8_0_21/src
eval `scram runtime -sh`
mkdir Submit

scram b
cd ../../
cmsDriver.py step1 --filein "file:test_gen.root" --fileout file:test_pumix.root  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 8 --datamix PreMix --era Run2_2016 --python_filename run_pumix.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 100 || exit $? ; 

cp run_pumix.py CMSSW_8_0_21/src/Submit/.

cmsDriver.py step2 --filein file:test_pumix.root --fileout file:test_aod.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 8 --era Run2_2016 --python_filename run_aod.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 100 || exit $? ;

cp run_aod.py CMSSW_8_0_21/src/Submit/.

cp crab_pumixing.py CMSSW_8_0_21/src/Submit/.
cp crab_aod.py CMSSW_8_0_21/src/Submit/.
cp test_gen.root CMSSW_8_0_21/src/Submit/.
