import tkinter as tk

root = tk.Tk()

class MemoryGame:
    def __init__ (self, root):
        self.root = root
        self.root.after(700, lambda: self.root.attributes("-zoomed", True))
        self.root.title("Memory Game")
















root.mainloop()