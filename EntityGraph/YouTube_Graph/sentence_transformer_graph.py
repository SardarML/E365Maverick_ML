import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rdflib import Graph, Literal, RDF, URIRef, BNode, SDO
from rdflib.namespace import RDF
from get_merged_data import get_data
from sentence_transformer_generate_embeddings import SentenceTransformer_embeddings

merged_df, str_lst, vocab, identifier_vocab, identifier = get_data('data/merged_data_for_AI.csv')
model, embeddings = SentenceTransformer_embeddings()

def fill_graph_sentence_transformer(query):
        # graph initialization
        g = Graph()

        # encode query
        query_vec = np.array(model.encode([query])[0]).reshape(1,-1)
        print(query_vec.shape)

        # loop for calculating similarities and saving them in the list
        similarity_list = []
        for i, sent_vec in enumerate(embeddings):
            sim = cosine_similarity(query_vec, sent_vec.reshape(1, -1))[0][0]
            similarity_list.append((vocab[i], sim))

        # sorting the list of similarities in descending order by the 2nd element (similarity)
        sorted_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)

        # define nodes
        query_term = BNode()
        g.add((query_term, RDF.type, SDO.DefinedTerm))
        g.add((query_term, SDO.termCode, Literal(query)))

        # parsing output of the sorted list in RDF
        for item in sorted_list[:5]:
            id = identifier_vocab.get(item[0])  # retrieve identifier for the current element
            learning_resource = BNode()
            g.add((learning_resource, RDF.type, SDO.LearningResource))
            g.add((learning_resource, SDO.identifier, Literal(id)))
            g.add((learning_resource, SDO.title, Literal(f'Entity: {item[0]} ; cosine similarity to the refered skill: {query}: {item[1]}')))
            g.add((learning_resource, SDO.teaches, query_term))
        return g
        