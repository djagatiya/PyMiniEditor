import tkinter as tk
from tkinter import ttk
from mini_editor.shell import c_run, c_compile
from tkinter import filedialog
from mini_editor.c_lexer import get_c_lexer
import json


class Editor:

    def __init__(self, master: tk.Tk):
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=0)
        master.grid_rowconfigure(1, weight=6)
        master.grid_rowconfigure(2, weight=2)

        self.master = master

        frame = tk.Frame(master, bg='red')
        frame.grid(row=0, column=0, sticky='nswe')

        ttk.Button(frame, text="New", command=self.new_fn).pack(side='left')
        ttk.Button(frame, text="Open", command=self.open_fn).pack(side='left')
        ttk.Button(frame, text="Save", command=self.save_fn).pack(side='left')
        ttk.Button(frame, text="Save As.", command=self.save_as_fn).pack(side='left')
        ttk.Button(frame, text="Compile", command=self.compile_fn).pack(side='left')
        ttk.Button(frame, text="Run", command=self.run_fn).pack(side='left')
        ttk.Button(frame, text="Highlights", command=self.highlights_fn).pack(side='left')

        mid_frame = tk.Frame(master, bg='blue')
        mid_frame.grid(row=1, column=0, sticky='nswe')
        mid_frame.pack_propagate(0)

        bottom_frame = tk.Frame(master, bg='green')
        bottom_frame.grid(row=2, column=0, sticky='nswe')
        bottom_frame.pack_propagate(0)

        self.text = tk.Text(mid_frame, bg='gray99')
        self.text.pack(fill='both', expand=True)

        self.mapping = {}
        with open("themes\\demo_theme.json") as style_file:
            json_data = json.load(style_file)
            for data in json_data["styles"]:
                print(data)
                name = data.get("lexer_name")
                if name is not None:
                    self.text.tag_configure(name, **data['data'])
                    self.mapping[name] = name
                else:
                    print("Lexer name not found:", data)

        self.logs = tk.Text(bottom_frame, font=('Helvetica', 10, 'bold'))
        self.logs.pack(fill='both', expand=True)

        self.file_path = None
        self.update_title()
        self.lexer = get_c_lexer()

    def update_title(self):
        path = "New File." if self.file_path is None else self.file_path
        self.master.title(f"MiniEditor : [{path}]")

    def new_fn(self):
        self.file_path = None
        self.text.delete("1.0", tk.END)
        self.update_title()

    def open_fn(self):
        file = filedialog.askopenfile()
        data = file.read()
        file.close()
        self.file_path = file.name
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", data)
        self.update_title()

    def get_all_text(self):
        return self.text.get("1.0", tk.END)

    def save_as_fn(self):
        file = filedialog.asksaveasfile()
        file.write(self.get_all_text())
        file.close()
        self.file_path = file.name
        print(self.file_path)
        self.update_title()

    def save_fn(self):
        if self.file_path is None:
            self.save_as_fn()
        else:
            with open(self.file_path, mode="w") as out_file:
                out_file.write(self.get_all_text())

    def run_fn(self):
        exit_code = self.compile_fn()
        if exit_code == 0:
            c_run(["start", "./a.exe"])
        else:
            print("Error found..", exit_code)

    def compile_fn(self):
        exit_code, out, error = c_compile(self.get_all_text())
        out_str = f"Exit Code: {exit_code}\n"
        if exit_code == 0:
            out_str += "[Success.]\n\n"
        else:
            if len(out) > 0:
                out_str += f"[Out]\n{out}\n"
            if len(error) > 0:
                out_str += f"[Error]{error}\n"
        self.logs.insert("end", out_str)
        return exit_code

    def highlights_fn(self):
        self.lexer.input(self.get_all_text())
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            self.apply_highlight(tok)

    def apply_highlight(self, tok):
        pos = tok.lexpos
        token_len = len(tok.value)
        token_type = tok.type
        pos_args = [f"1.0+{pos}c", f"1.0+{pos + token_len}c"]
        tag_name = self.mapping.get(token_type)
        if tag_name is not None:
            print(tag_name, tok)
            self.text.tag_add(tag_name, *pos_args)
        else:
            print("unable to find style tag_name:", tok)
