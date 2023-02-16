# This is a Python version of the game Deal or No Deal.

import random
import time


def pick_case(case_id_list_display):
    """
    this function returns a case chosen by the player
    :param case_id_list_display: list of cases left
    :return: chosen case
    """
    print("Enter a case:")
    keepAsking = True
    while keepAsking:
        case_choice = input("> ").strip() # remove whitespace
        if case_choice.isnumeric(): # if a number was entered
            case_choice = int(case_choice) # convert to int
            if case_choice < 1 or case_choice > 26: # outside case id range
                print("Please enter a valid number.")
            else:
                if case_choice in case_id_list_display: # not in list of cases left
                    keepAsking = False
                    return case_choice
                else: # is not in list of cases left
                    print("Case", case_choice, "was already chosen.")
        else:
            print("Please enter a valid number.")


def remove_id_from_display(chosen_case, case_id_list_display):
    """
    This function replaces the case id in the display with a space
    :param chosen_case: id of case choen
    :param case_id_list_display:
    :return: nothing
    """
    for id in case_id_list_display: # go through every id in the list
        if id == chosen_case: # find the one that matches players_case
            if id < 10:
                case_id_list_display[case_id_list_display.index(id)] = " " # one char, one space
            else:
                case_id_list_display[case_id_list_display.index(id)] = "  " # 2 chars, 2 spaces


def remove_prize_from_display(chosen_case, list_of_prizes_display, case_values):
    """
    this function replaces prizes in the display with spaces
    :param chosen_case: case id
    :param list_of_prizes_display: the thing being displayed
    :param case_values: to match case id to prize value
    :return: none
    """
    value_to_remove = case_values[chosen_case] # whatever prize at the case id in the dictionary
    for prize in list_of_prizes_display: # loop through prizes in the display
        if prize == value_to_remove: # find the prize
            spacestring = ""
            for i in range(len(str(prize))):
                spacestring += " " # make the string the same number of characters as the prize it's replacing
            list_of_prizes_display[list_of_prizes_display.index(prize)] = spacestring # replace it with a space


def displayBoard(case_id_list_display, list_of_prizes_display):
    """
    This function prints the board and prizes left
    This was adapted from the function written by @DrewSkotarczak on replit
    :param case_id_list_display: list with case id's left
    :param list_of_prizes_display: list with prizes left
    :return: nothing
    """
    print("Board:\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tRemaining Prizes:")
    print(' -----      -----      -----      -----      -----      -----      ----- ')
    print('| ', case_id_list_display[0], ' |    | ', case_id_list_display[1], ' |    | ', case_id_list_display[2], ' |    | ',
    case_id_list_display[3], ' |    | ', case_id_list_display[4], ' |    | ', case_id_list_display[5], ' |    | ',
    case_id_list_display[6], ' |         ', list_of_prizes_display[0], '           ', list_of_prizes_display[13])
    print(' -----      -----      -----      -----      -----      -----      -----             ', list_of_prizes_display[1],
          '           ', list_of_prizes_display[14])
    print('                                                                                     ', list_of_prizes_display[2],
          '          ', list_of_prizes_display[15])
    print('      -----      -----      ------     ------     ------     ------                 ', list_of_prizes_display[3],
          '          ', list_of_prizes_display[16])
    print('     | ', case_id_list_display[7], ' |    | ', case_id_list_display[8], ' |    | ', case_id_list_display[9], ' |   | ',
          case_id_list_display[10], ' |   | ', case_id_list_display[11], ' |   | ', case_id_list_display[12], ' |                ',
          list_of_prizes_display[4], '          ', list_of_prizes_display[17])
    print('      -----      -----      ------     ------     ------     ------                 ', list_of_prizes_display[5],
          '          ', list_of_prizes_display[18])
    print('                                                                                    ', list_of_prizes_display[6],
          '         ', list_of_prizes_display[19])
    print(' ------     ------     ------     ------     ------     ------     ------          ', list_of_prizes_display[7],
          '         ', list_of_prizes_display[20])
    print('| ', case_id_list_display[13], ' |   | ', case_id_list_display[14], ' |   | ', case_id_list_display[15], ' |   | ',
          case_id_list_display[16], ' |   | ', case_id_list_display[17], ' |   | ', case_id_list_display[18], ' |   | ',
          case_id_list_display[19], ' |         ', list_of_prizes_display[8], '         ', list_of_prizes_display[21])
    print(' ------     ------     ------     ------     ------     ------     ------          ', list_of_prizes_display[9],
          '         ', list_of_prizes_display[22])
    print('                                                                                   ', list_of_prizes_display[10],
          '         ', list_of_prizes_display[23])
    print('      ------     ------     ------     ------     ------     ------                ', list_of_prizes_display[11],
          '         ', list_of_prizes_display[24])
    print('     | ', case_id_list_display[20], ' |   | ', case_id_list_display[21], ' |   | ', case_id_list_display[22], ' |   | ',
          case_id_list_display[23], ' |   | ', case_id_list_display[24], ' |   | ', case_id_list_display[25], ' |               ',
          list_of_prizes_display[12], '        ', list_of_prizes_display[25])
    print('      ------     ------     ------     ------     ------     ------ ')


