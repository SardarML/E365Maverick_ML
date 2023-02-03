import pandas as pd

# get video infos as entities
infos = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_infos_entities_benchmark.csv')
print('\n video infos as entities:\n', infos)

# get video tags as properties
tags = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_tags_benchmark.csv')
print('\n video tags as properties:\n', tags)

# get video captions as properties
captions = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_descriptions_benchmark.csv')
print('\n video captions/descriptions as properties:\n', captions)

# get video transcriptions as properties (whisper)
transcriptions_whisper = pd.read_csv('data_benchmarks/transcriptions_benchmark/transcriptions_benchmark_whisper.csv')
print('\n video transcriptions via openai-whisper as properties:\n', transcriptions_whisper)

# get video transcriptions as properties (pydub SpeechRecognition)
transcriptions_pydub = pd.read_csv('data_benchmarks/transcriptions_benchmark/transcriptions_benchmark_pydub.csv')
print('\n video transcriptions via pydub SpeechRecognition as properties:\n', transcriptions_pydub)