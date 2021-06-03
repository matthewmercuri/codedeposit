import numpy as np
from random import randint


def monty_hall_sim(games=1000, doors=3, switch=True):
    wins = 0
    losses = 0

    for i in range(1, games+1):
        chosen_door = randint(1, doors)
        prize_door = randint(1, doors)

        doors_array = np.zeros(doors)
        doors_array[prize_door-1] = 1

        choice_array = np.zeros(doors)
        choice_array[chosen_door-1] = 1

        if switch is True:
            option_door = _option_door(prize_door, chosen_door, doors)
            choice_array = np.zeros(doors)
            choice_array[option_door-1] = 1

        if np.array_equal(choice_array, doors_array):
            wins += 1
        else:
            losses += 1

    print(f'Out of {games} games played:')
    print(f'There were {wins} games won ({losses} losses)')
    print(f'For a winning percentage of %{round((wins / games), 2) * 100}')


def _option_door(prize_door, chosen_door, doors):

    if prize_door != chosen_door:
        option_door = prize_door
    else:
        valid_door = False
        while valid_door is False:
            option_door = randint(1, doors)
            if option_door == chosen_door:
                valid_door = False
            else:
                valid_door = True

    return option_door


monty_hall_sim()
