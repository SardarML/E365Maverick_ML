import pandas as pd

def get_data():
        merged_df = pd.read_csv('data\merged_df.csv')
        strings = merged_df['String']
        str_lst = strings.values

        vocab = merged_df['Title'].values
        identifier = merged_df['identifier'].values
        identifier_vocab = pd.DataFrame({'ID': identifier, 'Vocab': vocab})
        identifier_vocab = identifier_vocab.set_index('Vocab')['ID'].to_dict()
        return str_lst, vocab, identifier_vocab

str_lst, vocab, identifier_vocab = get_data()

# get embeddings like in doc2vec
from sentence_transformers import SentenceTransformer
import numpy as np

def SentenceTransformer_embeddings():
        '''https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2
        This is a sentence-transformers model: 
        It maps sentences & paragraphs to a 768 
        dimensional dense vector space and can 
        be used for tasks like clustering or semantic search.'''

        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        embeddings = model.encode(str_lst)
        embeddings = pd.DataFrame(embeddings)
        embeddings.to_csv('data/sentence_transformer_embedding.csv')
        embeddings = np.array(embeddings)
        print(embeddings.shape)
        return model, embeddings

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rdflib import Graph, Literal, RDF, URIRef, BNode, SDO
from rdflib.namespace import RDF

model, embeddings = SentenceTransformer_embeddings()

from sklearn.metrics.pairwise import cosine_similarity

def fill_graph_sentence_transformer(query):
    # graph initialization
    g = Graph()
    # encode query
    query_vec = np.array(model.encode([query])[0]).reshape(1,-1)

    # loop for calculating similarities and saving them in the list
    similarity_list = []
    for sent in vocab:
          sent_vec = np.array(model.encode([sent])[0]).reshape(1,-1)
          sim = cosine_similarity(query_vec, sent_vec)[0][0]
          similarity_list.append((sent, sim))

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
        