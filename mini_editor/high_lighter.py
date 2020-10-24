from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import QSyntaxHighlighter, QFont, QColor
import re


# https://github.com/baoboa/pyqt5/blob/master/examples/richtext/syntaxhighlighter.py
# https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
# https://www.color-hex.com/color-palettes/
# https://www.canva.com/learn/100-color-combinations/

class HighLighter(QSyntaxHighlighter):

    def __init__(self, parent: QtWidgets.QTextEdit):
        super().__init__(parent)

        self.formats = []

        bracket_format = QtGui.QTextCharFormat()
        bracket_format.setForeground(QtGui.QBrush(QColor("#07689f")))

        digit_format = QtGui.QTextCharFormat()
        digit_format.setForeground(QtGui.QBrush(QColor("orange")))
        digit_format.setFontWeight(QFont.Bold)

        single_line_comment = QtGui.QTextCharFormat()
        single_line_comment.setForeground(QtGui.QBrush(QColor("green")))

        include_format = QtGui.QTextCharFormat()
        include_format.setForeground(QtGui.QBrush(QColor("darkred")))
        include_format.setFontWeight(QFont.Bold)

        string_format = QtGui.QTextCharFormat()
        string_format.setForeground(QtGui.QBrush(QColor("red")))

        key_words = QtGui.QTextCharFormat()
        key_words.setForeground(QtGui.QBrush(QColor("blue")))
        key_words.setFontWeight(QFont.Bold)

        self.formats.append([bracket_format, re.compile("[\\[\\](){};]")])
        self.formats.append([digit_format, re.compile("[0-9]")])
        self.formats.append([key_words, re.compile("\\b(auto|break|case|char|const|"
                                                   "continue|default|do|double|"
                                                   "else|enum|extern|float|for|goto|"
                                                   "if|int|long|register|return|short|"
                                                   "signed|sizeof|static|struct|switch|"
                                                   "typedef|union|unsigned|void|volatile|while)\\b")])
        self.formats.append([include_format, re.compile("^#include<.*>")])
        self.formats.append([string_format, re.compile("\".*\"")])
        self.formats.append([single_line_comment, re.compile("//.*")])

    def highlightBlock(self, text):
        # print(f"Text=[{text}]")
        for format, regex in self.formats:
            for matched in regex.finditer(text):
                start, end = matched.span()
                span_len = end - start
                self.setFormat(start, span_len, format)
        self.setCurrentBlockState(0)
