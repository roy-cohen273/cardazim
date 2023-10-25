#!/usr/bin/env python

'''
This is a script that runs a solver for your cards.
To run it just run in cmd `solver.py`

We used npyscreen to write the interactive cli.
To read about npyscreen see documentation here:
https://npyscreen.readthedocs.io/index.html#
'''

import sys
import argparse
from pathlib import Path
from typing import List, Tuple

import npyscreen

from card import Card
from saver import Saver

from utils import check_directory


CARD_STR = 'Card {card.name} by {card.creator}'


class ChooseCardsForm(npyscreen.ActionForm):

    def get_card_by_path(self, path: Path) -> Card:
        """Deserializes and returns the card stored in the given path."""
        if not path.is_file():
            raise Exception(f"The unsolved cards directory contains somthing that isn't a file: '{path}'")
        try:
            return Card.deserialize(path.read_bytes())
        except Exception as error:
            raise Exception(f"Error while trying to deserialize: '{path}'\n{error}") from error

    def get_card_string_by_path(self, path: Path) -> Card:
        """Returns the card string of the card stored in the given path."""
        return CARD_STR.format(card=self.get_card_by_path(path))

    def get_cards(self) -> List[Tuple[str, str]]:
        """Returns a list of (card_id, card_str) tuples."""
        return [
            (path.name, self.get_card_string_by_path(path))
            for path in self.parentApp.unsolved_cards_dir.iterdir()
        ]


    def create(self):
        self.cards = self.get_cards()
        cards_strs = [card_str for card_id, card_str in self.cards]
        self.add(npyscreen.FixedText,
                 value='Welcome to your cards solver!',
                 editable=False,
                 color='STANDOUT')
        self.add(npyscreen.FixedText,
                 value='Lets solve some riddles!',
                 editable=False,
                 color='STANDOUT')
        self.nextrely += 1
        self.card = self.add(npyscreen.TitleSelectOne,
                             name='Pick a card. any card. '
                                  '[press cancel to exit]',
                             values=cards_strs,
                             exit_right=True,
                             labelColor='DEFAULT')

    def on_ok(self):
        if self.card.value:
            card_id, card_str = self.cards[self.card.value[0]]
            card_path = self.parentApp.unsolved_cards_dir / card_id
            self.parentApp.card = self.get_card_by_path(card_path)
            self.parentApp.unsolved_card_path = card_path
            self.parentApp.setNextForm('SolveCard')
        else:
            self.parentApp.setNextForm('MAIN')

    def on_cancel(self):
        self.parentApp.setNextForm(None)


class SolveCardForm(npyscreen.Form):

    def check_solution(self, card: Card, solution: str):
        '''
        checks if soltion is correct (returns True or False)
        '''
        return card.solve(solution)

    def handle_correct_solution(self, card: Card, solution: str):
        '''
        this function handles a correct solution.
        It moves the card from the unsolved cards directory to the solved cards directory.
        '''
        self.parentApp.unsolved_card_path.unlink()
        self.parentApp.unsolved_card_path = None
        self.parentApp.saver.save(card)

    def solve(self, card, solution):
        if self.check_solution(card, solution):
            self.handle_correct_solution(card, solution)
            self.parentApp.setNextForm('RightSolution')
        else:
            self.parentApp.setNextForm('WrongSolution')

    def create(self):
        self.add(npyscreen.TitleText,
                 name=CARD_STR.format(card=self.parentApp.card),
                 editable=False,
                 labelColor='STANDOUT')
        self.nextrely += 1
        self.add(npyscreen.Textfield,
                 value=self.parentApp.card.riddle,
                 editable=False)
        self.nextrely += 1
        self.solution = self.add(npyscreen.TitleText,
                                 name='Enter solution:',
                                 labelColor='DEFAULT')

    def afterEditing(self):
        self.solve(self.parentApp.card, self.solution.value)


class RightSolutionForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText,
                 name='Well Done!',
                 editable=False)
        self.nextrely += 1
        self.add(npyscreen.Textfield,
                 value=f'press ok to solve another card :)',
                 editable=False)
        self.nextrely += 1
        self.add(npyscreen.ButtonPress,
                 name='see image',
                 when_pressed_function=self.parentApp.card.image.show)

    def afterEditing(self):
        self.parentApp.card = None
        self.parentApp.setNextForm('MAIN')


class WrongSolutionForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText,
                 name='Incorrect :(',
                 editable=False,
                 labelColor='DANGER')
        self.nextrely += 1
        self.add(npyscreen.Textfield,
                 value='press ok to try again '
                       'or cancel to try a different card...',
                 editable=False)

    def on_ok(self):
        self.parentApp.setNextFormPrevious()

    def on_cancel(self):
        self.parentApp.card = None
        self.parentApp.setNextForm('MAIN')


class InteractiveCLI(npyscreen.NPSAppManaged):
    def __init__(self, unsolved_cards_dir: Path, solved_cards_dir: Path):
        super().__init__()
        self.card = None
        self.unsolved_card_path = None
        self.saver = Saver(solved_cards_dir)
        self.unsolved_cards_dir = unsolved_cards_dir

    def onStart(self):
        self.addFormClass('MAIN',
                          ChooseCardsForm,
                          name='Cards Solver')
        self.addFormClass('SolveCard',
                          SolveCardForm,
                          name='Cards Solver')
        self.addFormClass('WrongSolution',
                          WrongSolutionForm,
                          name='Cards Solver')
        self.addFormClass('RightSolution',
                          RightSolutionForm,
                          name='Cards Solver')


def get_args():
    parser = argparse.ArgumentParser(description='Present unsolved cards to the user and try to solve them.')
    parser.add_argument('unsolved_cards_dir', type=Path,
                        help='The directory to read unsolved cards from')
    parser.add_argument('solved_cards_dir', type=Path,
                        help='The directory to save solved cards to')
    return parser.parse_args()


def main():
    args = get_args()
    try:
        if check_directory(args.unsolved_cards_dir) and check_directory(args.solved_cards_dir):
            InteractiveCLI(args.unsolved_cards_dir, args.solved_cards_dir).run()
        else:
            return 1
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == "__main__":
    sys.exit(main())
