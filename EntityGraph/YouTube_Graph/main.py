from sentence_transformer_graph import fill_graph_sentence_transformer
from txtai_skill_classification_graph import fill_graph_txtai

# Model sentence transformer
 # change QUERY!
s_g = fill_graph_sentence_transformer('Darstellung und Eigenschaften von Funktionen')
s_h = fill_graph_sentence_transformer('Potenzfunktionen')
s_i = fill_graph_sentence_transformer('Wurzelfunktionen')
s_j = fill_graph_sentence_transformer('Ganzrationale Funktionen')

s_g.serialize(destination='data/skill_turtles/sentence_transformer/Mathe_1/Funktionen/Darstellung_und_Eigenschaften_von_Funktionen_sentence_transformer.ttl')
s_h.serialize(destination='data/skill_turtles/sentence_transformer/Mathe_1/Funktionen/Potenzfunktionen_sentence_transformer.ttl')
s_i.serialize(destination='data/skill_turtles/sentence_transformer/Mathe_1/Funktionen/Wurzelfunktionen_sentence_transformer.ttl')
s_j.serialize(destination='data/skill_turtles/sentence_transformer/Mathe_1/Funktionen/Ganzrationale_Funktionen_sentence_transformer.ttl')


# Model txtai
# change QUERY!
t_g = fill_graph_txtai('Darstellung und Eigenschaften von Funktionen')
t_h = fill_graph_txtai('Potenzfunktionen')
t_i = fill_graph_txtai('Wurzelfunktionen')
t_j = fill_graph_txtai('Ganzrationale Funktionen')

t_g.serialize(destination='data/skill_turtles/txtai/Mathe_1/Funktionen/Darstellung_und_Eigenschaften_von_Funktionen_txtai.ttl')
t_h.serialize(destination='data/skill_turtles/txtai/Mathe_1/Funktionen/Potenzfunktionen_txtai.ttl')
t_i.serialize(destination='data/skill_turtles/txtai/Mathe_1/Funktionen/Wurzelfunktionen_txtai.ttl')
t_j.serialize(destination='data/skill_turtles/txtai/Mathe_1/Funktionen/Ganzrationale_Funktionen_txtai.ttl')