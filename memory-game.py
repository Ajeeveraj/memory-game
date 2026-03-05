import tkinter as tk
import random

root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# colors
colors = ["#00FFFF", "#FF00FF", "#FFFF00", "#00FF00", "#FF0000", "#0000FF", "#272d33", "#7A0C7E"]
back_color = "#0f1115"
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
        self.matches = 0
        self.main_menu()
    
    # Menu system
    def main_menu(self):
        self.difficulty_frame = tk.Frame(self.root, bg=back_color)
        self.difficulty_frame.pack(expand=True)

        tk.Label(
            self.difficulty_frame,
            text="Memory Game",
            font=("Arial", 68),
            bg=back_color,
            fg="white"
        ).pack(pady=120)

        tk.Button(self.difficulty_frame, text="Easy", font=("Arial", 18), width=12, command=lambda: self.diff_settings("Easy")).pack(pady=10)
        tk.Button(self.difficulty_frame, text="Medium", font=("Arial", 18), width=12, command=lambda: self.diff_settings("Medium")).pack(pady=10)
        tk.Button(self.difficulty_frame, text="Hard", font=("Arial", 18), width=12, command=lambda: self.diff_settings("Hard")).pack(pady=10)

    # Difficulty systm
    def diff_settings(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.time_left = 90
        elif difficulty == "Medium":
            self.time_left = 60
        else:
            self.time_left = 30

        self.difficulty_frame.destroy()

        # Align all widgets and labels
        self.top_bar = tk.Frame(self.root, bg=back_color)
        self.top_bar.pack(fill="x", pady=10)

        # Timer label
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.configure(text=f"Time: {self.time_left}")
            self.timer_label.pack_forget()
        else:
            self.timer_label = tk.Label(self.top_bar, text=f"Time: {self.time_left}", font=("Arial", 36), bg=back_color, fg="white")
            self.timer_label.pack(side="left", padx=20)

        # Match counter Label
        if hasattr(self, "match_label") and self.match_label.winfo_exists():
            self.match_label.configure(text=f"Matches: {self.matches} / 8")
            self.match_label.pack_forget() 
        else:
            self.match_label = tk.Label(self.top_bar, text=f"Matches: {self.matches} / 8", font=("Arial", 36), bg=back_color, fg="white")
            self.match_label.pack(side="right", padx=20)

        # Create play again button
        self.play_again_butn = tk.Button(self.root, text="Play Again", font=("Arial", 28), command=self.restart_game)
        self.play_again_butn.pack(pady=14)

        # Create back to menu button
        self.back_to_menu_butn = tk.Button(self.root, text="Back to Menu", font=("Arial", 28), command=self.back_to_menu)
        self.back_to_menu_butn.pack(pady=14)


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

    # Check for matches
    def check_match(self):
        butn1, butn2 = self.clicked_buttons
        row1, col1 = butn1.grid_info()["row"], butn1.grid_info()["column"]
        row2, col2 = butn2.grid_info()["row"], butn2.grid_info()["column"]

        color1 = self.card_values[row1][col1]
        color2 = self.card_values[row2][col2]

        if color1 == color2:
            butn1.configure(state="disabled")
            butn2.configure(state="disabled")
            self.matches += 1
            self.match_label.configure(text=f"Matches: {self.matches} / 8")
        else:
            butn1.configure(bg=card_color, relief="solid")
            butn2.configure(bg=card_color, relief="solid")

        self.clicked_buttons = []

        # Check if all cards are matched
        all_disabled = all(button["state"] == "disabled" for row in self.buttons for button in row)
        
        if all_disabled:
            self.game_won()


    def flip_cards(self, button, flipped_color, frame=0):
        widths = [14, 10, 6, 3, 1, 3, 6, 10, 14]
        
        if frame < len(widths):
            button.configure(width=widths[frame])

            # change color mid flip
            if frame == len(widths) // 2:
                button.configure(bg=flipped_color)
            self.root.after(15, lambda: self.flip_cards(button, flipped_color, frame + 1))


    # Run the timer
    def start_timer(self):
        self.update_timer()

    def update_timer(self):
        self.timer_label.configure(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.restart_game()

    # restart if time reaches 0
    def restart_game(self):
        if hasattr(self, "timer_id"):
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass

        
        if hasattr(self, "win_label") and self.win_label.winfo_exists():
            self.win_label.configure(text="")
            
         
        # restart timer based on difficulty
        if self.difficulty == "Easy":
            self.time_left = 90
        elif self.difficulty == "Medium":
            self.time_left = 60
        else:
            self.time_left = 30

        # Update timer label
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.configure(text=f"Time: {self.time_left}")
        else:
            self.timer_label = tk.Label(self.root, text=f"Time: {self.time_left}", font=("Arial", 16), bg=back_color, fg="white")

        # Destroy old cards when creating new board
        if hasattr(self, "card_grid"):
            try:
                self.card_grid.destroy()
            except Exception:
                pass
        
        # Reset match counter
        self.matches = 0

        if hasattr(self, "Match_label") and self.match_label.winfo_exists():
            self.top_bar.destroy()

        self.top_bar = tk.Frame(self.root, bg=back_color)
        self.top_bar.pack(fill="x", pady=10)

        # Create a new card grid frame
        self.card_grid = tk.Frame(self.root, bg = back_color)
        self.card_grid.pack(expand=True)

        # reset match counter
        self.matches = 0
        self.match_label.configure(text=f"Matches: 0/8")

        # reset game if time runs out
        values = colors * 2
        random.shuffle(values)
        self.card_values = [values[i:i+4] for i in range(0, 16, 4)]
        self.clicked_buttons = []
        self.create_board()
        self.start_timer()

    # Game won
    def game_won(self):
        if hasattr(self, "timer_id"):
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass
        
        if hasattr(self, "card_grid"):
            try:
                self.card_grid.destroy()
            except Exception:
                pass
        
        # Ensure win label is visible
        if not (hasattr(self, "win_label") and getattr(self, "win_label", None) is not None and self.win_label.winfo_exists()):
            self.win_label = tk.Label(self.root, text="You won", font=("Arial", 54), bg=back_color, fg="white")
            self.win_label.pack(pady=20)
        else:
            self.win_label.configure(text="You Won!")
            try:
                if not self.win_label.winfo_ismapped():
                    self.win_label.pack(pady=10)
            except Exception:
                pass


    # Return back to the main menu if the button is clicked
    def back_to_menu(self): 
        if hasattr(self, "timer_id"): 
            try: 
                self.root.after_cancel(self.timer_id) 
            except Exception: 
                pass

        if hasattr(self, "play_again_butn"):
                self.play_again_butn.pack_forget()

        if hasattr(self, "back_to_menu_butn"): 
            self.back_to_menu_butn.pack_forget()

        if hasattr(self, "win_label") and self.win_label.winfo_exists(): 
            try: 
                self.win_label.configure(text="") 
            except Exception: 
                pass

        if hasattr(self, "timer_label") and self.timer_label.winfo_exists(): 
            try: 
                self.timer_label.destroy() 
            except Exception: 
                pass

        if hasattr(self, "card_grid"): 
            try: 
                self.card_grid.destroy() 
            except Exception: 
                pass 
        
        self.main_menu()






            














MemoryGame(root)


root.mainloop()