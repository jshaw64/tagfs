#!/usr/bin/env python3

import json
import argparse
import datetime
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument('--find', action='store_true')
parser.add_argument('--list-tags', action='store_true')
parser.add_argument('--any-value', action='store_true')
parser.add_argument('--write', action='store_true')
parser.add_argument('--fuzzy', action='store_true')
parser.add_argument('--update', action='store_true')
parser.add_argument('--key', type=int, default=-1)
parser.add_argument('--search', type=str, default="")
parser.add_argument('--name', type=str, default="")
parser.add_argument('--description', type=str, default="")
parser.add_argument('--value', type=str, default="")
parser.add_argument('--tags', nargs='+')
parser.add_argument('--print', action='store_true')
parser.add_argument('--delete', action='store_true')
args = parser.parse_args()

name = args.name
search = args.search
description = args.description
value = args.value
tags = args.tags

data_path = os.path.join(os.environ['jfs_dir_appdata'], 'tagfs')

if not os.path.isdir(data_path):
    data_path = f'{os.path.dirname(__file__)}/data/'

def print_json(output):
    print(json.dumps(output, indent=4))

def write_json(output):
    timestamp = datetime.datetime.now().timestamp()
    filename = f"{data_path}/{timestamp}.json"

    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(output, indent=4))

def get_latest_dataset():
    list_of_files = glob.glob(f'{data_path}/*')
    latest_file = max(list_of_files, key=os.path.getctime)

    return latest_file

def print_latest_dataset():
    with open(get_latest_dataset()) as json_file:
        print_json(json.load(json_file))

def print_all_tags():
    with open(get_latest_dataset()) as json_file:
        data = json.load(json_file)

        all_tags = []
        for entry in data["entries"]:
            for tag in entry["tags"]:
                all_tags.append(tag)

        all_tags_deduped = []
        seen = []
        for tag in all_tags:
            if tag not in seen:
                all_tags_deduped.append(tag)
                seen.append(tag)

        print_json(all_tags_deduped)

def run_write():
    with open(get_latest_dataset()) as json_file:
        data = json.load(json_file)

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

        write_json(data)

def find_exact(search):
    with open(get_latest_dataset()) as json_file:
        data = json.load(json_file)
        filtered = [entry for entry in data["entries"] if str(search) in entry["tags"]]

        print_json(filtered)

        return filtered

def find_fuzzy(search):
    with open(get_latest_dataset()) as json_file:
        data = json.load(json_file)
        filtered = [entry for entry in data["entries"] for tag in entry["tags"] if str(search) in tag]

        print_json(filtered)

        return filtered

def find_exact_by_any_value():
    with open(get_latest_dataset()) as json_file:
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

        deduped = []
        seen = []
        for entry in filtered:
            if entry['key'] not in seen:
                deduped.append(entry)
                seen.append(entry['key'])

        print_json(deduped)

        return deduped

def find_fuzzy_by_any_value():
    with open(get_latest_dataset()) as json_file:
        data = json.load(json_file)

        filtered = []
        for entry in data["entries"]:
            for key, val in entry.items():
                if key == 'tags':
                    for tag in entry[key]:
                        if search in str(tag):
                            filtered.append(entry)
                            break
                if search in str(val):
                    filtered.append(entry)
                    break

        deduped = []
        seen = []
        for entry in filtered:
            if entry['key'] not in seen:
                deduped.append(entry)
                seen.append(entry['key'])


        print_json(deduped)

        return deduped

def update_by_key(key):
    with open(get_latest_dataset()) as json_file:
        data = json.load(json_file)

        filtered = [entry for entry in data["entries"] if entry["key"] == key][0]

        if args.name:
            filtered["name"] = args.name
        if args.description:
            filtered["description"] = args.description
        if args.value:
            filtered["value"] = args.value
        if args.tags:
            filtered["tags"] = args.tags

        for entry in data['entries']:
            if entry['key'] == args.key:
                entry = filtered
                break

        return data

def run_update_by_key(key):
    updated = update_by_key(key)

    print_json(updated)
    write_json(updated)

def delete_by_key(key):
    with open(get_latest_dataset()) as json_file:
        data = json.load(json_file)

        filtered = [entry for entry in data["entries"] if entry["key"] != key]
        data["entries"] = filtered

        return data

def run_delete_by_key(key):
    updated = delete_by_key(key)

    print_json(updated)
    write_json(updated)

if args.write:
    run_write()
elif args.update:
    run_update_by_key(args.key)
elif args.any_value:
    if args.fuzzy:
        find_fuzzy_by_any_value()
    else:
        find_exact_by_any_value()
elif args.fuzzy:
    find_fuzzy(search)
elif args.find:
    find_exact(search)
elif args.print:
    print_latest_dataset()
elif args.list_tags:
    print_all_tags()
elif args.delete:
    run_delete_by_key(args.key)
else:
    print('invalid option')
