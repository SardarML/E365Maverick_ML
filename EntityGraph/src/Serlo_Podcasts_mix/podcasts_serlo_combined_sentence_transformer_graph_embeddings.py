import pandas as pd
import numpy as np
from rdflib import Graph, Literal, RDF, URIRef, BNode, SDO
from rdflib.namespace import RDF, XSD
import logging

def get_data(path):
        merged_df = pd.read_csv(path,
                 lineterminator='\n')
        strings = merged_df['String']
        str_lst = strings.values

        vocab = merged_df['title'].values
        identifier = merged_df['id']
        identifier_vocab = pd.DataFrame({'ID': identifier, 'Vocab': vocab})
        identifier_vocab = identifier_vocab.set_index('Vocab')['ID'].to_dict()
        urls = merged_df['url']
        url_vocab = pd.DataFrame({'ID': identifier, 'URL': urls})
        url_vocab = url_vocab.set_index('URL')['ID'].to_dict()

        return merged_df, str_lst, vocab, identifier_vocab, identifier, urls, url_vocab

merged_df, str_lst, vocab, identifier_vocab, identifier, urls, url_vocab = get_data('data/Serlo_Podcasts_mix/merged_serlo_podcast_data_without_stopwords.csv')

# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

# embeddings = model.encode(str_lst)
# weights = embeddings
# weights = pd.DataFrame(weights)
# weights.to_csv('data/Serlo_Podcasts_mix/merged_serlo_podcast_embeddings.csv')
# print(weights.shape)

import numpy as np

weights = pd.read_csv('data/Serlo_Podcasts_mix/merged_serlo_podcast_embeddings.csv')
del weights['Unnamed: 0']
weights = weights.values
weights.shape

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# get embeddings like in doc2vec
def SentenceTransformer_embeddings():
        '''https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2
        This is a sentence-transformers model:
        It maps sentences & paragraphs to a 768
        dimensional dense vector space and can
        be used for tasks like clustering or semantic search.'''

        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        embeddings = weights
        print(embeddings.shape)
        return model, embeddings

model, embeddings = SentenceTransformer_embeddings()

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
        return identifiers

    identifiers = extract_id()

    def get_urls():
        id_to_url_vocab = {v: k for k, v in url_vocab.items()}
        for s, p, o in g.triples((None, RDF.type, SDO.LearningResource)):
            # Retrieve the identifier for the current node
            identifier = g.value(subject=s, predicate=SDO.identifier)
            if identifier is not None:
                # Convert the identifier to a string
                id_str = str(identifier)
                # Retrieve the URL for the current identifier
                url = id_to_url_vocab.get(id_str)
                # Add the URL to the graph if it exists
                if url is not None:
                    g.add((s, SDO.url, Literal(url)))
    get_urls()

    return g
