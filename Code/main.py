# Visualization of the analysed data
class GraphVisualizer:
    def __init__(self):
        ...
    
    def plotLogLog(self):
        ...
    
    def plotLogLin(self):
        ...

# Tkinter GUI or PyQt6 GUI
class GUI:
    ...
    
# Main class that will run the app
class App:
    def __init__(self):
        self.inputTextFile = None
        self.textData = None
        self.graphVisualizer = None
        self.gui = None
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
    
    def readTextFile(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            return f.read().strip()
    
if __name__ == '__main__':
    print('Running the app...')