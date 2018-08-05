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


scram b
cd ../../
cmsDriver.py step1 --filein "file:test_aod.root" --fileout file:test_miniaod.root --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step PAT --nThreads 4 --era Run2_2016 --python_filename run_miniaod.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 100 || exit $? ; 

mkdir CMSSW_8_0_21/src/Submit
cp run_miniaod.py CMSSW_8_0_21/src/Submit/.
cp test_aod.root CMSSW_8_0_21/src/Submit/.
cp crab_miniaod.py CMSSW_8_0_21/src/Submit/.
