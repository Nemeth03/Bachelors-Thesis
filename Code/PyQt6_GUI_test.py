from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout, \
                            QWidget, QComboBox, QCheckBox, QGridLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QTimer

# Main class that will run the app
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inputTextFile = None
        self.textData = None
        self.languageOptions = ['', 'Slovak', 'English', 'Czech', 'German', 'French', 'Spanish']
        self.selectedLanguage = ''
        self.punctuation = {'Period': '.', 
                            'Comma': ',', 
                            'Exclamation': '!', 
                            'Question': '?', 
                            'Semicolon': ';', 
                            'Colon': ':', 
                            'Parenthesis': '()', 
                            'Apostrophe': "'", 
                            'Quotation': '"..."',
                            'Slash': '/', 
                            'Hyphen': '-',
                            'Dash': '—'}
        self.specificPunctuation = {'Slovak': {'Quotation': ['„“']},
                                    'English': {}, 
                                    'Czech': {'Quotation': ['„“']},
                                    'German': {'Quotation': ['„“', '«»']}, 
                                    'French': {'Quotation': ['«»']}, 
                                    'Spanish': {'Quotation': ['„“', '«»'], 'Exclamation': ['¡','!'], 'Question': ['¿','?']}}
        self.selectedPunctuation = {}
        self.visualization = ['Log Log', 'Log Lin']
        self.selectedVisualization = {}
        self.initGUI()
    

    def readTextFile(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    

    def initGUI(self):
        # window settings
        self.setWindowTitle('PMA')
        self.setGeometry(250, 150, 700, 450)
        self.setFixedSize(700, 500)

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
        self.selectAllPuncCheckbox = QCheckBox('Select All', self)
        self.selectAllPuncCheckbox.stateChanged.connect(self.selectAllPunctuation)
        self.punctuationLabel = QLabel('Select Punctuation:', self)
        punctuationLayout = QGridLayout()
        self.punctuationCheckboxes = {}
        for i, (label, symbol) in enumerate(self.punctuation.items()):
            checkbox = QCheckBox(f'{label}  {symbol}', self)
            checkbox.stateChanged.connect(self.updateSelectedPunctuation)
            punctuationLayout.addWidget(checkbox, i//2, i%2)
            self.punctuationCheckboxes[label] = checkbox
        
        # visualization selection
        self.visualizationLabel = QLabel('Select Visualization:', self)
        visualizationLayout = QHBoxLayout()
        visualizationLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.visualizationCheckboxes = {}
        for viz in self.visualization:
            checkbox = QCheckBox(viz, self)
            checkbox.stateChanged.connect(self.updateSelectedVisualization)
            visualizationLayout.addWidget(checkbox)
            self.visualizationCheckboxes[viz] = checkbox

        # submit button
        self.submitButton = QPushButton('Submit', self)
        self.submitButton.clicked.connect(self.submitSelectedData)
        self.submitButton.setFixedWidth(150)
        self.submitButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.submitButton.setEnabled(False)

        # exit button
        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(self.exitApp)
        self.exitButton.setFixedWidth(150)
        self.exitButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.submitButton)
        buttonLayout.addWidget(self.exitButton)
        buttonLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.labelFileSelect)
        layout.addLayout(fileSelectLayout)
        layout.addLayout(languageLayout)
        layout.addWidget(self.punctuationLabel)
        layout.addWidget(self.selectAllPuncCheckbox)
        layout.addLayout(punctuationLayout)
        layout.addWidget(self.visualizationLabel)
        layout.addLayout(visualizationLayout)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addLayout(buttonLayout)
        layout.setSpacing(10)
        
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def selectInputFile(self):
        fileDialog = QFileDialog()
        filePath, _ = fileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
        if filePath:
            self.inputTextFile = filePath
            self.labelFileSelectPath.setText(self.inputTextFile)
            print(f"Selected file: {self.inputTextFile}")
            self.validateInputData()
        

    def languageChange(self, index):
        self.selectedLanguage = self.languageOptions[index]
        print(f"Selected language: {self.selectedLanguage}")
        self.validateInputData()


    def updateSelectedPunctuation(self, state):
        sender = self.sender()
        punctuationCheckboxLabel = sender.text().split()[0]
        if state == 2:
            self.selectedPunctuation[punctuationCheckboxLabel] = self.punctuation[punctuationCheckboxLabel]
        else:
            if punctuationCheckboxLabel in self.selectedPunctuation:
                del self.selectedPunctuation[punctuationCheckboxLabel]
            self.selectAllPuncCheckbox.blockSignals(True)
            self.selectAllPuncCheckbox.setChecked(False)
            self.selectAllPuncCheckbox.blockSignals(False)
        if all(checkbox.isChecked() for checkbox in self.punctuationCheckboxes.values()):
            self.selectAllPuncCheckbox.blockSignals(True)
            self.selectAllPuncCheckbox.setChecked(True)
            self.selectAllPuncCheckbox.blockSignals(False)
        print(f"Selected Punctuation: {self.selectedPunctuation}")
        self.validateInputData()
    

    def selectAllPunctuation(self, state):
        if state == 2:
            for checkbox in self.punctuationCheckboxes.values():
                checkbox.setChecked(True)
        else:
            for checkbox in self.punctuationCheckboxes.values():
                checkbox.setChecked(False)
        self.validateInputData()
    

    def updateSelectedVisualization(self, state):
        sender = self.sender()
        visualizationCheckboxLabel = sender.text()
        if state == 2:
            self.selectedVisualization[visualizationCheckboxLabel] = True
        else:
            if visualizationCheckboxLabel in self.selectedVisualization:
                del self.selectedVisualization[visualizationCheckboxLabel]
        print(f"Selected Visualization: {self.selectedVisualization}")
        self.validateInputData()


    def submitSelectedData(self):
        self.submitButton.setEnabled(False)
        QTimer.singleShot(3000, self.enableSubmitButton)

        print("Submitting data...")
        print(f"File selected: {self.labelFileSelectPath.text()}")
        print(f"Language: {self.selectedLanguage}")
        print(f"Selected Punctuation: {self.selectedPunctuation}")
        print(f"Selected Visualization: {self.selectedVisualization}")


    def enableSubmitButton(self):
        self.submitButton.setEnabled(True)
    

    def validateInputData(self):
        self.submitButton.setEnabled(bool(self.inputTextFile and self.selectedLanguage and \
                                          self.selectedPunctuation and self.selectedVisualization))


    def processSubmittedData(self):
        ...
    

    def exitApp(self):
        print('App terminated...')
        self.close()

        
def main():
    print('Running the app...')
    app = QApplication([])
    window = App()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()