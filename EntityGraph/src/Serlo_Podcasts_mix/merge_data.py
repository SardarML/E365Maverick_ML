import pandas as pd

podcast_data = pd.read_csv('data\Serlo_Podcasts_mix\podcast_data.csv',
                 lineterminator='\n')
serlo_data = pd.read_csv('data\Serlo_Podcasts_mix\serlo_data.csv',
                 lineterminator='\n')

# print(podcast_data.head())
# print(serlo_data.head())
merged_data = df = pd.concat([serlo_data, podcast_data])

print(f'we work with {len(merged_data)} mixed data')
# print(merged_data.head())
# print(merged_data.tail())

podcast_data.to_csv('data\Serlo_Podcasts_mix\merged_serlo_podcast_data.csv')