from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF , XSD
import jsonlines
import json

IMG_PATH = "https://art.hearthstonejson.com/v1/render/latest/enUS/256x/"
MYNS = Namespace('http://hskg.org/')

# Create a Graph
hs_kg = Graph()

# read json data for cards and decks(form crawler)
cards = json.load(open('../src/cards.json'))
for card in cards:
    name = Literal(card['name'])
    cId = card['id']
    rdfID = card['dbfId']
    img_url = f"{IMG_PATH}{cId}.png"

    tmpCard = URIRef(f"{MYNS}card/{rdfID}")
    hs_kg.add((tmpCard, FOAF.name, name))
    hs_kg.add((tmpCard, MYNS.img_url, Literal(img_url)))
    for key in card.keys():
        if key not in ['name']:
            value = Literal(card[key])
            hs_kg.add((tmpCard, MYNS[key], value))

with jsonlines.open('../src/desks.jsonl') as decks:
    d_id = 0
    for deck in decks:
        tmpDeck = URIRef(f"{MYNS}deck/{d_id}")
        name = Literal(deck['name'])
        hs_kg.add((tmpDeck, FOAF.name, name))
        for card in deck['cards']:
            hs_kg.add((tmpDeck, MYNS['hasCard'], Literal(card)))
        for key in deck.keys():
            if key not in ['name', 'cards']:
                value = Literal(deck[key])
                hs_kg.add((tmpDeck, MYNS[key], value))

        d_id += 1

hs_kg.serialize('hskg.ttl', format="turtle")