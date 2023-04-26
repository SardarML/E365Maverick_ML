import pandas as pd

df = pd.read_csv('youtube_video_data/nodes\merged_df_old_and_new.csv')
df = df.drop_duplicates(subset=df.columns[0], keep='first')
df.to_csv("youtube_video_data/nodes\merged_df_old_and_new.csv", index=False)
