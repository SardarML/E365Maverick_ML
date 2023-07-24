from rdflib import Literal, Graph
from MIX_SentenceTransformer_Youtube_Serlo_Podcast import fill_graph_sentence_transformer

# esco graphs
skill_graph = Graph()
skill_graph.parse('data/Esco/esco_skill_graph.ttl', format='ttl')
print(f'skill graph has {len(skill_graph)} facts')

# Now lets take the objects of esco graphs as prompts for sentence transformer
def fill_all(graph, transformer_function):
    combined_graph = Graph()
    for subj, pred, obj in graph:
        if isinstance(obj, Literal):
            sentence_transformer_graph = transformer_function(str(obj))
            combined_graph = combined_graph + sentence_transformer_graph
    return combined_graph

# AI generated graphs
# skill graph
AI_skill_graph = fill_all(skill_graph, fill_graph_sentence_transformer)
AI_skill_graph.serialize('data/MIX_Youtube_Serlo_Podcasts/youtube_serlo_podcasts_big_esco_skill_sentence_transformer_graph.ttl', format='ttl')
