import py7zr
with py7zr.SevenZipFile('data/youtube_entities.7z', mode='r') as z:
    z.extractall('data/videos_04_2023')

