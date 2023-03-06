import pandas as pd

def get_texts_for_ai():
        # get all the Textdata and bring it together
        entities_frame = pd.read_csv('')
        titles = entities_frame['Title']

        tags_frame = pd.read_csv('')
        tags = tags_frame['tags']

        captions_frame = pd.read_csv('')
        captions = captions_frame['description']

        transcriptions_whisper_frame = pd.read_csv('')
        transcriptions_whisper = transcriptions_whisper_frame['transcriptions']
        
        return titles, tags, captions, transcriptions_whisper