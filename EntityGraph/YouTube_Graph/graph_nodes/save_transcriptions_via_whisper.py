import whisper
import os
import pandas as pd
import logging

def get_large_audio_transcription(path):
        # model: https://huggingface.co/spaces/openai/whisper
        model = whisper.load_model("base") 
        result = model.transcribe(path, fp16=False)
        return result["text"]

# path to the folder with audio files
folder_path = 'youtube_video_data/audios/MP4_Data'

# create a list of all audio files in the folder
audio_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

# create an empty list to save the transcriptions and file names
results = []

# iterate over all audio files in the folder
for audio_file in audio_files:
    file_path = os.path.join(folder_path, audio_file)
    try:
        transcription = get_large_audio_transcription(file_path)
        results.append([audio_file, transcription])
    except Exception as e:
        logging.exception(f"error in the transcription of {audio_file}, error: {e}")

def save_DataFrame():
        transcriptions_frame = pd.DataFrame(results, columns=['video_id', 'transcriptions']) 
        return transcriptions_frame

transcriptions_frame = save_DataFrame()
transcriptions_frame.to_csv('youtube_video_data/nodes/transcriptions_whisper/transcriptions_whisper.csv', index=False)


