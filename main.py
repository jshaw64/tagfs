#!/usr/bin/env python3

import json
import sys

name = sys.argv[1]
description = sys.argv[2]
value = sys.argv[3]
tags = sys.argv[4].split(" ")

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
