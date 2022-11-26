# Goals & Objectives

We plan to build a knowledge graph about Hearthstone cards & decks . The knowledge graph will include information about the card, such asname, text, flavor, artist, attack, cardClass, cost... Also, there will be some hot decks information in our knowledge graph.

This knowledge graph will be designed to help players discover valuable cards and better find cards suited for their deck or help them seek hot good decks.

We want to use this knowledge graph to find the hottest decks, best rating cards in different classes or different card sets, and visualize the relationships between cards, decks, classes and some other interesting entities, so that players can have fun explore the knowledge. We also want to achieve some recommendation functions by using this knowledge graph if possible.

# Technical challenges

## Challenge1: Big data volume

### Problem

How to get so many data without damaging the server or be banned by the server?

For unstructured data, we crawled from https://www.hearthstonetopdecks.com/ to get the desks (a combination of cards) infomation shared on the website. We implemented a crawler to get infomation from 100 website pages, and each page contain about 20 desk urls, our crawler program will go to the desk url to get the detail infomation (cost, score, contains which cards) in the desk.

We need to request more than 2000 pages, which is a large load to the website server. Also, due to the large volume, our crawler maybe banned by the website. So we have to design some strateges, like show our identify or use a delay between two requests to avoid a large volume in short time.

### Example

When we use crawler to update our knowledge graph, there is a problem.

### Solution

Set a delay between every two requests.

### Evaluation:

- Request one or two times per second is just like a normal human action, so not damage the server;
- Succesfully got all data without any restriction or ban by the website  after the program ran several hours.

## Challenge2:Explore Card & Deck

### Problem

How to give player a easy way to explore the card they want? 

### Example

A player want to find a replacement of a card in mage class and cost 7+.

### Solution: 

- Build KG for cards

- Use sparql to search and filter the entitys

- Return result as a graph to help player find the card they want. 

### Evaluation:

- That’s very precise. Player can modify the parameter of filter to get  the result space as a graph.

## Challenge3:Recommender System

### Problem

How to recommend more cards for a existing desk? 

### Example

Player want to change their deck and want to get some recommend cards

### Solution

Build a TransE model. (More details in report)

### Evaluation

Randomly hide 20% data in the triples (desk-hasCard->card) as test dataset, got a 0.09 MRR.

# Lessons learned