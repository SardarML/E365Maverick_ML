import pandas as pd
import youtube_dl
from pytube import extract
import time
import logging
from get_video_urls_from_crawler import get_file_urls

# videos from crawler
urls = get_file_urls()
urls_lst = list(urls)

# video-info as entity in node
def video_info(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info["title"]
        author = info["uploader"]
        thumb = info["thumbnail"]
        duration = info["duration"]
        video_id = extract.video_id(url) # extract video ID from URL     
        video_information = pd.DataFrame(data= {'Title': [title],
                                                'Author' : [author],                                              
                                                'Duration': [duration],
                                                'Thumbnail' : [thumb]},
                                         index=[video_id])
        video_information.index.name = 'identifier'
        return video_information

# save the infos 
infos = []
for url in urls_lst:
  try:
    info = video_info(url)
    infos.append(info)
    # delay the next request by 5 seconds
    time.sleep(5)
  except Exception as e:
     logging.exception('no infos found', e)

all_infos = pd.concat(infos, axis=0)
all_infos.to_csv('youtube_video_data/nodes/video_infos_entities.csv')