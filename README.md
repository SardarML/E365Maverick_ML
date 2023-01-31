# Recommendation Graph: 
The mapping of skills to educational content:

In this project, we want to recommend to users a logical learning path for each targeted skill, 
consisting of different educational content arranged chronologically. To automate the recommendations, 
we use different natural language processing (NLU) techniques.

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
