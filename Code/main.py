# TODO
# najst vhodny vstupny text v anglictine na analyzu (projek guttenberg), anglictina vhodna kvoli tomu, ze nema sklonovanie
# prestudovat materialy o slovnych sietiach a analyze textu
# napisat program na generovanie slovnych sieti, moznosti bez alebo vratane interpunkcie
# pripadna vizualizacia slovnej siete

import matplotlib.pyplot as plt
import networkx as nx
import re

def readTextFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
    
    
def processTextFile(text, includePunctuation=False):
    if includePunctuation:
        data = re.findall(r"\.{3}|[\w']+|[.,!?;:()\"'/-]", text)
    else:
        data = re.findall(r"\w+", text)
    if data is None:
        return []
    splits = []
    for element in data:
        if "'" in element:
            splits.extend(re.findall(r"\w+|'", element))
        else:
            splits.append(element)
    return [word.lower() for word in splits]
    

def createGraphData(data):
    graphDataDict = {}

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
    print(processTextFile('"Hi, (How) are you?"', False))
    # inputData = readTextFile("inputText.txt")
    # processedData = processTextFile(inputData)
    # graphData = createGraphData(processedData)
    # plotGraph(graphData)