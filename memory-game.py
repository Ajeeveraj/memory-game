import tkinter as tk

root = tk.Tk()

# colors
colors = ["#00FFFF", "#FF00FF", "#FFFF00", "#00FF00", "#FF0000", "#0000FF", "#272d33"]
back_color = "#272d33"
card_color = "#382E2E"

class MemoryGame:
    def __init__ (self, root):
        self.root = root
        self.root.title("Memory Game")
        self.root.geometry("720x720")
        self.root.minsize(600,600)
        self.root.configure(bg=back_color)
        self.buttons = []
        self.clicked_buttons = []

        self.create_board()

    def create_board(self):
        for r in range(4):
            for c in range(4):
                button = tk.Button(self.root, bg = card_color, width=10, height=5, command=lambda row=r, col=c: self.on_button_clicked(row, col))
                button.grid(row=r, column=c, padx=5, pady=5)

    def on_button_clicked(self, row, col):
        print("Button clicked at:", row, col)














MemoryGame(root)


root.mainloop()