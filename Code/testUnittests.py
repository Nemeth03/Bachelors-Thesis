import unittest
import main

class TestreadTextFile(unittest.TestCase):
    def testReadFile(self):
        self.assertEqual(main.readTextFile('Code\inputTextFiles\oneLineNoPunct.txt'),
                         'In the afternoon we saw what was supposed to be a rock')

class TestProcessTextFile(unittest.TestCase):
    def testEmptyStringFP(self):
        self.assertEqual(main.processTextFile('', False, main.allPunctuation, True), [])
    
    def testEmptyStringTP(self):
        self.assertEqual(main.processTextFile('', True, main.allPunctuation, True), [])
    
    def testOneWordFP(self):
        self.assertEqual(main.processTextFile('word', False, main.allPunctuation, True), ['word'])
    
    def testOneWordTP(self):
        self.assertEqual(main.processTextFile('word', True, main.allPunctuation, True), ['word'])

    def testSentenceNoPunctFP(self):
        self.assertEqual(main.processTextFile('In the afternoon we saw what was supposed to be a rock', False, main.allPunctuation, True),
                         ['in', 'the', 'afternoon', 'we', 'saw', 'what', 'was', 'supposed', 'to', 'be', 'a', 'rock'])
    
    def testSentenceNoPunctTP(self):
        self.assertEqual(main.processTextFile('In the afternoon we saw what was supposed to be a rock', True, main.allPunctuation, True),
                         ['in', 'the', 'afternoon', 'we', 'saw', 'what', 'was', 'supposed', 'to', 'be', 'a', 'rock'])
    
    def testIgnorePunctFP(self):
        self.assertEqual(main.processTextFile('"Hi, How are: you?"', False, main.allPunctuation, True), 
                         ['hi', 'how', 'are', 'you'])
    
    def testDotTP(self):
        self.assertEqual(main.processTextFile('TesTinG. TeStIng.', True, main.allPunctuation, True), ['testing', '.', 'testing', '.'])
    
    def testCommaTP(self):
        self.assertEqual(main.processTextFile('TesTinG, TeStIng', True, main.allPunctuation, True), ['testing', ',', 'testing'])
    
    def testQuestionMarkTP(self):
        self.assertEqual(main.processTextFile('QuestionMark? QuestionMark?', True, main.allPunctuation, True),
                         ['questionmark', '?', 'questionmark', '?'])
    
    def testExclamationMarkTP(self):
        self.assertEqual(main.processTextFile('ExclamationMark! ExclamationMark!', True, main.allPunctuation, True),
                         ['exclamationmark', '!', 'exclamationmark', '!'])
    
    def testSemicolonTP(self):
        self.assertEqual(main.processTextFile('Semicolon; Semicolon;', True, main.allPunctuation, True), 
                         ['semicolon', ';', 'semicolon', ';'])
    
    def testColonTP(self):
        self.assertEqual(main.processTextFile('Colon: Colon:', True, main.allPunctuation, True), ['colon', ':', 'colon', ':'])
    
    def testParenthesesTP(self):
        self.assertEqual(main.processTextFile('Parentheses (Parentheses)', True, main.allPunctuation, True), 
                         ['parentheses', '(', 'parentheses', ')'])
    
    def testThreeDotsTP(self):
        self.assertEqual(main.processTextFile('ThreeDots... ThreeDots...', True, main.allPunctuation, True), 
                         ['threedots', '...', 'threedots', '...'])
    
    def testUnderscoreTP(self):
        self.assertEqual(main.processTextFile('Under_score Under_score', True, main.allPunctuation, True), 
                         ['under', '_', 'score', 'under', '_', 'score'])
    
    def testHyphenTP(self):
        self.assertEqual(main.processTextFile('Hyphen-hyphen Hyphen-hyphen', True, main.allPunctuation, True), 
                         ['hyphen', '-', 'hyphen', 'hyphen', '-', 'hyphen'])
    
    def testApostropheTP(self):
        self.assertEqual(main.processTextFile("Apostrophe's Apostrophe's", True, main.allPunctuation, True), 
                         ['apostrophe', "'", 's', 'apostrophe', "'", 's'])
    
    def testQuotationMarksTP(self):
        self.assertEqual(main.processTextFile('"QuotationMarks", "QuotationMarks"', True, main.allPunctuation, True), 
                         ['"', 'quotationmarks', '"', ',', '"', 'quotationmarks', '"'])
    
    def testNumbersCommaTP(self):
        self.assertEqual(main.processTextFile('Number 1,20375', True, main.allPunctuation, True), 
                         ['number', '1', ',', '20375'])
    
    def testNumbersDotTP(self):
        self.assertEqual(main.processTextFile('Number 723.97', True, main.allPunctuation, True), 
                         ['number', '723', '.', '97'])
    
    def testNumbersSlashTP(self):
        self.assertEqual(main.processTextFile('Number 13/21', True, main.allPunctuation, True), 
                         ['number', '13', '/', '21'])

    def testMultiplePunct1(self):
        self.assertEqual(main.processTextFile('"Wait... did you see that?" she asked.', True, main.allPunctuation, True), 
                         ['"', 'wait', '...', 'did', 'you', 'see', 'that', '?', '"', 'she', 'asked', '.'])
    
    def testMultiplePunct2(self):
        self.assertEqual(main.processTextFile('Also, file paths use slashes, like "C:/Users/John_Doe/".', True, main.allPunctuation, True), 
                         ['also', ',', 'file', 'paths', 'use', 'slashes', ',', 'like', '"', 'c', ':', '/', 'users', '/', 'john', '_', 'doe', '/', '"', '.'])
    
    def testCaseSensitiveIgnorePunct(self):
        self.assertEqual(main.processTextFile('Also, file paths use slashes, like "C:/Users/John_Doe/".', False, main.allPunctuation, False), 
                         ['Also', 'file', 'paths', 'use', 'slashes', 'like', 'C', 'Users', 'John', 'Doe'])
    
    def testPunctuationSelection1(self):
        self.assertEqual(main.processTextFile('[brackets], \{braces\}, and (parentheses)—all in one place!', True, ['brackets', 'comma'], True),
                         ['[', 'brackets', ']', ',', 'braces', ',', 'and', 'parentheses', 'all', 'in', 'one', 'place'])
    
    def testPunctuationSelection2(self):
        self.assertEqual(main.processTextFile('[brackets], \{braces\}, and (parentheses)—all in one place!', True, ['braces', 'emDash'], True),
                         ['brackets', '{', 'braces', '}', 'and', 'parentheses', '—', 'all', 'in', 'one', 'place'])
    

if __name__ == '__main__':
    unittest.main()