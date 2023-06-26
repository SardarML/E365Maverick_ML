import numpy as np
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, BNode, Namespace
from rdflib.namespace import FOAF, DCTERMS as dc, XSD, RDF, SDO, SKOS as skos, RDFS

# skill graph
def get_esco_skills():
    skills_frame = pd.read_csv('data\Esco\skills_de.csv')
    
    skills = np.array(skills_frame['preferredLabel'])
    skillType = np.array(skills_frame['skillType'])
    skill_conceptURI = np.array(skills_frame['conceptUri'])
    resueLevel = np.array(skills_frame['reuseLevel'])
    print(f'we have a list of {len(skills)} skills/competences')
    return skills_frame, skills, skillType, skill_conceptURI, resueLevel

skills_frame, skills, skillType, skill_conceptURI, resueLevel = get_esco_skills()

def Esco_skill_graph():
    skill_graph = Graph()
    for i in range(len(skills)):
      skill_graph.add((URIRef(skill_conceptURI[i]), SDO.skills, Literal(skills[i])))
    return skill_graph

skill_graph = Esco_skill_graph()

print(f'skill graph has {len(skill_graph)} facts')
skill_graph.serialize(destination='data/Esco/esco_skill_graph.ttl')


# language skills graph
def get_esco_languages(): 
    # Speaking, writing and understanding languages | conceptType = KnowledgeSkillCompetence
    languageSkillsCollection_de = pd.read_csv('data\Esco\languageSkillsCollection_de.csv')

    languages_preferredLabel = languageSkillsCollection_de['preferredLabel'].values
    languages_description_altLabels = languageSkillsCollection_de['altLabels'].values
    language_broaderConceptPT = languageSkillsCollection_de['broaderConceptPT'].values
    language_conceptURI = languageSkillsCollection_de['conceptUri'].values
    return languages_preferredLabel, languages_description_altLabels, language_broaderConceptPT, language_conceptURI

languages_preferredLabel, languages_description_altLabels, language_broaderConceptPT, language_conceptURI = get_esco_languages()  

def Esco_language_graph():
    lang_graph = Graph()
    for i in range(len(languages_preferredLabel)):
      lang_graph.add((URIRef(language_conceptURI[i]), SDO.skills, Literal(languages_preferredLabel[i])))
    return lang_graph

lang_graph = Esco_language_graph()

print(f'language graph has {len(lang_graph)} facts')
lang_graph.serialize('data/Esco/esco_language_graph.ttl', format='ttl')