def fill_case_values(case_id_list, list_of_prizes, case_values):
    """
    randomly assigns each case id to a prize and saves it to case_values dictionary
    :param case_id_list: ints 1 to 26
    :param list_of_prizes: list of prizes
    :param case_values: empty dictionary
    :return: none
    """
    list_of_prizes_copy = [] # create a copy so that the prizes don't actually get removed from list_of_prizes
    for prize in list_of_prizes:
        list_of_prizes_copy.append(prize)
    for case_id in case_id_list: # go through every case id in the list
        value = random.choice(list_of_prizes_copy) # randomly select one of the prizes
        case_values[case_id] = value # assign that value to the case id
        list_of_prizes_copy.remove(value) # remove that value from the list of prizes so it doesn't get picked again


def eliminate_case(num_cases_to_eliminate, case_id_list_display, list_of_prizes_display, case_values):
    """
    this function is called everytime the player chooses a case to remove from the board
    :param num_cases_to_eliminate: number of times a case will be chosen
    :param case_id_list_display: for display
    :param list_of_prizes_display: for display
    :param case_values: for display
    :return: none
    """
    print("You must choose ", num_cases_to_eliminate, "case(s) to eliminate this round")
    for i in range(num_cases_to_eliminate):  # do this num_cases_to_eliminate times
        eliminated_case = pick_case(case_id_list_display)  # pick case
        print("You chose case # " + str(eliminated_case))
        print("Opening case:")
        drumroll()
        print(case_values[eliminated_case], "has been eliminated.")
        time.sleep(1)
        # update displays:
        remove_id_from_display(eliminated_case, case_id_list_display)
        remove_prize_from_display(eliminated_case, list_of_prizes_display, case_values)
        if (num_cases_to_eliminate - 1 - i) != 0: # if that wasn't the last case to be chosen
            print("Choose", num_cases_to_eliminate - 1 - i, "more.")
            displayBoard(case_id_list_display, list_of_prizes_display)


def get_prizes_left(list_of_prizes_display):
    """
    This function creats a list of remaining prizes without the blank spaces
    :param list_of_prizes_display: list of remaining prizes with blank spaces
    :return: prizes_left, no blank spaces
    """
    prizes_left = []
    for prize in list_of_prizes_display: # go through display prize list
        if str(prize).isnumeric(): # if entry contains number (ie still in play)
            prizes_left.append(prize) # add to list
    return prizes_left


