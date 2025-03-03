# TODO
# najst vhodny vstupny text v anglictine na analyzu (projek guttenberg), anglictina vhodna kvoli tomu, ze nema sklonovanie
# prestudovat materialy o slovnych sietiach a analyze textu
# napisat program na generovanie slovnych sieti, moznosti bez alebo vratane interpunkcie
# pripadna vizualizacia slovnej siete

import matplotlib.pyplot as plt
import networkx as nx

def readTextFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
    
def processTextFile(text):
    return []

def createGraphData(data, includePunctuation=False):
    graphDataDict = {}
    if includePunctuation:
        ...
    else:
        ...
    return graphDataDict
    

def plotGraph(data):
    G = nx.Graph()

    for node, edges in data.items():
        for edge in edges:
            if not G.has_edge(node, edge):
                G.add_edge(node, edge)

    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=37)

    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=30, node_color='orange', alpha=1)
    nx.draw_networkx_edges(G, pos, width=0.8, alpha=0.4, edge_color='gray')

    plt.title('Word Association Network')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    inputData = readTextFile("testing.txt")
    processedData = processTextFile(inputData)
    graphData = createGraphData(processedData)
    plotGraph(graphData)