import pandas as pd
import ast
import random

def get_data():
    data = pd.read_csv('data\MIX_Youtube_Serlo_Podcasts\mixed_dataset_with_sums_and_keywords.csv')
    del data['Unnamed: 0']
    data = data.rename(columns={"Author\r": "author"})
    data = data.rename(columns={"String": "string"})
    return data

data = get_data()

def check(n):
    # let's sort the data by columns first & transfer them to lists
    id = data['id'][n]
    title = data['title'][n]
    content = data['content'][n]
    url = data['url'][n]
    author = data['author'][n]

    # generated
    summary = data['summary'][n]
    summary_keywords = data['summary keywords'][n]
    summary_keywords = ast.literal_eval(summary_keywords)
    text_keywords = data['text keywords'][n]
    text_keywords = ast.literal_eval(text_keywords)

    # we get the best keyword extraction from the original text, but the summary is also helpful for other tasks
    print('title:', title, '\n',
          'url:' , url, '\n',
          'summary:', summary, '\n',
          'text keywords:', text_keywords, '\n',
          'summary keywords:', summary_keywords, '\n',
          'length of the original text:', len(content), '\n',
          'length of the summary:', len(summary))
    return id, title, content, url, author, summary, summary_keywords, text_keywords

id, title, content, url, author, summary, summary_keywords, text_keywords = check(random.randint(0, len(data)))

print(f'\nwe have {len(text_keywords)} keywords:\n')