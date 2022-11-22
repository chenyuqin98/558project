from rdflib import Graph
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer
from collections import defaultdict
import sys

g = Graph().parse("src/hskg.ttl", format="turtle")
q2 = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT * WHERE { 
            ?p foaf:name ?name .
            ?p ns1:cost ?cost
        }
    """
for r in g.query(q2):
    print(r)

# test get all properties
g = Graph().parse("src/hskg.ttl", format="turtle")
q2 = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?p ?property ?value WHERE { 
            ?p foaf:name ?name .
            ?p ?property ?value.
        } 
    """
res = defaultdict(dict)
for r in g.query(q2):
    res[r.p.toPython()][r.property.toPython()] = r.value.toPython()
    break

print(res)