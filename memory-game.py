import tkinter as tk
import random

root = tk.Tk()

# colors
colors = ["#00FFFF", "#FF00FF", "#FFFF00", "#00FF00", "#FF0000", "#0000FF", "#272d33", "#7A0C7E"]
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
        
        # create 16 cards with 8 pairs of colors
        values = colors * 2
        random.shuffle(values)
        self.card_values = [values[i:i+4] for i in range(0, 16, 4)]

        self.card_grid = tk.Frame(self.root, bg=back_color)
        self.card_grid.pack(expand=True)

        self.create_board()

    def create_board(self):
        self.buttons = []


        for r in range(4):
            button_row = []
            for c in range(4):
                button = tk.Button(
                    self.card_grid,
                    bg = card_color,
                    width=10,
                    height=5,
                    command=lambda row=r, col=c: self.on_button_clicked(row, col)
                    )
                
                button.grid(row=r, column=c, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

    def on_button_clicked(self, row, col):
        button = self.buttons[row][col]
        color = self.card_values[row][col]
        button.configure(bg=color)  















MemoryGame(root)


root.mainloop()