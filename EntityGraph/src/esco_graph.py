import numpy as np
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, BNode, Namespace
from rdflib.namespace import FOAF, DCTERMS as dc, XSD, RDF, SDO, SKOS as skos, RDFS

# Esco graph (queries can be all data from esco!!!)
def Esco_graph(path):
    frame = pd.read_csv(path)
    labels = np.array(frame['preferredLabel'])
    conceptURI = np.array(frame['conceptUri'])
    print(f'we have a list of {len(labels)} labels')
    esco_graph = Graph()
    for i in range(len(labels)):
      esco_graph.add((URIRef(conceptURI[i]), SDO.skills, Literal(labels[i])))
    return esco_graph
