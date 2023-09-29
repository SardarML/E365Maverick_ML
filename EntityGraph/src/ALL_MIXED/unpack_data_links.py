import pandas as pd
import requests

serlo_data = pd.read_csv('data/serlo_data.csv')

# for example: get serlo textdata
base_url = 'https://entitygraph.azurewebsites.net'
urls = []

for i in serlo_data['contentUrl']:
    url = base_url + i
    urls.append(url)

# for url in urls:
#     print(url)

data_s = pd.DataFrame(columns=['id', 'name', 'content', 'url'])

for index, row in serlo_data.iterrows():
    response = requests.get(base_url + row['contentUrl'])
    if response.status_code == 200:

        # Extract the ID and name from the row
        id = row['identifier']
        name = row['name']

        # Add new data point to the DataFrame using pd.concat
        data_s = pd.concat([data_s, pd.DataFrame({'id': [id], 'name': [name], 'content': [response.text], 'url' : ['https://serlo.org/'+str(id)]})], ignore_index=True)
    else:
        print(f"The file at URL {base_url + row['contentUrl']} could not be downloaded.")

data_s = data_s.set_index('id')
data_s = data_s.rename(columns={"name": "title"})
data_s = data_s.rename(columns={"article": "LearningResource"})

print('new serlo data with texts: ', data_s.head())