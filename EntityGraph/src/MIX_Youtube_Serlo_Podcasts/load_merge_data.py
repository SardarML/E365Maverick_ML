import pandas as pd

serlo_podcast_data = pd.read_csv('data/Serlo_Podcasts_mix/merged_serlo_podcast_data_without_stopwords.csv', lineterminator='\n')
youtube_data = pd.read_csv('data\YouTube\merged_data_for_AI_without_stopwords.csv', lineterminator='\n')

serlo_podcast_data = serlo_podcast_data.drop(['Unnamed: 0'], axis=1)
print(serlo_podcast_data.head())

youtube_data = youtube_data.rename(columns={"Title": "title"})
youtube_data = youtube_data.rename(columns={"String\r": "String"})
youtube_data = youtube_data.rename(columns={"identifier": "id"})
youtube_data = youtube_data.rename(columns={"transcript": "content"})
youtube_data.head()

# extract identifiers
def extract_id():
    identifiers = youtube_data['id'].values
    return identifiers

identifiers = extract_id()

# extract urls
def get_file_urls(ids):
    base_url = 'https://www.youtube.com/watch?v='
    file_urls = []
    for file_id in ids:
        file_url = f"{base_url}{file_id}"
        file_urls.append(file_url)
    return file_urls

urls = get_file_urls(identifiers)
youtube_data['url'] = urls

youtube_data.head()

merged_data = df = pd.concat([serlo_podcast_data, youtube_data])
print(merged_data.head())

merged_data.to_csv('data/MIX_Youtube_Serlo_Podcasts/MIX_merged_yt_serlo_pdcast.csv')