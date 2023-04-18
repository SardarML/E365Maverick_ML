import pandas as pd
import numpy as np
from txtai.embeddings import Embeddings
from sentence_transformer_graph import get_data

str_lst, vocab, identifier_vocab = get_data()
merged_df = pd.read_csv('data\merged_df.csv')
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
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF

# graph initialization
g = Graph()

def fill_graph(query):
    # search for things that have the word __ in it and pass in how many results we want to see
    res = embeddings.search(query, 10)

    for r in res:
        # retrieve the key from the tuple
        key = txtai_data[r[0]][2]
        # retrieve the text from the tuple
        text = txtai_data[r[0]][1]
        
        # print the key, first 50 characters of the text and the similarity score
        learning_resource = URIRef('http://schema.org/LearningResource/' + Literal(key))
        g.add((learning_resource, RDF.type, Literal(f'Entity: {text[:50]} ; Similarity (txtai!!! sentence-transformers/paraphrase-multilingual-mpnet-base-v2):  {r[1]}')))
        g.add((learning_resource, URIRef('https://schema.org/Property/teaches'), Literal(query)))

fill_graph('Polynomdivision')

print(f'Graph g has {len(g)} facts')
for triples in g:
    print(f'triples{triples}')

g.serialize(destination='data/txtai_example_labeled_graph.ttl')


'''# best matches for our skill graph
print("%-20s %s" % ("Query/Topic", "Best Match"))
print("-" * 50)

# for the first 5 skills
skill_lst = skills[:5]

for query in (skill_lst):
    # Get index of best section that best matches query
    uid = embeddings.similarity(query, strings)[0][0]

    print("%-20s %s" % (f'skill: {query}',f'\nmost similar entity: {strings[uid][:50]}\n')) # take just the first 50 characters of the strings'''