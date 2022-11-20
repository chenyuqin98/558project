from rdflib import Graph

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