# in terminal: 
# pip install git+https://github.com/mumi/entitygraph-client.git

import entitygraph
from entitygraph import Application, Entity
import pandas as pd
import requests

host = "https://entitygraph.azurewebsites.net"
path = "api/entities"
key = ""

entitygraph.connect(host=host, api_key=key)

application_podcasts = "podcasts"
application_serlo = "serlo"
app_podcasts = Application().get_by_label(application_podcasts)
app_serlo = Application().get_by_label(application_serlo)

query= """

PREFIX sdo: <https://schema.org/>

SELECT ?PodcastEpisode ?title ?url ?identifier ?description

WHERE {
    ?PodcastEpisode a sdo:PodcastEpisode .
    ?PodcastEpisode sdo:title ?title .
    ?PodcastEpisode sdo:url ?url .
    ?PodcastEpisode sdo:identifier ?identifier .
    ?PodcastEpisode sdo:description ?description .
}

"""

podcast_data = app_podcasts.Query().select(query)
#podcast_data = podcast_data.rename(columns={"PodcastEpisode": "LearningResource"})
podcast_data = podcast_data.rename(columns={"identifier": "id"})
podcast_data = podcast_data.rename(columns={"description": "content"})
podcast_data = podcast_data.set_index('id')

podcast_data = podcast_data[['title', 'content', 'url']]
print(f'we work with {len(podcast_data)} podcasts')
#print(f'podcast data: {podcast_data.head()}')
podcast_data.to_csv('data\Serlo_Podcasts_mix\podcast_data.csv')

query_str = """

PREFIX schema: <http://schema.org/>
PREFIX sdo: <https://schema.org/>

SELECT ?article ?name ?contentUrl ?identifier
WHERE {
    ?article a schema:Article .
    ?article schema:name ?name .
    ?article sdo:text ?MediaObject .
    ?MediaObject sdo:contentUrl ?contentUrl .
    ?article schema:identifier/schema:value ?identifier .
}

"""

serlo_data = app_serlo.Query().select(query_str)
print(f'we work with {len(serlo_data)} serlo articles')
#print(f' serlo data: {serlo_data.head()}')

# get serlo textdata
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
data_s.to_csv('data\Serlo_Podcasts_mix\serlo_data.csv')

