import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

# Game Categories
categories = {
    "Animals": ["elephant", "tiger", "kangaroo", "giraffe"],
    "Fruits": ["banana", "apple", "mango", "pineapple"],
    "Actors": ["al pacino", "brad pitt", "tom cruise", "johnny depp"],
    "Tech": ["python", "keyboard", "laptop", "internet"]
}

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.word = ""
        self.hint = ""
        self.guessed_letters = []
        self.attempts = 6
        self.time_limit = 60
        self.start_time = None

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        title = tk.Label(self.root, text=" Hangman Game", font=("Helvetica", 24))
        title.pack(pady=20)

        btn_single = tk.Button(self.root, text="Single Player", font=("Helvetica", 16), width=20, command=self.choose_category)
        btn_single.pack(pady=10)

        btn_multi = tk.Button(self.root, text="Multiplayer", font=("Helvetica", 16), width=20, command=self.multiplayer_setup)
        btn_multi.pack(pady=10)

    def choose_category(self):
        self.clear_window()

        tk.Label(self.root, text="Choose a Category", font=("Helvetica", 20)).pack(pady=10)

        for category in categories:
            btn = tk.Button(self.root, text=category, font=("Helvetica", 14),
                            command=lambda cat=category: self.start_game(cat, random.choice(categories[cat]).upper()))
            btn.pack(pady=5)

    def multiplayer_setup(self):
        self.clear_window()

        word = simpledialog.askstring("Word Input", "Player 1: Enter a word to guess:").upper()
        hint = simpledialog.askstring("Hint", "Enter a hint for Player 2 (e.g., Actor, Tech):")
        self.start_game(hint, word)

    def start_game(self, hint, word):
        self.hint = hint
        self.word = word
        self.guessed_letters = []
        self.attempts = 6
        self.start_time = time.time()

        self.clear_window()

        self.label_hint = tk.Label(self.root, text=f"Hint: {self.hint}", font=("Helvetica", 16))
        self.label_hint.pack(pady=10)

        self.label_timer = tk.Label(self.root, text="Time left: 60s", font=("Helvetica", 14))
        self.label_timer.pack()

        self.label_attempts = tk.Label(self.root, text=f"Attempts remaining: {self.attempts}", font=("Helvetica", 14))
        self.label_attempts.pack(pady=5)

        self.label_word = tk.Label(self.root, text=self.get_display_word(), font=("Courier", 24))
        self.label_word.pack(pady=20)

        self.entry = tk.Entry(self.root, font=("Helvetica", 18), width=5, justify='center')
        self.entry.pack()
        self.entry.focus()

        self.submit_btn = tk.Button(self.root, text="Guess", font=("Helvetica", 14), command=self.make_guess)
        self.submit_btn.pack(pady=10)

        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.feedback_label.pack()

        self.update_timer()

    def get_display_word(self):
        return " ".join([letter if letter in self.guessed_letters or letter == " " else "_" for letter in self.word])

    def make_guess(self):
        guess = self.entry.get().upper()
        self.entry.delete(0, tk.END)

        if not guess or len(guess) != 1 or not guess.isalpha():
            self.feedback_label.config(text="Enter a single valid letter.")
            return

        if guess in self.guessed_letters:
            self.feedback_label.config(text="You already guessed that letter.")
            return

        self.guessed_letters.append(guess)

        if guess in self.word:
            self.feedback_label.config(text=" Good guess!")
        else:
            self.attempts -= 1
            self.label_attempts.config(text=f"Attempts remaining: {self.attempts}")
            self.feedback_label.config(text=" Wrong guess.")

        self.label_word.config(text=self.get_display_word())

        if all(letter in self.guessed_letters or letter == " " for letter in self.word):
            self.game_over(won=True)
        elif self.attempts == 0:
            self.game_over(won=False)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        remaining = self.time_limit - elapsed
        self.label_timer.config(text=f"Time left: {remaining}s")

        if remaining <= 0:
            self.game_over(timeout=True)
        elif self.attempts > 0:
            self.root.after(1000, self.update_timer)

    def game_over(self, won=False, timeout=False):
        self.entry.config(state='disabled')
        self.submit_btn.config(state='disabled')

        if timeout:
            msg = f" Time's up! The word was: {self.word}"
        elif won:
            msg = f" You won! The word was: {self.word}"
        else:
            msg = f" You lost! The word was: {self.word}"

        messagebox.showinfo("Game Over", msg)
        self.play_again_prompt()

    def play_again_prompt(self):
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            self.create_main_menu()
        else:
            self.root.destroy()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the GUI
root = tk.Tk()
game = HangmanGame(root)
root.mainloop()
