import tkinter as tk
from tkinter import messagebox
import math
import random

#Med hjälp av AI från todo.py

class TicTacToe:

    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        self.root.resizable(False, False)

        self.human = "X"
        self.ai = "O"

        self.board = [""] * 9
        self.buttons = []

        # Poäng
        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0

        # Svårighetsgrad
        self.difficulty = tk.StringVar(value="Svår")

        # -------------------------
        # GUI
        # -------------------------

        tk.Label(
            root,
            text="Svårighetsgrad",
            font=("Arial", 12)
        ).grid(row=0, column=0, columnspan=3)

        for i, level in enumerate(["Lätt", "Normal", "Svår"]):
            tk.Radiobutton(
                root,
                text=level,
                variable=self.difficulty,
                value=level
            ).grid(row=1, column=i)


        self.status = tk.Label(
            root,
            text="Din tur (X)",
            font=("Arial", 14)
        )
        self.status.grid(
            row=2,
            column=0,
            columnspan=3,
            pady=10
        )


        self.score_label = tk.Label(
            root,
            text="Du: 0   Dator: 0   Oavgjort: 0",
            font=("Arial", 12)
        )
        self.score_label.grid(
            row=3,
            column=0,
            columnspan=3
        )


        # Spelplan
        for i in range(9):
            button = tk.Button(
                root,
                text="",
                font=("Arial", 24),
                width=5,
                height=2,
                command=lambda i=i: self.player_move(i)
            )

            button.grid(
                row=i // 3 + 4,
                column=i % 3
            )

            self.buttons.append(button)


        tk.Button(
            root,
            text="Starta om",
            font=("Arial", 12),
            command=self.reset_game
        ).grid(
            row=7,
            column=0,
            columnspan=3,
            pady=5
        )


        tk.Button(
            root,
            text="Nollställ poäng",
            font=("Arial", 12),
            command=self.reset_score
        ).grid(
            row=8,
            column=0,
            columnspan=3
        )


    # -------------------------
    # Spelarens drag
    # -------------------------

    def player_move(self, index):

        if self.board[index] != "":
            return

        self.board[index] = self.human
        self.buttons[index].config(text=self.human)


        if self.check_end():
            return


        self.status.config(text="Datorn tänker...")
        self.root.after(500, self.ai_move)



    # -------------------------
    # AI-drag Tack AI.
    # -------------------------

    def ai_move(self):

        level = self.difficulty.get()


        if level == "Lätt":

            move = random.choice(
                self.available_moves()
            )


        elif level == "Normal":

            if random.random() < 0.5:
                move = random.choice(
                    self.available_moves()
                )
            else:
                move = self.best_move()


        else:

            move = self.best_move()



        self.board[move] = self.ai
        self.buttons[move].config(text=self.ai)


        if not self.check_end():
            self.status.config(text="Din tur (X)")



    # -------------------------
    # Minimax AI Tack Google
    # -------------------------

    def best_move(self):

        best_score = -math.inf
        move_choice = None


        for move in self.available_moves():

            self.board[move] = self.ai

            score = self.minimax(False)

            self.board[move] = ""


            if score > best_score:
                best_score = score
                move_choice = move


        return move_choice



    def minimax(self, maximizing):

        result = self.evaluate()


        if result is not None:
            return result



        if maximizing:

            best = -math.inf

            for move in self.available_moves():

                self.board[move] = self.ai

                score = self.minimax(False)

                self.board[move] = ""

                best = max(best, score)

            return best



        else:

            best = math.inf

            for move in self.available_moves():

                self.board[move] = self.human

                score = self.minimax(True)

                self.board[move] = ""

                best = min(best, score)

            return best



    # -------------------------
    # Spelkontroll
    # -------------------------

    def evaluate(self):

        wins = [
            (0,1,2),
            (3,4,5),
            (6,7,8),
            (0,3,6),
            (1,4,7),
            (2,5,8),
            (0,4,8),
            (2,4,6)
        ]


        for a,b,c in wins:

            if (
                self.board[a] ==
                self.board[b] ==
                self.board[c]
                != ""
            ):

                if self.board[a] == self.ai:
                    return 1

                else:
                    return -1


        if "" not in self.board:
            return 0


        return None



    def check_end(self):

        result = self.evaluate()


        if result is None:
            return False


        if result == 1:

            self.ai_score += 1

            messagebox.showinfo(
                "Resultat",
                "Datorn vann!"
            )


        elif result == -1:

            self.player_score += 1

            messagebox.showinfo(
                "Resultat",
                "Du vann!"
            )


        else:

            self.draw_score += 1

            messagebox.showinfo(
                "Resultat",
                "Oavgjort!"
            )


        self.update_score()
        self.reset_game()

        return True



    def available_moves(self):

        return [
            i for i, value in enumerate(self.board)
            if value == ""
        ]



    # -------------------------
    # Poäng
    # -------------------------

    def update_score(self):

        self.score_label.config(
            text=f"Du: {self.player_score}   "
                 f"Dator: {self.ai_score}   "
                 f"Oavgjort: {self.draw_score}"
        )



    def reset_score(self):

        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0

        self.update_score()



    # -------------------------
    # Ny omgång
    # -------------------------

    def reset_game(self):

        self.board = [""] * 9

        self.status.config(
            text="Din tur (X)"
        )


        for button in self.buttons:
            button.config(text="")



# Starta appen

root = tk.Tk()

game = TicTacToe(root)

root.mainloop()