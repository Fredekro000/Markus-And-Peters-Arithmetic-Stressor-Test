# Foreword, this program was made in
# collaboration with ChatGPT.
# Currently, there is a bug, sometimes
# when participants have written a wrong
# answer but not have not submitted, then
# the text will flash green, and still
# say `incorrect'.

import tkinter as tk
from tkinter import messagebox
import random

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markus and Peters Arithmetic Stressor Test")
        self.root.geometry("800x600")  # Enlarge the window

        # Variables
        self.current_trial = 0
        self.step = 1
        self.timer_value = 0
        self.correct_answer = 0
        self.previous_answer = 0
        self.total_trials = 20
        self.timer_running = False
        self.timer_id = None  # To track the active timer

        # UI Elements
        self.title_label = tk.Label(root, text="Markus and Peters Arithmetic Stressor Test", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        self.trials_label = tk.Label(root, text="Trials Completed: 0/20", font=("Arial", 16))
        self.trials_label.pack(pady=10)

        self.question_label = tk.Label(root, text="", font=("Arial", 16))
        self.question_label.pack(pady=20)

        self.timer_label = tk.Label(root, text="", font=("Arial", 14))
        self.timer_label.pack()

        self.answer_entry = tk.Entry(root, font=("Arial", 14))
        self.answer_entry.pack(pady=10)
        self.answer_entry.config(state="disabled")  # Initially disabled

        self.feedback_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
        self.feedback_label.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit", font=("Arial", 14), state="disabled", command=self.check_answer)
        self.submit_button.pack(pady=20)

        self.start_button = tk.Button(root, text="Start Test", font=("Arial", 16), command=self.start_quiz)
        self.start_button.pack(pady=20)

    def start_quiz(self):
        self.start_button.pack_forget()  # Remove the start button
        self.answer_entry.config(state="normal")  # Enable the answer entry
        self.next_question()

    def start_timer(self):
        # Ensure any previously active timer is canceled
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        # Explicitly stop the timer
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False  # Reset running state

    def update_timer(self):
        # Only proceed if the timer is still running
        if not self.timer_running:
            return
        self.timer_label.config(text=f"Time left: {self.timer_value}s")
        if self.timer_value > 0:
            self.timer_value -= 1
            self.timer_id = self.root.after(1000, self.update_timer)  # Schedule the next tick
        else:
            self.timer_running = False
            self.timer_id = None
            self.show_correct_answer()

    def enable_submit(self):
        self.submit_button.config(state="normal")

    def disable_submit(self):
        self.submit_button.config(state="disabled")

    def update_trial_counter(self):
        self.trials_label.config(text=f"Trials Completed: {self.current_trial}/{self.total_trials}")

    def next_question(self):
        self.feedback_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.disable_submit()
        self.stop_timer()  # Ensure no timer is running
        self.timer_running = False

        if self.current_trial >= self.total_trials:
            messagebox.showinfo("Test Complete", "You have completed all the trials!")
            self.root.destroy()
            return

        if self.step == 1:
            # Generate multiplication question
            num1, num2 = random.randint(10, 39), random.randint(10, 39)
            self.correct_answer = num1 * num2
            self.question_label.config(text=f"{num1} x {num2}")
            self.timer_value = 40
        elif self.step == 2:
            # Addition/Subtraction question 1
            modifier = random.randint(-9, 9)
            self.correct_answer = self.previous_answer + modifier
            self.question_label.config(text=f"{'+' if modifier >= 0 else ''}{modifier}")
            self.timer_value = 10
        elif self.step == 3:
            # Addition/Subtraction question 2
            modifier = random.randint(-9, 9)
            self.correct_answer = self.previous_answer + modifier
            self.question_label.config(text=f"{'+' if modifier >= 0 else ''}{modifier}")
            self.timer_value = 10

        self.previous_answer = self.correct_answer
        self.update_trial_counter()
        self.enable_submit()
        self.start_timer()

    def show_correct_answer(self):
        self.feedback_label.config(text=f"Correct Answer: {self.correct_answer}")
        self.disable_submit()
        self.timer_running = False
        self.root.after(2000, self.move_to_next_step)

    def move_to_next_step(self):
        # Ensure Submit button stays disabled while transitioning
        self.disable_submit()
        if self.step == 3:
            self.step = 1
            self.current_trial += 1
        else:
            self.step += 1
        self.next_question()

    def check_answer(self):
        # Stop the timer immediately when the Submit button is pressed
        self.stop_timer()
        self.disable_submit()  # Prevent button spamming
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                self.feedback_label.config(text="Correct!", fg="green")
            else:
                self.feedback_label.config(text=f"Incorrect! Correct Answer: {self.correct_answer}", fg="red")
        except ValueError:
            # Display the correct answer if input is invalid
            self.feedback_label.config(text=f"Invalid input! Correct Answer: {self.correct_answer}", fg="red")

        # Move to the next step after 2 seconds
        self.root.after(2000, self.move_to_next_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
