import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QKeySequence

from mini_editor.editor import Editor

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    editor = Editor(window.setWindowTitle)
    window.setCentralWidget(editor)

    new_action = QtWidgets.QAction(window, text="New.")
    new_action.setShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_N))
    new_action.triggered.connect(editor.new_fn)

    open_action = QtWidgets.QAction(window, text="Open")
    open_action.setShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_O))
    open_action.triggered.connect(editor.open_fn)

    save_action = QtWidgets.QAction(window, text="Save")
    save_action.setShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S))
    save_action.triggered.connect(editor.save_fn)

    save_as_action = QtWidgets.QAction(window, text="Save As")
    save_as_action.setShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_S))
    save_as_action.triggered.connect(editor.save_as_fn)

    exit_action = QtWidgets.QAction(window, text="Exit")
    exit_action.setShortcut(QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_X))
    exit_action.triggered.connect(lambda: sys.exit(0))

    compile_action = QtWidgets.QAction(window, text="Compile")
    compile_action.setShortcut(QKeySequence(QtCore.Qt.Key_F9))
    compile_action.triggered.connect(editor.compile_fn)

    run_action = QtWidgets.QAction(window, text="Run")
    run_action.setShortcut(QKeySequence(QtCore.Qt.Key_F10))
    run_action.triggered.connect(editor.run_fn)

    bar = window.menuBar()
    file_menu = bar.addMenu("&File")
    file_menu.addAction(new_action)
    file_menu.addAction(open_action)
    file_menu.addAction(save_action)
    file_menu.addAction(save_as_action)
    file_menu.addAction(exit_action)

    option_menu = bar.addMenu("&Options")
    option_menu.addAction(compile_action)
    option_menu.addAction(run_action)

    window.setWindowTitle("New.")
    window.resize(800, 500)
    window.show()

    sys.exit(app.exec_())
