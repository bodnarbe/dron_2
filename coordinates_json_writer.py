import json

koordinatesjson = {}
koordinatesjson['koordinate']=[]
koordinates=[]
permet = []

koordinates_out = [[0, 0], [50, 0], [100, 0], [150, 0], [200, 0], [250, 0], [300, 0],
                   [300, 50], [250, 50], [200, 50], [150, 50], [100, 50], [50, 50], [0, 50],
                   [0, 100], [50, 100], [100, 100], [150, 100], [200, 100], [250, 100], [300, 100],
                   [300, 150], [250, 150], [200, 150], [150, 150], [100, 150], [50, 150], [0, 150],
                   [0, 200], [50, 200], [100, 200], [150, 200], [200, 200], [250, 200], [300, 200]]

# [[0, 0], [50, 0], [100, 0], [150, 0], [200, 0], [200, 50], [150, 50], [100, 50], [50, 50], [0, 50],
               # [0, 100], [50, 100], [100, 100],
               # [150, 100], [200, 100], [200, 150], [150, 150], [100, 150], [50, 150], [0, 150], [0, 200], [50, 200],
               # [100, 200], [150, 200], [200, 200]]

permet_out = [[0, 0], [0, 100], [100, 50]]

for i in enumerate(koordinates_out):
    koordinatesjson['koordinate'].append(i)

with open('koordinates.txt', 'w') as outfile:
    json.dump(koordinatesjson, outfile)

with open('koordinates.txt') as json_file:
    koordinatesjson_r = json.load(json_file)
    for p in koordinatesjson_r['koordinate']:
        permet.append(p[1])
        print(p)

print(permet)