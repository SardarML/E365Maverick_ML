import pandas as pd
from txtai.embeddings import Embeddings
from get_all_textdata import get_texts_for_ai

# work with the embeddings class
embeddings = Embeddings({
    
    'path':'sentence-transformers/all-MiniLM-L6-v2'
})

# get all the textdata and bring it together
titles, tags, captions, transcriptions_whisper =  get_texts_for_ai()

# get your data from the bechmark 
data = {
    "Title": titles,
    "tags": tags,
    "description": captions,
    "transcriptions": transcriptions_whisper
}

# store data
# data = pd.DataFrame(data)
# data.to_csv("/content/drive/MyDrive/EntityGraph/Benchmarks/data/embedding_data_benchmark.csv", index=False)

# get strings for textminig
strings = []
for i in range(len(titles)):
    string = titles[i] + " | " + tags[i] + " | " + captions[i] + " | " + transcriptions_whisper[i]
    strings.append(string)

## use txtai, a huggingface transformer architecture
# https://github.com/neuml/txtai
txtai_data = []
i=0
for text in strings:
    ''' appending the index, the text 
    and None because the embeddings object 
    is expecting 3 different components'''
    txtai_data.append((i, text, None))
    i+=1

# let's quickly create our index (embeddings-vocab) of all the data
embeddings.index(txtai_data)

# try out with esco skills
skills_esco = pd.read_csv('data_benchmarks\skills_de.csv')
skills = skills_esco['preferredLabel']

# now we can query this data
'''search for things that have the word __ in it 
and pass in how many results we want to see'''

# pick a random skill and compare with entities
search_word = skills[7]

res = embeddings.search(search_word, 20)
for r in res:
    '''we'll get a set of tuples that correspond to 2 things:
      1. index number, that has been retrieved. So in this case the thing that is most similar
      2. score of similarity'''
    print(f'Text: {strings[r[0]][:100]}') # take just the first 100 characters of the strings
    print(f'Similarity for the competence *{search_word}*: {r[1]}\n')


# best matches for our skill graph
print("%-20s %s" % ("Query/Topic", "Best Match"))
print("-" * 50)

# for the first 5 skills
for query in (skills[:5]):
    # Get index of best section that best matches query
    uid = embeddings.similarity(query, strings)[0][0]

    print("%-20s %s" % (f'skill: {query}',f'\nmost similar entity: {strings[uid][:100]}\n')) # take just the first 100 characters of the strings


## for another script
# save the embeddings index
embeddings.save('data_benchmarks\embeddings_benchmark')
