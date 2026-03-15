import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad2000:
    def __init__(self, root):
        self.root = root
        self.root.title("Untitled - Notepad")
        self.root.geometry("600x400")

        # The Text Area
        self.textarea = tk.Text(self.root, font=("Courier New", 11), undo=True)
        self.textarea.pack(expand=True, fill="both")

        # Menu Bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # File Menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

    def new_file(self):
        self.textarea.delete(1.0, tk.END)
        self.root.title("Untitled - Notepad")

    def open_file(self):
        f = filedialog.askopenfilename(filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if f:
            self.textarea.delete(1.0, tk.END)
            with open(f, "r") as file:
                self.textarea.insert(1.0, file.read())
            self.root.title(f"{f} - Notepad")

    def save_file(self):
        f = filedialog.asksaveasfilename(defaultextension=".txt")
        if f:
            with open(f, "w") as file:
                file.write(self.textarea.get(1.0, tk.END))
            self.root.title(f"{f} - Notepad")

if __name__ == "__main__":
    root = tk.Tk()
    Notepad2000(root)
    root.mainloop()
