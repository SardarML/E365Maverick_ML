import entitygraph
from entitygraph import Application, Entity

host = "https://entitygraph.azurewebsites.net"
path = "api/entities"
key = ""
application = "oersi"

#client = entitygraph.Client(api_key=key)
entitygraph.connect(host=host, api_key=key)
app = Application().get_by_label(application)

query_str_0 = """

PREFIX schema: <http://schema.org/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?LearningResource ?name (GROUP_CONCAT(?keyword; SEPARATOR=", ") AS ?keywords) ?sameAs ?description
WHERE {
    ?LearningResource a schema:LearningResource .
    ?LearningResource schema:name ?name .
    ?LearningResource schema:keywords ?keyword .
    ?LearningResource owl:sameAs ?sameAs .
    ?LearningResource schema:description ?description .
}
GROUP BY ?LearningResource ?name ?sameAs ?description
LIMIT 10000 OFFSET 0

"""

oersi_0 = app.Query().select(query_str_0)
print(oersi_0.head())

# Change OFFSET to get all data: 10000, 20000, ...

query_str_1 = """

PREFIX schema: <http://schema.org/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?LearningResource ?name (GROUP_CONCAT(?keyword; SEPARATOR=", ") AS ?keywords) ?sameAs ?description
WHERE {
    ?LearningResource a schema:LearningResource .
    ?LearningResource schema:name ?name .
    ?LearningResource schema:keywords ?keyword .
    ?LearningResource owl:sameAs ?sameAs .
    ?LearningResource schema:description ?description .
}
GROUP BY ?LearningResource ?name ?sameAs ?description
LIMIT 10000 OFFSET 10000

"""

oersi_1 = app.Query().select(query_str_1)
print(oersi_1.head())

#...

import pandas as pd

OERSI_dataframes = [oersi_0,
              oersi_1
              #,...
                    ]

OERSI_data = pd.concat(OERSI_dataframes, axis=0, ignore_index=True)
print(OERSI_data.head())
#OERSI_data.to_csv('data\OERSI\merged_OERSI_data.csv')

