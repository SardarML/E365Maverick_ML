import pandas as pd
from langdetect import detect
from nltk.corpus import stopwords
from collections import defaultdict
import nltk
import tensorflow as tf
import re
import string
nltk.download('stopwords')
from load_merge_data import merge_data

data = merge_data()
# or load it: 
# data = pd.read_csv('/content/drive/MyDrive/EntityGraph/Graphs/HPI/data/merged_HPI_data.csv',
#                  lineterminator='\n')

# del data['Unnamed: 0']

def combine_columns(row):
    # You could also use a list here and then join it with " ".join().
    combined_string = ""
    if pd.notna(row.get('name')):
        combined_string += str(row['name']) + " "
    if pd.notna(row.get('description')):
        combined_string += str(row['description']) + " "
    if pd.notna(row.get('keywords')):
        combined_string += str(row['keywords'])
    return combined_string.strip()  # Use strip() to remove superfluous spaces at the beginning or end.

data['String'] = data.apply(combine_columns, axis=1)

# Removing HTML and XML-like tags & non-alphanumeric characters (except whitespace) & # Replace superfluous whitespace with a single space character
data['String'] = data['String'].str.replace(r'<.*?>|span|br|h5|lang', '', regex=True)
#data['String'] = data['String'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
data['String'] = data['String'].str.split().str.join(' ')
strings = data['String'].values

def remove_stopwords(texts, language):
    if language not in stopwords.fileids():
        language = 'german', 'english'  # Fallback to english if the detected language is not supported
    stop_words = set(stopwords.words(language))
    new_texts = []
    for text in texts:
        words = text.split()
        words = [word for word in words if word not in stop_words]
        new_texts.append(' '.join(words))
    return new_texts


# Recognize the language of the text
languages = [detect(text) for text in strings]

# Remove stop words for any text based on the recognized language
new_texts = remove_stopwords(strings, languages)

# Update the "Strings" column in the DataFrame
data['String'] = new_texts

# Replace the umlauts
for column in data.columns:
    if data[column].dtype == 'object':
        data[column] = data[column].str.replace('ü', 'ue').str.replace('ä', 'ae').str.replace('ö', 'oe').str.replace('Ü', 'Ue').str.replace('Ä', 'Ae').str.replace('Ö', 'Oe')

strings = data['String'].values

data.to_csv('data\HPI\merged_HPI_data_without_stopwords_and_umlauts.csv')