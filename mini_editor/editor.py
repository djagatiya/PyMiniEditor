import os

from PySide2 import QtWidgets
from mini_editor.shell import c_compile, c_run


class Editor(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        l = QtWidgets.QVBoxLayout()

        top_view = QtWidgets.QWidget()
        top_view_layout = QtWidgets.QHBoxLayout()
        top_view.setLayout(top_view_layout)

        b1 = QtWidgets.QPushButton("New.")
        b1.clicked.connect(self.new_fn)
        b2 = QtWidgets.QPushButton("Open")
        b2.clicked.connect(self.open_fn)
        b3 = QtWidgets.QPushButton("Save")
        b3.clicked.connect(self.save_fn)
        b4 = QtWidgets.QPushButton("Save As.")
        b4.clicked.connect(self.save_as_fn)
        b5 = QtWidgets.QPushButton("Compile")
        b5.clicked.connect(self.compile_fn)
        b6 = QtWidgets.QPushButton("Run")
        b6.clicked.connect(self.run_fn)

        top_view_layout.addWidget(b1)
        top_view_layout.addWidget(b2)
        top_view_layout.addWidget(b3)
        top_view_layout.addWidget(b4)
        top_view_layout.addWidget(b5)
        top_view_layout.addWidget(b6)
        top_view_layout.addStretch()

        l.addWidget(top_view)

        self.edit = QtWidgets.QTextEdit()
        l.addWidget(self.edit)

        self.logs = QtWidgets.QTextEdit()
        self.logs.setMaximumHeight(200)
        l.addWidget(self.logs)

        self.setLayout(l)
        self.current_file = None

    def new_fn(self):
        self.edit.clear()
        self.setWindowTitle("New.")
        self.current_file = None

    def setWindowTitle(self, arg__1: str):
        super().setWindowTitle(f"MiniEditor : [{arg__1}]")

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
                self.setWindowTitle(self.current_file)

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
            self.setWindowTitle(self.current_file)
            with open(self.current_file, mode='w') as write_file:
                write_file.write(self.edit.toPlainText())

    def compile_fn(self):
        returncode, output, error = c_compile(self.edit.toPlainText())
        self.logs.append(error)
        self.logs.append("------------------------------------------")

    def run_fn(self):
        print("run.")
        if os.path.exists("./a.exe"):
            c_run(["start", "./a.exe"])
        else:
            print("Unable to find a.exe, please compile first.")
