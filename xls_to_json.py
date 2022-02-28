import json
import os
from os import listdir
from os.path import isfile, join

import pandas as pd

# path to data dir
dir_path_source = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

# check for files in data dir and puts them to list
onlyfiles = []
for f in listdir(dir_path_source):
    if isfile(join(dir_path_source, f)):
        onlyfiles.append(f)

url = 'https://www.mhlw.go.jp/content/'

list_with_json = []
for filename in onlyfiles:
    # use pandas to read exls file and create dataframe
    df = pd.read_excel(join(dir_path_source, filename), sheet_name=0, skiprows=1)
    # transorm dataframe to json to read dataset easier
    df_to_json = json.loads(df.to_json(orient='records', date_format='iso'))

    for item in df_to_json:
        json_schema = {
            "source": 'Japan',
            "url": join(url, filename),
            "item": item['ITEM'].lower() if 'ITEM' in item.keys() else None,
            # if ITEM exist to item keys, lowercase its value
            "exporting_country": item['EXPORTING COUNTRY'] if 'EXPORTING COUNTRY' in item.keys() else None,
            "publication_day": item['Publication day'] if 'Publication day' in item.keys() else None,
            "contents_of_violation": item['CONTENTS OF VIOLATION'] if 'CONTENTS OF VIOLATION' in item.keys() else None,
            "quarantin_station": item['QUARANTIN STATION'] if 'QUARANTIN STATION' in item.keys() else None,
            "other_info": []
        }

        other_info = []
        for key in item.keys():
            if key not in ["ITEM", "EXPORTING COUNTRY", "Publication day", "QUARANTIN STATION",
                           "CONTENTS OF VIOLATION"]:
                info = {key.lower(): item[key]}
                other_info.append(info)
        json_schema['other_info'] = other_info

    list_with_json.append(json_schema)

# write list_with_json to json file
with open('converted_data.json', 'w') as f:
    json.dump(list_with_json, f)
