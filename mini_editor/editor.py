import os

from PySide2 import QtWidgets, QtGui
from PySide2.QtGui import QFont

from mini_editor.shell import c_compile, c_run
from mini_editor.high_lighter import HighLighter


class Editor(QtWidgets.QWidget):

    def __init__(self, set_title_function):
        super().__init__()
        self.set_title_function = set_title_function

        l = QtWidgets.QVBoxLayout()

        self.edit = QtWidgets.QTextEdit()
        edit_font = QFont()
        edit_font.setFamily('Courier')
        edit_font.setPointSizeF(11)
        self.edit.setStyleSheet("background-color: black; color:white;")
        self.edit.setFont(edit_font)
        l.addWidget(self.edit)

        self.high_lighter = HighLighter(self.edit)

        self.logs = QtWidgets.QTextEdit()
        log_font = QFont()
        log_font.setFamily('Helvetica')
        log_font.setPointSizeF(10)
        self.logs.setFont(log_font)
        self.logs.setMaximumHeight(200)
        l.addWidget(self.logs)

        self.setLayout(l)
        self.current_file = None
        self.new_fn()

    def new_fn(self):
        self.edit.clear()
        self.set_title("New.")
        self.current_file = None

    def set_title(self, arg__1: str):
        self.set_title_function(f"MiniEditor : [{arg__1}]")

    def get_selected_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        if file_dialog.exec_():
            return file_dialog.selectedFiles()[0]
        return None

    def open_fn(self):
        print("Open clicked.")
        file_path = self.get_selected_file()
        if file_path:
            with open(file_path, mode='r') as open_file:
                text = open_file.read()
                self.edit.setText(text)
                self.current_file = file_path
                self.set_title(self.current_file)

    def save_fn(self):
        if self.current_file is None:
            self.save_as_fn()
        else:
            with open(self.current_file, mode='w') as write_file:
                write_file.write(self.edit.toPlainText())

    def save_as_fn(self):
        file_path = self.get_selected_file()
        if file_path:
            self.current_file = file_path
            self.set_title(self.current_file)
            with open(self.current_file, mode='w') as write_file:
                write_file.write(self.edit.toPlainText())

    def compile_fn(self):
        self.logs.append("[Compilation] ......")
        return_code, output, error = c_compile(self.edit.toPlainText())
        self.logs.append(f"Return code:{return_code}")
        self.logs.append(error)
        self.logs.moveCursor(QtGui.QTextCursor.End)

    def run_fn(self):
        print("run.")
        if os.path.exists("a.exe"):
            c_run(["start", "a.exe"])
        else:
            print("Unable to find a.exe, please compile first.")
