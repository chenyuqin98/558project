import json

max_p, min_p, max_s, min_s = 0,0,0,0
with open('./src/desks.jsonl') as f:
    for line in f.readlines():
        data = json.loads(line)
        # print(data)
        # print(data['price'], data['score'])
        if int(data['price']) > max_p: max_p = int(data['price'])
        if int(data['price']) < min_p: min_p = int(data['price'])
        if int(data['score']) > max_s: max_s = int(data['score'])
        if int(data['score']) < min_s: min_s = int(data['score'])

print(max_p, min_p, max_s, min_s)