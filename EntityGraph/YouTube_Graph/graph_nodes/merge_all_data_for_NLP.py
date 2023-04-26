import os
import pandas as pd
import re

# directory containing the RDF triple files (new video data)
dir = 'youtube_video_data/videos/NEU_videos_04_2023/turtles'

# create list of files in directory
file_paths = [os.path.join(dir, file) for file in os.listdir(dir) if file.endswith(".ttl")]

data = []

# search out the arguments you need
for file_path in file_paths:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

        identifier = re.search(r'identifier "(.*?)"', content)
        title = re.search(r'title "(.*?)"', content)
        caption = re.search(r'description "(.*?)"', content)      
        # uploader must be added
        #author = re.search(r'uploader "(.*?)"', content)
        #duration = re.search(r'duration (\d+)', content)
        #thumbnail = re.search(r'thumbnailUrl "(.*?)"', content)

        data.append({
            "identifier": identifier.group(1) if identifier else None,
            "Title": title.group(1) if title else None,
            "description": caption.group(1) if caption else None,
        })

data = pd.DataFrame(data)
data.to_csv("youtube_video_data/nodes/entities_NEW.csv", index=False)


# get all the textdata and bring it together
entities_frame_old = pd.read_csv('youtube_video_data/nodes/video_infos_entities_old.csv')
del entities_frame_old['Author']
del entities_frame_old['Duration']
del entities_frame_old['Thumbnail']

entities_frame_new = pd.read_csv('youtube_video_data/nodes/entities_NEW.csv')
entities_frame = pd.concat([entities_frame_old, entities_frame_new], ignore_index=True)
entities_frame = entities_frame.set_index('identifier')

captions_frame_old = pd.read_csv('youtube_video_data/nodes/captions_old.csv')
captions_frame_new = pd.read_csv('youtube_video_data/nodes/transcripts.csv')

#captions_frame = captions_frame = pd.concat([captions_frame_old, captions_frame_new], ignore_index=True)
captions_frame = captions_frame_old.join(captions_frame_new)
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
merged_df.to_csv("youtube_video_data/nodes/merged_df_old_and_new.csv", index='identifier')