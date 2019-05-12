#!/usr/bin/env python3

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--find', action='store_true')
parser.add_argument('--search', type=str, default="")
parser.add_argument('--name', type=str, default="")
parser.add_argument('--description', type=str, default="")
parser.add_argument('--value', type=str, default="")
parser.add_argument('--tags', type=str, default="")
args = parser.parse_args()

action = "find" if args.find else "write"
name = args.name
search = args.search
description = args.description
value = args.value
tags = args.tags.split(" ")

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
