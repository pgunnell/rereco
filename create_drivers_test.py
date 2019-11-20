from core.model.driver_dataset_functions import *
import json

data = {
    "dataset_name": "MinimumBias", 
    "steps": "RAW2DIGI,L1Reco,RECO,EI,PAT",
    "global_tag": "102XXX",
    "datatier": "AOD,MINIAOD",
    "eventcontent":"AOD,MINIAOD",
    "era":"Run2_2017",
    "scenario": "pp"
}

with open("data_file_driver.json", "w") as write_file:
    json.dump(data, write_file)

with open('data_file_driver.json', 'r') as f:
    json_keys = json.load(f)

createDriver(dataset_name=json_keys['dataset_name'],steps=json_keys['steps'],global_tag=json_keys['global_tag'],datatier=json_keys['datatier'],eventcontent=json_keys['eventcontent'],era=json_keys['era'],scenario=json_keys['scenario'])
