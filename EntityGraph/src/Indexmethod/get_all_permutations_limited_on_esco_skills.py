import pandas as pd
import re
import rdflib
from rdflib import Graph
from collections import Counter
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

data = pd.read_csv('data\ALL_MIXED\ALL_merged_without_stps_and_umlts.csv', low_memory=False)
ttl_text = Graph()
ttl_text = ttl_text.parse('data\Esco\esco_skill_graph.ttl')

def get_skills():
        objects = []
        for _, _, obj in ttl_text:
            objects.append(str(obj))
        return objects

skills = get_skills()

stop_words = set(stopwords.words('german', 'english'))
if skills:
    # Create a list of all unique words that occur in the objects
    relevant_words = set()
    for skill in skills:
        if isinstance(skill, str):  # Make sure that skill is a string
            for word in skill.split():
                if word.lower() not in stop_words:
                    relevant_words.add(word.lower()) # To ignore case sensitivity
        else:
            print(f"Unexpected data type in skills: {type(skill)}")
else:
    print("The skills list is empty")

# Output of the relevant words
if relevant_words:
    print(len(relevant_words))
else:
    print("No relevant words found")




# Filtering the words in our texts
def get_permutation_counts(text):
    """we want to store not only the bigrams 
    (words that are immediately next to each other) 
    but how often all words occur before each other"""

    wordlist = [word for word in text.split() if word.lower() in relevant_words]
    permutations = [(wordlist[i], wordlist[j]) for i in range(len(wordlist)) for j in range(i+1, len(wordlist))]
    counts = Counter(permutations)
    return ', '.join([f"{pair}: {amount}" for pair, amount in counts.items()])

data['permutations_one_direction_RELEVANT_ESCO_SKILLS'] = data['String'].apply(get_permutation_counts)
data.to_csv('data/ALL_MIXED/merged_all_data_with_all_one_directed_permutations_limited_on_esco.csv')

print(relevant_words)
relevant_words.to_csv('data/skills_whitelist.csv')