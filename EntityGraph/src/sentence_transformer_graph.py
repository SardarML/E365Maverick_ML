import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rdflib import Graph, Literal, RDF, URIRef, BNode, SDO
from rdflib.namespace import RDF, XSD
from pytube import YouTube
import logging
from get_merged_data import get_data
from sentence_transformer_generate_embeddings import SentenceTransformer_embeddings

merged_df, str_lst, vocab, identifier_vocab, identifier = get_data('data\merged_data_for_AI.csv')
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
    for i, sent_vec in enumerate(embeddings):
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
                    g.add((s, SDO.cosineSimilarity, Literal(float(parts[1]), datatype=XSD.float)))

    extract_skill()

    # extract identifiers
    def extract_id():
        identifiers = []
        for res in g.subjects(predicate=SDO.identifier):
            identifier = g.value(subject=res, predicate=SDO.identifier)
            identifiers.append(identifier)
        return identifiers

    identifiers = extract_id()

    # extract urls
    def get_file_urls(ids):
        base_url = 'https://www.youtube.com/watch?v='
        file_urls = []

        for file_id in ids:
            file_url = f"{base_url}{file_id}"
            file_urls.append(file_url)
        return file_urls

    file_urls = get_file_urls(identifiers)

    # extract infos (here: thumbnail)
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
                logging.error(f"error: {e} when extracting thumbnail for URL: {url}")
        video_information.drop_duplicates(subset='identifier', keep='first', inplace=True)
        video_information.set_index('identifier', inplace=True)
        return video_information

    infos = infos(file_urls)

    # loop over the DataFrame and find the matching node in the RDF graph | only one matching node is assumed
    def find_matches():
        for idx, row in infos.iterrows():
            matching_nodes = list(g.subjects(predicate=SDO.identifier, object=Literal(idx)))
            if matching_nodes:
                node = matching_nodes[0]

                # add the new properties
                g.add((node, SDO.url, Literal(row['url'], datatype=XSD.anyURI)))
                g.add((node, SDO.thumbnailUrl, Literal(row['Thumbnail'], datatype=XSD.anyURI)))

    find_matches()

    return g