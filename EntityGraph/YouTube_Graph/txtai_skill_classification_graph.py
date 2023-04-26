import pandas as pd
import numpy as np
from txtai.embeddings import Embeddings
from sentence_transformer_graph import get_data

str_lst, vocab, identifier_vocab = get_data()
merged_df = pd.read_csv('data\merged_df_old_and_new.csv')
strings = merged_df['String']

# work with the embeddings class
embeddings = Embeddings({'path':'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'})

txtai_data = []
i=0
for id, text in zip(merged_df.index, strings):
    ''' appending the index, the text 
    and None because the embeddings object 
    is expecting 3 different components'''
    txtai_data.append((i, text, id))
    i+=1

print(f'we work with {len(txtai_data)} entitiy-textdata')

# let's quickly create our index of all the data
embeddings.index(txtai_data)

# save the embeddings index
embeddings.save('data/txtai_embeddings_encoded.csv')

import numpy as np
from rdflib import Graph, Literal, URIRef, BNode, SDO
from rdflib.namespace import RDF

def fill_graph_txtai(query):
        # graph initialization
        h = Graph()

        # search for things that have the word __ in it and pass in how many results we want to see
        res = embeddings.search(query, 5)

        for r in res:
            # retrieve the key from the tuple
            key = txtai_data[r[0]][2]
            # retrieve the text from the tuple
            text = txtai_data[r[0]][1]
            
            # define nodes
            query_term = BNode()
            h.add((query_term, RDF.type, SDO.DefinedTerm))
            h.add((query_term, SDO.termCode, Literal(query)))


            learning_resource = BNode()
            h.add((learning_resource, RDF.type, SDO.LearningResource))
            h.add((learning_resource, SDO.identifier, Literal(key)))
            # print the key, first 50 characters of the text and the similarity score
            h.add((learning_resource, SDO.title, Literal(f'Entity: {text[:50]} ; cosine similarity to the refered skill: {query}: {r[1]}')))
            h.add((learning_resource, SDO.teaches, query_term))    
        return h