import requests
import json
import pandas as pd

def get_data_HPI(path):
    response = requests.get(path)

    # Check if the request was successful & Convert JSON data to a Python object
    if response.status_code == 200:
        data = response.json()

    #     # Extract data (here as an example the names of the courses)
    #     for course in data['data']:
    #         print(course['attributes']['name'])
    # else:
    #     print(f"Request failed with status code {response.status_code}.")

    # Extract the data points from the 'data' key
    data_points = data['data']
    data = pd.DataFrame([point['attributes'] for point in data_points])
    return data

imoox = get_data_HPI('https://imoox.at/mooc/local/moochubs/classes/webservice.php')
oncampus = get_data_HPI('https://moodalis.oncampus.de/files/moochub.php')
open_vhb = get_data_HPI('https://open.vhb.org/moochub_new.json')
openHPI = get_data_HPI('https://open.hpi.de/bridges/moochub/courses')
KI_campus = get_data_HPI('https://learn.ki-campus.org/bridges/moochub/courses')
openSAP = get_data_HPI('https://open.sap.com/bridges/moochub/courses')
lernen_cloud = get_data_HPI('https://lernen.cloud/bridges/moochub/courses')
future_learn_lab = get_data_HPI('https://futurelearnlab.de/hub/local/ildmeta/get_moochub_courses.php')
eGov_campus = get_data_HPI('https://learn.egov-campus.org/bridges/moochub/courses')

def merge_data():
    HPI_dataframes = [imoox,
                oncampus,
                open_vhb,
                openHPI,
                KI_campus,
                openSAP,
                lernen_cloud,
                eGov_campus,
                future_learn_lab]

    HPI_dataframes = pd.concat(HPI_dataframes, axis=0, ignore_index=True)
    return HPI_dataframes

HPI_dataframes = merge_data()
print(HPI_dataframes)

# HPI_dataframes.to_csv('data\HPI\merged_HPI_data.csv')