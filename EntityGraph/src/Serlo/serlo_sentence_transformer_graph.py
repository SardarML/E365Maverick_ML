import numpy as np
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, BNode, SDO
from rdflib.namespace import RDF, XSD
import logging
from sklearn.metrics.pairwise import cosine_similarity
from get_data import get_data
from generate_embeddings import SentenceTransformer_embeddings

merged_df, str_lst, vocab, identifier_vocab, identifier = get_data('data\Serlo\merged_serlo_data_without_stopwords.csv')
model, weights = SentenceTransformer_embeddings()

def fill_graph_sentence_transformer(query):
    # graph initialization
    g = Graph()

    # encode query into a vector
    query_vec = np.array(model.encode([query])[0]).reshape(1,-1)
    print(query_vec.shape)

    # loop for calculating similarities and saving them in the list
    '''here we go through the entire weight matrix and compare the
    similarity of the entered skill (query) with the embeddings of all learning
    resources from our dataset'''
    similarity_list = []
    for i, sent_vec in enumerate(weights):
        sim = cosine_similarity(query_vec, sent_vec.reshape(1, -1))[0][0]
        similarity_list.append((vocab[i], sim))

    # sorting the list of similarities in descending order by the 2nd element (similarity)
    sorted_list = sorted(similarity_list, key=lambda x: x[1], reverse=True)

    # define nodes | DefinedTerm is the skill
    query_term = BNode()
    g.add((query_term, RDF.type, SDO.DefinedTerm))
    g.add((query_term, SDO.termCode, Literal(query)))

    # parsing output of the sorted list in RDF
    for item in sorted_list[:5]:
        # retrieve identifier for the current element
        id = identifier_vocab.get(item[0])
        learning_resource = BNode()
        g.add((learning_resource, RDF.type, SDO.LearningResource))
        g.add((learning_resource, SDO.identifier, Literal(id)))
        g.add((learning_resource, SDO.title, Literal(f'{item[0]} ; cosine similarity to the refered skill: {query}: {item[1]}')))
        g.add((learning_resource, SDO.teaches, query_term))

    def extract_skill():
        # split out the cosine similarity
        # find the node that defines the skill taught in the learning resources
        for s, p, o in g.triples((None, RDF.type, SDO.DefinedTerm)):
            termCode = str(g.value(s, SDO.termCode))

        # now termCode variable contains the specific skill
        print(f"Extracted skill: {termCode} \n")

        # get the cosine similarity of the referenced skill separately
        # search all learning resource nodes
        for s, p, o in g.triples((None, RDF.type, SDO.LearningResource)):

            # find the title for the current node and split the string
            for title in g.objects(s, SDO.title):
                parts = title.split(f"; cosine similarity to the refered skill: {termCode}: ")

                # update the title and add the cosine similarity if present
                if len(parts) == 2:
                    g.set((s, SDO.title, Literal(parts[0])))
                    g.add((s, SDO.result, Literal(float(parts[1]), datatype=XSD.float)))

    extract_skill()

    # extract identifiers
    def extract_id():
        identifiers = []
        for s, p, o in g.triples((None, RDF.type, SDO.LearningResource)):
            identifier = g.value(subject=s, predicate=SDO.identifier)
            if identifier is not None:
                identifiers.append(str(identifier))
                g.add((s, SDO.url, Literal('https://serlo.org/' + str(identifier))))
        return identifiers

    identifiers = extract_id()
    return g