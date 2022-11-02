import json

def get_json():
    json_file = open('website/static/json_files/suggestions.json')

    data = json.load(json_file)

    # for continent in data:
    #     for trip in data[continent]:
    #         print(trip + ": " + data[continent][trip])
    return data

