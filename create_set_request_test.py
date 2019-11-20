from core.model.request import Request
from core.model.driver_dataset_functions import *
import json

dataset_name = GetDatasets("Run2017B","MINIAOD")
print(dataset_name)

for data_name in dataset_name:
    data = {
        "energy": 1.0, 
        "memory": 2300,
        "input_dataset_name": data_name['dataset']
    }

    req = Request(data)
    print req
