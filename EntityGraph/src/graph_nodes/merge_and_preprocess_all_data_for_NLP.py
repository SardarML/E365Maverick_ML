import pandas as pd
from langdetect import detect
from nltk.corpus import stopwords
from collections import defaultdict
import nltk

nltk.download('stopwords')

# just merge entities/infos (title & uploader) with the transcriptions!
entities_frame = pd.read_csv('youtube_video_data/nodes/entities.csv')
entities_frame = entities_frame.set_index('identifier')

transcripts_frame= pd.read_csv('youtube_video_data/nodes/transcripts.csv')
transcripts_frame = transcripts_frame.set_index('identifier')

merged_df = entities_frame.join(transcripts_frame)
merged_df['String'] = merged_df.apply(lambda row: ''.join([str(row[col]) for col in merged_df.columns]), axis=1)
strings = merged_df['String']

import pandas as pd
from collections import defaultdict
from langdetect import detect
from nltk.corpus import stopwords

def remove_stopwords(texts, language):
    if language not in stopwords.fileids():
        language = 'german'  # Fallback to German if the detected language is not supported
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
merged_df['String']  = new_texts

# save for later
merged_df.to_csv("youtube_video_data/nodes/merged_data_for_AI_without_stopwords.csv", index='identifier')     # copy into your data file