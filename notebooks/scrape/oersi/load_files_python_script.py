import requests
import json


# ### Section : TO get a PIT id ####
headers = {
    'accept': 'application/json',
}

response = requests.post('https://oersi.org/resources/api/search/oer_data/_pit?keep_alive=15m&pretty', headers=headers)
# keep_alive in the above url creates the pit id  valid for next 15 minutes ; duration can be changed

res = json.loads(response.content)
pit_id = res['id']  # Pit Id received here

# #### Section : Create the first post request for first 500 records ####
headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json',
}

json_data = {
    'size': 500,  # size of requested results ; can be changed
    'query': {
        'match': {
            'mainEntityOfPage.provider.name': 'twillo',  # change here the entity provider
        },
    },
    'pit': {
        'id': pit_id,  # here the pit id
        'keep_alive': '15m',
    },
    'sort': [
        {
            'id': 'asc',
        },
    ],
    'track_total_hits': True,
}

response = requests.post('https://oersi.org/resources/api/search/_search?pretty', headers=headers, json=json_data)

res = json.loads(response.content)

output = []  # creating an empty list to store the json response later used to store in file

for hit_index in range(len(res["hits"]["hits"])):
    output.append(res["hits"]["hits"][hit_index])

last_sort_result = res['hits']['hits'][-1]['sort']
print(last_sort_result)

# #### Section:  Repeat the search query in batch of 500 results till all the results are searched.
while res['hits']['hits']:
    last_sort_result = res['hits']['hits'][-1]['sort']  # this value keeps track of last result searched

    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
    }

    json_data = {
        'size': 500,
        'query': {
            'match': {
                'mainEntityOfPage.provider.name': 'twillo',  # change here the entity provider

            },
        },
        'pit': {
            'id': pit_id,
            'keep_alive': '15m',
        },
        'sort': [
            {
                'id': 'asc',
            },
        ],
        'track_total_hits': True,
        'search_after': last_sort_result
    }

    response = requests.post('https://oersi.org/resources/api/search/_search?pretty', headers=headers, json=json_data)
    res = json.loads(response.content)

    for hit_index in range(len(res["hits"]["hits"])):
        output.append(res["hits"]["hits"][hit_index])

    print(last_sort_result)
    print(len(res['hits']['hits']))


# #### Section:  All the data in list is stored in a json file format.
# A empty json file needs to be created before running the script as only "append" ('a') command is used. ####
print(len(output))  # to check the total number of results stored in the end.
with open("twillo_data_oersi.json", "a") as outfile:
    json.dump(output, outfile, indent=4)
