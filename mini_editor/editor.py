import tkinter as tk
from tkinter import ttk
from mini_editor.shell import c_run, c_compile
from tkinter import filedialog


class Editor:

    def __init__(self, master: tk.Tk):
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=0)
        master.grid_rowconfigure(1, weight=6)
        master.grid_rowconfigure(2, weight=2)

        frame = tk.Frame(master, bg='red')
        frame.grid(row=0, column=0, sticky='nswe')

        ttk.Button(frame, text="New", command=self.new_fn).pack(side='left')
        ttk.Button(frame, text="Open", command=self.open_fn).pack(side='left')
        ttk.Button(frame, text="Save", command=self.save).pack(side='left')
        ttk.Button(frame, text="Save As.", command=self.save_as).pack(side='left')
        ttk.Button(frame, text="Run", command=self.run).pack(side='left')

        mid_frame = tk.Frame(master, bg='blue')
        mid_frame.grid(row=1, column=0, sticky='nswe')
        mid_frame.pack_propagate(0)

        bottom_frame = tk.Frame(master, bg='green')
        bottom_frame.grid(row=2, column=0, sticky='nswe')
        bottom_frame.pack_propagate(0)

        self.text = tk.Text(mid_frame)
        self.text.pack(fill='both', expand=True)

        self.logs = tk.Text(bottom_frame, font=('Helvetica', 10, 'bold'))
        self.logs.pack(fill='both', expand=True)

        self.file_path = None

    def new_fn(self):
        self.file_path = None
        self.text.delete("1.0", tk.END)

    def open_fn(self):
        file = filedialog.askopenfile()
        data = file.read()
        file.close()
        self.file_path = file.name
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", data)

    def get_all_text(self):
        return self.text.get("1.0", tk.END)

    def save_as(self):
        file = filedialog.asksaveasfile()
        file.write(self.get_all_text())
        file.close()
        self.file_path = file.name
        print(self.file_path)

    def save(self):
        if self.file_path is None:
            self.save_as()
        else:
            with open(self.file_path, mode="w") as out_file:
                out_file.write(self.get_all_text())

    def run(self):
        text_str = self.get_all_text()
        exit_code, out, error = c_compile(text_str)
        self.logs.insert(tk.END, "-------------------------------\n")
        self.logs.insert(tk.END, str(exit_code) + "\n")
        self.logs.insert(tk.END, out + "\n")
        self.logs.insert(tk.END, error + "\n")
        if exit_code == 0:
            c_run(["start", "./a.exe"])
        else:
            print("Error found..", exit_code)
