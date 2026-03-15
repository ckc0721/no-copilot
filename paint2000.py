import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageColor

class MSPaint2000:
    def __init__(self, root):
        self.root = root
        self.root.title("untitled - Paint")
        self.root.geometry("1000x800")
        self.root.configure(bg="#d4d0c8")

        # --- State Variables ---
        self.active_tool = "pencil"
        self.pen_color = "black"
        self.rgb_color = (0, 0, 0)
        self.brush_size = 2
        self.old_x, self.old_y = None, None
        
        # PIL Image for Fill & Saving
        self.image = Image.new("RGB", (1600, 1200), "white")
        self.draw = ImageDraw.Draw(self.image)

        # --- Sidebar (Tools & Size) ---
        self.sidebar = tk.Frame(self.root, width=70, bg="#d4d0c8", relief="raised", bd=2)
        self.sidebar.pack(side="left", fill="y", padx=2, pady=2)

        self.tool_btns = {}
        tools = [("✏️", "pencil"), ("🧽", "eraser"), ("🪣", "fill"), ("A", "text")]
        for icon, name in tools:
            btn = tk.Button(self.sidebar, text=icon, width=4, height=2,
                            command=lambda n=name: self.set_tool(n),
                            relief="raised", bg="#d4d0c8")
            btn.pack(padx=5, pady=2)
            self.tool_btns[name] = btn
        
        # Brush Size Selector
        tk.Label(self.sidebar, text="Size", bg="#d4d0c8", font=("Arial", 8)).pack(pady=(10, 0))
        self.size_list = tk.Listbox(self.sidebar, height=4, width=6, exportselection=False)
        self.size_list.pack(padx=5, pady=5)
        for s in [2, 5, 10, 20]: self.size_list.insert("end", f" {s}px")
        self.size_list.select_set(0)
        self.size_list.bind("<<ListboxSelect>>", self.change_size)

        tk.Button(self.sidebar, text="Clear", command=self.clear_canvas, bg="#d4d0c8").pack(pady=10, padx=5, fill="x")
        tk.Button(self.sidebar, text="💾", command=self.save_file, bg="#d4d0c8").pack(padx=5, fill="x")

        # --- Status Bar ---
        self.status_bar = tk.Frame(self.root, bg="#d4d0c8", relief="sunken", bd=1)
        self.status_bar.pack(side="bottom", fill="x")
        self.coords_label = tk.Label(self.status_bar, text="0, 0", bg="#d4d0c8", font=("Arial", 9))
        self.coords_label.pack(side="right", padx=10)

        # --- Color Palette (Bottom) ---
        self.palette = tk.Frame(self.root, bg="#d4d0c8", relief="raised", bd=2)
        self.palette.pack(side="bottom", fill="x")
        
        # Expanded color list including pink
        colors = ["black", "gray", "darkred", "red", "orange", "yellow", "green", "blue", "purple", "hotpink", "white"]
        for col in colors:
            btn = tk.Button(self.palette, bg=col, width=2, height=1, relief="sunken",
                            command=lambda c=col: self.set_color(c))
            btn.pack(side="left", padx=2, pady=5)

        # --- Canvas Area ---
        self.canvas = tk.Canvas(self.root, bg="white", relief="sunken", bd=3, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coords)
        self.canvas.bind("<Motion>", self.update_coords)

    def set_tool(self, name):
        for n, btn in self.tool_btns.items():
            btn.config(relief="raised")
        self.tool_btns[name].config(relief="sunken")
        self.active_tool = name

    def change_size(self, event):
        idx = self.size_list.curselection()
        if idx:
            sizes = [2, 5, 10, 20]
            self.brush_size = sizes[idx[0]]
            self.set_tool("pencil")

    def set_color(self, color):
        self.pen_color = color
        self.rgb_color = ImageColor.getrgb(color)
        if self.active_tool == "eraser":
            self.set_tool("pencil")

    def update_coords(self, event):
        self.coords_label.config(text=f"{event.x}, {event.y}")

    def handle_click(self, event):
        if self.active_tool == "fill":
            ImageDraw.floodfill(self.image, (event.x, event.y), self.rgb_color, thresh=10)
            self.sync_canvas()
        elif self.active_tool == "text":
            txt = simpledialog.askstring("Text Tool", "Enter text:")
            if txt:
                self.canvas.create_text(event.x, event.y, text=txt, fill=self.pen_color, font=("Arial", 12), anchor="nw")
                self.draw.text((event.x, event.y), txt, fill=self.rgb_color)

    def paint(self, event):
        self.update_coords(event)
        if self.active_tool in ["pencil", "eraser"]:
            color_str = "white" if self.active_tool == "eraser" else self.pen_color
            color_rgb = (255, 255, 255) if self.active_tool == "eraser" else self.rgb_color
            # Eraser uses a fixed large size, pencil uses the selector size
            draw_size = 25 if self.active_tool == "eraser" else self.brush_size
            
            if self.old_x and self.old_y:
                self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, 
                                       width=draw_size, fill=color_str, capstyle="round", smooth=True)
                self.draw.line([self.old_x, self.old_y, event.x, event.y], 
                               fill=color_rgb, width=draw_size)
            self.old_x, self.old_y = event.x, event.y

    def sync_canvas(self):
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")

    def reset_coords(self, event):
        self.old_x, self.old_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (1600, 1200), "white")
        self.draw = ImageDraw.Draw(self.image)

    def save_file(self):
        f = filedialog.asksaveasfilename(defaultextension=".png")
        if f: self.image.save(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = MSPaint2000(root)
    root.mainloop()
