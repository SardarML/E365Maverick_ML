import pandas as pd
import youtube_dl
from pytube import extract
import time
from video_urls_from_crawler import get_youtube_video_urls

# videos from crawler
urls = get_youtube_video_urls()
# save urls of the first 3 videos
urls_lst = list(urls[:3])

# only for NLU (as property)
def video_description(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        # description
        description = info["description"]
        video_id = extract.video_id(url) # extract video ID from URL       
        video_information = pd.DataFrame(data= {'Description': [description]},
                                         index=[video_id])
        video_information.index.name = 'VideoID'
        return video_information

def get_video_descriptions(url_list):
    results = []
    for url in url_list:
        video_id = extract.video_id(url) # extract video ID from URL 
        description = video_description(url)
        results.append({
            "video_id": video_id,
            "description": description.at[video_id, "Description"]
        })
        time.sleep(5)
    return pd.DataFrame(results)

captions = get_video_descriptions(urls_lst)
captions.to_csv('video_descriptions_benchmark.csv', index=False)