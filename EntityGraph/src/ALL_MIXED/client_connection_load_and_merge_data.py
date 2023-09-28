import entitygraph
from entitygraph import Application, Entity
import pandas as pd
import logging

# connect to entitygraph
def client_connection(host, path, key):
    entitygraph.connect(host=host, api_key=key)

client_connection('https://entitygraph.azurewebsites.net', 'api/entities', 'Tzre7295T10z1K')

# get data from entitygraph
def connect_to_application(application_name):
    application = Application().get_by_label(application_name)
    return application

podcasts = connect_to_application('podcasts')
serlo = connect_to_application('serlo')
wlo = connect_to_application('wlo')
oersi = connect_to_application('oer')
youtube = connect_to_application('youtube')
# hpi = connect_to_application('hpi') hpi scraper not yet available

# get metadata of all LearningResources in the different applications
def get_metadata_LearningResources(application_name):
    metadata_query = """
    PREFIX sdo: <https://schema.org/>
    PREFIX schema: <http://schema.org/>
    SELECT DISTINCT ?property WHERE {
      ?LearningResource ?property ?object .
    }
    """
    metadata = application_name.Query().select(metadata_query)
    metadata_values = metadata['property'].values
    name_list = []
    for property_value in metadata_values:
        if "https://schema.org/" in property_value:
            name_list.append(property_value.split("/")[-1])

    # Dynamic generation of the SELECT clause
    select_clause = "SELECT ?LearningResource "
    for value in name_list:
        select_clause += f"?{value} "

    # Basis of SPARQL query
    query_base = f"""
    PREFIX hydra: <http://www.w3.org/ns/hydra/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sdo: <https://schema.org/>
    PREFIX schema: <http://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    {select_clause}
    WHERE {{
        ?LearningResource a ?type .
        FILTER (?type IN (sdo:LearningResource, schema:LearningResource))
    """

    # Dynamic addition to the query
    for value in name_list:
        query_base += f" OPTIONAL {{?LearningResource sdo:{value} ?{value} .}}  \n"
        query_base += f" OPTIONAL {{?LearningResource schema:{value} ?{value} .}}  \n"

    # Close the SPARQL query
    query_base += "} LIMIT 10"
    return metadata, query_base

podcast_metadata, podcasts_query_base = get_metadata_LearningResources(podcasts)
wlo_metadata, wlo_query_base = get_metadata_LearningResources(wlo)
oersi_metadata, oersi_query_base = get_metadata_LearningResources(oersi)
youtube_metadata, youtube_query_base = get_metadata_LearningResources(youtube)
serlo_metadata, serlo_query_base = get_metadata_LearningResources(serlo)

def get_values(app, query_base):
    print(app, query_base)
    app_data = app.Query().select(query_base)
    return app_data

try:
    podcasts_data = get_values(podcasts, podcasts_query_base)
    print(podcasts_data)
    serlo_data = get_values(serlo, serlo_query_base)
    print(serlo_data)
    wlo_data = get_values(wlo, wlo_query_base)
    print(wlo_data)
    oersi_data = get_values(oersi, oersi_query_base)
    print(oersi_data)
    youtube_data = get_values(youtube, youtube_query_base)
    print(youtube_data)
except Exception as e:
    logging.exception('error found:', e)

