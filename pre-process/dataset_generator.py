import jsonlines
import csv
import json
import random

csvFile = open('../src/recommend_dataset.csv', 'w+')
csvWriter = csv.writer(csvFile)

card_pool = set()

with jsonlines.open('../src/desks.jsonl') as decks:
    # 1st round: generate has card data
    for deck in decks:
        name = deck['name']
        for card in deck['cards']:
            tmp_data = [name, "has_card", card]
            csvWriter.writerow(tmp_data)

            # update card pool
            # card_pool.add(card)

cards = json.load(open('../src/cards.json'))
for card in cards:
    name = card['name']
    properties = ['cardClass', 'cost', 'rarity', 'type']
    for p in properties:
        if p in card:
            p_value = card[p]
            csvWriter.writerow([name, f"{p}_is", p_value])

# with jsonlines.open('../src/desks.jsonl') as decks:
#     # 2nd round: generate not has card data
#     for deck in decks:
#         name = deck['name']
#         deck_cards_set = set(deck['cards'])
#         card_num = len(deck_cards_set)
#         tmp_pool = tuple(card_pool)
#         random_set = set()
#         while True:
#             random_card = random.choice(tmp_pool)
#             if random_card not in deck_cards_set and random_card not in random_set:
#                 tmp_data = [name, "not_has_card", random_card]
#                 csvWriter.writerow(tmp_data)
#                 random_set.add(random_card)
#             # ratio of not_has_card data / has_card data is 3:1
#             if len(random_set) == 3 * card_num:
#                 break
csvFile.close()