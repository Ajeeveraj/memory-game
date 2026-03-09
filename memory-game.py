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

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    # Menu system
    def main_menu(self):
        self.clear_screen()  # clear everything when going to menu

        self.difficulty_frame = tk.Frame(self.root, bg=back_color)
        self.difficulty_frame.pack(expand=True)

        tk.Label(
            self.difficulty_frame,
            text="Memory Game",
            font=("Arial", 68),
            bg=back_color,
            fg="white"
        ).pack(pady=120)

        tk.Button(self.difficulty_frame, text="Easy", font=("Arial", 20), width=20, bg="green", fg="white", command=lambda: self.diff_settings("Easy")).pack(pady=20)

        tk.Button(self.difficulty_frame, text="Medium", font=("Arial", 20), width=20, bg="yellow", fg="black", command=lambda: self.diff_settings("Medium")).pack(pady=20)

        tk.Button(self.difficulty_frame, text="Hard", font=("Arial", 20), width=20, bg="red", fg="white", command=lambda: self.diff_settings("Hard")).pack(pady=20)

    # Difficulty system
    def diff_settings(self, difficulty):
        # set difficulty and time
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.time_left = 90
        elif difficulty == "Medium":
            self.time_left = 60
        else:
            self.time_left = 30

        # remove menu frame
        try:
            self.difficulty_frame.destroy()
        except Exception:
            pass

        # Top bar
        if hasattr(self, "top_bar") and getattr(self, "top_bar", None) is not None and self.top_bar.winfo_exists():
            try:
                self.top_bar.destroy()
            except Exception:
                pass
        self.top_bar = tk.Frame(self.root, bg=back_color)
        self.top_bar.pack(fill="x", pady=(8,4))

        # Create a main content area with three columns:
        # left: Play Again, center: card grid, right: timer/match/back
        if hasattr(self, "content") and getattr(self, "content", None) is not None and self.content.winfo_exists():
            try:
                self.content.destroy()
            except Exception:
                pass
        self.content = tk.Frame(self.root, bg=back_color)
        self.content.pack(expand=True, fill="both")

        # Left column (Play Again)
        self.left_col = tk.Frame(self.content, bg=back_color)
        self.left_col.pack(side="left", fill="y", padx=(20,10), pady=10)

        # Center column (card grid container)
        self.center_col = tk.Frame(self.content, bg=back_color)
        self.center_col.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        # Right column (timer, match counter, back to menu)
        self.right_col = tk.Frame(self.content, bg=back_color)
        self.right_col.pack(side="right", fill="y", padx=(10,20), pady=10)


        # Destroy old labels
        if hasattr(self, "timer_label") and getattr(self, "timer_label", None) is not None and self.timer_label.winfo_exists():
            try:
                self.timer_label.destroy()
            except Exception:
                pass
        if hasattr(self, "match_label") and getattr(self, "match_label", None) is not None and self.match_label.winfo_exists():
            try:
                self.match_label.destroy()
            except Exception:
                pass

        self.timer_label = tk.Label(self.right_col, text=f"Time: {self.time_left}", font=("Arial", 28), bg=back_color, fg="yellow")
        self.timer_label.pack(anchor="ne", pady=(0,8))

        self.match_label = tk.Label(self.right_col, text=f"Matches: {self.matches} / 8", font=("Arial", 28), bg=back_color, fg="white")
        self.match_label.pack(anchor="ne", pady=(0,12))

        # Back to Menu button on the right (below labels)
        self.back_to_menu_butn = tk.Button(self.right_col, text="Back to Menu", font=("Arial", 18), command=self.back_to_menu)
        self.back_to_menu_butn.pack(anchor="ne")

        # Play Again button on the left (top)
        # Destroy old if exists
        if hasattr(self, "play_again_butn") and getattr(self, "play_again_butn", None) is not None and self.play_again_butn.winfo_exists():
            try:
                self.play_again_butn.destroy()
            except Exception:
                pass

        self.play_again_butn = tk.Button(self.left_col, text="Play Again", font=("Arial", 18), command=self.restart_game)
        self.play_again_butn.pack(anchor="nw")

        
        if hasattr(self, "card_grid") and getattr(self, "card_grid", None) is not None and self.card_grid.winfo_exists():
            try:
                self.card_grid.destroy()
            except Exception:
                pass
        self.card_grid = tk.Frame(self.center_col, bg=back_color)
        # center the grid
        self.card_grid.place(relx=0.5, rely=0.5, anchor="center")

        # create 16 cards with 8 pairs of colors
        values = colors * 2
        random.shuffle(values)
        self.card_values = [values[i:i+4] for i in range(0, 16, 4)]

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
                    width=12,
                    height=6,
                    relief="solid",
                    bd=5,
                    command=lambda row=r, col=c: self.on_button_clicked(row, col)
                    )
                
                button.grid(row=r, column=c, padx=6, pady=6)
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
            if hasattr(self, "match_label") and self.match_label.winfo_exists():
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
        widths = [12, 9, 6, 3, 1, 3, 6, 9, 12]
        
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
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.configure(text=f"Time: {self.time_left}")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.restart_game()

    # restart the game 
    def restart_game(self):

        # cancel timer
        if hasattr(self, "timer_id"):
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass

        # clear win label if it exists
        if hasattr(self, "win_label") and getattr(self, "win_label", None) is not None and self.win_label.winfo_exists():
            try:
                self.win_label.configure(text="")
            except Exception:
                pass

        # reset timer based on difficulty
        if self.difficulty == "Easy":
            self.time_left = 90
        elif self.difficulty == "Medium":
            self.time_left = 60
        else:
            self.time_left = 30

        # update existing labels (do NOT destroy top_bar or content columns)
        if hasattr(self, "timer_label") and self.timer_label.winfo_exists():
            self.timer_label.configure(text=f"Time: {self.time_left}")

        self.matches = 0
        if hasattr(self, "match_label") and self.match_label.winfo_exists():
            self.match_label.configure(text="Matches: 0 / 8")

        # destroy old card grid safely and recreate centered in center_col
        if hasattr(self, "card_grid") and getattr(self, "card_grid", None) is not None and self.card_grid.winfo_exists():
            try:
                self.card_grid.destroy()
            except Exception:
                pass

        self.card_grid = tk.Frame(self.center_col, bg=back_color)
        self.card_grid.place(relx=0.5, rely=0.5, anchor="center")

        # reset game values
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


    # return to menu
    def back_to_menu(self): 
        if hasattr(self, "timer_id"): 
            try: 
                self.root.after_cancel(self.timer_id) 
            except Exception: 
                pass

        self.clear_screen()
        self.main_menu()

MemoryGame(root)
root.mainloop()




                     