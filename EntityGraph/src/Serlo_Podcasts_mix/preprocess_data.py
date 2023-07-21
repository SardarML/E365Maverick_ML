import pandas as pd
from langdetect import detect
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

data = pd.read_csv('data/Serlo_Podcasts_mix/merged_serlo_podcast_data.csv',
                 lineterminator='\n')

data['String'] = data['title'] + " " + data['content']
print('with stops:', data.head())

def remove_stopwords(texts, language):
    if language not in stopwords.fileids():
        language = 'german'  # Fallback to english if the detected language is not supported
    stop_words = set(stopwords.words(language))
    new_texts = []
    for text in texts:
        words = text.split()
        words = [word for word in words if word not in stop_words]
        new_texts.append(' '.join(words))
    return new_texts


# Recognize the language of the text & remove stopwords for any text based on the recognized language
languages = [detect(text) for text in data['String']]
new_texts = remove_stopwords(data['String'], languages)

# Update the "Strings" column in the DataFrame
data['String'] = new_texts
print('without stops:', data.head())

data.to_csv('data/Serlo_Podcasts_mix/merged_serlo_podcast_data_without_stopwords.csv')

