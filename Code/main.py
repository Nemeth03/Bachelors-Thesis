import matplotlib.pyplot as plt
import networkx as nx
import re

regex_dict = {
    "wordsNumbers": r"[a-zA-Z0-9]+",
    "ellipsis": r"\.{3}",
    "underscore": r"_",
    "period": r"\.",
    "comma": r",",
    "exclamation": r"!",
    "question": r"\?",
    "semicolon": r";",
    "colon": r":",
    "parenthesis_open": r"\(",
    "parenthesis_close": r"\)",
    "double_quote": r"\"", 
    "single_quote": r"'",
    "slash": r"/",
    "hyphen": r"-"
}


def readTextFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
    
    
def processTextFile(text, includePunctuation=False):
    if includePunctuation:
        data = re.findall(r"[a-zA-Z0-9]+|\.{3}|_|[.,!?;:()\"'/-]", text)
    else:
        data = re.findall(r"[a-zA-Z0-9]+", text)
    if not data:
        return []
    return [word.lower() for word in data]
    

def createGraphData(data):
    graphDataDict = {}
    previousWord = None
    for element in data:
        if element not in graphDataDict:
            graphDataDict[element] = []
        if previousWord is not None:
            graphDataDict[previousWord].append(element)
            graphDataDict[element].append(previousWord)
        previousWord = element
    return graphDataDict
    

def plotGraph(data):
    G = nx.Graph()

    for node, edges in data.items():
        for edge in edges:
            if not G.has_edge(node, edge):
                G.add_edge(node, edge)

    pos = nx.spring_layout(G, k=0.15, iterations=11, seed=33)

    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=30, node_color='orange', alpha=1)
    nx.draw_networkx_edges(G, pos, width=0.8, alpha=0.4, edge_color='gray')

    plt.title('Word Association Network')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    inputData = readTextFile("inputTextFiles\oneLineNoPunct.txt")
    processedData = processTextFile(inputData)
    graphData = createGraphData(processedData)
    plotGraph(graphData)