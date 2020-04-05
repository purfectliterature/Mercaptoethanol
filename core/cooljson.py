import json

def read_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read()
    return json.loads(data)

def write_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return 1

def parse_json(data):
    return json.loads(data)
