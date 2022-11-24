from rdflib import Graph
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer
from collections import defaultdict
import sys

# g = Graph().parse("src/hskg.ttl", format="turtle")
# q2 = """
#         PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#         SELECT * WHERE { 
#             ?p foaf:name ?name .
#             ?p ns1:cost ?cost
#         }
#     """
# for r in g.query(q2):
#     print(r)

# # test get all properties
# g = Graph().parse("src/hskg.ttl", format="turtle")
# q2 = """
#         PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#         SELECT ?p ?property ?value WHERE { 
#             ?p foaf:name ?name .
#             ?p ?property ?value.
#         } 
#     """
# res = defaultdict(dict)
# for r in g.query(q2):
#     res[r.p.toPython()][r.property.toPython()] = r.value.toPython()
#     break

# print(res)

# test desk filter
# q2 = """
#         PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#         SELECT * WHERE { 
#             ?desk ns2:name ?deskName .
#             ?desk ns1:price ?deskPrice .
#             ?desk ns1:score ?deskScore .
#             Filter(xsd:integer(?deskScore) >= 20 && xsd:integer(?deskScore) <= 25) .
#             Filter(xsd:integer(?deskPrice) >= 2000 && xsd:integer(?deskPrice) <= 250000) .
#         } 
#     """
# for r in g.query(q2):
#     print(r)


# test model
from ampligraph.utils import restore_model
from ampligraph.discovery import query_topn
restored_model = restore_model(model_name_path = 'recommend.pkl')  
rlt = query_topn(restored_model, top_n=5,
                    head="Reno Paladin – RegisKillbin – Sunken City", relation='has_card', tail=None,
                    ents_to_consider=None, rels_to_consider=None)[0]
print(rlt.tolist())