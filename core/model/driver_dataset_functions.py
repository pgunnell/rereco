import json
from dbs.apis.dbsClient import DbsApi

url="https://cmsweb.cern.ch/dbs/prod/global/DBSReader"
api=DbsApi(url=url)

from Configuration.Skimming.autoSkim import autoSkim
from Configuration.AlCa.autoAlca import AlCaRecoMatrix

#Example of json file
#jsonFile = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'


def GetRuns(jsonFile):

    with open(jsonFile) as data_file:
        data = json.load(data_file)

    AlltheRuns = map(int,data.keys())
    #print sorted(AlltheRuns)
    #print "# of runs in the JSON: ", len(AlltheRuns)
    
    return AlltheRuns

#this will give us the input datasets for the first requests (if datatier="MINIAOD", one has the input for NanoAOD)
def GetDatasets(era="RunYearVersion", datatier="RAW"):
    
    theDatasets = api.listDatasets( dataset='/*/%s*/%s' % (era , datatier) )
    #print theDatasets
    
    return theDatasets

#return skim matrix which needs to be used in the driver
def GetAutoSkim(dataset_name="JetHT"):
    
    skimseq = ''
    if dataset_name in autoSkim.keys():
        skimseq='SKIM:%s,'%(autoSkim[dataset_name])

    return skimseq

#return alcareco matrix which needs to be used in the driver
def GetAlcaRecoMatrix(dataset_name="JetHT"):
    
    alcaseq=''
    if dataset_name in AlCaRecoMatrix.keys():
         alcaseq='ALCA:%s,'%(AlCaRecoMatrix[dataset_name])

    return alcaseq

#return alcareco matrix which needs to be used in the driver
def GetDQMsequence(dataset_name="JetHT"):
    
    dqmseq=''
    if (dataset_name=="ZeroBias") :
        dqmseq = 'DQM:@rerecoZeroBias'
    elif(dataset_name=="SingleMuon") :
        dqmseq = 'DQM:@rerecoSingleMuon'
    else :
        dqmseq = 'DQM:@rerecoCommon'

    return dqmseq

def createDriver(dataset_name="JetHT", global_tag="102XXX", steps="RAW2DIGI,L1Reco,RECO,EI,PAT",datatier="AOD,MINIAOD", eventcontent="AOD,MINIAOD", era="Run2_2017", scenario="pp", customize="Configuration/DataProcessing/RecoTLR.customisePostEra_Run2_2017", filename="file_cfg.py", n_cores=8, extra=""):

    alcaseq=GetAlcaRecoMatrix(dataset_name)
    skimseq=GetAutoSkim(dataset_name)
    dqmseq=GetDQMsequence(dataset_name)
    steps=str(steps)+str(alcaseq)+str(skimseq)+str(dqmseq)

    sequences = "RECO --step %s --runUnscheduled --nThreads %i --data --era %s --scenario %s --conditions %s --eventcontent %s --datatier %s --customize %s --filein file:pippo.root -n 100 --python_filename=%s %s" %(steps, n_cores, era, global_tag, scenario, eventcontent, datatier, customize, filename, extra) 

    print(sequences)

    return sequences

def createHarvestDriver(dataset_name="JetHT", global_tag="102XXX", steps="HARVEST", datatier="DQMIO", era="Run2_2017", filename="file_cfg.py", extra=""):

    dqmseq=GetDQMsequence(dataset_name)

    sequences = "step4 --step %s --filetype DQM --data --era %s --conditions %s --filein file:pippo.root -n 100 --python_filename=%s %s" %(steps, era, global_tag, filename, extra)

    return sequences
