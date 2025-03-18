from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout, \
                            QWidget, QComboBox, QCheckBox, QGridLayout, QSpacerItem, QSizePolicy, QTextEdit
from PyQt6.QtCore import Qt, QTimer
import matplotlib.pyplot as plt
import networkx as nx
import re
from collections import Counter
import numpy as np


class App(QMainWindow):
    def __init__(self):
        super().__init__()
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
        # window settings
        self.setWindowTitle('Punctuation Marks Analysis')
        self.setGeometry(250, 150, 700, 450)
        self.setFixedSize(700, 700)

        # file selction
        self.labelFileSelect = QLabel('Select a text file:', self)
        self.labelFileSelect.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelFileSelectPath = QLabel('No file selected', self)
        self.labelFileSelectPath.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.labelFileSelectPath.setStyleSheet("background-color: white; border: 1px solid #000000; padding: 5px; color: black")
        self.labelFileSelectPath.setFixedSize(600, 30)
        self.buttonSelectFile = QPushButton('Select File', self)
        self.buttonSelectFile.clicked.connect(self.selectInputFile)
        fileSelectLayout = QHBoxLayout()
        fileSelectLayout.addWidget(self.labelFileSelectPath)
        fileSelectLayout.addWidget(self.buttonSelectFile)
        fileSelectLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        fileSelectLayout.setSpacing(10)

        # language selection
        self.languageDropdown = QComboBox(self)
        self.languageDropdown.addItems(self.languageOptions)
        self.languageDropdown.currentIndexChanged.connect(self.languageChange)
        languageLayout = QHBoxLayout()
        languageLayout.addWidget(QLabel('Select Language:'))
        languageLayout.addWidget(self.languageDropdown)
        languageLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        languageLayout.setSpacing(10)
        self.languageDropdown.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # punctuation selection
        self.selectAllCheckbox = QCheckBox('Select All', self)
        self.selectAllCheckbox.stateChanged.connect(self.selectAllPunctuation)
        self.punctuationLabel = QLabel('Select Punctuation:', self)
        punctuationLayout = QGridLayout()
        self.punctuationCheckboxes = {}
        for i, (label, symbol) in enumerate(self.punctuation.items()):
            checkbox = QCheckBox(f'{label}  {symbol}', self)
            checkbox.stateChanged.connect(self.updateSelectedPunctuation)
            punctuationLayout.addWidget(checkbox, i//3, i%3)
            self.punctuationCheckboxes[label] = checkbox

        # exit button
        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(self.exitApp)
        self.exitButton.setFixedWidth(150)
        self.exitButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.exitButton)
        buttonLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # network button
        self.networkButton = QPushButton('Network', self)
        self.networkButton.clicked.connect(self.plotNetwork)
        self.networkButton.setFixedWidth(150)
        self.networkButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.networkButton.setEnabled(False)

        # histogram 1 button
        self.histogramOneButton = QPushButton('Histogram 1', self)
        self.histogramOneButton.clicked.connect(self.plotHistogramOne)
        self.histogramOneButton.setFixedWidth(150)
        self.histogramOneButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.histogramOneButton.setEnabled(False)

        # histogram 2 button
        self.histogramTwoButton = QPushButton('Histogram 2', self)
        self.histogramTwoButton.clicked.connect(self.plotHistogramTwo)
        self.histogramTwoButton.setFixedWidth(150)
        self.histogramTwoButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.histogramTwoButton.setEnabled(False)

        # visualisation buttons layout
        visualisationButtonsLayout = QHBoxLayout()
        visualisationButtonsLayout.addWidget(self.networkButton)
        visualisationButtonsLayout.addWidget(self.histogramOneButton)
        visualisationButtonsLayout.addWidget(self.histogramTwoButton)
        visualisationButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # log print button
        self.outputValues = QPushButton('Calculate Values', self)
        self.outputValues.clicked.connect(self.logOutputValues)
        self.outputValues.setFixedWidth(150)
        self.outputValues.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.outputValues.setEnabled(False)
        visualisationButtonsLayout.addWidget(self.outputValues)

        # log window
        self.logWindow = QTextEdit(self)
        self.logWindow.setReadOnly(True)
        self.logWindow.setFixedHeight(275)
        self.logWindow.setStyleSheet("background-color: #f0f0f0; border: 1px solid #000000; padding: 5px;")
        
        # main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.labelFileSelect)
        layout.addLayout(fileSelectLayout)
        layout.addLayout(languageLayout)
        layout.addWidget(self.punctuationLabel)
        layout.addWidget(self.selectAllCheckbox)
        layout.addLayout(punctuationLayout)
        layout.addWidget(self.logWindow)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addLayout(visualisationButtonsLayout)
        layout.addLayout(buttonLayout)
        layout.setSpacing(10)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    

    def logMessage(self, message):
        self.logWindow.append(message)


    def selectInputFile(self):
        fileDialog = QFileDialog()
        filePath, _ = fileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
        if filePath:
            self.inputTextFile = filePath
            self.labelFileSelectPath.setText(self.inputTextFile)
            self.validateInputData()


    def languageChange(self, index):
        self.selectedLanguage = self.languageOptions[index]
        self.validateInputData()


    def updateSelectedPunctuation(self, state):
        sender = self.sender()
        punctuationCheckboxLabel = sender.text().split()[0]
        if state == 2:
            self.selectedPunctuation[punctuationCheckboxLabel] = self.punctuation[punctuationCheckboxLabel]
        else:
            if punctuationCheckboxLabel in self.selectedPunctuation:
                del self.selectedPunctuation[punctuationCheckboxLabel]
            self.selectAllCheckbox.blockSignals(True)
            self.selectAllCheckbox.setChecked(False)
            self.selectAllCheckbox.blockSignals(False)
        if all(checkbox.isChecked() for checkbox in self.punctuationCheckboxes.values()):
            self.selectAllCheckbox.blockSignals(True)
            self.selectAllCheckbox.setChecked(True)
            self.selectAllCheckbox.blockSignals(False)
        self.validateInputData()


    def selectAllPunctuation(self, state):
        if state == 2:
            for checkbox in self.punctuationCheckboxes.values():
                checkbox.setChecked(True)
        else:
            for checkbox in self.punctuationCheckboxes.values():
                checkbox.setChecked(False)
        self.validateInputData()

    
    def logOutputValues(self):
        self.logMessage(self.collectInputDataInfo())
        self.logMessage(self.calculateValues(*self.processData(self.selectedPunctuation)))
        self.logMessage('\n')

    
    def processData(self, selectedPunctuation={}):
        return self.createGraphData(self.processTextFile(selectedPunctuation))


    def plotNetwork(self):
        self.logMessage(self.collectInputDataInfo())
        graphData, occurrenceData = self.processData(self.selectedPunctuation)
        self.logMessage(self.calculateValues(graphData, occurrenceData))  
        self.logMessage('Plotting network...')
        G = nx.Graph(graphData)
        pos = nx.spring_layout(G, iterations=35, seed=21)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_nodes(G, pos, node_size=1, node_color='black', alpha=1)
        nx.draw_networkx_edges(G, pos, width=0.6, alpha=0.5, edge_color='black')
        plt.title('Word Association Network')
        plt.axis('off')
        plt.show()
        self.logMessage('\n')


    def plotHistogramOne(self):
        self.logMessage(self.collectInputDataInfo())
        graphData, occurrenceData = self.processData(self.selectedPunctuation)
        self.logMessage(self.calculateValues(graphData, occurrenceData)) 
        self.logMessage('Plotting degree distribution histogram...')

        # G = nx.Graph(graphData)

        # y = nx.degree_histogram(G)
        # x = np.arange(0, len(y)).tolist()
        # nNodes = G.number_of_nodes()
        # for i in range(len(y)):
        #     y[i] = y[i]/nNodes
        # plt.xlabel('Degree\n(log scale)')
        # plt.ylabel('Number of Nodes\n(log scale)')
        # plt.xscale("log")
        # plt.yscale("log")
        # plt.plot(x, y, 'b-')
        # ba_c = nx.degree_centrality(G)
        # ba_c2 = dict(Counter(ba_c.values()))
        # plt.figure(figsize=(8, 8))
        # plt.xscale('log')
        # plt.yscale('log')
        # plt.scatter(ba_c2.keys(),ba_c2.values(),c='b',marker='x')
        # plt.xlim((1e-4,1e-1))
        # plt.ylim((.9,1e4))
        # plt.xlabel('Degree')
        # plt.ylabel('Frequency')
        # plt.show()

        self.logMessage('\n')


    def plotHistogramTwo(self):
        self.logMessage(self.collectInputDataInfo())
        graphDataOnlyWords, occurrenceDataOnlyWords = self.processData()
        self.logMessage(self.calculateValues(graphDataOnlyWords, occurrenceDataOnlyWords))
        graphDataCombined, occurrenceDataCombined = self.processData(self.selectedPunctuation)
        self.logMessage(self.calculateValues(graphDataCombined, occurrenceDataCombined))
        self.logMessage('Plotting degree distribution comparison histogram...')

        # G = nx.Graph(graphDataOnlyWords)
        # M = nx.Graph(graphDataCombined)

        self.logMessage('\n')


    def validateInputData(self):
        self.networkButton.setEnabled(bool(self.inputTextFile and self.selectedLanguage))
        self.histogramOneButton.setEnabled(bool(self.inputTextFile and self.selectedLanguage))
        self.histogramTwoButton.setEnabled(bool(self.inputTextFile and self.selectedLanguage))
        self.outputValues.setEnabled(bool(self.inputTextFile and self.selectedLanguage))


    def collectInputDataInfo(self):
        return f'Input Data...\nFile selected: {self.labelFileSelectPath.text()}\nLanguage: {self.selectedLanguage} \
                \nSelected Punctuation: {self.selectedPunctuation}'


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


    def calculateValues(self, data, occurrenceData):
        result = ['Network Values...']
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
        return '\n'.join(result)


    def exitApp(self):
        self.logMessage('App terminated...')
        QTimer.singleShot(500, self.close)



def main():
    print('Running the app...')
    app = QApplication([])
    window = App()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()