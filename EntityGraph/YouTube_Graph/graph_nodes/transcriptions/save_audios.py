from pytube import YouTube
from pytube.exceptions import VideoUnavailable
def download_audio(url_list):
    # get audio-mp4
    for url in url_list:
      try:
          selected_video = YouTube(url)
          video_id = selected_video.video_id
          audio = selected_video.streams.filter(only_audio=True, file_extension='mp4').first()
          audio.download(filename=f'{video_id}.mp4', output_path='/content/drive/MyDrive/EntityGraph/Benchmarks/audios_benchmark/MP4_Data')
      except VideoUnavailable:
          print(f"Video {url} is unavailable.\n skip")          