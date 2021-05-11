import re
import time

from PyQt5 import QtWidgets, QtGui, QtCore, uic

from asrInterface import Ui_MainWindow
import sys
import threading
import win32api

import speech_recognition as sr


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.recognize_btn.clicked.connect(self.listen_thread)
        self.ui.text_box.returnPressed.connect(self.text_thread)

    def text_thread(self):
        t = threading.Thread(target=self.text)
        t.setDaemon(True)
        t.start()

    def text(self):
        content = self.ui.text_box.text()

        Instruction = ["music", "text", "calculator"]

        instruction_play_music = re.search(Instruction[0].lower(), content.lower())
        instruction_open_text_file = re.search(Instruction[1].lower(), content.lower())
        instruction_calculator = re.search(Instruction[2].lower(), content.lower())

        if instruction_play_music:
            self.ui.label.setText("Play Music!")
            win32api.ShellExecute(0, 'open', 'E:\\song.wma', '', '', 1)
        elif instruction_open_text_file:
            self.ui.label.setText("Open Text")
            win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 0)
        elif instruction_calculator:
            self.ui.label.setText("Calculator")
            win32api.ShellExecute(0, 'open', 'calc.exe', '', '', 0)
        else:
            self.ui.label.setText("I have no idea...")


    def listen_thread(self):
        self.ui.label.setText("I'm listening......")
        t = threading.Thread(target=self.listen)
        t.setDaemon(True)
        t.start()

    def listen(self):
        mic = sr.Recognizer()
        with sr.Microphone() as source:
            audio = mic.listen(source)

        try:
            content = mic.recognize_sphinx(audio)
        except sr.RequestError:
            self.ui.label.setText("Error!")

        Instruction = ["music", "text", "calculator"]

        instruction_play_music = re.search(Instruction[0].lower(), content.lower())
        instruction_open_text_file = re.search(Instruction[1].lower(), content.lower())
        instruction_calculator = re.search(Instruction[2].lower(), content.lower())

        if instruction_play_music:
            self.ui.label.setText("Playing Music!")
            win32api.ShellExecute(0, 'open', 'E:\\song.wma', '', '', 1)
        elif instruction_open_text_file:
            self.ui.label.setText("Opening Text")
            win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 0)
        elif instruction_calculator:
            self.ui.label.setText("Opening Calculator")
            win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 0)
        else:
            print(content)
            self.ui.label.setText("I have no idea...")

        time.sleep(2.1)
        self.ui.label.setText("How can i help you?")


app = QtWidgets.QApplication([])
application = myWindow()
application.show()
sys.exit(app.exec())

