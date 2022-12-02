# KG for Hearthstone cards & decks

> Group members:
>
> Xuyang Wang, Yuqin Chen

##  Demonstration Video

https://www.youtube.com/watch?v=G3rBZVr4Ej0

##  Domain & Goals

We plan to build a knowledge graph about **Hearthstone cards & decks**. The knowledge graph will include information about the card, such asname, text, flavor, artist, attack, cardClass, cost... Also, there will be some hot decks information in our knowledge graph.

This knowledge graph will be designed to help players discover valuable cards and better find cards suited for their deck or help them seek hot good decks.

We want to use this knowledge graph to find the hottest decks, best rating cards in different classes or different card sets, and visualize the relationships between cards, decks, classes and some other interesting entities, so that players can have fun explore the knowledge. We also want to achieve some recommendation functions by using this knowledge graph if possible.

##  Datasets 

1. [HearthstoneJSON](https://hearthstonejson.com/docs/cards.html): a json structured dataset for Hearthstone cards.

2. Unstructured data:
   - Cards: https://hearthstone.blizzard.com/en-us/cards
   - Decks: https://hsreplay.net/decks/
   - Decks:https://www.hearthstonetopdecks.com/

## Crawler part
Crawl data from websites:
    Cards: https://hearthstone.blizzard.com/en-us/cards
    Decks: https://hsreplay.net/decks/
    Decks:https://www.hearthstonetopdecks.com/

    https://www.hearthstonetopdecks.com/decks/

Expect data structure:
    Cards in Decks

Run crawler:
    scrapy crawl desk

## RDF part
Example URIRef for card:
```
@prefix ns1: <http://hkg.org/> .
@prefix ns2: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://hkg.org/card/52424> ns1:attack 0 ;
    ns1:cardClass "NEUTRAL" ;
    ns1:cost 0 ;
    ns1:dbfId 52424 ;
    ns1:faction "ALLIANCE" ;
    ns1:health 0 ;
    ns1:id "ART_BOT_Bundle_001" ;
    ns1:img_url "https://art.hearthstonejson.com/v1/render/latest/enUS/256x/ART_BOT_Bundle_001.jpg" ;
    ns1:rarity "LEGENDARY" ;
    ns1:set "TB" ;
    ns1:type "MINION" ;
    ns2:name "Golden Legendary" .
```

Example URIRef for deck:
```
@prefix ns1: <http://hskg.org/> .
@prefix ns2: <http://xmlns.com/foaf/0.1/> .

<http://hskg.org/deck/0>
    ns2:name "XL Secret Thief Rogue – #9 Legend (syoutotolo) – Knights of Hallow’s End" .
    ns1:price "17680" ;
    ns1:score "5" ;
    ns1:url "https://www.hearthstonetopdecks.com/decks/xl-secret-thief-rogue-9-legend-syoutotolo-knights-of-hallows-end/" ;
    ns1:hasCard
        "Contraband Stash",
        "Crabatoa",
        "Double Cross",
        "Ghastly Gravedigger",
        "Jackpot!",
        "Maestra of the Masquerade",
        "Perjury",
        "Preparation",
        "Prince Renathal",
        "Private Eye",
        "Queen Azshara",
        "Reconnaissance",
        "Serrated Bone Spike",
        "Shadowcrafter Scabbs",
        "Shadowstep",
        "Sire Denathrius",
        "Sketchy Stranger",
        "Sprint",
        "Swiftscale Trickster",
        "Tess Greymane",
        "The Sunwell",
        "Theotar, the Mad Duke",
        "Tooth of Nefarian",
        "Wicked Stab (Rank 1)",
        "Wildpaw Gnoll" ;
```