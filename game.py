# This is a Python version of the game Deal or No Deal.
import math
import random
import statistics
import time

import sqlite3 as sl
db = "dond.db"

id_list = []  # new id list

class datarow:
    # just a super class from which game and round inherit because both are types of data
    def __init__(self, game_id, player_id, game_mode):
        self.game_id = game_id
        self.player_id = player_id
        self.game_mode = game_mode


class game(datarow):
    """
    holds data about one played game
    """
    def __init__(self, game_id, player_id, game_mode, end_result, stop_round, winnings):
        super().__init__(game_id, player_id, game_mode)
        self.stop_round = stop_round
        self.end_result = end_result
        self.winnings = winnings

    def save(self):
        # append to data file
        # with open("played_data.txt", "a") as f_in:
        #     f_in.write(str(self.game_id) + "\t" + str(self.player_id) + "\t" + "\t" + str(self.game_mode) + "\t" +
        #                self.end_result + "\t" + str(self.stop_round) + "\t" + str(self.winnings) + "\n")
        # open a connection
        conn = sl.connect(db)
        # get a cursor
        curs = conn.execute("INSERT INTO games (game_id, player_id, game_mode, end_result, stop_round, winnings)"
                            f"VALUES ({self.game_id}, {self.player_id}, {self.game_mode}, '{self.end_result}', {self.stop_round}, {self.winnings})")
        conn.commit()
        curs.close()
        conn.close()


class _round(datarow):
    """
    holds data about one round played by a player
    """
    def __init__(self, game_id, player_id, game_mode, round, offer, remaining_cases):
        super().__init__(game_id, player_id, game_mode)
        self.round = round
        self.offer = offer
        self.remaining_cases = remaining_cases

    def save(self):
        # append to data file
        # with open("round_data.txt", "a") as f_in:
        #     f_in.write(str(self.game_id) + "\t" + str(self.player_id) + "\t" + "\t" + str(self.game_mode) + "\t" +
        #                str(self.round) + "\t" + str(self.bankers_offer) + "\t" + str(self.remaining_cases) + "\n")
        conn = sl.connect(db)
        curs = conn.execute("INSERT INTO rounds (game_id, player_id, game_mode, round, offer, remaining_cases)"
                            f"VALUES ({self.game_id}, {self.player_id}, {self.game_mode}, {self.round}, {self.offer}, '{self.remaining_cases}')")
        conn.commit()
        curs.close()
        conn.close()


class error(datarow):
    """
    holds data about a player's offer entry mistake
    """
    def __init__(self, game_id, player_id, game_mode, round, error_descr):
        super().__init__(game_id, player_id, game_mode)  # won't use game_mode
        self.round = round
        self.error_descr = error_descr

    def save(self):
        # # append to data file
        # with open("errors.txt", "a") as f_in:
        #     f_in.write(str(self.game_id) + "\t" + str(self.player_id) + "\t" + str(self.round) + "\t" +
        #                str(self.error_descr) + "\n")
        conn = sl.connect(db)
        stmt = "INSERT INTO errors (game_id, player_id, round, error_descr) " \
                f"VALUES ({self.game_id}, {self.player_id}, {self.round}, '{self.error_descr}')"
        curs = conn.execute(stmt)
        conn.commit()
        curs.close()
        conn.close()




def pick_case(case_id_list_display, game_id, player_id, game_mode, round):
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
                new_error = error(game_id, player_id, game_mode, round, "chose case #" + str(case_choice) + " not in range")
                new_error.save()
            else:
                if case_choice in case_id_list_display: # not in list of cases left
                    keepAsking = False
                    return case_choice
                else: # is not in list of cases left
                    print("Case", case_choice, "was already chosen.")
                    new_error = error(game_id, player_id, game_mode, round, "chose case #" + str(case_choice) + " not available")
                    new_error.save()
        else:
            new_error = error(game_id, player_id, game_mode, round, "chose case #" + str(case_choice) + " not numeric")
            new_error.save()
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


def displayPrizes(list_of_prizes_display):
    """
    This function prints the prizes left
    :param list_of_prizes_display: list with prizes left
    :return: nothing
    """
    print("Remaining Prizes:")
    print()
    print(list_of_prizes_display[0], '           ', list_of_prizes_display[13])
    print(list_of_prizes_display[1], '           ', list_of_prizes_display[14])
    print(list_of_prizes_display[2], '          ', list_of_prizes_display[15])
    print(list_of_prizes_display[3], '          ', list_of_prizes_display[16])
    print(list_of_prizes_display[4], '          ', list_of_prizes_display[17])
    print(list_of_prizes_display[5], '          ', list_of_prizes_display[18])
    print(list_of_prizes_display[6], '         ', list_of_prizes_display[19])
    print(list_of_prizes_display[7], '         ', list_of_prizes_display[20])
    print(list_of_prizes_display[8], '         ', list_of_prizes_display[21])
    print(list_of_prizes_display[9], '         ', list_of_prizes_display[22])
    print(list_of_prizes_display[10], '         ', list_of_prizes_display[23])
    print(list_of_prizes_display[11], '         ', list_of_prizes_display[24])
    print(list_of_prizes_display[12], '        ', list_of_prizes_display[25])
    print()


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


