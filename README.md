# Benchmark_YouTubeGraph:

1. We get audio data from a list of Youtube Video URLs (mp4, wav) with pydub AudioSegment

2. Now we can generate transcriptions of the wav files with pydub SpeechRecognition and save them into a csv 
    - let's integrate a language detection with langdetect

**The transcriptions can be** 
    - parsed as nodes in rdf 
    - used in recommendation NLU Systems

3. We generate transcriptions of the mp4 files via whisper and save them in a csv to:
    - compare with transcriptions via pydub SpeechRecognition
    - parse as nodes in rdf 
    - use in recommendation NLU Systems  
