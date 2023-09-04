import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk import bigrams
from collections import Counter
from nltk.corpus import stopwords
from load_merge_data import load_data

merged_df = load_data()
texts = merged_df.String.values

nltk.download('stopwords')
nltk.download('punkt')

def filter_texts():
        stop_words = set(stopwords.words('german', 'english'))
        filtered_texts = []
        for text in texts:
            words = word_tokenize(text)
            filtered_words = [word for word in words if word.lower() not in stop_words]
            filtered_texts.append(' '.join(filtered_words))
        return filtered_texts

filtered_texts = filter_texts()
print(filtered_texts[0])


# Tokenize any text into words and generate the bigrams
bigram_list = [bigram for text in filtered_texts for bigram in bigrams(nltk.word_tokenize(text))]

# Count the frequencies of the bigrams
bigram_counts = Counter(bigram_list)

# Sort the bigrams according to their frequency
sorted_bigrams = sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True)

# Display the sorted bigram frequencies
for bigram, count in sorted_bigrams:
    print(f"{bigram}: {count}")
        
bigram_df = pd.DataFrame(bigram_counts.items(), columns=['Bigram', 'Count'])

# Sort the DataFrame by the Count column in descending order
bigram_df = bigram_df.sort_values(by='Count', ascending=False)

bigram_df.to_csv('data/bigrams.csv', index=False)