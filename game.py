# This is a Python version of the game Deal or No Deal.
import math
import random
import statistics
import time

class datarow:
    # just a super class from which game and round inherit because both are types of data
    def __init__(self, game_id, player_id, player_email, game_mode):
        self.game_id = game_id
        self.player_id = player_id
        self.player_email = player_email
        self.game_mode = game_mode


class game(datarow):
    """
    holds data about one played game
    """
    def __init__(self, game_id, player_id, player_email, game_mode, end_result, stop_round, winnings):
        super().__init__(game_id, player_id, player_email, game_mode)
        self.stop_round = stop_round
        self.end_result = end_result
        self.winnings = winnings

    def write_to_file(self):
        # append to data file
        with open("played_data.txt", "a") as f_in:
            f_in.write(str(self.game_id) + "\t" + str(self.player_id) + "\t" + self.player_email + "\t" + str(self.game_mode) + "\t" + self.end_result + "\t" + str(self.stop_round) + "\t" + str(self.winnings) + "\n")


class round(datarow):
    """
    holds data about one round played by a player
    """
    def __init__(self, game_id, player_id, player_email, game_mode, round, bankers_offer, remaining_cases):
        super().__init__(game_id, player_id, player_email, game_mode)
        self.round = round
        self.bankers_offer = bankers_offer
        self.remaining_cases = remaining_cases

    def write_to_file(self):
        # append to data file
        with open("round_data.txt", "a") as f_in:
            f_in.write(str(self.game_id) + "\t" + str(self.player_id) + "\t" + self.player_email + "\t" + str(self.game_mode) + "\t" + str(self.round) + "\t" + str(self.bankers_offer) + "\t" + str(self.remaining_cases) + "\n")


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
        if str(prize).isnumeric() or prize == 0.01: # if entry contains number (ie still in play)
            prizes_left.append(prize) # add to list
    return prizes_left


def get_bank_offer(list_of_prizes_display, game_mode, round):
    """
    This function calculates the banker's offer.
    :param list_of_prizes_display: list of prizes displayed
    :return: banker's offer
    """
    prizes_left = get_prizes_left(list_of_prizes_display)
    sum = 0
    for prize in prizes_left:
        sum += prize

    ev = sum / len(prizes_left)  # find average case value
    # basic 0.8 algorithm:
    if game_mode == 1:
        return int(ev*0.8)
    # banker's offer algorithm from Chen and John 2018
    elif game_mode == 2 or game_mode == 4:
        sd = statistics.pstdev(prizes_left)
        cv = sd/ev
        log10ev = math.log10(ev)
        log10bo = 0.195 + 0.991*log10ev - 0.057*cv - 0.037*len(prizes_left)
        bo = math.pow(10, log10bo)
        return int(bo)
    # constantly increase ratio
    else: # game mode 3
        ratio = 0.5 + round/20.0
        return int(ev*ratio)

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

def early_round_eliminate_cases(r, case_id_list_display, list_of_prizes_display, case_values):
    """
    eliminating cases during rounds 1-6
    :param r: round (int)
    :param case_id_list_display: list of cases for gui display
    :param list_of_prizes_display: list of prizes on right hand side
    :param case_values: dict w/case values
    :return: none
    """
    print("Round", r, "\n")
    if r < 6:  # first 5 rounds, when more than 1 case will have to be eliminated
        num_cases_to_eliminate = 7 - r  # number of cases decreases as rounds increase
    elif r >= 6:  # at round 6 and later
        num_cases_to_eliminate = 1  # only 1 to eliminate
    displayBoard(case_id_list_display, list_of_prizes_display)  # show board
    eliminate_case(num_cases_to_eliminate, case_id_list_display, list_of_prizes_display,
                   case_values)  # remove needed cases


def get_player_offer():
    """
    obtains player offer
    :return: player offer (int)
    """
    print("Enter an offer for the banker. If the banker accepts, you will win whatever amount of points you have entered.\
    \nIf it is too high, the banker will reject your offer.")
    player_offer = input("> ")
    while not player_offer.isnumeric(): # while non-int
        print("Please enter an integer.")
        player_offer = input("> ")
    return int(player_offer)


def deal(offer, case_values, players_case, game_id, player_id, player_email, r, game_mode):
    time.sleep(1)
    print("You won", offer, "points!")
    time.sleep(1)
    print("Your case contained", case_values[players_case])
    new_game = game(game_id, player_id, player_email, game_mode, "D", r, offer)  # create game object
    new_game.write_to_file()  # write that object into the file


