import youtube_dl
from pytube import YouTube
import io
import numpy as np
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, SKOS


## get entities
def entities():
    infos = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_infos_entities_benchmark.csv', index_col=0)
    video_entities =infos.values
    return video_entities

video_entities = entities()
#print('entities:\n', video_entities)


## get properties

# generate uris as property
def uris():
    infos = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_infos_entities_benchmark.csv', index_col=0) 
    ids = infos.index.values
    video_identifiers = np.array([URIRef(id) for id in ids])
    return video_identifiers

video_identifiers = uris()
#print('IDs:\n', video_identifiers) 

tags_frame = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_tags_benchmark.csv', index_col=0)
tags = tags_frame.values

captions_frame = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_descriptions_benchmark.csv', index_col=0)
captions = captions_frame.values

transcriptions_whisper_frame = pd.read_csv('data_benchmarks/transcriptions_benchmark/transcriptions_benchmark_whisper.csv', index_col=0)
transcriptions_whisper = transcriptions_whisper_frame.values

transcriptions_pydub_frame = pd.read_csv('data_benchmarks/transcriptions_benchmark/transcriptions_benchmark_pydub.csv', index_col=0)
transcriptions_pydub = transcriptions_pydub_frame.values


## graph initialization
g = Graph()

def fill_graph():
    for i in range(len(video_entities)):
        learning_resource = URIRef('http://schema.org/LearningResource/' + video_identifiers[i])
        g.add((learning_resource, RDF.type, Literal(video_entities[i])))

        g.add((learning_resource, URIRef('https://schema.org/Property/tags'), Literal(tags[i])))

        # get the 500 first characters of the string
        g.add((learning_resource, URIRef('https://schema.org/Property/captions'), Literal(captions[i][0][:500])))

        # get the 500 first characters of the string
        g.add((learning_resource, URIRef('https://schema.org/Property/transcript'), Literal(transcriptions_whisper[i][0][:500])))

        g.add((learning_resource, URIRef('https://schema.org/Property/teaches'), Literal('Recommendation_node' + video_identifiers[i])))

fill_graph()

'''# get graph & triples (s,p,o)
print('Graph g:\n', g.serialize(format='ttl'))
print(f'Graph g has {len(g)} facts')
for triples in g:
    print(f'triples{triples}')'''

## download graph
# plot the graph --> https://www.ldf.fi/service/rdf-grapher
g.serialize(destination='data_benchmarks/benchmark_EntitiyGraph.ttl')