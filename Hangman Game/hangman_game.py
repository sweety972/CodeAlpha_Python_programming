import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# List of words
words_list = ['python', 'hangman', 'challenge', 'developer', 'programming']

# Function to choose a random word
def choose_word():
    return random.choice(words_list)

# Function to update the displayed word with guessed letters
def update_displayed_word():
    displayed_word.set(' '.join([letter if letter in correct_guesses else '_' for letter in word]))

# Function to handle button click (guessing a letter)
def guess_letter(letter):
    if letter in correct_guesses or letter in incorrect_guesses:
        messagebox.showinfo("Hangman", "You've already guessed that letter.")
        return

    if letter in word:
        correct_guesses.append(letter)
        update_displayed_word()
        if all(l in correct_guesses for l in word):
            show_celebration_animation()  # Trigger celebration on win
    else:
        incorrect_guesses.append(letter)
        incorrect_guesses_label.config(text="Incorrect guesses: " + ', '.join(incorrect_guesses))
        attempts_left.set(attempts_left.get() - 1)
        draw_hangman(len(incorrect_guesses))  # Draw the hangman based on incorrect guesses
        if attempts_left.get() == 0:
            messagebox.showinfo("Hangman", f"Game Over! The word was: {word}")
            reset_game()

# Function to reset the game
def reset_game():
    global word, correct_guesses, incorrect_guesses
    word = choose_word()
    correct_guesses = []
    incorrect_guesses = []
    update_displayed_word()
    incorrect_guesses_label.config(text="Incorrect guesses: ")
    attempts_left.set(max_attempts)
    canvas.delete("all")  # Clear the hangman figure

# Celebration Animation
def show_celebration_animation():
    for button in buttons_frame.winfo_children():
        button.config(state="disabled")
    
    celebration_window = tk.Toplevel(root)
    celebration_window.geometry("400x400")
    celebration_window.title("Congratulations!")
    celebration_window.configure(bg="white")  # Set background color to avoid transparency

    center_window(celebration_window, 400, 400)

    canvas = tk.Canvas(celebration_window, width=400, height=400, bg='white')  # Set canvas background to white
    canvas.pack()

    canvas.create_text(200, 100, text="Congratulations!", font=("Helvetica", 24, "bold"), fill="green")


# Function to center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to draw the hangman figure using canvas lines and shapes
def draw_hangman(stage):
    canvas.delete("all")  # Clear previous drawings
    # Draw the gallows
    canvas.create_line(20, 280, 180, 280, width=4)  # Base
    canvas.create_line(50, 280, 50, 50, width=4)    # Vertical pole
    canvas.create_line(50, 50, 150, 50, width=4)    # Horizontal pole
    canvas.create_line(150, 50, 150, 80, width=4)   # Rope

    # Draw hangman stages
    if stage >= 1:
        canvas.create_oval(120, 80, 180, 140, width=3)  # Head
    if stage >= 2:
        canvas.create_line(150, 140, 150, 200, width=3)  # Body
    if stage >= 3:
        canvas.create_line(150, 160, 120, 180, width=3)  # Left arm
    if stage >= 4:
        canvas.create_line(150, 160, 180, 180, width=3)  # Right arm
    if stage >= 5:
        canvas.create_line(150, 200, 120, 240, width=3)  # Left leg
    if stage >= 6:
        canvas.create_line(150, 200, 180, 240, width=3)  # Right leg
    if stage >= 7:
        canvas.create_line(140, 110, 160, 110, width=2)  # Eyes
        canvas.create_line(140, 115, 160, 115, width=2)  # Mouth

# Initialize the main window
root = tk.Tk()
root.title("Hangman Game")

# Set the dimensions of the main window and center it
window_width = 900
window_height = 600
center_window(root, window_width, window_height)

# Variables
correct_guesses = []
incorrect_guesses = []
max_attempts = 7  # 7 stages of the hangman
attempts_left = tk.IntVar(value=max_attempts)
displayed_word = tk.StringVar()

# Choose a random word to start
word = choose_word()

# GUI Layout
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# Word display and attempts left labels
word_label = tk.Label(top_frame, textvariable=displayed_word, font=('Helvetica', 22))
word_label.pack(pady=10)

attempts_label = tk.Label(top_frame, text="Attempts left: ", font=('Helvetica', 16))
attempts_label.pack()

attempts_left_label = tk.Label(top_frame, textvariable=attempts_left, font=('Helvetica', 16))
attempts_left_label.pack()

incorrect_guesses_label = tk.Label(top_frame, text="Incorrect guesses: ", font=('Helvetica', 14))
incorrect_guesses_label.pack(pady=5)

# Canvas for drawing the hangman
canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.LEFT, padx=40, pady=20)
canvas = tk.Canvas(canvas_frame, width=300, height=300, bg='white')
canvas.pack()

# Alphabet buttons for guessing letters
buttons_frame = tk.Frame(root)
buttons_frame.pack(side=tk.RIGHT, padx=20)

# Create buttons for each letter in a grid
for letter in 'abcdefghijklmnopqrstuvwxyz':
    btn = tk.Button(buttons_frame, text=letter.upper(), width=4, height=2,
                    command=lambda l=letter: guess_letter(l))
    btn.grid(row=(ord(letter) - 97) // 9, column=(ord(letter) - 97) % 9, padx=5, pady=5)

# Reset button to start a new game
reset_button = tk.Button(root, text="Reset Game", command=reset_game, font=('Helvetica', 16), height=2, width=20, bg='white', fg='black')
reset_button.pack(pady=0, padx=0, side=tk.BOTTOM, fill=tk.X)

# Initial word display
update_displayed_word()

# Run the main application loop
root.mainloop()
