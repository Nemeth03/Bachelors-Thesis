

class InputTextFile:
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        with open(self.filename, 'r', encoding="utf-8") as f:
            return f.read().strip()


class GraphVisualizer:
    def __init__(self, data):
        self.data = data

class GUI:
    ...
    
class App:
    ...
    
if __name__ == '__main__':

    print('Running the app...')
    slovakInput = InputTextFile('pribeh_sk.txt')
    englishInput = InputTextFile('pribeh_eng.txt')
    textSk = slovakInput.read()
    textEng = englishInput.read()