def eliminate_case(num_cases_to_eliminate, case_id_list_display, list_of_prizes_display, case_values, game_id, player_id, game_mode, round):
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
        eliminated_case = pick_case(case_id_list_display, game_id, player_id, game_mode, round)  # pick case
        print("You chose case # " + str(eliminated_case))
        print("Opening case:")
        drumroll()
        print("The", case_values[eliminated_case], "point prize has been eliminated from the board.")
        userinput = input("Press enter to continue.\n")
        # update displays:
        remove_id_from_display(eliminated_case, case_id_list_display)
        remove_prize_from_display(eliminated_case, list_of_prizes_display, case_values)
        if (num_cases_to_eliminate - 1 - i) != 0: # if that wasn't the last case to be chosen
            displayBoard(case_id_list_display, list_of_prizes_display)
            print("Choose", num_cases_to_eliminate - 1 - i, "more.")



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


def create_id():
    """
    This function generates a number 10000-99999 as a unique game id.
    It checks if ID was used before.
    :return: a unique ID
    """
    # with open("played_data.txt", "r") as f_in: # from past game data
    #     for line in f_in: # loop through lines
    #         id = line[:5] # set id as first 5 characters of the line
    #         id_list.append(id)

    # TODO: retrieve list of all previously used id's
    conn = sl.connect(db)
    curs = conn.execute("SELECT game_id, player_id FROM games")
    cols = curs.fetchall()
    game_ids = [cols[i][0] for i in range(len(cols))]
    player_ids = [cols[i][1] for i in range(len(cols))]
    id_list = game_ids + player_ids

    generateNew = True # true if need to generate a new id
    while generateNew: # while id has been used
        id = random.randrange(10000, 100000)  # get a number 10000-99999
        if id in id_list:
            generateNew = True
        else: # unique id was generated
            return id
            generateNew = False # no need to generate another one


def early_round_eliminate_cases(r, case_id_list_display, list_of_prizes_display, case_values, game_id, player_id, game_mode):
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
                   case_values, game_id, player_id, game_mode, r)  # remove needed cases


def get_player_offer(case_values, game_id, player_id, round):
    """
    obtains player offer
    :return: player offer (int)
    """
    userinput = input("You will make an offer to the banker. Press enter to continue.\n")
    print("Enter an offer for the banker. If the banker accepts, you will win whatever amount of points you have entered.\
    \nIf your offer is too high, the banker will reject your offer.")
    player_offer = input("> ")
    while not player_offer.isnumeric(): # while non-int
        print("Please enter an integer.")
        player_offer = input("> ")
    while (int(player_offer) > max(case_values.values())) or (int(player_offer) < min(case_values.values())):
        if int(player_offer) > max(case_values.values()): # greater than max possible prize
            new_error = error(game_id, player_id, 4, round, "player offer > max prize = " +
                              str(max(case_values.values())))
            new_error.save()
            print("Your offer must be less than the biggest prize left in play. Try again.")
            player_offer = input("> ")
        elif int(player_offer) < min(case_values.values()): # less than min possible prize
            new_error = error(game_id, player_id, 4, round, "player offer < min prize = " +
                              str(min(case_values.values())))
            new_error.save()
            print("Your offer must be greater than the smallest prize left in play. Try again.")
            player_offer = input("> ")
    return int(player_offer)


def deal(offer, case_values, players_case, game_id, player_id, r, game_mode):
    time.sleep(1)
    print("You won", offer, "points!")
    time.sleep(1)
    print("Your case contained", case_values[players_case])
    print()
    new_game = game(game_id, player_id, game_mode, "D", r, offer)  # create game object
    new_game.save()  # write that object into the file


