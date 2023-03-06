import pandas as pd
from YoutubeTags import videotags
from pytube import extract
import logging
from get_video_urls_from_crawler import get_file_urls

# videos from crawler
urls = get_file_urls()
urls_lst = list(urls)

def get_video_tags(url_list):
    results = []
    for url in url_list:
      try:  
        video_id = extract.video_id(url) # extract video ID from URL
        tags = videotags(url)
        results.append({
            "video_id": video_id,
            "tags": tags
        })
      except Exception as e:
        logging.exception('no tags found', e)
    return pd.DataFrame(results)

# save the tags (of the first 3 videos)
all_tags = get_video_tags(urls_lst)
all_tags.to_csv('youtube_video_data/nodes/video_tags.csv', index=False)