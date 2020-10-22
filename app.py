import sys

from PySide2 import QtWidgets

from mini_editor.editor import Editor

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    e = Editor()
    e.setWindowTitle("New.")
    e.resize(800, 500)
    e.show()

    sys.exit(app.exec_())
