import pandas as pd

def get_youtube_video_urls():
    urls = pd.read_csv(r'data_benchmarks/urls.csv')
    urls = urls['0']
    return urls

urls = get_youtube_video_urls()
print(f'we work with {len(urls)} videos')