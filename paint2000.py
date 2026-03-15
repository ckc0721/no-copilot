import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageColor

class MSPaint2000:
    def __init__(self, root):
        self.root = root
        self.root.title("untitled - Paint")
        self.root.geometry("1000x800")
        self.root.configure(bg="#d4d0c8")

        self.active_tool = "pencil"
        self.pen_color = "black"
        self.rgb_color = (0, 0, 0)
        self.brush_size = 2
        self.start_x, self.start_y = None, None
        self.old_x, self.old_y = None, None
        self.current_ghost = None
        
        self.image = Image.new("RGB", (2000, 2000), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Sidebar
        self.sidebar = tk.Frame(self.root, width=70, bg="#d4d0c8", relief="raised", bd=2)
        self.sidebar.pack(side="left", fill="y", padx=2, pady=2)

        self.tool_btns = {}
        tools = [("✏️", "pencil"), ("🧽", "eraser"), ("🪣", "fill"), ("A", "text"), ("⭕", "circle"), ("🟦", "square")]
        for icon, name in tools:
            btn = tk.Button(self.sidebar, text=icon, width=4, height=2, command=lambda n=name: self.set_tool(n), bg="#d4d0c8")
            btn.pack(padx=5, pady=2)
            self.tool_btns[name] = btn
        
        self.size_list = tk.Listbox(self.sidebar, height=4, width=6)
        self.size_list.pack(padx=5, pady=10)
        for s in [2, 5, 10, 20]: self.size_list.insert("end", f" {s}px")
        self.size_list.bind("<<ListboxSelect>>", self.change_size)

        tk.Button(self.sidebar, text="Clear", command=self.clear_canvas).pack(pady=5)
        tk.Button(self.sidebar, text="💾", command=self.save_file).pack()

        # Palette
        self.palette = tk.Frame(self.root, bg="#d4d0c8", relief="raised", bd=2)
        self.palette.pack(side="bottom", fill="x")
        colors = ["black", "gray", "darkred", "red", "orange", "yellow", "green", "blue", "purple", "hotpink", "white"]
        for col in colors:
            tk.Button(self.palette, bg=col, width=2, command=lambda c=col: self.set_color(c)).pack(side="left", padx=2, pady=5)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white", relief="sunken", bd=3)
        self.canvas.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def set_tool(self, name):
        for btn in self.tool_btns.values(): btn.config(relief="raised")
        self.tool_btns[name].config(relief="sunken")
        self.active_tool = name

    def set_color(self, color):
        self.pen_color = color
        self.rgb_color = ImageColor.getrgb(color)

    def change_size(self, event):
        idx = self.size_list.curselection()
        if idx: self.brush_size = [2, 5, 10, 20][idx[0]]

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.active_tool == "fill":
            ImageDraw.floodfill(self.image, (event.x, event.y), self.rgb_color)
            self.sync_canvas()
        elif self.active_tool == "text":
            txt = simpledialog.askstring("Text", "Enter text:")
            if txt:
                self.canvas.create_text(event.x, event.y, text=txt, fill=self.pen_color, anchor="nw")
                self.draw.text((event.x, event.y), txt, fill=self.rgb_color)

    def on_drag(self, event):
        if self.active_tool in ["pencil", "eraser"]:
            c = "white" if self.active_tool == "eraser" else self.pen_color
            sz = 20 if self.active_tool == "eraser" else self.brush_size
            if self.old_x:
                self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=sz, fill=c, capstyle="round")
                self.draw.line([self.old_x, self.old_y, event.x, event.y], fill=self.rgb_color if self.active_tool=="pencil" else (255,255,255), width=sz)
            self.old_x, self.old_y = event.x, event.y
        
        elif self.active_tool in ["circle", "square"]:
            if self.current_ghost: self.canvas.delete(self.current_ghost)
            if self.active_tool == "circle":
                self.current_ghost = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.brush_size)
            else:
                self.current_ghost = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.pen_color, width=self.brush_size)

    def on_release(self, event):
        if self.active_tool in ["circle", "square"]:
            if self.active_tool == "circle":
                self.draw.ellipse([self.start_x, self.start_y, event.x, event.y], outline=self.rgb_color, width=self.brush_size)
            else:
                self.draw.rectangle([self.start_x, self.start_y, event.x, event.y], outline=self.rgb_color, width=self.brush_size)
        self.old_x, self.old_y = None, None
        self.current_ghost = None

    def sync_canvas(self):
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (2000, 2000), "white")
        self.draw = ImageDraw.Draw(self.image)

    def save_file(self):
        f = filedialog.asksaveasfilename(defaultextension=".png")
        if f: self.image.save(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = MSPaint2000(root)
    root.mainloop()

