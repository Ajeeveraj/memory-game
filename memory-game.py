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

        # Timer label
        self.timer_label = tk.Label(self.root, text="Time: 60", font=("Arial", 16), bg=back_color, fg="white")
        self.timer_label.pack(pady=10)

        
        # create 16 cards with 8 pairs of colors
        values = colors * 2
        random.shuffle(values)
        self.card_values = [values[i:i+4] for i in range(0, 16, 4)]

        self.card_grid = tk.Frame(self.root, bg=back_color)
        self.card_grid.pack(expand=True)

        self.create_board()

        # start timer
        self.start_timer()

    def create_board(self):
        self.buttons = []


        for r in range(4):
            button_row = []
            for c in range(4):
                button = tk.Button(
                    self.card_grid,
                    bg = card_color,
                    width=14,
                    height=7,
                    relief="solid",
                    bd=5,
                    command=lambda row=r, col=c: self.on_button_clicked(row, col)
                    )
                
                button.grid(row=r, column=c, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

    def on_button_clicked(self, row, col):

        if len(self.clicked_buttons) == 2:
            return
        
        button = self.buttons[row][col]
        color = self.card_values[row][col]

        if button in self.clicked_buttons:
            return
        
        # Make it look like its flipping
        self.flip_cards(button, color)
        self.clicked_buttons.append(button)
        if len(self.clicked_buttons) == 2:
            self.root.after(600, self.check_match)  

    def check_match(self):
        butn1, butn2 = self.clicked_buttons
        row1, col1 = butn1.grid_info()["row"], butn1.grid_info()["column"]
        row2, col2 = butn2.grid_info()["row"], butn2.grid_info()["column"]

        color1 = self.card_values[row1][col1]
        color2 = self.card_values[row2][col2]

        if color1 == color2:
            butn1.configure(state="disabled")
            butn2.configure(state="disabled")
        else:
            butn1.configure(bg=card_color, relief="solid")
            butn2.configure(bg=card_color, relief="solid")

        self.clicked_buttons = []

    def flip_cards(self, button, flipped_color, frame=0):
        widths = [14, 10, 6, 3, 1, 3, 6, 10, 14]
        
        if frame < len(widths):
            button.configure(width=widths[frame])

            # change color mid flip
            if frame == len(widths) // 2:
                button.configure(bg=flipped_color)
            self.root.after(20, lambda: self.flip_cards(button, flipped_color, frame + 1))


    # Run the timer
    def start_timer(self):
        self.time_left = 60
        self.update_timer()

    def update_timer(self):
        self.timer_label.configure(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.restart_game()

    # restart if time reaches 0
    def restart_game(self):
        for widget in self.card_grid.winfo_children():
            widget.destroy()

        # reset game if time runs out
        values = colors * 2
        random.shuffle(values)
        self.card_values = [values[i:i+4] for i in range(0, 16, 4)]
        self.clicked_buttons = []
        self.create_board()
        self.start_timer()


            














MemoryGame(root)


root.mainloop()