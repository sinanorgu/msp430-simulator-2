from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
import re
import parser
import micro_processor
class SimpleHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        # Anahtar kelimeler (renklenecek)
        instructions = parser.instruction_set
        instructions.extend([i.upper() for i in instructions])
        
        

        instructions_format = QTextCharFormat()
        instructions_format.setForeground(QColor(255,153,51))
        instructions_format.setFontWeight(QFont.Bold)

        register_names = list(micro_processor.registers.keys())
        register_names.extend([i.upper() for i in register_names])
        special_regs = ["p1out","p2out","p2in","p1in",'p1dir',"p2dir","P1OUT","P2OUT","P1IN","P2IN",'P1DIR',"P2DIR"]

        for i in special_regs:
            register_names.append(i)

        

        registers_format = QTextCharFormat()
        registers_format.setForeground(QColor(204,0,204))
        registers_format.setFontWeight(QFont.Bold)



        for word in instructions:
            pattern = r"\b" + word + r"\b"
            self.rules.append((re.compile(pattern), instructions_format))
        
        for word in register_names:
            pattern = r"\b" + word + r"\b"
            self.rules.append((re.compile(pattern), registers_format))
        

        # Yorumlar için (//...)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("gray"))
        comment_pattern = re.compile(r";.*")
        self.rules.append((comment_pattern, comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.start(), match.end()
                self.setFormat(start, end - start, fmt)
