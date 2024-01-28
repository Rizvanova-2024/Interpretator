# https://github.com/art1415926535/PyQt5-syntax-highlighting/tree/master
from PyQt5 import QtWidgets

import sys
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format

STYLES = {
    'keyword1': format([86 , 156, 214]),
    'keyword2': format([78 , 201, 176]),
    'comment' : format([87 , 136, 41 ]),
    'numbers' : format([156, 220, 254]),
}

class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # GridMaster keywords
    keywords1 = ['RIGHT', 'LEFT', 'UP', 'DOWN', 'SET', 'CALL']
    keywords2 = ['IFBLOCK', 'ENDIF', 'REPEAT', 'ENDREPEAT', 'PROCEDURE', 'ENDPROC']

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        rules = []
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword1'])
                  for w in PythonHighlighter.keywords1]
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword2'])
                  for w in PythonHighlighter.keywords2]

        rules += [
            # Comments
            (r'#[^\n]*', 0, STYLES['comment']),
            # Numbers
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter.indexIn(text)
            add = delimiter.matchedLength()

        while start >= 0:
            end = delimiter.indexIn(text, start + add)
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            self.setFormat(start, length, style)
            start = delimiter.indexIn(text, start + length)

        if self.currentBlockState() == in_state:
            return True
        else:
            return False



class CodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, parent : QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.move(10, 60)
        self.resize(425, 425)

        self.setStyleSheet("""QPlainTextEdit{
	        font-family:'Consolas'; 
            font-size: 14px;
	        color: #c8bb97; 
	        background-color: #1e1e1e;}""")
        self.highlight = PythonHighlighter(self.document())
        self.show()

if __name__ == "__main__":
    print('This module can\'t be executed')
    exit(1)