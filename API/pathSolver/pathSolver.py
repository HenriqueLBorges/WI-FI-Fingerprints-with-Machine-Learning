import json
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

if __name__ == '__main__': json_data=open('./graph.json').read()
else: json_data=open('./pathSolver/graph.json').read()

data = json.loads(json_data)

map = nx.Graph()

for edge in data['graph']['edges']:
    map.add_edge(edge['source'], edge['target'], weight = edge['metadata']['weight'])

#nx.draw(G, with_labels = True)
#plt.show()
#print(nx.shortest_path(G, 'sala A101', 'sala D161', weight='weight'))

#Returns the shortest path between current position and destination
def solve(current, destination):
    #print(current)
    #print(destination)
    try:
        #print(nx.shortest_path(map, current, destination, weight='weight'))
        return nx.shortest_path(map, current, destination, weight='weight')
    except Exception as e:
        return []

def getInstruction(nodeA, nodeB):
    print('nodeA = ' + str(nodeA))
    print('nodeB = ' + str(nodeB))
    for edge in data['graph']['edges']:
        if edge['source'] == nodeA and edge['target'] == nodeB:
            return edge

    return []

def findall(v, k):
  if type(v) == type({}):
     for k1 in v:
         if k1 == k:
            print v[k1]
         findall(v[k1], k)

print(findall(data, 'sala A101'))