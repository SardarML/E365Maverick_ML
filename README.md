# Recommendation Graph: 
The mapping of skills to educational content:

In this project, we want to recommend to users a logical learning path for each targeted skill, 
consisting of different educational content arranged chronologically. 
To automate the recommendations, we use different natural language processing (NLU) techniques.

## Benchmark_YouTubeGraph:

1. We get audio data from a list of Youtube Video URLs (mp4, wav) with pydub AudioSegment
2. Now we can generate transcriptions of the audio files with pydub SpeechRecognition
 and save them into a csv 
    - let's integrate a language detection with langdetect

### this transcriptions can be: 
    - parsed as nodes in rdf 
    - used in recommendation NLU Systems

3. We generate transcriptions of the audio files via whisper and save them in a csv to:
    - compare with the transcriptions we generated via pydub SpeechRecognition
    - parse as nodes in rdf 
    - use in recommendation NLU Systems  


- We take the whisper transcriptions:
    - they are easy and fast to generate

4. Now we can classify the esco skills with all the textdata in the graph (title, tags, captions, transcriptions):
    1. work with the embeddings class
    2. get all the textdata and bring it together
    3. get strings for textminig
    4. use txtai, a huggingface transformer architecture
        - https://github.com/neuml/txtai/blob/master/examples/  01_Introducing_txtai.ipynb
    5. indexing the data
    6. query this data:
        - pick a random skill and compare with entities
    7. save the embeddings index for other NLU models
    8. give attention to the to the transformer architecture:
        - https://arxiv.org/pdf/1706.03762.pdf