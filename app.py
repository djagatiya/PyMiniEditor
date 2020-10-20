import tkinter as tk

from mini_editor.editor import Editor

main_tk = tk.Tk()
main_tk.geometry("700x600")
Editor(main_tk)
main_tk.mainloop()
