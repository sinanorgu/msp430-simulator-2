from PyQt5.QtWidgets import (
     QWidget, QPlainTextEdit
)
from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtGui import QPen

from PyQt5.QtWidgets import QWidget


from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import QStringListModel
from highlighter import *
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
import micro_processor
import parser

breakpoints  = set()



class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)

    def mousePressEvent(self, event: QMouseEvent):
        block = self.code_editor.firstVisibleBlock()
        top = self.code_editor.blockBoundingGeometry(block).translated(self.code_editor.contentOffset()).top()
        line_number = block.blockNumber()
        click_y = event.pos().y()

        while block.isValid():
            bottom = top + self.code_editor.blockBoundingRect(block).height()

            if top <= click_y <= bottom:
                if line_number in self.code_editor.breakpoints:
                    self.code_editor.breakpoints.remove(line_number)
                else:
                    self.code_editor.breakpoints.add(line_number)
                self.code_editor.viewport().update()
                self.code_editor.line_number_area.update() # I added this line to get instant result for breakpoint visulation

                break
           

            block = block.next()
            top = bottom
            line_number += 1

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        global breakpoints
        self.breakpoints = breakpoints
        self.highlighter = SimpleHighlighter(self.document())
        self.current_executing_line = -1

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        #self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        #self.highlight_current_line()


        keywords = parser.instruction_set[:]
        keywords.extend(list(micro_processor.registers.keys()))
        print(keywords)

        self.completer = QCompleter(keywords)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)


    def line_number_area_width(self):
        digits = len(str(self.blockCount()))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits + 16

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        try:
            self.current_executing_line = parser.code_list[micro_processor.registers['pc']].line_number
        except:
            pass



        micro_processor.registers['pc']
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, int(top), self.line_number_area.width() - 4,
                                 int(self.fontMetrics().height()),
                                 Qt.AlignRight, number)

                if block_number in self.breakpoints:
                    radius = 6
                    center_x = 8
                    center_y = int(top + self.fontMetrics().height() / 2)
                    painter.setBrush(Qt.red)
                    painter.setPen(Qt.red)
                    painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

                if block_number == self.current_executing_line: 
                    center_x = 5
                    center_y = int(top + self.fontMetrics().height() / 2)
                   
                    painter.setBrush(Qt.blue)
                    painter.setPen(Qt.blue)
                    
                                        
                    pen = QPen(Qt.blue)
                    pen.setWidth(3)  # Kalınlığı artır
                    painter.setPen(pen)

                    #painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
                    painter.drawLine(center_x,center_y,center_x+10,center_y)
                    pen.setWidth(2)
                    painter.drawLine(center_x+10,center_y,center_x+7,center_y-5)
                    painter.drawLine(center_x+10,center_y,center_x+7,center_y+5)
                    
                    




            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def insert_completion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(tc.Left, tc.MoveAnchor, len(self.completer.completionPrefix()))
        for i in range( len(self.completer.completionPrefix())):
            tc.deleteChar()
        tc.insertText(completion)
        
        self.setTextCursor(tc)

    def keyPressEvent(self, event):
        if self.completer.popup().isVisible():
            # Enter, Return, Tab tuşu -> tamamlamayı tetikle
            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                selected_index = self.completer.popup().currentIndex()
                if selected_index.isValid():
                    completion = selected_index.data(Qt.EditRole)
                    self.insert_completion(completion)
                self.completer.popup().hide()
                return  # Editöre normal tuş gönderme, çünkü tamamladık

            # Escape tuşu ile popup'ı kapatma
            elif event.key() == Qt.Key_Escape:
                self.completer.popup().hide()
                return

        # Varsayılan davranış
        super().keyPressEvent(event)

        # Mevcut kelimeyi al ve eşleşme ara
        tc = self.textCursor()
        tc.select(tc.WordUnderCursor)
        prefix = tc.selectedText()

        if prefix != '':
            self.completer.setCompletionPrefix(prefix)
            self.completer.popup().setCurrentIndex(
                self.completer.completionModel().index(0, 0)
            )
            cr = self.cursorRect()
            cr.setWidth(
                self.completer.popup().sizeHintForColumn(0)
                + self.completer.popup().verticalScrollBar().sizeHint().width()
            )
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()



    """ def highlight_current_line(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)


        self.setExtraSelections(extraSelections)
 """
