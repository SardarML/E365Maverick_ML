import os
import pandas as pd

def get_file_urls():
        file_ids = []
        folder_path = "youtube_video_data/videos"
        for filename in os.listdir(folder_path):
            file_id = filename.split(".")[0]
            file_ids.append(file_id)
        base_url = 'https://www.youtube.com/watch?v='
        file_urls = []
        for file_id in file_ids:
            file_url = f"{base_url}{file_id}"
            file_urls.append(file_url)
        return file_urls


file_urls = get_file_urls()
print(f'we work with {len(file_urls)} new videos')
