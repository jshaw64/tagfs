#!/usr/bin/env python3

import json

with open('sample.json') as json_file:
    data = json.load(json_file)

with open('sample.json', 'w') as json_file:
    data["entries"].append({
            "hello": "world"
        }
    )
    json_file.write(json.dumps(data, indent=4))
