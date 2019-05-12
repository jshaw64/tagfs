#!/usr/bin/env python3

import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--find', action='store_true')
parser.add_argument('--write', action='store_true')
parser.add_argument('--fuzzy', action='store_true')
parser.add_argument('--search', type=str, default="")
parser.add_argument('--name', type=str, default="")
parser.add_argument('--description', type=str, default="")
parser.add_argument('--value', type=str, default="")
parser.add_argument('--tags', nargs='+')
args = parser.parse_args()

name = args.name
search = args.search
description = args.description
value = args.value
tags = args.tags

def print_json(output):
    print(json.dumps(output, indent=4))

def runWrite():
    with open('sample.json') as json_file:
        data = json.load(json_file)

    with open('sample.json', 'w') as json_file:
        newKey = data["lastKey"] + 1
        data["lastKey"] = newKey
        data["entries"].append({
                "key": newKey,
                "name": name,
                "description": description,
                "value": value,
                "tags": tags
            }
        )
        json_file.write(json.dumps(data, indent=4))

def find_exact(search):
    with open('sample.json') as json_file:
        data = json.load(json_file)
        filtered = [entry for entry in data["entries"] if str(search) in entry["tags"]]

        print_json(filtered)

        return filtered

def find_fuzzy(search):
    with open('sample.json') as json_file:
        data = json.load(json_file)
        filtered = [entry for entry in data["entries"] for tag in entry["tags"] if str(search) in tag]

        print_json(filtered)

        return filtered

def find_exact_by_any_value():
    with open('sample.json') as json_file:
        data = json.load(json_file)
        filtered = []

        for entry in data["entries"]:
            for key, val in entry.items():
                if key == 'tags':
                    for tag in entry[key]:
                        if str(tag) == search:
                            filtered.append(entry)
                            break
                if str(val) == search:
                    filtered.append(entry)
                    break

        print_json(filtered)

        return filtered


if args.write:
    runWrite()
elif args.fuzzy:
    find_fuzzy(search)
elif args.find:
    find_exact(search)
else:
    print('invalid option')
