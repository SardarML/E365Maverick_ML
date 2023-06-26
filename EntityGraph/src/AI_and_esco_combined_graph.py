from rdflib import Literal, Graph
from sentence_transformer_graph import fill_graph_sentence_transformer
from esco_skill_and_language_graph import Esco_skill_graph, Esco_language_graph

skill_graph = Esco_skill_graph()
lang_graph = Esco_language_graph() 

def fill_all(graph, transformer_function):
    combined_graph = Graph()
    for subj, pred, obj in graph:
        if isinstance(obj, Literal):
            sentence_transformer_graph = transformer_function(str(obj))
            combined_graph = combined_graph + sentence_transformer_graph
    return combined_graph

# skill graph
AI_skill_graph = fill_all(skill_graph, fill_graph_sentence_transformer)
AI_skill_graph.serialize('data/big_skill_graph.ttl', format='ttl')

# language graph
AI_language_graph = fill_all(lang_graph, fill_graph_sentence_transformer)
AI_language_graph.serialize('data/big_language_graph.ttl', format='ttl')