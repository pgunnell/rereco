from core.model.request import Request
import json

data = {
      "energy": 1.0, 
      "memory": 2300
}

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)

with open('data_file.json', 'r') as f:
    json_keys = json.load(f)

req = Request(json_keys)
print req
