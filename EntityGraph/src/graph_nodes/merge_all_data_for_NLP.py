import pandas as pd

# just merge entities/infos (title & uploader) with the transcriptions!
entities_frame = pd.read_csv('youtube_video_data/nodes/entities.csv')
entities_frame = entities_frame.set_index('identifier')

transcripts_frame= pd.read_csv('youtube_video_data/nodes/transcripts.csv')
transcripts_frame = transcripts_frame.set_index('identifier')

merged_df = entities_frame.join(transcripts_frame)
merged_df['String'] = merged_df.apply(lambda row: ''.join([str(row[col]) for col in merged_df.columns]), axis=1)
strings = merged_df['String']

# save for later
merged_df.to_csv("youtube_video_data/nodes/merged_data_for_AI.csv", index='identifier')     # copy into your data file