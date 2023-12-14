from rdflib import Graph

g = Graph()

# example
g.parse('data/txtai_embeddings_encoded\Meditation_s_t.json', format='json-ld')

from rdflib import Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import XSD

sdo = Namespace("https://schema.org/")

def extract_skill():
    # split out the cosine similarity
    # find the node that defines the skill taught in the learning resources
    for s, p, o in g.triples((None, RDF.type, sdo.DefinedTerm)):
        termCode = str(g.value(s, sdo.termCode))

    # now termCode variable contains the specific skill
    print(f"Extracted skill: {termCode} \n")

    # get the cosine similarity con of the referenced skill separately
    # search all learning resources nodes
    for s, p, o in g.triples((None, RDF.type, sdo.LearningResource)):

        # find the title for the current node
        for title in g.objects(s, sdo.title):

            # Remove the word 'Entity'
            clean_title = str(title).replace('Entity', '')

            # split the title string
            parts = clean_title.split(f"; cosine similarity to the refered skill: {termCode}: ")

            # update the title and add the cosine similarity if present
            if len(parts) == 2:
                g.set((s, sdo.title, Literal(parts[0])))
                g.add((s, sdo.cosineSimilarity, Literal(float(parts[1]), datatype=XSD.float)))

extract_skill()

# extract identifiers
def extract_id():
    identifiers = []
    for res in g.subjects(predicate=sdo.identifier):
        identifier = g.value(subject=res, predicate=sdo.identifier)
        identifiers.append(identifier)
    return identifiers

identifiers = extract_id()

def get_file_urls(ids):
    base_url = 'https://www.youtube.com/watch?v='
    file_urls = []

    for file_id in ids:
        file_url = f"{base_url}{file_id}"
        file_urls.append(file_url)
    return file_urls

file_urls = get_file_urls(identifiers)

from pytube import YouTube
import pandas as pd
import logging

def infos(urls):
    video_information = pd.DataFrame(columns=['identifier', 'Thumbnail'])
    for url in urls:
        try:
            yt = YouTube(url)
            thumb = yt.thumbnail_url
            video_id = yt.video_id
            new_row = pd.DataFrame({'identifier': [video_id], 
                                    'Thumbnail': [thumb],
                                    'url': [url]})
            video_information = pd.concat([video_information, new_row], ignore_index=True)
        except Exception as e:
            logging.error(f"Fehler: {e} beim Extrahieren von Thumbnail für URL: {url}")
    video_information.drop_duplicates(subset='identifier', keep='first', inplace=True)
    video_information.set_index('identifier', inplace=True)
    return video_information

infos = infos(file_urls)

import pandas as pd
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import XSD

sdo = Namespace("https://schema.org/")

# loop over the DataFrame
def find_matches():
    for idx, row in infos.iterrows():

        # find the matching node in the RDF graph
        matching_nodes = list(g.subjects(predicate=sdo.identifier, object=Literal(idx)))

        if matching_nodes:

            # it is assumed that there is only one matching node
            node = matching_nodes[0]

            # add the new properties
            #g.add((node, sdo.Article, Literal(wiki_zusammenfassung, datatype=XSD.anyURI)))
            g.add((node, sdo.url, Literal(row['url'], datatype=XSD.anyURI)))
            g.add((node, sdo.thumbnailUrl, Literal(row['Thumbnail'], datatype=XSD.anyURI)))

find_matches()

print(g.serialize(format='ttl'))

# change the format
g.serialize('data/txtai_embeddings_encoded\Meditation_s_t.json', format='json-ld')

# change the format
g.serialize('data/txtai_embeddings_encoded\Meditation_s_t.ttl', format='ttl')