def get_offer(list_of_prizes_display):
    """
    This function calculates the banker's offer.
    :param list_of_prizes_display: list of prizes displayed
    :return: banker's offer
    """
    prizes_left = get_prizes_left(list_of_prizes_display)
    sum = 0
    for prize in prizes_left:
        sum += prize

    # basic 0.8 algorithm:
    avg = sum / len(prizes_left) # find average case value
    avg *= 0.8
    return int(avg)


class datarow:
    # just a super class from which game and round inherit since both are types of data
    def __init__(self, game_id, player_id, player_email):
        self.game_id = game_id
        self.player_id = player_id
        self.player_email = player_email


class game(datarow):
    """
    holds data about one played game
    """
    def __init__(self, game_id, player_id, player_email, end_result, stop_round, winnings):
        super().__init__(game_id, player_id, player_email)
        self.stop_round = stop_round
        self.end_result = end_result
        self.winnings = winnings

    def write_to_file(self):
        # append to data file
        with open("played_data.txt", "a") as f_in:
            f_in.write(str(self.game_id) + "\t" + str(self.player_id) + "\t" + self.player_email + "\t" + self.end_result + "\t" + str(self.stop_round) + "\t" + str(self.winnings) + "\n")


class round(datarow):
    """
    holds data about one round played by a player
    """
    def __init__(self, game_id, player_id, player_email, round, bankers_offer, remaining_cases):
        super().__init__(game_id, player_id, player_email)
        self.round = round
        self.bankers_offer = bankers_offer
        self.remaining_cases = remaining_cases

    def write_to_file(self):
        # append to data file
        with open("round_data.txt", "a") as f_in:
            f_in.write(str(self.game_id) + "\t" + str(self.player_id) + "\t" + self.player_email + "\t" + str(self.round) + "\t" + str(self.bankers_offer) + "\t" + str(self.remaining_cases) + "\n")


def drumroll():
    # creates a little countdown for dramatic effect
    for i in range(3):
        time.sleep(0.25)
        print(".")
        time.sleep(0.25)


def create_game_id():
    """
    This function generates a number 10000-99999 as a unique game id.
    It checks if ID was used before.
    :return: a unique ID
    """
    id_list = [] # new list
    with open("played_data.txt", "r") as f_in: # from past game data
        for line in f_in: # loop through lines
            id = line[:5] # set id as first 5 characters of the line
            id_list.append(id)

    generateNew = True # true if need to generate a new id
    while generateNew: # while id has been used
        id = random.randrange(10000, 100000)  # get a number 10000-99999
        if id in id_list:
            generateNew = True
        else: # unique id was generated
            return id
            generateNew = False # no need to generate another one

