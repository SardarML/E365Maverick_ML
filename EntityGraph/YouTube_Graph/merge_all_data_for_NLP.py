import pandas as pd
import re


# get all the Textdata and bring it together
entities_frame_old = pd.read_csv('/content/drive/MyDrive/EntityGraph/Graphs/data/video_infos_entities.csv')
entities_frame_new = 

entities_frame = entities_frame.set_index('identifier')


captions_frame_old = pd.read_csv('/content/drive/MyDrive/EntityGraph/Graphs/data/captions.csv')
captions_frame_new =

captions_frame = captions_frame.set_index('identifier')

# remove timestamps
def remove_timestamps_and_html_tags(text):
    text = str(text)
    text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\s*', '', text)
    text = re.sub(r'&nbsp;', '', text)
    return text
captions_frame['caption'] = captions_frame['caption'].apply(remove_timestamps_and_html_tags)
captions_frame = captions_frame[captions_frame['language'] == 'de']
del captions_frame['language']

merged_df = entities_frame.join(captions_frame)
merged_df['String'] = merged_df.apply(lambda row: ''.join([str(row[col]) for col in merged_df.columns]), axis=1)
strings = merged_df['String']

# save for later
merged_df.to_csv("/data/merged_df_NEW.csv", index='identifier')