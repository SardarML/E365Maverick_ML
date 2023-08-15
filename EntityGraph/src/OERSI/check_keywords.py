import pandas as pd
import ast
import random

def get_data():
    data = pd.read_csv('data\OERSI\OERSI_data_with_50_keywords.csv')
    del data['Unnamed: 0']
    return data
data = get_data()

print(data['description keywords'])

def check(n):
    # let's sort the data by columns first & transfer them to lists
    title = data['name'][n]
    content = data['description'][n]
    url = data['sameAs'][n]

    # generated
    text_keywords = data['description keywords'][n]
    text_keywords = ast.literal_eval(text_keywords)

    # we get the best keyword extraction from the original text, but the summary is also helpful for other tasks
    print('title:', title, '\n',
          'url:' , url, '\n',
          'original text:', content, '\n',
          f'\nwe have {len(text_keywords)} keywords:\n\n',
          'text keywords:', text_keywords, '\n')
    return id, title, content, url, text_keywords

id, title, content, url, text_keywords = check(random.randint(0, len(data['name'])))