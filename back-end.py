# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, request, json, send_from_directory, render_template
from rdflib.namespace import FOAF
from rdflib import Graph
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer
import json
import sys
import requests

app = Flask(__name__, static_url_path='/static')
# app = Flask(__name__, static_url_path='/static', template_folder='knowledge-graph-browser-frontend/dist')
g = Graph().parse("src/hskg.ttl", format="turtle")


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/desk_explore', methods=['GET'])
def desk_explore():
    return render_template('desk_explore.html')


@app.route('/card_explore', methods=['GET'])
def card_explore():
    return render_template('card_explore.html')


@app.route('/search/card', methods=['GET'])
def search_card():
    card_name = request.args.get('card_name')

    # q = "SELECT * WHERE { ?p foaf:name ?name FILTER( ?name = \"" + card_name + "\")}"

    # encoder = JSONResultSerializer(g.query(q, initNs={'myns': 'http://hskg.org/', "foaf": FOAF}))
    # encoder.serialize(sys.stdout)
    # return ""
    img_url = "https://art.hearthstonejson.com/v1/render/latest/enUS/256x/NEW1_034.jpg"
    # q2 = "SELECT * WHERE { ?p myns:img_url ?url FILTER( ?url = \"" + img_url + "\")}"
    q2 = """
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT * WHERE { ?p foaf:name ?name}
    """
    for r in g.query(q2):
        print(r)
    return "test"


@app.route('/search/desk/<deskName>', methods=['GET'])
def search_desk(deskName): # "Reno Paladin – RegisKillbin – Sunken City"
    q = """
        SELECT * WHERE { 
            ?desk ns1:hasCard ?cardName .
            ?desk ns2:name "desk_name" .
            ?card ns2:name ?cardName .
            ?card ns1:img_url ?cardUrl .
        }
    """
    q = q.replace('desk_name', deskName)
    # print(1111, q, deskName)
    nodes = [{'id': 1, 'label': deskName}]
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


def sub_search_desk(deskName, id, nodes, edges):
    q = """
        SELECT * WHERE { 
            ?desk ns1:hasCard ?cardName .
            ?desk ns2:name "desk_name" .
            ?card ns2:name ?cardName .
            ?card ns1:img_url ?cardUrl .
        }
    """
    q = q.replace('desk_name', deskName)
    res = {}
    for r in g.query(q): 
        if r.cardName.toPython() not in res:
            res[r.cardName.toPython()] = r.cardUrl.toPython()
    desk_id = id - 3
    for k in res.keys():
        nodes.append({'id': id, 'label': k, 'shape': "image", 'image': res[k], 'shapeProperties': { 'useImageSize': False }})
        edges.append({ 'from': desk_id, 'to': id })
        id += 1  
    return id, nodes, edges


@app.route('/filter/desk', methods=['GET'])
def filter_desk():
    score_min = request.args.get("score_min")
    score_max = request.args.get("score_max")
    cost_min = request.args.get("cost_min")
    cost_max = request.args.get("cost_max")
    q = """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT * WHERE { 
            ?desk ns2:name ?deskName .
            ?desk ns1:price ?deskPrice .
            ?desk ns1:score ?deskScore .
            Filter(xsd:integer(?deskScore) >= scoreMin && xsd:integer(?deskScore) <= scoreMax) .
            Filter(xsd:integer(?deskPrice) >= costMin && xsd:integer(?deskPrice) <= costMax) .
        } ORDER BY DESC(?deskScore) (?deskPrice)
    """
    q = q.replace('scoreMin', score_min).replace('scoreMax', score_max).replace('costMin', cost_min).replace('costMax', cost_max)

    nodes, edges = [], []
    id = 1
    for r in g.query(q): 
        nodes.append({'id': id, 'label': r.deskName.toPython()})
        nodes.append({'id': id+1, 'label': r.deskPrice.toPython()})
        nodes.append({'id': id+2, 'label': r.deskScore.toPython()})
        edges.append({'from': id, 'to': id+1, 'label': 'cost'})
        edges.append({'from': id, 'to': id+2, 'label': 'score'})
        id += 3
        id, nodes, edges = sub_search_desk(r.deskName.toPython(), id, nodes, edges)
        if len(nodes) > 300: break

    return {'nodes': nodes, 'edges': edges}
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]