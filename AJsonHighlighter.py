from PyQt6.QtWidgets import *
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor

class AJsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#008000"))
        
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor("#0000FF"))
        
        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor("#000000"))
        
        self.key_format = QTextCharFormat()
        self.key_format.setForeground(QColor("#800000"))

    def highlightBlock(self, text):
        in_string = False
        start = 0
        
        for i, char in enumerate(text):
            if char == '"':
                if not in_string:
                    start = i
                    in_string = True
                else:
                    length = i - start + 1
                    if ':' in text[i:i+2]:
                        self.setFormat(start, length, self.key_format)
                    else:
                        self.setFormat(start, length, self.string_format)
                    in_string = False
            elif char in '[]{}':
                self.setFormat(i, 1, self.bracket_format)
            elif char.isdigit() or char in '.-':
                if i == 0 or not text[i-1].isalnum():
                    j = i
                    while j < len(text) and (text[j].isdigit() or text[j] in '.-'):
                        j += 1
                    if text[i:j].replace('.', '').replace('-', '').isdigit():
                        self.setFormat(i, j-i, self.number_format)
                        