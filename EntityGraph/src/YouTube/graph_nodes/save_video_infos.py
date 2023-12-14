import pandas as pd
import youtube_dl
from pytube import extract
import time
import logging
from get_video_urls_from_crawler import get_file_urls

# video-info as entity in node
def video_info(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info["title"]
        author = info["uploader"]
        #thumb = info["thumbnail"]
        #duration = info["duration"]
        video_id = extract.video_id(url) # extract video ID from URL     
        video_information = pd.DataFrame(data= {'Title': [title],
                                                'Author' : [author],                                              
                                                #'Duration': [duration],
                                                #'Thumbnail' : [thumb]
                                                },
                                         index=[video_id])
        video_information.index.name = 'identifier'
        return video_information

# videos from crawler
#urls = get_folder_urls()
urls_lst = get_file_urls('youtube_video_data/nodes/transcripts.csv')
print(f'we work with {len(urls_lst)} new videos')

# save the infos 
infos = []
for url in urls_lst:
  try:
    info = video_info(url)
    infos.append(info)
    # delay the next request by 2 seconds
    time.sleep(2)
  except Exception as e:
     logging.exception('no infos found', e)

all_infos = pd.concat(infos, axis=0)
all_infos.to_csv('youtube_video_data/nodes/entities.csv')
