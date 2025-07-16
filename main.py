#deneme satırı

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPlainTextEdit, QMainWindow,
    QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy,QGridLayout,QAction
)
from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QMouseEvent
import sys
from PyQt5.QtGui import QPainter, QColor, QFont, QMouseEvent, QTextFormat

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
import parser
from register_window import *
from code_editor_area import *

from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QFileDialog
import micro_processor



from PyQt5.QtCore import QThread, pyqtSignal
import time

running = False

class Worker(QThread):
    update_signal = pyqtSignal()  # GUI'ye sayı göndermek için
    
    def run(self):
        global running
        while running:
            time.sleep(0.001)
            self.update_signal.emit()



class LedPanel(QWidget):
    def __init__(self, led_states):
        super().__init__()
        self.led_states = led_states  # dışardan referans alınır (liste)

    def paintEvent(self, event):
        painter = QPainter(self)
        radius = 15
        spacing = 10
        offset_x = 20
        offset_y = 20

        for i in range(16):
            col = i // 8  # 0 veya 1
            row = i % 8

            x = offset_x + col * (2 * radius + spacing)
            y = offset_y + row * (2 * radius + spacing)

            color = QColor("red") if self.led_states[i] else QColor("lightgray")
            painter.setBrush(color)
            painter.setPen(Qt.black)
            painter.drawEllipse(x, y, 2 * radius, 2 * radius)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microcontroller Simulator")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #layout = QVBoxLayout()
        main_layout = QVBoxLayout()
        #layout = QGridLayout(3,0)
        
        

        central_widget.setLayout(main_layout)

        self.button_layout = QHBoxLayout()



        self.debug_button = QPushButton("Debug")
        self.debug_button.setFixedWidth(100)
        self.debug_button.clicked.connect(self.debug_function)
        self.button_layout.addWidget(self.debug_button)
        
        
        
        self.quit_debug = QPushButton("quit debug")
        self.quit_debug.setFixedWidth(100)
        self.quit_debug.clicked.connect(self.quit_debug_btn_function)
        self.button_layout.addWidget(self.quit_debug)
        self.quit_debug.hide()
        



        self.run_btn = QPushButton("Run")
        #self.step_button.setIcon(QIcon("icons/step.png"))  # 🔍 resim yolu
        self.run_btn.clicked.connect(self.run_btn_function)
        self.run_btn.setFixedWidth(100)
        self.run_btn.hide()
        self.button_layout.addWidget(self.run_btn)

        self.stop_btn = QPushButton("Stop")
        #self.step_button.setIcon(QIcon("icons/step.png"))  # 🔍 resim yolu
        self.stop_btn.clicked.connect(self.stop_btn_function)
        self.stop_btn.setFixedWidth(100)
        self.stop_btn.hide()
        self.button_layout.addWidget(self.stop_btn)





        self.step_btn = QPushButton("step")
        self.step_btn.clicked.connect(self.step_run_btn_funtion)
        self.step_btn.setFixedWidth(100)
        self.step_btn.hide()
        self.button_layout.addWidget(self.step_btn)

        self.goto_break_point_btn = QPushButton("gbp")
        self.goto_break_point_btn.clicked.connect(self.debug_function)
        self.goto_break_point_btn.setFixedWidth(100)
        self.goto_break_point_btn.hide()
        self.button_layout.addWidget(self.goto_break_point_btn)




        self.button_layout.addStretch()  # sona eklenirse elemanlar sola yaslanır
        main_layout.addLayout(self.button_layout)
        



        code_and_registers_layout =  QHBoxLayout()

        self.editor = CodeEditor()
        code_and_registers_layout.addWidget(self.editor)

        self.registers = micro_processor.registers


        self.register_info_area = RegisterWindow(self.registers)
        
        register_and_leds_layout = QHBoxLayout()
        
        self.led_states = [False] * 16
        self.led_panel = LedPanel(self.led_states)
        self.led_panel.setFixedSize(100, 400)  # boyut ayarı

        # Layout'a ekle

        register_and_leds_layout.addWidget(self.register_info_area)
        register_and_leds_layout.addWidget(self.led_panel)


        code_and_registers_layout.addLayout(register_and_leds_layout)



        main_layout.addLayout(code_and_registers_layout)





        menubar = self.menuBar()

        # "Dosya" menüsü
        file_menu = menubar.addMenu("Dosya")

        # Dosya Aç
        open_action = QAction("Dosya Aç", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Kaydet
        save_action = QAction("Kaydet", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Farklı Kaydet
        save_as_action = QAction("Farklı Kaydet", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        # Çıkış
        exit_action = QAction("Çıkış", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)



        
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Metin Dosyaları (*.txt *.asm *.c);;Tüm Dosyalar (*)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.editor.setPlainText(content)
                self.current_file = path  # Dosya yolunu kaydet

    def save_file(self):
        try:
            if hasattr(self, 'current_file'):
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.editor.toPlainText())
            else:
                self.save_file_as()
        except Exception as e:
            print("Kaydetme hatası:", e)

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Farklı Kaydet", "", "Metin Dosyaları (*.txt *.asm *.c);;Tüm Dosyalar (*)")
        if path:
            self.current_file = path
            self.save_file()
    

    def execute_one_step(self):
        pc = self.registers["pc"]
        self.registers["pc"] = pc+1
        parser.execute(parser.code_list[pc].line_text,self.registers,micro_processor.stack,micro_processor.memory)
        self.register_info_area.update_table()
        led_values = bin((self.registers['&p1dir'] %256+256) & (self.registers['&p1out'] %256 + 256))
        for i in range(len(led_values)):
            if i>2:
                self.led_states[i-3] = True if led_values[i] == '1' else False
        
        led_values = bin((self.registers['&p2dir'] %256+256) & (self.registers['&p2out'] %256 + 256))    
        for i in range(len(led_values)):
            if i>2:
                self.led_states[i-3+8] = True if led_values[i] == '1' else False
        
        self.led_panel.repaint()


    def debug_function(self):
        print("debug moduna geçioz")
        self.debug_button.hide()
        self.quit_debug.show()
        self.run_btn.show()
        self.step_btn.show()
        self.goto_break_point_btn.show()
      
        text = self.editor.toPlainText()
        parser.convert_execution_list(text)
        parser.find_labels(parser.code_list,micro_processor.memory)
        self.register_info_area.update_table()
        #self.led_panel.led_states = [False]*16
        self.led_panel.repaint()

        
    
    def quit_debug_btn_function(self):
        global running
        running = False
        self.debug_button.show()
        self.quit_debug.hide()
        self.run_btn.hide()
        self.step_btn.hide()
        self.goto_break_point_btn.hide()
        self.stop_btn.hide()

    
    def step_run_btn_funtion(self):
        self.execute_one_step()
        self.editor.line_number_area.update()
    
    def run_btn_function(self):
        self.worker = Worker()
        
        self.stop_btn.show()
        self.run_btn.hide()
        self.step_btn.hide()
        self.goto_break_point_btn.hide()

        global running
        if running == False:
            running = True    
            self.worker.update_signal.connect(self.step_run_btn_funtion)  # Label'a sayı yaz
            self.worker.start()

    def stop_btn_function(self):
        global running
        running = False
        self.run_btn.show()
        self.step_btn.show()
        self.goto_break_point_btn.show()
        self.stop_btn.hide()
     
  
        
    
            




        






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(700, 500)
    window.show()
    sys.exit(app.exec_())