def print_instructions(game_mode):
    print("How the game works: \
    \nThere are 26 briefcases on the board. Each case contains an unknown amount of points, \
ranging from 0.01 to 1,000,000 points. At the very beginning, you will choose one case to \
be your case. You will not know what is in it until the end of the game. \nPress enter to continue. ")
    userinput = input("") # ask something
    print("Every round, you will have to eliminate a number of cases from the board. \
The case will be opened, revealing the number of points it contained. By eliminating a \
case, you eliminate the possibility of winning that prize.\nPress enter to continue. ")
    userinput = input("")
    if game_mode == 4:
        print("You will make an offer at the end of every round after you have \
eliminated cases. The banker will choose to accept your deal and you will win whatever \
amount you offered (at which point the game ends), or he will decline your offer, and you must continue \
eliminating more cases from the board. When/if the banker accepts the your offer, you will \
also find out how much was in the case you originally chose.\nPress enter to continue. ")
        userinput = input("")
    else:
        print("The banker will make you an offer at the end of every round after you have \
eliminated cases. You may either choose to accept his deal and walk away with whatever \
amount he offers (at which point the game ends), or you can decline his offer and continue \
eliminating more cases from the board. When/if you accept the banker’s offer, you will \
also find out how much was in the case you originally chose.\nPress enter to continue. ")
        userinput = input("")
    print("If you keep eliminating cases until there is one left on the board, you can choose \
to either walk away with the case you originally chose or switch with the one left on the \
board. Whichever one you choose will contain your prize.\nPress enter to continue. ")
    userinput = input("")

def main():

    # WELCOME
    print("Welcome to Deal or No Deal! Zoom out (ctrl -) for a better display")
    time.sleep(1)
    # player_id = input("Please enter your USC ID: ")
    # add error checking
    # player_email = input("Please enter your USC email: ")
    # add error checking
    player_id = "7357" # test
    player_email = "test@usc.edu"
    game_id = create_game_id()

    # determine game mode
    print("Which version of the game would you like to play? \
          \nEnter 1 to play the banker's offer version (regular) \
          \nEnter 2 to play the player's offer version")
    game_mode = input("> ")
    while game_mode != "1" and game_mode != "2":
        game_mode = input("Please enter 1 or 2:\n> ")
        print(game_mode)

    if game_mode == "1":
        print("Regular Version")
        # generate 1 of 3 game modes
        game_mode = random.randint(1, 3)
    elif game_mode == "2":
        # player's offer version
        print("Player's Offer Version")
        game_mode = 4
    # random.randint(1, 4) # randomly generate

    instr = "m"  # initialize input to enter the loop
    print("Enter 1 if you would like to read about how to play the game. Enter 0 to skip the tutorial.")
    while instr != "0":
        instr = input("> ")
        if instr == "1":
            print_instructions(game_mode)
            print("Enter 0 to start. Enter 1 to display the instructions again.")
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
            early_round_eliminate_cases(r, case_id_list_display, list_of_prizes_display, case_values) # play rounds 1-6
            bank_offer = get_bank_offer(list_of_prizes_display, game_mode, r) # obtain bank offer
            if game_mode == 4: # player offer mode
                displayBoard(case_id_list_display, list_of_prizes_display)
                player_offer = get_player_offer() # obtain player offer
                offer = player_offer # so it can be saved to a new round
                print("Banker deciding...")
                drumroll()
                if player_offer < bank_offer/2: # extremely low offer
                    # deal
                    print("Offer accepted.")
                    gameOn = False # stop looping through the rounds
                    deal(player_offer, case_values, players_case, game_id, player_id, player_email, r, game_mode)
                else:
                    # no deal
                    print("Offer rejected.")
                    time.sleep(1)
            else: # bank offer mode
                displayBoard(case_id_list_display, list_of_prizes_display)
                print("Banker making offer")
                drumroll()
                print("Offer:", bank_offer)
                offer = bank_offer # so it can be saved to a new round
                dond = "m" # get into while loop
                while dond != "1" and dond != "0":
                    dond = input("Deal or No Deal? Enter 1 for Deal. Enter 0 for No Deal.\n> ")
                    if dond == "1":
                        print("You chose Deal.")
                        gameOn = False # stop looping through the rounds
                        deal(bank_offer, case_values, players_case, game_id, player_id, player_email, r, game_mode)
                    elif dond == "0":
                        print("You chose No Deal.")
                        time.sleep(1)
                        displayBoard(case_id_list_display, list_of_prizes_display)
                    else:
                        print("Please enter either 1 or 0. ")
            # save new round data
            new_round = round(game_id, player_id, player_email, game_mode, r, offer, get_prizes_left(list_of_prizes_display))
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
                    new_game = game(game_id, player_id, player_email, game_mode, "ND", r, winnings)  # create game object
                    new_game.write_to_file()  # write that object into the file
                    gameOn = False
                elif userswitch == "0":
                    print("You chose to keep your case.")
                    winnings = case_values[players_case]
                    print("You won...")
                    drumroll()
                    print(winnings, "points!")
                    new_game = game(game_id, player_id, player_email, game_mode, "ND" , r, winnings)  # create game object
                    new_game.write_to_file()  # write that object into the file
                    gameOn = False
                else:
                    print("Please enter either 1 or 0.")
        r += 1
    print("Thanks for playing :)")


if __name__ == "__main__":
    main()
