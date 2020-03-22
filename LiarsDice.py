"""
Liar's Dice Game.
"""

import numpy as np
import random
import tkinter as tk


class LiarsDice():
    """Liars Dice game through Tkinter UI"""

    def __init__(self, root):
        root.title("Liars Dice")
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Dice Control Buttons
        self.start_button = tk.Button(self.frame, text='Start Game', command=self.start_game)
        self.start_button.grid(column=0, row=0)

        self.roll_hidden_button = tk.Button(self.frame, text='Roll Hidden', command=self.roll_hidden)
        self.roll_hidden_button.grid(column=0, row=1)

        self.roll_visible_button = tk.Button(self.frame, text='Roll Visible', command=self.roll_visible)
        self.roll_visible_button.grid(column=0, row=2)

        self.pass_dice_button = tk.Button(self.frame, text='Pass Dice', command=self.pass_dice)
        self.pass_dice_button.grid(column=0, row=3)

        # Dice Viewing Frames
        self.visible_dice_title = tk.Label(self.frame, text='Visible Dice:')
        self.visible_dice_title.grid(column=1, row=1)
        self.visible_dice = tk.Label(self.frame, text='-')
        self.visible_dice.grid(column=1, row=2)

        self.show_button = tk.Button(self.frame, text='Hidden Dice:', command = self.show_dice)
        self.show_button.grid(column=2, row=1)
        self.show_state = False
        self.hidden_dice = tk.Label(self.frame, text='# # # # #')
        self.hidden_dice.grid(column=2, row=2)

        # Move Dice
        self.visible_var = tk.StringVar
        self.to_visible_field = tk.Entry(self.frame, text="To Visible", textvariable=self.visible_var)
        self.to_visible_field.grid(row=3, column=1)

        self.to_hidden_field = tk.Entry(self.frame, text='To Hidden')
        self.to_hidden_field.grid(row=3, column=2)

        self.move_button = tk.Button(self.frame, text='Move', command=self.move_dice)
        self.move_button.grid(row=4, column=1, columnspan=2)

        # Decision Buttons
        self.accept_button = tk.Button(self.frame, text='Accept', command=self.accept)
        self.accept_button.grid(column=3, row=3)

        self.bullshit_button = tk.Button(self.frame, text='Bullshit!', command=self.bullshit)
        self.bullshit_button.grid(column=3, row=4)

        # Initialize Buttons for Gameplay
        self.initialize_game()

    def initialize_game(self):
        """Initialize all state trackers"""
        self.game = False
        self.time_to_roll = False
        self.time_to_pass = False
        self.time_to_call = False
        self.transition_state()

    def transition_state(self):
        """Set all buttons according to game state."""

        start_state = 'disabled'
        roll_state = 'disabled'
        pass_state = 'disabled'
        call_state = 'disabled'

        if self.game:

            if self.time_to_roll:
                roll_state = 'normal'
                pass_state = 'normal'

            elif self.time_to_pass:
                pass_state = 'normal'

            elif self.time_to_call:
                call_state = 'normal'

            dice_text = self.dice.show_visible()
            self.visible_dice.config(text=dice_text)

        else:
            start_state = 'normal'

        self.start_button.config(state = start_state)
        self.show_button.config(state = pass_state)
        self.roll_hidden_button.config(state = roll_state)
        self.roll_visible_button.config(state = roll_state)
        self.move_button.config(state=roll_state)
        self.pass_dice_button.config(state = pass_state)
        self.accept_button.config(state = call_state)
        self.bullshit_button.config(state = call_state)

        print(pass_state)

    def set_state(self, state):
        self.time_to_roll = False
        self.time_to_call = False
        self.time_to_pass = False

        if state == 'pass':
            self.time_to_pass = True
        elif state == 'roll':
            self.time_to_roll = True
        elif state == 'call':
            self.time_to_call = True

        self.transition_state()

    def start_game(self):

        self.dice = SetOfDice()

        # Set Game State
        self.game = True
        self.set_state('pass')
        print('start game')

    def show_dice(self):
        """Toggle hidden dice"""
        self.show_state = not self.show_state
        self.update_dice_display()

    def update_dice_display(self):
        if self.show_state:
            hidden_text = self.dice.show_hidden()
        else:
            hidden_text = ''.join(['#' for i in self.dice.hidden_dice])

        self.hidden_dice.config(text=hidden_text)
        self.visible_dice.config(text=self.dice.show_visible())

    def move_dice(self):
        to_visible_dice = [int(s) for s in self.to_visible_field.get().split() if s.isdigit()]
        self.dice.move2visible(to_visible_dice)

        to_hidden_dice = [int(s) for s in self.to_hidden_field.get().split() if s.isdigit()]
        self.dice.move2hidden(to_hidden_dice)

        self.update_dice_display()

    def roll_hidden(self):
        self.dice.roll_hidden()
        self.set_state('pass')
        self.update_dice_display()
        print(self.dice.show_hidden)
        print('roll hidden')

    def roll_visible(self):
        self.dice.roll_visible()
        self.set_state('pass')
        self.update_dice_display()
        print('roll visible')

    def pass_dice(self):
        self.show_state = False
        self.update_dice_display()
        self.set_state('call')
        print('pass dice')

    def accept(self):
        self.set_state('roll')
        print('accept')

    def bullshit(self):
        self.game = False #end game
        end_message = tk.Tk()
        end_message.title("Game Over!")
        end_label = tk.Label(end_message, text='You called bullshit! Were you right?')
        end_label.grid(row=0, column=0, columnspan=2)

        heck_yea = tk.Button(end_message, text='Heck Yea', command=end_message.destroy)
        heck_yea.grid(row=1, column=0)

        dang = tk.Button(end_message, text='Dang, no :(', command=end_message.destroy)
        dang.grid(row=1, column=1)

        self.game = False
        self.set_state('')

class SetOfDice():


    def __init__(self):
        """Constructor - roll 5 dice randomly"""
        self.hidden_dice = self.roll_dice(5)
        self.visible_dice = []

    def display_public(self):
        """Display the visible dice set"""
        print('Visible Dice:', self.visible_dice)

    def display_private(self):
        print('Visible Dice:', self.visible_dice)
        print('Hidden Dice:', self.hidden_dice)

    def roll_hidden(self):
        self.hidden_dice = self.roll_dice(self.hidden_dice.__len__())
        self.display_private()

    def roll_visible(self):
        self.visible_dice = self.roll_dice(self.visible_dice.__len__())
        self.display_private()

    def show_hidden(self):
        return ' '.join([str(i) for i in self.hidden_dice])

    def show_visible(self):
        return ' '.join([str(i) for i in self.visible_dice])

    @staticmethod
    def roll_dice(num_dice):
        dice = []
        for i in range(num_dice):
            dice.append(random.randint(1,6))
        return dice

    @staticmethod
    def __move_dice(origin, destination, dice_to_move):
        # Verify that the dice_to_move are all in the origin
        valid = all([x in origin for x in dice_to_move])
        if valid:
            for d in dice_to_move:
                origin.remove(d)
                destination.append(d)
        else:
            print('You can only move dice that you have...')

    def move2visible(self, dice_to_move):
        self.__move_dice(self.hidden_dice, self.visible_dice, dice_to_move)
        self.display_private()

    def move2hidden(self, dice_to_move):
        self.__move_dice(self.visible_dice, self.hidden_dice, dice_to_move)
        self.display_private()


if __name__ == '__main__':
    root = tk.Tk()
    LiarsDice(root)
    root.mainloop()
