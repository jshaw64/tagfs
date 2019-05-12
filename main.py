#!/usr/bin/env python3

import json

with open('sample.json') as json_file:
    data = json.load(json_file)
    print(data);