def main():
    # WELCOME
    print("Welcome to Deal or No Deal!")
    time.sleep(1)
    player_id = input("Please enter your USC ID: ")
    player_email = input("Please enter your USC email: ")
    game_id = create_game_id()

    instr = "m" # initialize input to enter the loop
    print("Enter 1 if you would like to read about how to play the game. Enter 0 to skip the tutorial.")
    while instr != "0":
        instr = input("> ")
        if instr == "1":
            print("[instructions].\nEnter 0 to start. ") # fill in later
        elif instr == "0":
            print("Let's play Deal or No Deal!") # start game
            time.sleep(1)
        else:
            print("Please enter a valid input. ")

    # INITIALIZE STUFF

    # create a list of case id's
    case_id_list = [] # will contain ints 1-26
    for i in range(1, 27):
        case_id_list.append(i) # populate with ints 1-26

    # create copy for display
    case_id_list_display = []
    for case_id in case_id_list:
        case_id_list_display.append(case_id)
        # in this copy, the case id's will be replaced by spaces once chosen by the player

    list_of_prizes = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 5000, 10000, 25000, 50000, 75000,
                      100000, 200000, 300000, 400000, 500000, 750000, 1000000]
    case_values = {}  # dict with key = case_id, value=prize values
    fill_case_values(case_id_list, list_of_prizes, case_values)  # randomly populate cases

    list_of_prizes_display = []  # create a copy so that the prizes don't actually get removed from list_of_prizes
    for prize in list_of_prizes:
        list_of_prizes_display.append(prize)

    # player picks case
    displayBoard(case_id_list_display, list_of_prizes_display)
    print("Pick your case. You'll keep this case for the whole game.")
    players_case = pick_case(case_id_list_display)
    print("You chose case #", players_case, "\n")
    time.sleep(1)
    if players_case < 10:
        case_id_list_display[case_id_list_display.index(players_case)] = "*"  # to distinguish it in display
    else:
        case_id_list_display[case_id_list_display.index(players_case)] = "* "
    remove_id_from_display(players_case, case_id_list_display)

    # START ROUNDS

    r = 1 # initialize round number
    gameOn = True # stays true until player accepts deal or there is one case left
    while gameOn:
        if r < 10:
            print("Round", r, "\n")
            if r < 6: # first 5 rounds, when more than 1 case will have to be eliminated
                num_cases_to_eliminate = 7-r # number of cases decreases as rounds increase
            elif r >= 6: # at round 6 and later
                num_cases_to_eliminate = 1 # only 1 to eliminate
            displayBoard(case_id_list_display, list_of_prizes_display) # show board
            eliminate_case(num_cases_to_eliminate, case_id_list_display, list_of_prizes_display, case_values) # remove needed cases
            # works up to here

            # figure out banker's offer
            offer = get_offer(list_of_prizes_display)
            print("Banker making offer")
            drumroll()
            print("The banker offers you", offer, "points.")

            dond = "m" # get into while loop
            while dond != "1" and dond != "0":
                dond = input("Deal or No Deal? Enter 1 for Deal. Enter 0 for No Deal.\n> ")
                if dond == "1":
                    gameOn = False # stop looping through the rounds
                    print("You chose Deal.")
                    time.sleep(1)
                    print("You won", offer, "points!")
                    new_game = game(game_id, player_id, player_email, "D", r, offer) # create game object
                    new_game.write_to_file() # write that object into the file
                elif dond == "0":
                    print("You chose No Deal.")
                    time.sleep(1)
                    displayBoard(case_id_list_display, list_of_prizes_display)
                else:
                    print("Please enter either 1 or 0. ")
            new_round = round(game_id, player_id, player_email, r, offer, get_prizes_left(list_of_prizes_display))
            new_round.write_to_file()
        else:
            # find last case:
            for case_id in case_id_list_display:
                if str(case_id).isnumeric():
                    lastcase = case_id
            print("There is 1 case left on the board, case # " + str(lastcase) + " . You chose case #", players_case, "at the beginning.")
            print("Do you wish to walk away with the amount in your case or switch it with case # " + str(lastcase) + "?")
            userswitch = "m"
            while userswitch != "1" and userswitch != "0": # keep asking until user enters either 1 or 0
                userswitch = input("Enter 1 to switch or enter 0 to keep your case.\n> ")
                if userswitch == "1":
                    print("Switching cases...")
                    players_case = lastcase
                    print("Your case is now case # " + str(players_case))
                    winnings = case_values[players_case]
                    print("You won...")
                    drumroll()
                    print(winnings, "points!")
                    new_game = game(game_id, player_id, player_email, "ND", r, winnings)  # create game object
                    new_game.write_to_file()  # write that object into the file
                    gameOn = False
                elif userswitch == "0":
                    print("You chose to keep your case.")
                    winnings = case_values[players_case]
                    print("You won...")
                    drumroll()
                    print(winnings, "points!")
                    new_game = game(game_id, player_id, player_email, "ND" , r, winnings)  # create game object
                    new_game.write_to_file()  # write that object into the file
                    gameOn = False
                else:
                    print("Please enter either 1 or 0.")
        r += 1
    print("Thanks for playing :)")


if __name__ == "__main__":
    main()
