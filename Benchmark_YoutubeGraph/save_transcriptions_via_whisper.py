import whisper
import ffmpeg

def get_large_audio_transcription(path):
    model = whisper.load_model("base")
    result = model.transcribe(path)
    return result["text"]

import os

# path to the folder with audio files
folder_path = 'data_benchmarks/audios_benchmark\WAV_Data'

# create a list of all audio files in the folder
audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# create an empty list to save the transcriptions and file names
results = []

# iterate over all audio files in the folder
for audio_file in audio_files:
    file_path = os.path.join(folder_path, audio_file)
    try:
        transcription = get_large_audio_transcription(file_path)
        results.append([audio_file, transcription])
    except Exception as e:
        print(f"error in the transcription of {audio_file}, error: {e}")

import pandas as pd

def save_DataFrame():
        transcriptions_frame = pd.DataFrame(results)
        return transcriptions_frame

transcriptions_frame = save_DataFrame()
transcriptions_frame.to_csv('transcriptions_benchmark_whisper.csv', index=False)