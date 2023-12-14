import pandas as pd

def get_texts_for_ai():
        # get all the Textdata and bring it together
        entities_frame = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_infos_entities_benchmark.csv')
        titles = entities_frame['Title']

        tags_frame = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_tags_benchmark.csv')
        tags = tags_frame['tags']

        captions_frame = pd.read_csv('data_benchmarks\entities_properties_benchmark/video_descriptions_benchmark.csv')
        captions = captions_frame['description']

        transcriptions_whisper_frame = pd.read_csv('data_benchmarks/transcriptions_benchmark/transcriptions_benchmark_whisper.csv')
        transcriptions_whisper = transcriptions_whisper_frame['transcriptions']
        
        return titles, tags, captions, transcriptions_whisper