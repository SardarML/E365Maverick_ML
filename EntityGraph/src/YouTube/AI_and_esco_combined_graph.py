from rdflib import Literal, Graph
from sentence_transformer_graph import fill_graph_sentence_transformer
from esco_graph import Esco_graph

# esco graphs
skill_graph = Esco_graph('data\Esco\skills_de.csv')
print(f'skill graph has {len(skill_graph)} facts')
skill_graph.serialize(destination='data/Esco/esco_skill_graph.ttl')

lang_graph = Esco_graph('data\Esco\languageSkillsCollection_de.csv') 
print(f'language graph has {len(lang_graph)} facts')
lang_graph.serialize('data/Esco/esco_language_graph.ttl', format='ttl')


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
AI_skill_graph.serialize('data/big_skill_graph.ttl', format='ttl')

# language graph
AI_language_graph = fill_all(lang_graph, fill_graph_sentence_transformer)
AI_language_graph.serialize('data/big_language_graph.ttl', format='ttl')