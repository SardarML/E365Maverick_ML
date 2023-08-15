import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import nltk
nltk.download('punkt')
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

model = SentenceTransformer('valurank/MiniLM-L6-Keyword-Extraction')

def get_data(path):
        merged_df = pd.read_csv(path,
                 lineterminator='\n')
        strings = merged_df['String']
        str_lst = strings.values
        str_combined = " ".join(str_lst)
        return merged_df, str_combined, str_lst

merged_df, str_combined, str_lst = get_data('data\OERSI\OERSI_data_without_stpwrds_and_duplicates.csv')

def get_keywords(txt, n=50):
    word_tokens = word_tokenize(txt)
    filtered_words =  [word for word in word_tokens if not word.isnumeric()]
    filtered_words = [word for word in word_tokens if word.isalpha()]
    filtered_words = [word for word in word_tokens if word.isalpha() and len(word) > 2]
    word_freq = Counter(filtered_words)
    keywords = word_freq.most_common(n)
    return keywords

# Apply functions to DataFrame
merged_df['description keywords'] = merged_df['String'].apply(get_keywords)
del merged_df['Unnamed: 0']

merged_df.to_csv('data\OERSI\OERSI_data_with_50_keywords.csv')
