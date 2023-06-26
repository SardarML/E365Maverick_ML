import webvtt
import logging
import os
import pandas as pd

# remove the timestamps 
def process_file(file_path):
    try:
        video_text = webvtt.read(file_path)
        transcript = ""
        lines = []

        for line in video_text:
            lines.extend(line.text.strip().splitlines())

        previous = None
        for line in lines:
            if line == previous:
                continue
            transcript += " " + line
            previous = line

        return transcript
    except Exception as e:
        logging.exception(f"Error processing file {file_path}: {e}")
        return None

# directory containing the VTT files
directory = 'youtube_video_data/nodes/captions'

# create list of VTT files in the directory
file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".de.vtt")]

transcripts = []

for file_path in file_paths:
    if os.stat(file_path).st_size == 0:
        print(f"Skipping empty file: {file_path}")
        continue

    video_id = os.path.basename(file_path).replace('.de.vtt', '')
    transcript = process_file(file_path)

    if transcript is not None:
        transcripts.append({'identifier': video_id, 'transcript': transcript})

transcripts = pd.DataFrame(transcripts)
transcripts.to_csv("youtube_video_data/nodes/transcripts.csv", index=False)