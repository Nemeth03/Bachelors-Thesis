import wx
import matplotlib.pyplot as plt
import networkx as nx
import re
from collections import Counter
import numpy as np
import pickle
from scipy.stats import linregress

class App(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Punctuation Marks Analysis', size=(700, 700), \
                         style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        
        self.inputTextFile = None
        self.languageOptions = ['', 'English', 'German']
        self.selectedLanguage = ''
        self.punctuation = {'period': '.',
                            'comma': ',',
                            'exclamation': '!',
                            'question': '?', 
                            'semicolon': ';',
                            'colon': ':', 
                            'quotation': '"..."',
                            'apostrophe': '\'',
                            'underscore': '_',
                            'hyphen': '-',
                            'enDash': '–',
                            'emDash': '—',
                            'ellipsis': '...',
                            'slash': '/',
                            'parenthesis': '()',
                            'brackets': '[]',
                            'braces': '{}',
                            }
        self.selectedPunctuation = {}

        self.regexDictEng = {'wordsNumbers': r'[a-zA-Z0-9]+',
                            'ellipsis': r'\.{3}',
                            'underscore': r'_',
                            'period': r'\.',
                            'comma': r',',
                            'exclamation': r'!',
                            'question': r'\?',
                            'semicolon': r';',
                            'colon': r':',
                            'parenthesis': r'[()]',
                            'brackets': r'[\[\]]',
                            'braces': r'[{}]',
                            'quotation': r'["“”]',
                            'apostrophe': r'[\'’‘]',
                            'slash': r'/',
                            'hyphen': r'-',
                            'enDash': r'–',
                            'emDash': r'—'
                            }
        self.regexDictGer = self.regexDictEng
        self.regexDictGer['wordsNumbers'] = r'[a-zA-ZäöüÄÖÜß0-9]+'
        self.regexDictGer['quotation'] = r'["„“«»]'
        self.regexDictGer['apostrophe'] = r'[\'’‘]'
        self.initGUI()


    def readTextFile(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()


    def initGUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # File Selection
        self.labelFileSelect = wx.StaticText(panel, label='Select a text file:')
        self.labelFileSelectPath = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.labelFileSelectPath.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.labelFileSelectPath.SetForegroundColour(wx.Colour(0, 0, 0))
        self.labelFileSelectPath.SetValue('No file selected.')
        self.buttonSelectFile = wx.Button(panel, label='Select File')
        self.buttonSelectFile.Bind(wx.EVT_BUTTON, self.selectInputFile)
        
        fileSelectLayout = wx.BoxSizer(wx.HORIZONTAL)
        fileSelectLayout.Add(self.labelFileSelectPath, proportion=1, flag=wx.EXPAND | wx.ALIGN_LEFT)
        fileSelectLayout.Add(self.buttonSelectFile, flag=wx.LEFT, border=10)
        
        # Language Selection
        self.languageDropdown = wx.Choice(panel, choices=self.languageOptions)
        self.languageDropdown.Bind(wx.EVT_CHOICE, self.languageChange)
        languageLayout = wx.BoxSizer(wx.HORIZONTAL)
        languageLayout.Add(wx.StaticText(panel, label='Select Language:'), flag=wx.ALIGN_LEFT)
        languageLayout.Add(self.languageDropdown, flag=wx.LEFT, border=10)

        # Punctuation Selection
        self.selectAllCheckbox = wx.CheckBox(panel, label='Select All')
        self.selectAllCheckbox.Bind(wx.EVT_CHECKBOX, self.selectAllPunctuation)
        self.punctuationLabel = wx.StaticText(panel, label='Select Punctuation:')
        punctuationLayout = wx.GridSizer(5, 5, 5, 10)
        self.punctuationCheckboxes = {}
        for label, symbol in self.punctuation.items():
            checkbox = wx.CheckBox(panel, label=f'{label}  {symbol}')
            checkbox.Bind(wx.EVT_CHECKBOX, self.updateSelectedPunctuation)
            punctuationLayout.Add(checkbox, flag=wx.EXPAND)
            self.punctuationCheckboxes[label] = checkbox

        # Log window
        self.logWindow = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.logWindow.SetBackgroundColour(wx.Colour(240, 240, 240))

        # Buttons
        self.exitButton = wx.Button(panel, label='Exit')
        self.exitButton.Bind(wx.EVT_BUTTON, self.exitApp)

        self.networkButton = wx.Button(panel, label='Network Graph')
        self.networkButton.Bind(wx.EVT_BUTTON, self.plotNetwork)
        self.networkButton.Enable(False)

        self.visualizeAnalysisButton = wx.Button(panel, label='Visualize Analysis')
        self.visualizeAnalysisButton.Bind(wx.EVT_BUTTON, self.visualizeAnalysis)
        self.visualizeAnalysisButton.Enable(False)

        self.compareDistributionsButton = wx.Button(panel, label='Compare Distributions')
        self.compareDistributionsButton.Bind(wx.EVT_BUTTON, self.compareDistributions)
        self.compareDistributionsButton.Enable(False)

        self.outputValues = wx.Button(panel, label='Calculate Analysis Data')
        self.outputValues.Bind(wx.EVT_BUTTON, self.logOutputValues)
        self.outputValues.Enable(False)

        # Buttons Layout
        buttonLayout = wx.BoxSizer(wx.HORIZONTAL)
        buttonLayout.Add(self.networkButton, flag=wx.LEFT, border=10)
        buttonLayout.Add(self.visualizeAnalysisButton, flag=wx.LEFT, border=10)
        buttonLayout.Add(self.compareDistributionsButton, flag=wx.LEFT, border=10)
        buttonLayout.Add(self.outputValues, flag=wx.LEFT, border=10)
        buttonLayout.Add(self.exitButton, flag=wx.LEFT, border=10)

        # Layout
        vbox.Add(self.labelFileSelect, flag=wx.EXPAND | wx.LEFT | wx.TOP, border=10)
        vbox.Add(fileSelectLayout, flag=wx.EXPAND | wx.LEFT | wx.TOP, border=10)
        vbox.Add(languageLayout, flag=wx.EXPAND | wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.punctuationLabel, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.selectAllCheckbox, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(punctuationLayout, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(self.logWindow, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)        
        vbox.Add(buttonLayout, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        panel.SetSizer(vbox)
        self.Centre()


    def logMessage(self, message):
        self.logWindow.AppendText(f'{message}\n')


    def selectInputFile(self, event):
        fileDialog = wx.FileDialog(self, 'Open Text File', wildcard='Text files (*.txt)|*.txt', style=wx.FD_OPEN)
        if fileDialog.ShowModal() == wx.ID_OK:
            self.inputTextFile = fileDialog.GetPath()
            self.labelFileSelectPath.SetValue(self.inputTextFile)
            self.validateInputData()


    def languageChange(self, event):
        self.selectedLanguage = self.languageOptions[self.languageDropdown.GetSelection()]
        self.validateInputData()


    def updateSelectedPunctuation(self, event):
        sender = event.GetEventObject()
        punctuationCheckboxLabel = sender.GetLabel().split()[0]
        if sender.IsChecked():
            self.selectedPunctuation[punctuationCheckboxLabel] = self.punctuation[punctuationCheckboxLabel]
        else:
            if punctuationCheckboxLabel in self.selectedPunctuation:
                del self.selectedPunctuation[punctuationCheckboxLabel]
        self.selectAllCheckbox.SetValue(False) if any([not checkbox.IsChecked() \
                                    for checkbox in self.punctuationCheckboxes.values()]) else self.selectAllCheckbox.SetValue(True)
        self.validateInputData()


    def selectAllPunctuation(self, event):
        checked = event.IsChecked()
        self.selectedPunctuation.clear()
        for label, checkbox in self.punctuationCheckboxes.items():
            checkbox.SetValue(checked)
            if checked:
                self.selectedPunctuation[label] = self.punctuation[label]
        self.validateInputData()


    def logOutputValues(self, event):
        self.logMessage(self.collectInputDataInfo())
        self.logMessage(self.calculateValues(*self.processData(self.selectedPunctuation)))
        self.logMessage('\n')


    def processData(self, selectedPunctuation={}):
        return self.createGraphData(self.processTextFile(selectedPunctuation))


    def plotNetwork(self, event):
        self.logMessage(self.collectInputDataInfo())
        self.logMessage('Plotting network...\n')

        G = nx.Graph(self.processData(self.selectedPunctuation)[0])
        pos = nx.spring_layout(G, iterations=35, seed=21)
        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, node_size=1, node_color='black', alpha=1)
        nx.draw_networkx_edges(G, pos, width=0.6, alpha=0.5, edge_color='black')
        plt.title('Word Association Network')
        plt.axis('off')
        plt.show()


    def visualizeAnalysis(self, event):
        self.logMessage(self.collectInputDataInfo())
        self.logMessage('Visualizing Analysis...')

        graphData, occurrenceData = self.processData(self.selectedPunctuation)
        # create graph from graphData
        G = nx.Graph()
        for node, neighbors in graphData.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        degrees = [G.degree(n) for n in G.nodes()]
        unique, counts = np.unique(degrees, return_counts=True)

        # create Barabasi-Albert model, with same number of nodes and edges as my data
        numNodes = len(G.nodes())
        numEdges = int(np.mean(degrees)/2)
        BA_G = nx.barabasi_albert_graph(numNodes, numEdges)
        baDegrees = [BA_G.degree(n) for n in BA_G.nodes()]
        baUnique, baCounts = np.unique(baDegrees, return_counts=True)

        # create Dorogovtsev-Goltsev-Mendes model, with same number of nodes as my data
        # dgm_graph_10000_edges.gpickle
        # dgm_graph_20000_edges.gpickle
        # dgm_graph_30000_edges.gpickle
        # dgm_graph_70000_edges.gpickle
        with open('dgm_graph_70000_edges.gpickle', 'rb') as f:
            DGM_G = pickle.load(f)
        dgmDegrees = [DGM_G.degree(n) for n in DGM_G.nodes()]
        dgmUnique, dgmCounts = np.unique(dgmDegrees, return_counts=True)

        # set my data raw degree distribution to be same range as in ba model
        start, end = baUnique[0], baUnique[-1]
        mask = (unique >= start) & (unique <= end)
        unique = unique[mask]
        counts = counts[mask]

        # my data, log binning, selecting only the longest decreasing slice
        binCenters, binValues = self.calculateLogBin(np.array(degrees), 20)
        start, end = self.longestDecreasingSlice(binValues)
        binValues = binValues[start: end+1]
        binCenters = binCenters[start: end+1]

        # simulated ba model, log binning, selecting only the longest decreasing slice
        baBinCenters, baBinValues = self.calculateLogBin(np.array(baDegrees), 20)
        baStart, baEnd = self.longestDecreasingSlice(baBinValues)
        baBinValues = baBinValues[baStart: baEnd+1]
        baBinCenters = baBinCenters[baStart: baEnd+1]

        # simulated dmg model, log binning, selecting only the longest decreasing slice
        dgmBinCenters, dgmBinValues = self.log_bin_data(np.array(dgmDegrees), 1.01)
        # dgmStart, dgmEnd = self.longestDecreasingSlice(dgmBinValues)
        # dgmBinValues = dgmBinValues[dgmStart: dgmEnd+1]
        # dgmBinCenters = dgmBinCenters[dgmStart: dgmEnd+1]

        # calculate slopes
        slope = self.calculateLogLogSlope(binCenters, binValues)
        baSlope = self.calculateLogLogSlope(baBinCenters, baBinValues)
        dgmSlope = self.calculateLogLogSlope(dgmBinCenters, dgmBinValues)

        # calculate Zipf's law on my data and slope
        wordFrequencies = sorted(occurrenceData.values(), reverse=True)
        ranks = np.arange(1, len(wordFrequencies) + 1)
        zipfSlope = self.calculateLogLogSlope(ranks, wordFrequencies)

        # plotting
        plt.figure(figsize=(12, 10))

        plt.subplot(3, 1, 1)
        plt.loglog(unique, counts, 'bo', markersize=4, label=f'Word Network')
        plt.loglog(baUnique, baCounts, 'ro', markersize=4, label=f'BA Model')
        plt.loglog(dgmUnique, dgmCounts, 'go', markersize=4, label=f'DGM Model')
        plt.xlabel("Degree (k)")
        plt.ylabel("P(k)")
        plt.title("Degree Distribution Comparison")
        plt.legend()
        
        plt.subplot(3, 1, 2)
        plt.loglog(binCenters, binValues, 'x', color='black', alpha=0.9)
        plt.loglog(binCenters, binValues, '-', color='blue', alpha=0.8, label=f'Word Network, Slope={slope:.5f}')
        plt.loglog(baBinCenters, baBinValues, 'x', color='black', alpha=0.9)
        plt.loglog(baBinCenters, baBinValues, '-', color='red', alpha=0.8, label=f'Simulated BA Model, Slope={baSlope:.5f}')
        plt.loglog(dgmBinCenters, dgmBinValues, 'x', color='black', alpha=0.9)
        plt.loglog(dgmBinCenters, dgmBinValues, '-', color='green', alpha=0.8, label=f'Simulated DGM Model, Slope={dgmSlope:.5f}')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Degree Distribution with Log-Binning')
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.loglog(ranks, wordFrequencies, 'x', color='black', alpha=0.9)
        plt.loglog(ranks, wordFrequencies, '-', color='black', alpha=0.8, label=f'Zipf\'s Law, Slope={zipfSlope:.5f}')
        plt.xlabel('Rank')
        plt.ylabel('Frequency')
        plt.title('Zipf\'s Law Analysis')
        plt.legend()

        plt.tight_layout()
        plt.show()

        self.logMessage('\n')


    def compareDistributions(self, event):
        self.logMessage(self.collectInputDataInfo())
        graphDataOnlyWords, occurrenceDataOnlyWords = self.processData()
        graphDataCombined, occurrenceDataCombined = self.processData(self.selectedPunctuation)
        self.logMessage('Plotting degree distribution comparison histogram...\n')

        # graph without punctuation
        G = nx.Graph()
        for node, neighbors in graphDataOnlyWords.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        gDegrees = [G.degree(n) for n in G.nodes()]
        gUnique, gCounts = np.unique(gDegrees, return_counts=True)

        # graph with punctuation
        M = nx.Graph()
        for node, neighbors in graphDataCombined.items():
            for neighbor in neighbors:
                M.add_edge(node, neighbor)
        mDegrees = [M.degree(n) for n in M.nodes()]
        mUnique, mCounts = np.unique(mDegrees, return_counts=True)

        # log binning
        gBinCenters, gBinValues = self.calculateLogBin(np.array(gDegrees), 20)
        mBinCenters, mBinValues = self.calculateLogBin(np.array(mDegrees), 20)

        # selecting longest decreasing slice, same range for both
        gStart, gEnd = self.longestDecreasingSlice(gBinValues)
        mStart, mEnd = self.longestDecreasingSlice(mBinValues)
        if gEnd-gStart < mEnd-mStart:
            gStart, gEnd = mStart, mEnd
        if gEnd-gStart > mEnd-mStart:
            mStart, mEnd = gStart, gEnd
        gBinValues = gBinValues[gStart: gEnd + 1]
        mBinValues = mBinValues[gStart: gEnd + 1]
        gBinCenters = gBinCenters[gStart: gEnd + 1]
        mBinCenters = mBinCenters[gStart: gEnd + 1]

        # calculate slopes
        gSlope = self.calculateLogLogSlope(gBinCenters, gBinValues)
        mSlope = self.calculateLogLogSlope(mBinCenters, mBinValues)

        plt.figure(figsize=(12, 10))

        plt.subplot(2, 1, 1)
        plt.loglog(gUnique, gCounts, 'bo', markersize=4, label='Words')
        plt.loglog(mUnique, mCounts, 'ro', markersize=4, label='Words + Punctuation')
        plt.xlabel("Degree (k)")
        plt.ylabel("P(k)")
        plt.title("Degree Distribution Comparison")
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.loglog(gBinCenters, gBinValues, '-', color='red', alpha=0.8, label=f'Words Only, Slope={gSlope:.5f}')
        plt.loglog(mBinCenters, mBinValues, '-', color='blue', alpha=0.8, label=f'Words + Punctuation, Slope={mSlope:.5f}')
        plt.loglog(gBinCenters, gBinValues, 'x', alpha=0.9, color='black')
        plt.loglog(mBinCenters, mBinValues, 'x', alpha=0.9, color='black')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Degree Distribution Comparison with Log-Binning')
        plt.legend()

        plt.show()


    def calculateLogBin(self, degrees, binCount):
        minDegree = max(1, min(degrees))
        maxDegree = degrees.max()
        bins = np.logspace(np.log10(minDegree), np.log10(maxDegree), num=binCount)
        hist, binEdges = np.histogram(degrees, bins=bins, density=True)
        binCenters = (binEdges[:-1] + binEdges[1:]) / 2
        nonzero = hist > 0
        return binCenters[nonzero], hist[nonzero]
    

    def log_bin_data(self, raw_degrees, bin_base=1.1):
        bins = [bin_base ** i for i in range(int(np.log(max(raw_degrees)) / np.log(bin_base)) + 1)]
        binned_degrees = []
        binned_counts = []
        for i in range(len(bins) - 1):
            bin_min, bin_max = bins[i], bins[i + 1]
            bin_mask = (raw_degrees >= bin_min) & (raw_degrees < bin_max)
            if np.any(bin_mask):
                binned_degrees.append(np.mean(raw_degrees[bin_mask]))
                binned_counts.append(np.sum(bin_mask))
        return np.array(binned_degrees), np.array(binned_counts)
    

    def calculateLogLogSlope(self, x, y):
        log_degrees = np.log10(x)
        log_counts = np.log10(y)
        slope, intercept, r_value, p_value, std_err = linregress(log_degrees, log_counts)
        return slope
    
    
    def longestDecreasingSlice(self, data):
        sliceStart, sliceEnd = 0, 0
        currentStart = 0
        for i in range(1, len(data)):
            if data[i] >= data[i-1]:
                currentStart = i
            elif i - currentStart > sliceEnd - sliceStart:
                sliceStart, sliceEnd = currentStart, i
        return sliceStart, sliceEnd
    

    def validateInputData(self):
        self.networkButton.Enable(bool(self.inputTextFile and self.selectedLanguage))
        self.visualizeAnalysisButton.Enable(bool(self.inputTextFile and self.selectedLanguage))
        self.compareDistributionsButton.Enable(bool(self.inputTextFile and self.selectedLanguage))
        self.outputValues.Enable(bool(self.inputTextFile and self.selectedLanguage))


    def processTextFile(self, selectedPunctuation={}):
        if self.selectedLanguage == 'English':
            regexDict = self.regexDictEng
        if self.selectedLanguage == 'German':
            regexDict = self.regexDictGer
        if not selectedPunctuation:
            regexPattern = regexDict['wordsNumbers']
        else:
            usePunctuation = [regexDict[key] for key in selectedPunctuation.keys()]
            regexPattern = '|'.join([regexDict['wordsNumbers']] + usePunctuation)
        data = re.findall(regexPattern, self.readTextFile(self.inputTextFile))
        if not data:
            return []
        return [word.lower() for word in data]


    def createGraphData(self, data):
        if self.selectedLanguage == 'English':
            regexDict = self.regexDictEng
        if self.selectedLanguage == 'German':
            regexDict = self.regexDictGer
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


    def calculateValues(self, graphData, occurrenceData):
        result = ['Grafová analýza...']
        G = nx.Graph(graphData)
        degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)
        degValues = [deg for _, deg in G.degree()]
        correlationDegreeCloseness = np.corrcoef(list(nx.degree_centrality(G).values()), list(nx.closeness_centrality(G).values()))[0, 1]
        correlationDegreeBetweenness = np.corrcoef(list(nx.degree_centrality(G).values()), list(nx.betweenness_centrality(G).values()))[0, 1]
        correlationClosenessBetweenness = np.corrcoef(list(nx.closeness_centrality(G).values()), list(nx.betweenness_centrality(G).values()))[0, 1]
        
        result.append(f'Number of nodes: {G.number_of_nodes()}')
        result.append(f'Number of edges: {G.number_of_edges()}')
        result.append(f'Max degree: {degrees[0]}')
        result.append(f'Min degree: {degrees[-1]}')
        result.append(f'Average degree: {sum(degValues)/len(degValues):.5f}')
        result.append(f'Network density: {nx.density(G):.5f}')
        result.append(f'Correlation (Degree vs Closeness): {correlationDegreeCloseness:.5f}')
        result.append(f'Correlation (Degree vs Betweenness): {correlationDegreeBetweenness:.5f}')
        result.append(f'Correlation (Closeness vs Betweenness): {correlationClosenessBetweenness:.5f}')
        result.append(f'Average clustering coefficient: {nx.average_clustering(G):.5f}')
        result.append(f'Average shortest path length: {nx.average_shortest_path_length(G):.5f}')
        result.append(f'Diameter: {nx.diameter(G)}')

        result.append('Jazyková analýza...')
        wordLengths = [len(word) for word in occurrenceData.keys()]
        processedSentences = self.processTextFile({'period': '.', 'exclamation': '!', 
                                              'question': '?', 'ellipsis': '...', 'apostrophe': '\'’‘'})
        i = 0
        while i < len(processedSentences):
            if processedSentences[i] in ['\'', '’', '‘'] and i > 0 and i < len(processedSentences)-1:
                processedSentences[i-1:i+2] = [''.join(processedSentences[i-1:i+2])]
            else:
                i += 1
        sentences = []
        subList = []
        sentencelengths = []
        for element in processedSentences:
            if element in ['.', '!', '?', '...'] and subList:
                sentences.append(subList)
                sentencelengths.append(len(subList))
                subList = []
            else:
                subList.append(element)
        data = self.processTextFile(self.selectedPunctuation)
        bigramCounter = Counter(zip(data[:-1], data[1:]))
        bigramFrequencies = [count for _, count in bigramCounter.items()]
        trigramCounter = Counter(zip(data[:-2], data[1:-1], data[2:]))
        trigramFrequencies = [count for _, count in trigramCounter.items()]

        result.append(f'Number of words: {len(wordLengths)}')
        result.append(f'Max word length: {max(wordLengths)}')
        result.append(f'Min word length: {min(wordLengths)}')
        result.append(f'Average word length: {(sum(wordLengths)/len(wordLengths)):.5f}')
        result.append(f'Number of sentences: {len(sentences)}')
        result.append(f'Max sentence length: {max(sentencelengths)}')
        result.append(f'Min sentence length: {min(sentencelengths)}')
        result.append(f'Average sentence length: {(sum(sentencelengths)/len(sentencelengths)):.5f}')
        result.append(f'Number of bigrams: {len(bigramCounter)}')
        result.append(f'Max bigram frequency: {max(bigramFrequencies)}')
        result.append(f'Min bigram frequency: {min(bigramFrequencies)}')
        result.append(f'Average bigram frequency: {sum(bigramFrequencies)/len(bigramFrequencies):.5f}')
        result.append(f'Number of trigrams: {len(trigramCounter)}')
        result.append(f'Max trigram frequency: {max(trigramFrequencies)}')
        result.append(f'Min trigram frequency: {min(trigramFrequencies)}')
        result.append(f'Average trigram frequency: {sum(trigramFrequencies)/len(trigramFrequencies):.5f}')

        return '\n'.join(result)


    def collectInputDataInfo(self):
        return f'Input Data...\nFile selected: {self.labelFileSelectPath.GetValue()}\nLanguage: {self.selectedLanguage} \
            \nSelected Punctuation: {", ".join(self.selectedPunctuation.keys())}'


    def exitApp(self, event):
        self.logMessage('Exiting application...')
        wx.CallLater(500, self.Close)


if __name__ == '__main__':
    app = wx.App(False)
    frame = App()
    frame.Show()
    app.MainLoop()



# vypocitat chybu medzi mojou sietou chybou
# zacat pisat teoriu
# porozumiet dgm modelu
# gephi
# viacero textov pre analyzu