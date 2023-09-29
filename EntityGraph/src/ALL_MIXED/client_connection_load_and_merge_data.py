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
#serlo = connect_to_application('serlo')
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
        if "://schema.org/" in property_value:
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
        #query_base += f" OPTIONAL {{?LearningResource schema:{value} ?{value} .}}  \n"

    # Close the SPARQL query
    query_base += "}"
    return metadata, query_base

podcast_metadata, podcasts_query_base = get_metadata_LearningResources(podcasts)
wlo_metadata, wlo_query_base = get_metadata_LearningResources(wlo)
oersi_metadata, oersi_query_base = get_metadata_LearningResources(oersi)
youtube_metadata, youtube_query_base = get_metadata_LearningResources(youtube)
# serlo_metadata, serlo_query_base = get_metadata_LearningResources(serlo)

def get_values(app, query_base, use_pagination=False, limit=1000, max_iterations=None):
    if not use_pagination:
        print(query_base)
        app_data = app.Query().select(query_base)
        return app_data.drop_duplicates()

    offset = 0
    all_data_frames = []
    iteration = 0

    while True:
        # Optional check for max_iterations
        if max_iterations and iteration >= max_iterations:
            print("Max iterations reached!")
            break

        # Add LIMIT and OFFSET to your query
        paginated_query = f"{query_base} LIMIT {limit} OFFSET {offset}"
        print(paginated_query)

        data_chunk = app.Query().select(paginated_query)

        # Log the amount of data fetched in this chunk
        print(f"Received {len(data_chunk)} rows in iteration {iteration}")

        # Break the loop if the data chunk has less than the limit, indicating that we've fetched all data
        if len(data_chunk) < limit:
            all_data_frames.append(data_chunk)
            break

        # Remove duplicates from the current data chunk
        data_chunk = data_chunk.drop_duplicates()
        all_data_frames.append(data_chunk)

        offset += limit
        iteration += 1

    # Combine all data frames
    combined_data = pd.concat(all_data_frames, ignore_index=True)

    # Final check for duplicates after combining all chunks
    return combined_data.drop_duplicates()

# Example usage
try:
    podcasts_data = get_values(podcasts, podcasts_query_base, use_pagination=True)
    podcasts_data.to_csv('data\ALL_MIXED\podcasts_data.csv')

    wlo_data = get_values(wlo, wlo_query_base, use_pagination=True)
    wlo_data.to_csv('data\ALL_MIXED\wlo_data.csv')

    oersi_data = get_values(oersi, oersi_query_base, use_pagination=True)
    oersi_data.to_csv('data\ALL_MIXED\oersi_data.csv')

    youtube_data = get_values(youtube, youtube_query_base, use_pagination=True)
    youtube_data.to_csv('data\ALL_MIXED\youtube_data.csv')

    # serlo_data = get_paginated_values(serlo, serlo_query_base)
    # serlo_data.to_csv('data\ALL_MIXED\serlo_data.csv')

except Exception as e:
    logging.exception('error found:', e)

