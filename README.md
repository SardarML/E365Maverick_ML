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
        - https://github.com/neuml/txtai
    5. indexing the data
    6. query this data:
        - pick a random skill and compare with textdata of entities & properties
    7. save the embeddings index for other NLU models
    8. give attention to transformer architectures (state of the art 2023):
        - https://arxiv.org/pdf/1706.03762.pdf

## EntityGraph & Skill classification

1. take current videos and unique identifiers from crawler
2. generate entities (video info)
3  generate properties:
    1. tags, captions
    2. audiodata (only for transcriptions)
    3. transcriptions via openai-whisper 
    https://huggingface.co/spaces/openai/whisper
4. YouTubeGraph: connect the nodes with schema.org & skos (property, label)
5. SkillGraph: get esco skills & parse them into another graph
6. use txtai to classify skills & entities:
    - a skill-vector (embeddings) should have the highest cosine similarity to the embedded textual data (titles, tags, captions transcriptions) of a video source/entity, that most often contains the word, or contextually fits best
7. check the embeddings with tsne (t distributed stochastical neighborhood embedding) and try to find out what's inside the blackbox of txtai's training
8. connect entity nodes (YouTubeGraph) with most similar skill nodes (SkillGraph) with schema.org property (teaches)
9. generation of fixed learning paths:
    1. AI index method:
        - search for appropriate teaching resources on the different skills
        - find subordinate and superordinate skills by indexing chronological learning requirements
        - generate learning paths
10. receive user feedback (& credentials) and feed it into further text classification procedures to adapt the learning paths