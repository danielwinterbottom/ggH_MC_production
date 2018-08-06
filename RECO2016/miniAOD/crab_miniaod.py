from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from multiprocessing import Process
config = config()

config.General.requestName     = 'MiniAOD'
config.General.workArea        = 'MiniAOD'
config.General.transferOutputs = True
config.General.transferLogs    = True
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000

config.JobType.pluginName = 'ANALYSIS'
config.JobType.psetName   = 'run_miniaod.py'

config.Data.inputDBS             = 'phys03'
config.Data.splitting            = 'EventAwareLumiBased'
config.Data.unitsPerJob          = 6000
config.Data.totalUnits           = -1
config.Data.outLFNDirBase        = '/store/user/%s/MG5MC_2016/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.ignoreLocality      = True
config.Site.whitelist   = ['T2_*','T1_*','T3_*']

#config.Debug.extraJDL = [
#    '+DESIRED_Sites="T3_UK_Opportunistic_dodas"',
#    '+JOB_CMSSite="T3_UK_Opportunistic_dodas"',
#    '+AccountingGroup="highprio.dciangot"',
#    '+PeriodicRemove=False',
#]

#config.Data.outputDatasetTag = 'GluGluToHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2017-MiniAOD'
#config.General.requestName = 'GluGluHToTauTau_M125_MG5'
#config.Data.inputDataset = '/GluGluToHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2017-GEN/dwinterb-GluGluToHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2017-AOD-c3d6de13a4792afb4dd0c4ab58e49a3d/USER'


config.Site.storageSite = 'T2_UK_London_IC'

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
    

    tasks.append(('GluGluToPseudoscalarHToTauTau_M125_MG5', '/GluGluToPseudoscalarHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-GEN/dwinterb-GluGluToPseudoscalarHToTauTauPlusTwoJets_M125_13TeV_amcatnloFXFX_pythia8_2016-AOD-b1a4edca9adfa7a2e4059536bf605cd7/USER', 'GluGluToPseudoscalarHToTauTau_M125_13TeV_amcatnloFXFX_pythia8_2016-MiniAOD'))

    for task in tasks:
        print task[0]
        config.Data.outputDatasetTag = task[2]
        config.General.requestName = task[2]
        config.Data.inputDataset = task[1]
        #submit(config)

        p = Process(target=submit, args=(config,))
        p.start()
        p.join()



