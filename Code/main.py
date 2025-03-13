import matplotlib.pyplot as plt
import networkx as nx
import re
import time
from collections import Counter

regexDictEng = {
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
    "apostrophe": r'[\'’‘]',
    "slash": r'/',
    "hyphen": r'-',
    "enDash": r'–',
    "emDash": r'—'
}

regexDictGer = regexDictEng.copy()
regexDictGer["wordsNumbers"] = r'[a-zA-ZäöüÄÖÜß0-9]+'
regexDictGer["quotation"] = r'["„“«»]'
regexDictGer["apostrophe"] = r'[\'’‘]'

allPunctuationEng = regexDictEng.keys()
allPunctuationGer = regexDictGer.keys()


def readTextFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
    

def processTextFile(text, includePunctuation=False, punctuationSelection=None, toLowerCase=False, language='eng'):
    if language == 'eng':
        regexDict = regexDictEng
    elif language == 'ger':
        regexDict = regexDictGer

    if not includePunctuation:
        regexPattern = regexDict['wordsNumbers']
    else:
        selectedPunctuation = [regexDict[pat] for pat in punctuationSelection] if punctuationSelection else []
        regexPattern = '|'.join([regexDict['wordsNumbers']] + selectedPunctuation)
    
    data = re.findall(regexPattern, text)
    if not data:
        return []

    return [word.lower() for word in data] if toLowerCase else data


def createGraphData(data, language='eng'):
    if language == 'eng':
        regexDict = regexDictEng
    elif language == 'ger':
        regexDict = regexDictGer
    graphDataDict = {}
    nodeCounter = Counter()
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
        nodeCounter[element] += 1
    return graphDataDict, nodeCounter


def plotGraph(data):
    G = nx.Graph(data)

    pos = nx.spring_layout(G, iterations=35, seed=21)

    plt.figure(figsize=(8, 8))
    nx.draw_networkx_nodes(G, pos, node_size=1, node_color='black', alpha=1)
    nx.draw_networkx_edges(G, pos, width=0.6, alpha=0.5, edge_color='black')

    plt.title('Word Association Network')
    plt.axis('off')
    plt.show()
    

def calculateValues(data, occurrenceData):
    result = []
    G = nx.Graph(data)
    degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    degValues = [deg for _, deg in G.degree()]

    result.append(f'Number of nodes: {G.number_of_nodes()}')
    result.append(f'Number of edges: {G.number_of_edges()}')
    result.append(f'Top occurrences: {occurrenceData.most_common(5)}')
    result.append(f'Highest degrees: {degrees[:5]}')
    result.append(f'Average degree: {sum(degValues)/len(degValues):.4f}')
    result.append(f'Max degree: {degrees[0]}')
    result.append(f'Min degree: {degrees[-1]}')
    result.append(f'Network density: {nx.density(G):.4f}')
    result.append(f'Average clustering coefficient: {nx.average_clustering(G):.4f}')
    # result.append(f'Number of connected components: {len(list(nx.connected_components(G)))}')
    # result.append(f'Centrality Nodes: {sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:3]}')
    # result.append(f'Diameter: {nx.diameter(G)}')
    # result.append(f'Average shortest path: {nx.average_shortest_path_length(G):.4f}')
    return '\n'.join(result)


if __name__ == "__main__":
    startTime = time.time()

    textLanguage = 'ger'    # 'eng' or 'ger'
    
    ### ENG ###

    # inputData = readTextFile('inputTextFiles\oneLineNoPunct.txt')
    # processedData = processTextFile(inputData, False, allPunctuationEng, False, textLanguage)

    # inputData = readTextFile('inputTextFiles\shortENG.txt')
    # processedData = processTextFile(inputData, True, allPunctuationEng, True, textLanguage)

    # inputData = readTextFile('inputTextFiles\mediumENG.txt')
    # processedData = processTextFile(inputData, True, allPunctuationEng, True, textLanguage)

    # inputData = readTextFile('inputTextFiles\longENG.txt')
    # processedData = processTextFile(inputData, True, allPunctuationEng, True, textLanguage)
    
    # inputData = readTextFile('inputTextFiles\OliverTwistENG.txt')
    # processedData = processTextFile(inputData, True, allPunctuationEng, True, textLanguage)

    ### GER ###

    inputData = readTextFile('inputTextFiles\mediumGER.txt')
    processedData = processTextFile(inputData, True, allPunctuationGer, True, textLanguage)

    # inputData = readTextFile('inputTextFiles\longGER.txt')
    # processedData = processTextFile(inputData, True, allPunctuationGer, True, textLanguage)

    # inputData = readTextFile('inputTextFiles\OliverTwistGER.txt')
    # processedData = processTextFile(inputData, True, allPunctuationGer, True, textLanguage)

    graphData, occurrenceDict  = createGraphData(processedData, textLanguage)
    print(calculateValues(graphData, occurrenceDict))

    minutes, seconds = divmod(time.time() - startTime, 60)
    print(f"--- {int(minutes)} minutes, {seconds:.2f} seconds ---")

    plotGraph(graphData)

    minutes, seconds = divmod(time.time() - startTime, 60)
    print(f"--- {int(minutes)} minutes, {seconds:.2f} seconds ---")