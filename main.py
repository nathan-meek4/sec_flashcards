import tkinter as tk
from random import shuffle, sample
import re

def load_flashcards(file_path):
    flashcards = {}
    with open(file_path, 'r') as file:
        content = file.read()
    
    matches = re.findall(r'(\w+)\s+(.*?)(?=(\n[A-Z]{2,}\s)|\Z)', content, re.DOTALL)
    
    for match in matches:
        acronym = match[0].strip()
        spelled_out = match[1].replace('\n', ' ').strip()
        flashcards[acronym] = spelled_out
    
    return flashcards

class FlashcardGame:
    def __init__(self, root, flashcards):
        self.root = root
        self.flashcards = flashcards
        self.acronyms = list(flashcards.keys())
        shuffle(self.acronyms)
        self.current_index = 0
        self.score = 0

        self.root.title("Flashcard Game")
        self.root.geometry("800x600")

        self.acronym_label = tk.Label(root, text="", font=("Arial", 24), pady=20)
        self.acronym_label.pack()

        self.buttons = []
        for _ in range(4):
            btn = tk.Button(root, text="", font=("Arial", 16), command=lambda b=_: self.check_answer(b))
            btn.pack(pady=10, fill=tk.X)
            self.buttons.append(btn)

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14), pady=10)
        self.score_label.pack()

        self.next_flashcard()

    def next_flashcard(self):
        if self.current_index >= len(self.acronyms):
            self.end_game()
            return

        self.current_acronym = self.acronyms[self.current_index]
        self.current_correct_answer = self.flashcards[self.current_acronym]
        
        all_answers = list(self.flashcards.values())
        wrong_answers = sample([a for a in all_answers if a != self.current_correct_answer], 3)
        choices = wrong_answers + [self.current_correct_answer]
        shuffle(choices)

        self.acronym_label.config(text=self.current_acronym)
        for i, btn in enumerate(self.buttons):
            btn.config(text=choices[i], state=tk.NORMAL)

        self.current_index += 1

    def check_answer(self, button_index):
        selected_answer = self.buttons[button_index].cget("text")
        if selected_answer == self.current_correct_answer:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.score_label.config(text=f"Score: {self.score} (Wrong!)")

        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.root.after(1000, self.next_flashcard)

    def end_game(self):
        self.acronym_label.config(text="Game Over!")
        for btn in self.buttons:
            btn.pack_forget()
        self.score_label.config(text=f"Final Score: {self.score}/{len(self.acronyms)}")

file_path = 'sec+_vocab.txt'
flashcards = load_flashcards(file_path)

root = tk.Tk()
game = FlashcardGame(root, flashcards)
root.mainloop()
