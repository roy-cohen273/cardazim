#!/usr/bin/env python

'''
This is a script that runs a solver for your cards.
To run it just run in cmd `solver.py`.
Feel free to change it however you like.
Add your code in the marked sections.
Without your code it doesn't really do anything.
(You can run it before adding your code just to see what happens...)

We used npyscreen to write the interactive cli.
To read about npyscreen see documentation here:
https://npyscreen.readthedocs.io/index.html#

Final notes:
We assume your cards have name, creator and riddle attributes
(card.name, card.creator and card.riddle should work).
If they don't, you might have to change this script a little.
Also:
Currently this script doesn't receive any arguments,
but you might have to add some (like the directory of your cards or something).
But you already know how to do that, so...
Good Luck!
'''

import npyscreen
# add your imports here!


CARD_STR = 'Card {card.name} by {card.creator}'

#####################################################################
####################### DELETE THIS SECTION #########################
#####################################################################


class ExampleCard:
    def __init__(self, name, creator, riddle):
        self.name = name
        self.creator = creator
        self.riddle = riddle


EXAMPLE_CARDS = [ExampleCard(name=str(n),
                             creator='Me',
                             riddle='Some riddle')
                 for n in range(1, 25)]


#####################################################################
#####################################################################
#####################################################################


class ChooseCardsForm(npyscreen.ActionForm):

    ###########################################################
    ####################### YOUR CODE #########################
    ###########################################################

    def get_cards(self):
        '''
        returns list of unsolved cards.
        replace this method with your own code
        (read files from memory etc.)
        '''
        return EXAMPLE_CARDS

    ###########################################################
    ##################### END OF YOUR CODE ####################
    ###########################################################

    def create(self):
        self.cards = self.get_cards()
        self.cards_strs = [CARD_STR.format(card=card)
                           for card in self.cards]
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
                             values=self.cards_strs,
                             exit_right=True,
                             labelColor='DEFAULT')

    def on_ok(self):
        if self.card.value:
            self.parentApp.card = self.cards[self.card.value[0]]
            self.parentApp.setNextForm('SolveCard')
        else:
            self.parentApp.setNextForm('MAIN')

    def on_cancel(self):
        self.parentApp.setNextForm(None)


class SolveCardForm(npyscreen.Form):

    ###########################################################
    ####################### YOUR CODE #########################
    ###########################################################

    def check_solution(self, card, solution):
        '''
        checks if soltion is correct (returns True or False)
        replace this with your own code.
        '''
        return solution != 'wrong solution'

    def handle_correct_solution(self, card, solution):
        '''
        this function handles a correct solution
        replace this with your own code.
        (move card to solved card etc.)
        '''
        print(f'{CARD_STR.format(card=card)} was solved correctly!')
        print(f'The solution was: {solution}')

    ###########################################################
    ##################### END OF YOUR CODE ####################
    ###########################################################

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
    card = None

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


if __name__ == "__main__":
    App = InteractiveCLI().run()
