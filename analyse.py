import json
list = []
n = 0
with open('bangumi_list.json', 'r') as f:
    data = json.load(f)
for i in data:
    
    #print(data[n]['title'])
    data[n]['title']
    list.append(f"{n} : {data[n]['title']}")
    n = n + 1



# now all the anime titles are in a list. you can do anything with it.
# for example, you can copy and paste it to a LLM to generate a summary.

print(list)
