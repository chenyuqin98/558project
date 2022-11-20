import requests

def get_card():
    data = requests.get('https://api.hearthstonejson.com/v1/155409/enUS/cards.json')
    return data.json()

# print(get_card())