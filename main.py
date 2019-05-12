#!/usr/bin/env python3

import json
import sys

action = sys.argv[1]
name = search = sys.argv[2]

if action == "write":
    description = sys.argv[3]
    value = sys.argv[4]
    tags = sys.argv[5].split(" ")

def runWrite():
    with open('sample.json') as json_file:
        data = json.load(json_file)

    with open('sample.json', 'w') as json_file:
        data["entries"].append({
                "name": name,
                "description": description,
                "value": value,
                "tags": tags
            }
        )
        json_file.write(json.dumps(data, indent=4))

def runFind():
    with open('sample.json') as json_file:
        data = json.load(json_file)
        print(json.dumps([entry for entry in data["entries"] if str(search) in entry["tags"]], indent=4))


if action == "write":
    runWrite()
if action == "find":
    runFind()
