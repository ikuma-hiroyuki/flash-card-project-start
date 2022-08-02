import random
import tkinter as tk

import pandas
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_lean = {}

try:
    data = pd.read_csv("data/words_to_lean.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_lean = original_data.to_dict(orient="records")
else:
    to_lean = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_lean)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_lean.remove(current_card)
    words_data = pandas.DataFrame(to_lean)
    words_data.to_csv("data/words_to_lean.csv", index=False)
    next_card()


window = tk.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# Canvas
canvas = tk.Canvas(width=800, height=526)
card_front_img = tk.PhotoImage(file="images/card_front.png")
card_back_img = tk.PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 40, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_image = tk.PhotoImage(file="images/wrong.png")
wrong_button = tk.Button(image=wrong_image, command=next_card)
wrong_button.config(bg=BACKGROUND_COLOR, highlightthickness=0)
wrong_button.grid(row=1, column=0)

right_image = tk.PhotoImage(file="images/right.png")
right_button = tk.Button(image=right_image, command=is_known)
right_button.config(bg=BACKGROUND_COLOR, highlightthickness=0)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
