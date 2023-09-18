import pandas as pd
from collections import Counter
from load_merge_data import load_data

data = load_data()

def get_permutation_counts(text):
        """we want to store not only the bigrams 
        (words that are immediately next to each other) 
        but how often all words occur before each other"""
        wordlist = text.split()
        permutations = [(wordlist[i], wordlist[j]) for i in range(len(wordlist)) for j in range(i+1, len(wordlist))]
        counts = Counter(permutations)
        return ', '.join([f"{pair}: {amount}" for pair, amount in counts.items()])

data['permutations one direction'] = data['String'].apply(get_permutation_counts)
data.to_csv('data/merged_all_with_all_one_directed_permutations.csv')