import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import threading

class Game:

    def __init__(self, master):
        self.numbers = [1,2,3,4,5,6]
        self.images = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
        self.money = 100

        # GUI setup
        self.master = master
        self.master.title("Game")

        # Money
        money_style = ttk.Style()
        money_style.configure("money.TButton", font=("Arial", 12))

        self.money_label = ttk.Label(self.master, style="money.TButton", text=f"Money: {self.money}")
        self.money_label.grid(row=0, column=0, padx=10, pady=10)

        # Image 
        self.image = Image.open(random.choice(self.images))
        self.image = self.image.resize((100, 100))
        self.photo = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self.master, image=self.photo)
        self.image_label.grid(row=1, column=1)

        # Bet
        self.bet_text = tk.Label(self.master, text="Place a bet:", font=("Arial", 12))
        self.bet_text.grid(row=1, column=0)

        self.bet_amount = tk.StringVar()
        vcmd = (self.master.register(self.validate_input), '%P')
        self.bet_entry = ttk.Entry(self.master, width=12, validatecommand=vcmd, textvariable=self.bet_amount, validate="key")
        self.bet_entry.grid(row=2, column=0, pady=5)

        self.bet_button = ttk.Button(self.master, text="Bet", command=self.start_rolling)
        self.bet_button.grid(row=3, column=0)

    def validate_input(self, value):
        if not value:
            return True

        if not value.isdigit():
            return False

        if int(value) > self.money:
            return False
        
        if int(value) == 0:
            return False

        return True

    def start_rolling(self):
        self.bet = int(self.bet_entry.get())

        self.bet_entry['state'] = 'disabled'
        self.bet_button['state'] = 'disabled'
        self.money = self.money - self.bet
        self.money_label.config(text=f"Money: {self.money}")
        self.end_result = random.choice(self.numbers)
        print("Dice rolled:", self.end_result)
        
        rolling_thread = threading.Thread(target=self.roll_dice, args=(self.end_result,))
        rolling_thread.start()


    def roll_dice(self, end_result):
        num_rolls = random.randint(10, 20)
        for _ in range(num_rolls):
            random_image_path = random.choice(self.images)
            self.show_image(random_image_path)
            time.sleep(0.3)

        final_image_path = f"{end_result}.png"
        self.show_image(final_image_path)
        self.update_money(end_result)
        self.master.after(100, self.reset_bet_ui) 

    def reset_bet_ui(self):
        self.bet_amount.set("")
        self.bet_entry['state'] = 'enabled'
        self.bet_button['state'] = 'enabled'

    def show_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def update_money(self, end_result):
        if end_result == 1:
            ...

        if end_result == 2:
            self.money = self.money + self.bet * 0.25

        if end_result == 3:
            self.money = self.money + self.bet * 0.50

        if end_result == 4:
            self.money = self.money + self.bet

        if end_result == 5:
            self.money = self.money + self.bet * 2

        if end_result == 6:
            self.money = self.money + self.bet * 3

        self.money_label.config(text=f"Money: {self.money}")
        self.bet_entry['state'] = 'enabled'
        self.bet_button['state'] = 'enabled'


if __name__ == "__main__":
    root = tk.Tk()
    app = Game(root)
    root.geometry("300x300")
    root.mainloop()