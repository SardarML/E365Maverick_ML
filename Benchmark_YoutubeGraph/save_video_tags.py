import pandas as pd
import YoutubeTags
from YoutubeTags import videotags
from pytube import extract
from video_urls_from_crawler import get_youtube_video_urls

# videos from crawler
urls = get_youtube_video_urls()
# save urls of the first 3 videos
urls_lst = list(urls[:3])

def get_video_tags(url_list):
    results = []
    for url in url_list:
        video_id = extract.video_id(url) # extract video ID from URL
        tags = videotags(url)
        results.append({
            "video_id": video_id,
            "tags": tags
        })
    return pd.DataFrame(results)

# save the tags (of the first 3 videos)
all_tags = get_video_tags(urls_lst)
all_tags.to_csv('data_benchmarks\entities_properties_benchmark/video_tags_benchmark.csv', index=False)