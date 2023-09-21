import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import nltk
nltk.download('punkt')
from collections import Counter
from nltk.tokenize import word_tokenize
import logging
from load_merge_data import load_data

model = SentenceTransformer('valurank/MiniLM-L6-Keyword-Extraction')


merged_df = load_data()
merged_df = merged_df.drop(['Unnamed: 0'], axis=1)

# print(merged_df.head())
# print(merged_df.tail())

def summary(txt, clusters=5):
    sentences = txt.split('.')
    sentence_vectors = model.encode(sentences)

    if len(sentences) < clusters:
        logging.warning(f"n_samples={len(sentences)} should be >= n_clusters={clusters}. The number of sentences is smaller than the number of clusters. The entire text is returned.")
        return txt

    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(sentence_vectors)

    summary_sentences = []
    for cluster_center in kmeans.cluster_centers_:
        distances = ((sentence_vectors - cluster_center)**2).sum(axis=1)
        closest_sentence_index = distances.argmin()
        summary_sentences.append(sentences[closest_sentence_index])

    summary = ' '.join(summary_sentences)
    return summary

def get_keywords(txt, n=10):
    word_tokens = word_tokenize(txt)
    filtered_words =  [word for word in word_tokens if not word.isnumeric()]
    filtered_words = [word for word in word_tokens if word.isalpha() and len(word) > 1]
    word_freq = Counter(filtered_words)
    keywords = word_freq.most_common(n)
    return keywords

# Apply functions to DataFrame
merged_df['summary'] = merged_df['String'].apply(summary)
merged_df['summary keywords'] = merged_df['summary'].apply(get_keywords)
merged_df['text keywords'] = merged_df['String'].apply(get_keywords)

merged_df.to_csv('data\ALL_MIXED\ALL_merged_without_stps_and_umlts_with_sums_and_keywords.csv')