def print_instructions(game_mode):
    print("\nHere's how the game works: \
    \nThere are 26 briefcases on the board. Each case contains an unknown amount of points,\n \
ranging from 0.01 to 1,000,000 points. An unopened case will look like this:")
    print(" ---- ")
    print("| 19 |")
    print(" ---- ")
    print("The remaining prizes will be displayed to the right of the cases.")
    print("Press enter to continue.")
    userinput = input("")
    print("At the very beginning, you will choose one case to be your case. \n\
You will not know what is in it until the end of the game.\n \
It will be labeled on the board with an asterisk:")
    print(" --- ")
    print("| * |")
    print(" --- ")
    print("Press enter to continue. ")
    userinput = input("") # ask something
    print("Every round, you will have to eliminate a number of cases from the board.\n\
The case will be opened, revealing the number of points it contained. By eliminating a\n\
case, you eliminate the possibility of winning that prize.\nPress enter to continue. ")
    userinput = input("")
    if game_mode == 4:
        print("PLAYER'S OFFER MODE: You will make an offer at the end of every round after\nyou have \
eliminated cases. The banker will choose to accept\nyour deal and you will win whatever \
amount you offered (at which point the game ends),\nor he will decline your offer, and you must continue \
eliminating more cases from the board.\nPress enter to continue")
        userinput = input("")
        print("When/if the banker accepts the your offer, you will\n \
also find out how much was in the case you originally chose.\nPress enter to continue. ")
        userinput = input("")
    else:
        print("BANKER'S OFFER MODE: The banker will make you an offer at the end of\nevery round after you have \
eliminated cases. You may either choose \nto accept his deal and walk away with whatever \
amount he offers (at which point the game ends), \nor you can decline his offer and continue \
eliminating more cases from the board.\nPress enter to continue")
        userinput = input("")
        print("When/if you accept the banker’s offer, you will \
also find out how much was in the case you originally chose.\nPress enter to continue. ")
        userinput = input("")
    print("If you keep eliminating cases until there is one left on the board, \nyou can choose \
to either walk away with the case you originally chose or \nswitch with the one left on the \
board. Whichever one you choose will contain your prize winnings. \
\nPress enter to start the game. ")
    userinput = input("")


def play(game_mode, first_time, player_id):
    print("Press enter to begin the ", end="")
    if first_time:
        print("first", end="")
    else:
        print("second", end="")
    print(" game.")
    userinput = input("")
    game_id = create_id()
    if game_mode == 1:
        print("You are now playing the banker's offer version")
        game_mode = random.randint(1, 3)  # pick from 3 algorithms to generate banker's offer
    elif game_mode == 2:
        print("You are now playing the player's offer version.")
        game_mode = 4 # no alg
    time.sleep(1)

    print_instructions(game_mode)

    # INITIALIZE STUFF

    # create a list of case id's
    case_id_list = []  # will contain ints 1-26
    case_id_list = [i for i in range(1, 27)] # populate with ints 1-26


    # create copy for display
    case_id_list_display = [case_id for case_id in case_id_list]
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
    players_case = pick_case(case_id_list_display, game_id, player_id, game_mode, 0)
    print("You chose case #", players_case, "\n")
    userinput = input("Press enter to begin.\n")
    if players_case < 10:
        case_id_list_display[case_id_list_display.index(players_case)] = "*"  # to distinguish it in display
    else:
        case_id_list_display[case_id_list_display.index(players_case)] = "* " # adjust for 2 digits
    remove_id_from_display(players_case, case_id_list_display)

    # START ROUNDS

    r = 1  # initialize round number
    gameOn = True  # stays true until player accepts deal or there is one case left
    while gameOn:
        if r < 10:
            early_round_eliminate_cases(r, case_id_list_display, list_of_prizes_display, case_values,
                                        game_id, player_id, game_mode)  # play rounds 1-6
            bank_offer = get_bank_offer(list_of_prizes_display, game_mode, r)  # obtain bank offer
            if game_mode == 4:  # player offer mode
                displayPrizes(list_of_prizes_display)
                player_offer = get_player_offer(case_values, game_id, player_id, r)  # obtain player offer
                offer = player_offer  # so it can be saved to a new round
                print("Banker deciding...")
                drumroll()
                if player_offer < bank_offer / 3:  # extremely low offer
                    # deal
                    print("Offer accepted.")
                    winnings = player_offer
                    gameOn = False  # stop looping through the rounds
                    deal(player_offer, case_values, players_case, game_id, player_id, r, game_mode)
                else:
                    # no deal
                    print("Offer rejected.")
                    time.sleep(1)
            else:  # bank offer mode
                displayPrizes(list_of_prizes_display)
                print("Banker making offer")
                drumroll()
                print("Offer:", bank_offer)
                offer = bank_offer  # so it can be saved to a new round
                dond = "m"  # get into while loop
                while dond != "1" and dond != "0":
                    dond = input("Deal or No Deal? Enter 1 for Deal. Enter 0 for No Deal.\n> ")
                    if dond == "1":
                        print("You chose Deal.")
                        winnings = bank_offer
                        gameOn = False  # stop looping through the rounds
                        deal(bank_offer, case_values, players_case, game_id, player_id, r, game_mode)
                    elif dond == "0":
                        print("You chose No Deal.")
                        userinput = input("Press enter to continue.\n")
                        displayBoard(case_id_list_display, list_of_prizes_display)
                    else:
                        new_error = error(game_id, player_id, game_mode, r, "entered neither 1 or 0 for DOND")
                        new_error.save()
                        print("Please enter either 1 or 0. ")
            # save new round data
            new_round = _round(game_id, player_id, game_mode, r, offer, get_prizes_left(list_of_prizes_display))
            new_round.save()
        else:
            # find last case:
            for case_id in case_id_list_display:
                if str(case_id).isnumeric():
                    lastcase = case_id
            print("There is 1 case left on the board, case # " + str(lastcase) + " . You chose case #", players_case,
                  "at the beginning.")
            print(
                "Do you wish to walk away with the amount in your case or switch it with case # " + str(lastcase) + "?")
            userswitch = "m"
            while userswitch != "1" and userswitch != "0":  # keep asking until user enters either 1 or 0
                userswitch = input("Enter 1 to switch or enter 0 to keep your case.\n> ")
                if userswitch == "1":
                    print("Switching cases...")
                    players_case = lastcase
                    print("Your case is now case # " + str(players_case))
                    winnings = case_values[players_case]
                    print("You won...")
                    drumroll()
                    print(winnings, "points!")
                    new_game = game(game_id, player_id, game_mode, "ND", r, winnings)  # create game object
                    new_game.save()  # write that object into the file
                    gameOn = False
                elif userswitch == "0":
                    print("You chose to keep your case.")
                    winnings = case_values[players_case]
                    print("You won...")
                    drumroll()
                    print(winnings, "points!")
                    new_game = game(game_id, player_id, game_mode, "ND", r, winnings)  # create game object
                    new_game.save()  # write that object into the file
                    gameOn = False
                else:
                    print("Please enter either 1 or 0.")
        r += 1
    print("You have finished playing the ", end="")
    if game_mode == 4:
        print("player's ", end="")
    else:
        print("banker's ", end="")
    print("offer mode. ")
    if first_time:
        print("You will now play the ", end="")
        if game_mode == 4:
            print("banker's ", end="")
        else:
            print("player's ", end="")
        print("offer mode. ")
        time.sleep(2)
    return winnings, game_id


