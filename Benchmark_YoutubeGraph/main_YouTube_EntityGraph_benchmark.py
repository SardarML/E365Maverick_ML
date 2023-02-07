import pandas as pd

# get entities
infos = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_infos_entities_benchmark.csv')

# get properties
tags = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_tags_benchmark.csv')
captions = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_descriptions_benchmark.csv')
transcriptions_whisper = pd.read_csv('data_benchmarks/transcriptions_benchmark/transcriptions_benchmark_whisper.csv')
transcriptions_pydub = pd.read_csv('data_benchmarks/transcriptions_benchmark/transcriptions_benchmark_pydub.csv')

# get skills as properties

