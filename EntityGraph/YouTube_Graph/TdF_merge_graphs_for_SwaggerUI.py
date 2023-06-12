from rdflib import Graph, URIRef, Namespace, Literal
import os

# Studienberatung
directory = 'data/Studienberatung'

g = Graph()

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        g.parse(filepath, format='json-ld')

g.serialize(destination='data/Studienberatung.json',format='json-ld')



# Studienfächer
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

def parse(): 
    g: Graph = Graph()

    base_path = "data/Studienfächer"
    
    for root, dirs, files in os.walk(base_path, topdown=True):
        relative_path = os.path.relpath(root, base_path)  # Get the relative path
        current_dir_name = os.path.basename(relative_path)  # Get the directory name
        current_dir_uri = URIRef(current_dir_name)
        
        # Handle sub-directories (narrower concept)
        for subdir in dirs:
            subdir_uri = URIRef(subdir)
            g.add((current_dir_uri, SKOS.narrower, subdir_uri))
            g.add((subdir_uri, SKOS.broader, current_dir_uri))
        
        # Parse the files in the directory
        for name in files:
            path = os.path.join(root, name)
            g.parse(path)
    return g

g: Graph = parse()

g.serialize('data/Studienfächer.ttl', format='ttl')
