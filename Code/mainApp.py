import wx
import matplotlib.pyplot as plt
import networkx as nx
import re
from collections import Counter
import numpy as np
import powerlaw

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
        self.regexDictGer['apostrophe'] = r'[\'’‚‘]'
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

        self.networkButton = wx.Button(panel, label='Network')
        self.networkButton.Bind(wx.EVT_BUTTON, self.plotNetwork)
        self.networkButton.Enable(False)

        self.histogramOneButton = wx.Button(panel, label='Histogram 1')
        self.histogramOneButton.Bind(wx.EVT_BUTTON, self.plotHistogramOne)
        self.histogramOneButton.Enable(False)

        self.histogramTwoButton = wx.Button(panel, label='Histogram 2')
        self.histogramTwoButton.Bind(wx.EVT_BUTTON, self.plotHistogramTwo)
        self.histogramTwoButton.Enable(False)

        self.outputValues = wx.Button(panel, label='Calculate Values')
        self.outputValues.Bind(wx.EVT_BUTTON, self.logOutputValues)
        self.outputValues.Enable(False)

        # Buttons Layout
        buttonLayout = wx.BoxSizer(wx.HORIZONTAL)
        buttonLayout.Add(self.networkButton, flag=wx.LEFT, border=10)
        buttonLayout.Add(self.histogramOneButton, flag=wx.LEFT, border=10)
        buttonLayout.Add(self.histogramTwoButton, flag=wx.LEFT, border=10)
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
        graphData, occurrenceData = self.processData(self.selectedPunctuation)
        # self.logMessage(self.calculateValues(graphData, occurrenceData))  
        self.logMessage('Plotting network...\n')

        G = nx.Graph(graphData)
        pos = nx.spring_layout(G, iterations=35, seed=21)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_nodes(G, pos, node_size=1, node_color='black', alpha=1)
        nx.draw_networkx_edges(G, pos, width=0.6, alpha=0.5, edge_color='black')
        plt.title('Word Association Network')
        plt.axis('off')
        plt.show()


    def plotHistogramOne(self, event):
        self.logMessage(self.collectInputDataInfo())
        graphData, occurrenceData = self.processData(self.selectedPunctuation)
        self.logMessage('Plotting degree distribution histogram...')

        G = nx.Graph(graphData)
        degrees = np.array([d for _, d in G.degree()])

        # degrees = [d for _, d in G.degree()]
        # degree_count = Counter(degrees)
        # self.logMessage(f'Degree distribution: {degree_count}')

        hist, binCenters = self.calculateLogBin(degrees, 20)

        fit = powerlaw.Fit(degrees)
        self.logMessage(f'Estimated power-law exponent (gamma): {fit.alpha:.3f}')
        self.logMessage(f'Estimated Xmin: {fit.xmin}')
        x_fit = np.linspace(min(binCenters), max(binCenters), 100)
        y_fit = (x_fit / fit.xmin) ** -fit.alpha

        plt.figure(figsize=(8, 8))
        plt.loglog(binCenters, hist, 'x', color='black', alpha=0.9)
        plt.loglog(binCenters, hist, '-', color='orange', alpha=0.8, label='Log-Binned Data')
        plt.loglog(x_fit, y_fit * max(hist) / max(y_fit), '--', color='red', label=f'Power-law Fit (γ={fit.alpha:.3f})')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Degree Distribution with Log-Binning')
        plt.legend()
        plt.show()
        self.logMessage('\n')


    def plotHistogramTwo(self, event):
        self.logMessage(self.collectInputDataInfo())
        graphDataOnlyWords, occurrenceDataOnlyWords = self.processData()
        graphDataCombined, occurrenceDataCombined = self.processData(self.selectedPunctuation)
        self.logMessage('Plotting degree distribution comparison histogram...\n')
    
        G = nx.Graph(graphDataOnlyWords)
        M = nx.Graph(graphDataCombined)
        histG, binCentersG = self.calculateLogBin(np.array([d for _, d in G.degree()]), 20)
        histM, binCentersM = self.calculateLogBin(np.array([d for _, d in M.degree()]), 20)

        plt.figure(figsize=(8, 8))
        plt.loglog(binCentersG, histG, '-', color='red', alpha=0.8, label='Words Only')
        plt.loglog(binCentersM, histM, '-', color='blue', alpha=0.8, label='Words + Punctuation')
        plt.loglog(binCentersG, histG, 'x', alpha=0.9, color='black')
        plt.loglog(binCentersM, histM, 'x', alpha=0.9, color='black')
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
        return hist[nonzero], binCenters[nonzero]


    def validateInputData(self):
        self.networkButton.Enable(bool(self.inputTextFile and self.selectedLanguage))
        self.histogramOneButton.Enable(bool(self.inputTextFile and self.selectedLanguage))
        self.histogramTwoButton.Enable(bool(self.inputTextFile and self.selectedLanguage))
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
        result.append(f'Number of nodes: {G.number_of_nodes()}')
        result.append(f'Number of edges: {G.number_of_edges()}')
        result.append(f'Max degree: {degrees[0]}')
        result.append(f'Min degree: {degrees[-1]}')
        result.append(f'Average degree: {sum(degValues)/len(degValues):.5f}')
        result.append(f'Network density: {nx.density(G):.4f}')
        result.append(f'Average clustering coefficient: {nx.average_clustering(G):.5f}')
        result.append(f'Average shortest path length: {nx.average_shortest_path_length(G):.5f}')
        result.append(f'Diameter: {nx.diameter(G)}')

        result.append('Jazyková analýza...')
        wordLengths = [len(word) for word in occurrenceData.keys()]
        result.append(f'Number of words: {len(wordLengths)}')
        result.append(f'Max word length: {max(wordLengths)}')
        result.append(f'Min word length: {min(wordLengths)}')
        result.append(f'Average word length: {(sum(wordLengths)/len(wordLengths)):.4f}')
        # pocet viet, max a min a avg dlzka vety
        # pocet dvojic slov
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



## TODO

# grafove (grafove algoritmy a veliciny) a jazykove (pocetnosti slov, znamienok, dvojic, atd..) analyzy
# treba navzorkovat text na vstupne velkosti 
# na roznych vstupnych velkostiach, pocetnosti slov: 100, 500, 1000, 2000, 3000, 5000...
# tak aby to zbehlo a ked uz sa to ustali, nebude velky rozdiel tak staci

# k vizualizacii grafov vyrezat loglogbin kde uz je optimalizovany, bez malych a velkych stupnov ktore tvoria anomalie
# zmerat smernicu priamky co dostaneme v logbinningu ak je 3 tak ideal, berieme do uvahy aj chybu

# (barabasi albert model, preferecne pripojenie) zacneme s trojuholnika a postupne pridavame uzly, vyskusat jej charakteristiky
# ak je 3 tak ideal, predpokladane byva okolo 2.7
# dorogovtsev-mendes model