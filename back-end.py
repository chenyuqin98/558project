# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
# from rdflib.namespace import FOAF
from rdflib import Graph
# from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer
from collections import defaultdict
import json
import sys
import requests
from ampligraph.utils import restore_model
from ampligraph.discovery import query_topn

app = Flask(__name__, static_url_path='/static')
CORS(app)
# app = Flask(__name__, static_url_path='/static', template_folder='knowledge-graph-browser-frontend/dist')
g = Graph().parse("src/hskg.ttl", format="turtle")

init_q = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?p ?property ?value WHERE { 
            ?p foaf:name ?name .
            ?p ?property ?value.
        } 
    """
kg_dict = defaultdict(dict)

for r in g.query(init_q):
    kg_dict[r.p.toPython()][r.property.toPython()] = r.value.toPython()

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/deck_explore', methods=['GET'])
def deck_explore():
    return render_template('deck_explore.html')


@app.route('/card_explore', methods=['GET'])
def card_explore():
    return render_template('card_explore.html')


@app.route('/recommend', methods=['GET'])
def recommend():
    return render_template('recommend.html')


@app.route('/search/deck/<deckName>', methods=['GET'])
def search_deck(deckName): # "Reno Paladin – RegisKillbin – Sunken City"
    q = """
        SELECT * WHERE { 
            ?deck ns1:hasCard ?cardName .
            ?deck ns2:name "deck_name" .
            ?card ns2:name ?cardName .
            ?card ns1:img_url ?cardUrl .
        }
    """
    q = q.replace('deck_name', deckName)
    # print(1111, q, deckName)
    nodes = [{'id': 1, 'label': deckName}]
    edges = []
    res = {}
    for r in g.query(q): 
        if r.cardName not in res:
            res[r.cardName.toPython()] = r.cardUrl.toPython()
    id = 2
    for k in res.keys():
        nodes.append({'id': id, 'label': k, 'shape': "image", 'image': res[k], 'shapeProperties': { 'useImageSize': False }})
        edges.append({ 'from': 1, 'to': id })
        id += 1  
    return {'nodes': nodes, 'edges': edges}


def sub_search_deck(deckName, id, nodes, edges, class_dic):
    q = """
        SELECT * WHERE { 
            ?deck ns1:hasCard ?cardName .
            ?deck ns2:name "deck_name" .
            ?card ns2:name ?cardName .
            ?card ns1:img_url ?cardUrl .
            ?card ns1:cardClass ?cardClass .
        }
    """
    q = q.replace('deck_name', deckName)
    res = {}
    for r in g.query(q): 
        if r.cardName.toPython() not in res:
            res[r.cardName.toPython()] = [r.cardUrl.toPython(), r.cardClass.toPython()]
    deck_id = id - 3
    for k in res.keys():
        nodes.append({'id': id, 'label': k, 'shape': "image", 'image': res[k][0], 'shapeProperties': { 'useImageSize': False }})
        edges.append({'from': deck_id, 'to': id })
        node_id = id
        id += 1  
        if res[k][1] not in class_dic:
            class_dic[res[k][1]] = id
            nodes.append({'id': id, 'label': res[k][1]})
            id += 1
        edges.append({'from': node_id, 'to': class_dic[res[k][1]], 'label': 'cardClass'})
    return id, nodes, edges, class_dic


@app.route('/filter/deck', methods=['GET'])
def filter_deck():
    score_min = request.args.get("score_min")
    score_max = request.args.get("score_max")
    cost_min = request.args.get("cost_min")
    cost_max = request.args.get("cost_max")
    q = """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT * WHERE { 
            ?deck ns2:name ?deckName .
            ?deck ns1:price ?deckPrice .
            ?deck ns1:score ?deckScore .
            Filter(xsd:integer(?deckScore) >= scoreMin && xsd:integer(?deckScore) <= scoreMax) .
            Filter(xsd:integer(?deckPrice) >= costMin && xsd:integer(?deckPrice) <= costMax) .
        } ORDER BY DESC(?deckScore) (?deckPrice)
    """
    q = q.replace('scoreMin', score_min).replace('scoreMax', score_max).replace('costMin', cost_min).replace('costMax', cost_max)

    nodes, edges = [], []
    id = 1
    class_dic = {} # className: id
    for r in g.query(q): 
        nodes.append({'id': id, 'label': r.deckName.toPython()})
        nodes.append({'id': id+1, 'label': r.deckPrice.toPython()})
        nodes.append({'id': id+2, 'label': r.deckScore.toPython()})
        edges.append({'from': id, 'to': id+1, 'label': 'cost'})
        edges.append({'from': id, 'to': id+2, 'label': 'score'})
        id += 3
        id, nodes, edges, class_dic = sub_search_deck(r.deckName.toPython(), id, nodes, edges, class_dic)
        if len(nodes) > 300: break

    return {'nodes': nodes, 'edges': edges}


@app.route('/filter/card', methods=['GET'])
def filter_card():
    card_class = request.args.get("class")
    cost = request.args.get("cost")
    rarity = request.args.get("rarity")
    card_type = request.args.get("type")

    res_card_list = []

    # filtering
    for k, v in kg_dict.items():
        if card_class != "Class":
            if 'http://hskg.org/cardClass' not in v:
                continue
            if v['http://hskg.org/cardClass'] != card_class:
                continue

        if cost != "Cost":
            if 'http://hskg.org/cost' not in v:
                continue
            else:
                if cost == 7:
                    if int(v['http://hskg.org/cost']) < 7:
                        continue
                else:
                    if int(v['http://hskg.org/cost']) != cost:
                        continue

        if rarity != "Rarity":
            if 'http://hskg.org/rarity' not in v :
                continue
            if v['http://hskg.org/rarity'] != rarity:
                continue

        if card_type != "Type":
            if 'http://hskg.org/type' not in v:
                continue
            if v['http://hskg.org/type'] != card_type:
                continue
        
        res_card_list.append(k)

    nodes, edges = [], []
    label_nodeId_dict = {}
    id = 1
    # generate response
    for k in res_card_list:
        nodes.append({'id': id, 'label': k})
        node_id = id
        p_id = None
        id += 1
        for i, p in enumerate(kg_dict[k].keys()):
            # ignore set battleground
            if 'battle' in p:
                continue
            if p in ["http://hskg.org/dbfId", "http://hskg.org/collectible", "http://hskg.org/health"]:
                continue
            if p != 'http://hskg.org/img_url':
                if kg_dict[k][p] not in label_nodeId_dict:
                    nodes.append({'id': id, 'label': kg_dict[k][p]})
                    label_nodeId_dict[kg_dict[k][p]] = id
                    id += 1
                p_id = label_nodeId_dict[kg_dict[k][p]]
            else:
                nodes.append({'id': id, 'label': k, 'shape': "image", 'image': kg_dict[k][p], 'shapeProperties': { 'useImageSize': False }})
                p_id = id
                id += 1
            edges.append({ 'from': node_id, 'to': p_id , 'label': p})

        if len(nodes) > 200: break

    return {'nodes': nodes, 'edges': edges}


@app.route('/recommend/deck/<deckName>', methods=['GET'])
def recommend_deck(deckName):
    # return 'test'
    restored_model = restore_model(model_name_path = 'recommend.pkl')  
    rlt = query_topn(restored_model, top_n=5,
                    head=deckName, relation='has_card', tail=None,
                    ents_to_consider=None, rels_to_consider=None)[0].tolist()
    print(rlt)
    # return rlt
    return jsonify(rlt)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]