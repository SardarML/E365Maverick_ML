from pytube import YouTube
import logging
from get_video_urls_from_crawler import get_file_urls

def download_audio(url_list):
    # get audio-mp4
    for url in url_list:
      try:
          selected_video = YouTube(url)
          video_id = selected_video.video_id
          audio = selected_video.streams.filter(only_audio=True, file_extension='mp4').first()
          audio.download(filename=f'{video_id}.mp4', output_path='youtube_video_data/audios/MP4_Data')
      except Exception:
          logging.exception(f"Video {url} is unavailable.\n skip")


urls = get_file_urls()
download_audio(urls)