def print_intro():
    print("\nWe thank you for participating in our study. \nToday you will play 2 modified versions of Deal or No Deal. \
Instructions on how to play will follow. \nClick the blank space below so that a blinking cursor appears and press enter to continue.")
    userinput = input("")
    print("Playing this game is voluntary, and you may stop at any time, though you will not receive\n\
compensation unless you reach the end of both games.\nPress enter to continue.")
    userinput = input("")
    print("In each game, you can win up to 1,000,000 points. Your final score will be divided by 100,000,\n\
converted to dollars, and added to your compensation for your participation.\nFor example, if you win a total \
of 623,211 points, you will be awarded an additional $6.23.\nPress enter to continue.")
    userinput = input("")
    print("Please do not refresh the web browser page or click the \"Stop\" button while you play.\
\nDoing so will cause you to lose your progress.\nPress enter to continue.")
    userinput = input("")

def main():
    # WELCOME
    print("Welcome to Deal or No Deal! Please zoom out in your browser (ctrl -) for a better display")
    time.sleep(1)
    print_intro()

    player_id = create_id()

    game_mode1 = random.randint(1, 2)  # randomly generate order in which to play
    if game_mode1 == 1:
        game_mode2 = 2
    elif game_mode1 ==2:
        game_mode2 = 1

    # play the games
    winnings1, game_id1 = play(game_mode1, True, player_id)
    winnings2, game_id2 = play(game_mode2, False, player_id)

    # concluding message.
    print("This concludes your participation in the study. Because you won", winnings1, "points during the first game\n\
and", winnings2, "in the second game for a total of", str(winnings1+winnings2), "points, you will be compensated\nan \
additional $" + str(round(0.00001*(winnings1+winnings2),2)) + ". Thanks for playing!")
    time.sleep(1)
    print("Your player ID was saved as", player_id, "and your game ID's were saved as", game_id1, "and", str(game_id2)
          + ". \nThese serve as confirmation that you have completed two games. ")

if __name__ == "__main__":
    main()
