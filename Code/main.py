import matplotlib.pyplot as plt
import networkx as nx
import re

regexDict = {
    "wordsNumbers": r'[a-zA-Z0-9]+',
    "ellipsis": r'\.{3}',
    "underscore": r'_',
    "period": r'\.',
    "comma": r',',
    "exclamation": r'!',
    "question": r'\?',
    "semicolon": r';',
    "colon": r':',
    "parenthesis": r'[()]',
    "brackets": r'[\[\]]',
    "braces": r'[{}]',
    "quotation": r'["“”]',
    "apostrophe": r'[\'’]',
    "slash": r'/',
    "hyphen": r'-',
    "enDash": r'–',
    "emDash": r'—'
}

allPunctuation = regexDict.keys()


def readTextFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

<<<<<<< HEAD

def processTextFile(text, includePunctuation=False, punctuationSelection=[], toLowerCase=False):
=======
    
# questionable if change splitted data to lowercase
def processTextFile(text, includePunctuation=False, punctuationSelection=None, toLowerCase=False):
>>>>>>> aee36c45b608d98da5223cfd5d99fe19c7787a3b
    if not includePunctuation:
        regexPattern = regexDict['wordsNumbers']
    else:
        selectedPunctuation = [regexDict[pat] for pat in punctuationSelection] if punctuationSelection else []
        regexPattern = '|'.join([regexDict['wordsNumbers']] + selectedPunctuation)
    
    data = re.findall(regexPattern, text)
    if not data:
        return []
    
    return [word.lower() for word in data] if toLowerCase else data
    

def createGraphData(data):
    graphDataDict = {}
    previousWord = None
    for element in data:
        if element in regexDict['quotation']:
            element = '"'
        if element in regexDict['apostrophe']:
            element = '\''
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

    pos = nx.spring_layout(G, k=0.15, iterations=21, seed=17)

    plt.figure(figsize=(8, 8))
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='red', alpha=1)
    nx.draw_networkx_edges(G, pos, width=0.6, alpha=0.5, edge_color='black')

    plt.title('Word Association Network')
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    # inputData = readTextFile('inputTextFiles\oneLineNoPunct.txt')
    # processedData = processTextFile(inputData, False)

    inputData = readTextFile('inputTextFiles\shortWithLotsPunct.txt')
    processedData = processTextFile(inputData, True, allPunctuation, True)

    graphData = createGraphData(processedData)
    nodesCount = len(graphData.keys())
    edgesCount = sum(len(edges) for edges in graphData.values()) // 2
    print(f"Number of nodes: {nodesCount} Number of edges: {edgesCount}")
    plotGraph(graphData)