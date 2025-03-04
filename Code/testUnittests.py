import unittest
import main

class TestreadTextFile(unittest.TestCase):
    def testReadFile(self):
        self.assertEqual(main.readTextFile('Code\inputTextFiles\oneLineNoPunct.txt'), \
                         'In the afternoon we saw what was supposed to be a rock')

class TestProcessTextFile(unittest.TestCase):
    def testEmptyStringFP(self):
        self.assertEqual(main.processTextFile('', False), [])
    
    def testEmptyStringTP(self):
        self.assertEqual(main.processTextFile('', True), [])
    
    def testOneWordFP(self):
        self.assertEqual(main.processTextFile('word', False), ['word'])
    
    def testOneWordTP(self):
        self.assertEqual(main.processTextFile('word', True), ['word'])

    def testSentenceNoPunctFP(self):
        self.assertEqual(main.processTextFile('In the afternoon we saw what was supposed to be a rock', False), \
                         ['in', 'the', 'afternoon', 'we', 'saw', 'what', 'was', 'supposed', 'to', 'be', 'a', 'rock'])
    
    def testSentenceNoPunctTP(self):
        self.assertEqual(main.processTextFile('In the afternoon we saw what was supposed to be a rock', True), \
                         ['in', 'the', 'afternoon', 'we', 'saw', 'what', 'was', 'supposed', 'to', 'be', 'a', 'rock'])
    
    def testIgnorePunct(self):
        self.assertEqual(main.processTextFile('"Hi, How are: you?"', False), ['hi', 'how', 'are', 'you'])
    
    def testDot(self):
        self.assertEqual(main.processTextFile('TesTinG. TeStIng.', True), ['testing', '.', 'testing', '.'])
    
    def testComma(self):
        self.assertEqual(main.processTextFile('TesTinG, TeStIng', True), ['testing', ',', 'testing'])
    
    def testQuestionMark(self):
        self.assertEqual(main.processTextFile('QuestionMark? QuestionMark?', True), ['questionmark', '?', 'questionmark', '?'])
    
    def testExclamationMark(self):
        self.assertEqual(main.processTextFile('ExclamationMark! ExclamationMark!', True), ['exclamationmark', '!', 'exclamationmark', '!'])
    
    def testSemicolon(self):
        self.assertEqual(main.processTextFile('Semicolon; Semicolon;', True), ['semicolon', ';', 'semicolon', ';'])
    
    def testColon(self):
        self.assertEqual(main.processTextFile('Colon: Colon:', True), ['colon', ':', 'colon', ':'])
    
    def testParentheses(self):
        self.assertEqual(main.processTextFile('Parentheses (Parentheses)', True), ['parentheses', '(', 'parentheses', ')'])
    
    def testThreeDots(self):
        self.assertEqual(main.processTextFile('ThreeDots... ThreeDots...', True), ['threedots', '...', 'threedots', '...'])
    
    def testUnderscore(self):
        self.assertEqual(main.processTextFile('Under_score Under_score', True), ['under_score', 'under_score'])
    
    def testHyphen(self):
        self.assertEqual(main.processTextFile('Hyphen-hyphen Hyphen-hyphen', True), ['hyphen', '-', 'hyphen', 'hyphen', '-', 'hyphen'])
    
    def testApostrophe(self):
        self.assertEqual(main.processTextFile("Apostrophe's Apostrophe's", True), ['apostrophe', "'", 's', 'apostrophe', "'", 's'])
    
    def testQuotationMarks(self):
        self.assertEqual(main.processTextFile('"QuotationMarks", "QuotationMarks"', True), ['"', 'quotationmarks', '"', ',', '"', 'quotationmarks', '"'])
    
    def testNumbersComma(self):
        self.assertEqual(main.processTextFile('Number 1,20375', True), ['number', '1', ',', '20375'])
    
    def testNumbersDot(self):
        self.assertEqual(main.processTextFile('Number 723.97', True), ['number', '723', '.', '97'])
    
    def testNumbersSlash(self):
        self.assertEqual(main.processTextFile('Number 13/21', True), ['number', '13', '/', '21'])

    def testMultiplePunct(self):
        self.assertEqual(main.processTextFile('MultiplePunct. MultiplePunct.', True), ['multiplepunct', '.', 'multiplepunct', '.'])
    
    def testMultiplePunct2(self):
        self.assertEqual(main.processTextFile('MultiplePunct! MultiplePunct!', True), ['multiplepunct', '!', 'multiplepunct', '!'])
    
    def testMultiplePunct3(self):
        self.assertEqual(main.processTextFile('MultiplePunct? MultiplePunct?', True), ['multiplepunct', '?', 'multiplepunct', '?'])
    

        
if __name__ == '__main__':
    unittest.main()