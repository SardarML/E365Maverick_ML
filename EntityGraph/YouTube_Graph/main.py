from sentence_transformer_graph import fill_graph_sentence_transformer
from txtai_skill_classification_graph import fill_graph_txtai


# Model sentence transformer
 # change QUERY!
s_g = fill_graph_sentence_transformer('Lineares Gleichungssystem')
s_h = fill_graph_sentence_transformer('Determinante')
#s_i = fill_graph_sentence_transformer('Matrizen')

s_g.serialize(destination='data/skill_turtles/sentence_transformer/Mathe_1/Lineare_Algebra/LGS_sentence_transformer.ttl')
s_h.serialize(destination='data/skill_turtles/sentence_transformer/Mathe_1/Lineare_Algebra/Determinate_sentence_transformer.ttl')
#s_i.serialize(destination='data/skill_turtles/sentence_transformer/Mathe_1/Vektoren_Matrizen/Matrizen_sentence_transformer.ttl')



# Model txtai
# change QUERY!
t_g = fill_graph_txtai('Lineares Gleichungssystem')
t_h = fill_graph_txtai('Determinante')
#t_i = fill_graph_txtai('Matrizen')


t_g.serialize(destination='data/skill_turtles/txtai/Mathe_1/Lineare_Algebra/LGS_txtai.ttl')
t_h.serialize(destination='data/skill_turtles/txtai/Mathe_1/Lineare_Algebra/Determinate_txtai.ttl')
#t_i.serialize(destination='data/skill_turtles/txtai/Mathe_1/Vektoren_Matrizen/Matrizen_txtai.ttl')