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
    if pd.notna(row.get('learningObjectives')):
        combined_string += str(row['learningObjectives'])
    return combined_string.strip()  # Use strip() to remove superfluous spaces at the beginning or end.

data['String'] = data.apply(combine_columns, axis=1)

# Removing HTML and XML-like tags & non-alphanumeric characters (except whitespace) & # Replace superfluous whitespace with a single space character
data['String'] = data['String'].str.replace(r'<.*?>|span|br|h5|lang', '', regex=True)
data['String'] = data['String'].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
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

def count_bigrams(texts):
    bigram_counts_list = []
    for text in texts:
        words = text.split()
        bigram_counts = defaultdict(int)
        for i in range(len(words) - 1):
            bigram = (words[i], words[i + 1])
            bigram_counts[bigram] += 1
        bigram_counts_list.append(bigram_counts)
    return bigram_counts_list


# Recognize the language of the text
languages = [detect(text) for text in strings]

# Remove stop words for any text based on the recognized language
new_texts = remove_stopwords(strings, languages)

# Count the bigrams for each cleaned text
bigram_counts_list = count_bigrams(new_texts)

# Update the "Strings" column in the DataFrame
data['String'] = new_texts
strings = data['String'].values

# data.to_csv('data\HPI\merged_HPI_data_without_stopwords.csv')