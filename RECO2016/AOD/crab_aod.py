from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from multiprocessing import Process
config = config()

config.General.requestName     = 'AOD'
config.General.workArea        = 'AOD'
config.General.transferOutputs = True
config.General.transferLogs    = True
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 15000

config.JobType.pluginName = 'ANALYSIS'
config.JobType.psetName   = 'run_aod.py'

config.Data.inputDBS             = 'phys03'
config.Data.splitting            = 'EventAwareLumiBased'
config.Data.unitsPerJob          = 2000
config.Data.totalUnits           = -1
config.Data.outLFNDirBase        = '/store/user/%s/MG5MC_2016/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.ignoreLocality      = True
config.Site.whitelist   = ['T2_*','T1_*','T3_*']
config.Site.storageSite = 'T2_UK_London_IC'

#config.Debug.extraJDL = [
#    '+DESIRED_Sites="T3_UK_Opportunistic_dodas"',
#    '+JOB_CMSSite="T3_UK_Opportunistic_dodas"',
#    '+AccountingGroup="highprio.dciangot"',
#    '+PeriodicRemove=False',
#]

#config.Data.outputDatasetTag = 'GluGluToHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2017-AOD-Plus2'
#config.General.requestName = 'GluGluHToTauTau_M125_MG5Plus2'
#config.Data.inputDataset = '/GluGluToHToTauTauPlusTwoJets_M125_13TeV_amcatnloFXFX_pythia8_2017-GEN/dwinterb-GluGluToHToTauTauPlusTwoJets_M125_13TeV_amcatnloFXFX_pythia8_2017-PUMIX-5b9cd2c7eef36524de7af1c8e43b0ebc/USER'


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print hte.headers

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    tasks=list()
    
    tasks.append(('GluGluToMaxmixHToTauTauPlusTwoJets_M125_MG5', '/GluGluToMaxmixHToTauTauPlusTwoJets_M125_13TeV_amcatnloFXFX_pythia8_2017-GEN/dwinterb-GluGluToMaxmixHToTauTauPlusTwoJets_M125_13TeV_amcatnloFXFX_pythia8_2017-PUMIX-5b9cd2c7eef36524de7af1c8e43b0ebc/USER', 'GluGluToMaxmixHToTauTauPlusTwoJets_M125_13TeV_amcatnloFXFX_pythia8_2017-AOD'))


    for task in tasks:
        print task[0]
        config.Data.outputDatasetTag = task[2]
        config.General.requestName = task[2]
        config.Data.inputDataset = task[1]
        #submit(config)

        p = Process(target=submit, args=(config,))
        p.start()
        p.join()



