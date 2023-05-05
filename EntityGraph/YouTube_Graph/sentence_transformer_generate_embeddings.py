import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from get_merged_data import get_data

merged_df, str_lst, vocab, identifier_vocab, identifier = get_data('data/merged_data_for_AI.csv')

# get embeddings like in doc2vec
def SentenceTransformer_embeddings():
        '''https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2
        This is a sentence-transformers model: 
        It maps sentences & paragraphs to a 768 
        dimensional dense vector space and can 
        be used for tasks like clustering or semantic search.'''
        
        # generate embeddings
        # embeddings = model.encode(str_lst)
        # embeddings = pd.DataFrame(embeddings)
        # embeddings.to_csv('data/sentence_transformer_embedding.csv')
        # embeddings = np.array(embeddings)
        # print(embeddings.shape)

        # get the embeddings
        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        embeddings = pd.read_csv('data/sentence_transformer_embedding.csv')
        del embeddings['Unnamed: 0']
        embeddings = embeddings.values
        print(embeddings.shape)
        return model, embeddings