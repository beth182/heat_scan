import json

temp_file_name = 'test_json_BRA.json'

with open(temp_file_name, 'r') as f:
    output = json.load(f)

print(' ')