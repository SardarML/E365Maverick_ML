import py7zr
with py7zr.SevenZipFile('youtube_video_data/videos/youtube_entities.7z', mode='r') as z:
    z.extractall('youtube_video_data/videos/NEW_videos_04_2023/turtles')

