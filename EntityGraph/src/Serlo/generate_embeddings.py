import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from get_data import get_data

merged_df, str_lst, vocab, identifier_vocab, identifier = get_data('data\Serlo\merged_serlo_data_without_stopwords.csv')
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

# def embed():
#       embeddings = model.encode(str_lst)
#       weights = embeddings
#       weights = pd.DataFrame(weights)
#       weights.to_csv('data\Serlo\serlo_embeddings.csv')
#       print(embeddings.shape)
#       return weights
        

# get embeddings like in doc2vec
def SentenceTransformer_embeddings():
        '''https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2
        This is a sentence-transformers model:
        It maps sentences & paragraphs to a 768
        dimensional dense vector space and can
        be used for tasks like clustering or semantic search.'''

        model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

        weights = pd.read_csv('data\Serlo\serlo_embeddings.csv')
        del weights['Unnamed: 0']
        weights = weights.values
        embeddings = weights
        print(embeddings.shape)
        return model, embeddings


