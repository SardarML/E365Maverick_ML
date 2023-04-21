from sentence_transformer_graph import fill_graph_sentence_transformer
from txtai_skill_classification_graph import fill_graph_txtai


# Model sentence transformer
# g = fill_graph_sentence_transformer('Polynomdivision')

# print(f'Graph g has {len(g)} facts')
# for triples in g:
#     print(f'triples{triples}')
# # change QUERY!
# g.serialize(destination='data/skill_turtles/sentence_transformer/Polynomdivision_graph.ttl')



# Model txtai
h = fill_graph_txtai('Darstellung und Eigenschaften von Funktionen')
i = fill_graph_txtai('Potenzfunktionen')
j = fill_graph_txtai('Wurzelfunktionen')
k = fill_graph_txtai('Ganzrationale Funktionen')


print(f'Graph h has {len(h)} facts')
for triples in h:
    print(f'triples{triples}')
# change QUERY!
h.serialize(destination='data/skill_turtles/txtai/Mathe_1/Funktionen/Funktionen_Darstellung_graph_txtai.ttl')
i.serialize(destination='data/skill_turtles/txtai/Mathe_1/Funktionen/Potenzfunktionen_graph_txtai.ttl')
j.serialize(destination='data/skill_turtles/txtai/Mathe_1/Funktionen/Wurzelfunktionen_graph_txtai.ttl')
k.serialize(destination='data/skill_turtles/txtai/Mathe_1/Funktionen/Ganzrationale_Funktionen_graph_txtai.ttl')

