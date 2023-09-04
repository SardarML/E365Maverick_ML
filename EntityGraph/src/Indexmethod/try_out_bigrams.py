import pandas as pd
from n_gramm import filter_texts

filtered_texts = filter_texts()
filtered_texts = pd.DataFrame(filtered_texts, columns=['text'])
print(filtered_texts)
bigram_df = pd.read_csv('data/bigrams.csv')

def count_occurrences_before(texts, x, y, max_distance=None):
        count = 0
        for _, row in texts.iterrows():
            text = row['text']
            x_index = text.find(x)
            y_index = text.find(y)
            if x_index != -1 and y_index != -1 and x_index < y_index:
                if max_distance is not None:
                    if y_index - x_index <= max_distance:
                        count += 1
                else:
                    count += 1
        return count

x = "?"
y = "Lerne"
n = count_occurrences_before(filtered_texts, x, y)
print(f"In {n} texts, the word '{x}' occurs before the word '{y}'.")

