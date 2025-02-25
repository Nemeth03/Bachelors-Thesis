from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout, \
                            QWidget, QComboBox, QCheckBox, QGridLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

# Visualization of the analysed data
class GraphVisualizer:
    def __init__(self):
        ...
    
    def plotLogLog(self):
        ...
    
    def plotLogLin(self):
        ...
    
# Main class that will run the app
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inputTextFile = None
        self.textData = None
        self.languageOptions = ['Slovak', 'English', 'Czech', 'German', 'French', 'Spanish']
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
        self.initGUI()
    
    def readTextFile(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def initGUI(self):
        self.setWindowTitle('PMA')
        self.setGeometry(250, 150, 600, 400)

        self.setFixedSize(700, 450)

        self.labelFileSelect = QLabel('Select a text file:', self)
        self.labelFileSelect.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # file selction
        self.label = QLabel('No file selected', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.label.setStyleSheet("background-color: white; border: 1px solid #000000; padding: 5px;")
        self.label.setFixedSize(600, 30)
        self.button = QPushButton('Select File', self)
        self.button.clicked.connect(self.select_file)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.label)
        file_layout.addWidget(self.button)
        file_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align elements to the left
        file_layout.setSpacing(10)  # Set spacing to zero between the label and the button
        self.label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # language selection
        self.language_combo = QComboBox(self)
        self.language_combo.addItems(self.languageOptions)
        self.language_combo.currentIndexChanged.connect(self.language_changed)
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel('Select Language:'))
        lang_layout.addWidget(self.language_combo)
        lang_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        lang_layout.setSpacing(10)
        self.language_combo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # punctuation selection
        self.select_all_checkbox = QCheckBox('Select All', self)
        self.select_all_checkbox.stateChanged.connect(self.select_all_punctuation)
        punctuation_headline = QLabel('Select Punctuation:', self)
        punctuation_layout = QGridLayout()
        row = 0
        col = 0
        self.checkboxes = {}
        for label, symbol in self.punctuation.items():
            checkbox = QCheckBox(f'{label}  {symbol}', self)
            checkbox.stateChanged.connect(self.update_punctuation)
            punctuation_layout.addWidget(checkbox, row, col)
            self.checkboxes[label] = checkbox
            col += 1
            if col > 1:
                col = 0
                row += 1

        # submit button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_data)
        self.submit_button.setFixedWidth(100)  # Make the button smaller
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # exit button
        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.exit_application)
        self.exit_button.setFixedWidth(100)  # Make the button smaller
        self.exit_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.exit_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.labelFileSelect)
        layout.addLayout(file_layout)
        layout.addLayout(lang_layout)
        layout.addWidget(punctuation_headline)
        layout.addWidget(self.select_all_checkbox)
        layout.addLayout(punctuation_layout)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addLayout(button_layout)

        layout.setSpacing(10)
        
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        if file_path:
            self.label.setText(file_path)
            print(f"Selected file: {file_path}")
        
    def language_changed(self, index):
        self.selectedLanguage = self.languageOptions[index]
        print(f"Selected language: {self.selectedLanguage}")

    def update_punctuation(self, state):
        sender = self.sender()
        punctuation_label = sender.text()
        if state == 2:
            self.selectedPunctuation[punctuation_label.split()[0]] = self.punctuation[punctuation_label.split()[0]]
        else:
            if punctuation_label in self.selectedPunctuation:
                del self.selectedPunctuation[punctuation_label]
        print(f"Selected Punctuation: {self.selectedPunctuation}")
    
    def select_all_punctuation(self, state):
        # If "Select All" is checked, select all individual checkboxes
        if state == 2:
            for checkbox in self.checkboxes.values():
                checkbox.setChecked(True)
        else:
            for checkbox in self.checkboxes.values():
                checkbox.setChecked(False)

    def submit_data(self):
        print("Submitting data...")
        print(f"File selected: {self.label.text()}")
        print(f"Language: {self.selectedLanguage}")
        print(f"Selected Punctuation: {self.selectedPunctuation}")
    
    def exit_application(self):
        print("Exiting application...")
        self.close()

        
def main():
    app = QApplication([])
    window = App()
    window.show()
    app.exec()

if __name__ == '__main__':
    print('Running the app...')
    main()
    print('App terminated...')

# prida visualizacia, vyber zobrazeni, aj do GUI
# refaktorovanie kodu
# fixnutie select all checkbox, aby sa uncheckoval
# namiesto printov aj premenne menit