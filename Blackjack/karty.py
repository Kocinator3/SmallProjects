import random
import time
import pyfiglet
allcards = []
def reset():
    global game, first_player, second_player, first_player_stop, first_player_cards, second_player_cards, second_player_stop, just_stopped
    game = True
    just_stopped = True
    first_player = True
    second_player = False
    first_player_stop = False
    first_player_cards = []
    second_player_cards = []
    second_player_stop = False
    print("\033[?1049h")
    print("\033[2J", end="")
    global allcards
    allcards = []
    for i in range(4):
        for ii in range(1,14):
            if i == 0:
                allcards.append(["listy", ii, False])
            if i == 1:
                allcards.append(["srdce", ii, False])
            if i == 2:
                allcards.append(["kříže", ii, False])
            if i == 3:
                allcards.append(["káry", ii, False])

    random.shuffle(allcards)
def clear_screen():
    print("\033[2J", end="")
def quit_game():
    global game
    game = False
def draw_card(hand):
    for card in allcards:
        if card[2] == False:
            card[2] = True
            hand.append(card)
            break
def in_hand(hand, card_package = 0, hide = False, winner = None):
    global first, second, third, fourth, fifth, sixth
    first = ""
    second = ""
    third = ""
    fourth = ""
    fifth = ""
    sixth = ""
    if card_package > 0:
        first += "┌——————┐"
        second += "|xxxxxx|"
        third += "|xxxxxx|"
        fourth += "|xxxxxx|"
        fifth += "|xxxxxx|"
        sixth += "└——————┘"
        for i in range(card_package-1):
            first += "—┐"
            second += "x|"
            third += "x|"
            fourth += "x|"
            fifth += "x|"
            sixth += "—┘"
        first += "\t"
        second += "\t"
        third += "\t"
        fourth += "\t"
        fifth += "\t"
        sixth += "\t"
    else:
        for i in range(2):
            first += "\t"
            second += "\t"
            third += "\t"
            fourth += "\t"
            fifth += "\t"
            sixth += "\t"
    
    if not hand == [] and hide == False:
        for card in hand[:-1]:
            if card[0] == "listy":
                color = "♠"
            elif card[0] == "srdce":
                color = "\033[91m" + "♥" + "\033[0m"
            elif card[0] == "kříže":
                color = "♣"
            elif card[0] == "káry":
                color = "\033[91m" + "♦" + "\033[0m"
            if card[1] == 1:
                number = "A"
            elif card[1] == 11:
                number = "J"
            elif card[1] == 12:
                number = "Q"
            elif card[1] == 13:
                number = "K"
            else:
                number = card[1]
            first += "┌———"
            if not number == 10:
                second += "| " + str(number) + " "
            else: second += "| " + str(number) + "" 
            third += "|   "
            fourth += "|   "
            fifth += "| " + str(color) + " "
            sixth += "└———"
        color = hand[len(hand) - 1][0]
        number = hand[len(hand) - 1][1]
        if color == "listy":
            color = "♠"
        elif color == "srdce":
            color = "\033[91m" + "♥" + "\033[0m"
        elif color == "kříže":
            color = "♣"
        elif color == "káry":
            color = "\033[91m" + "♦" + "\033[0m"
        if number == 1:
            number = "A"
        elif number == 11:
            number = "J"
        elif number == 12:
            number = "Q"
        elif number == 13:
            number = "K"
        first += "┌——————┐"
        if not number == 10:
            second += "| " + str(number) + "  " + str(color) + " |"
        else: second += "| " + str(number) + " " + str(color) + " |"
        third += "|      |"
        fourth += "|      |"
        if not number == 10:
            fifth += "| " + str(color) + "  " + str(number) + " |"
        else: fifth += "| " + str(color) + " " + str(number) + " |"
        sixth += "└——————┘"
    if hide == True and not hand == []:
        for card in hand[:-1]:
            first += "┌———"
            second += "|xxx"
            third += "|xxx"
            fourth += "|xxx"
            fifth += "|xxx"
            sixth += "└———"
        first += "┌——————┐"
        second += "|xxxxxx|"
        third += "|xxxxxx|"
        fourth += "|xxxxxx|"
        fifth += "|xxxxxx|"
        sixth += "└——————┘"
    if not winner == None:
        if winner == 1 and two_players:
            second +="\t\t\t\033[41m ____ _  _____  _          _  _         _      \033[0m"
            third += "\t\t\t\033[41m|_ | |_)(_  |  |_)|  /\\\\_/|_ |_) \\    // \\|\\ | \033[0m"
            fourth += "\t\t\t\033[41m| _|_| \\__) |  |  |_/--\\| |_ | \\  \\/\\/ \\_/| \\| \033[0m"
        if winner == 1 and not two_players:
            second +="\t\t\t\033[42m    _                _        _      \033[0m"
            third += "\t\t\t\033[42m\\_// \\| | |_| /\\\\  /|_ \\    // \\|\\ | \033[0m"
            fourth += "\t\t\t\033[42m | \\_/|_| | |/--\\\\/ |_  \\/\\/ \\_/| \\| \033[0m"
        if winner == 2 and two_players:
            second += "\t\t\t\033[44m __ _  _ _      _   _          _  _         _      \033[0m"
            third += "\t\t\t\033[44m(_ |_ / / \\|\\ || \\ |_)|  /\\\\_/|_ |_) \\    // \\|\\ | \033[0m"
            fourth += "\t\t\t\033[44m__)|_ \\_\\_/| \\||_/ |  |_/--\\| |_ | \\  \\/\\/ \\_/| \\| \033[0m"
        if winner == 2 and not two_players:
            second += "\t\t\t\033[41m___   _  _  _       _ _          __        _      \033[0m"
            third += "\t\t\t\033[41m ||_||_ | \\|_ /\ | |_|_) |_| /\\ (_  \\    // \\|\\ | \033[0m"
            fourth += "\t\t\t\033[41m || ||_ |_/|_/--\\|_|_| \\ | |/--\\__)  \\/\\/ \\_/| \\| \033[0m"

        if winner == 0:
            first += "\t\t\t\033[43m _____ _____ ___   _   _______   _________________ _ \033[0m"
            second += "\t\t\t\033[43m/  ___|_   _/ _ \\ | \\ | |  _  \\ |  _  |  ___|  ___| |\033[0m"
            third += "\t\t\t\033[43m\\ `--.  | |/ /_\\ \\|  \\| | | | | | | | | |_  | |_  | |\033[0m"
            fourth += "\t\t\t\033[43m `--. \\ | ||  _  || . ` | | | | | | | |  _| |  _| | |\033[0m"
            fifth += "\t\t\t\033[43m/\\__/ / | || | | || |\\  | |/ /  \\ \\_/ / |   | |   |_|\033[0m"
            sixth += "\t\t\t\033[43m\\____/  \\_/\\_| |_/\\_| \\_/___/    \\___/\\_|   \\_|   (_)\033[0m"
    return(first + "\n" + second + "\n" + third + "\n" + fourth + "\n" + fifth + "\n" + sixth)
def next_card():
    for card in allcards:
        if card[2] == False:
            print(card)
        break
def comparison():
    global winner
    if first_player_sum <= 21 and second_player_sum <= 21:
        if first_player_sum < second_player_sum:
            winner = 2
        elif first_player_sum > second_player_sum:
            winner = 1
        elif first_player_sum == 21 and len(first_player_cards) == 2 and not len(second_player_cards) == 2:
            winner = 1
        elif second_player_sum == 21 and len(second_player_cards) == 2 and not len(first_player_cards) == 2:
            winner = 2
        else:
            winner = 0
    elif first_player_sum > 21 and second_player_sum <= 21:
        winner = 2
    elif second_player_sum > 21 and first_player_sum <= 21:
        winner = 1
    else:
        winner = 0
    
def game_over():
    global winner, two_players, first_player, second_player, first_player_cards, second_player_cards, first_player_stop, second_player_stop, just_stopped
    winner = None
    first_player = True
    second_player = False
    first_player_stop = False
    second_player_stop = False
    just_stopped = True
    clear_screen()
    comparison()
    clear_screen()
    print("\033[41mDealer's turn\033[0m")
    print(in_hand(first_player_cards, 3, False, winner))
    print(in_hand(second_player_cards, 0, False))
    print("[new]: for new game in the same mode\n[restart]: to change game mode")
    wait = True
    while wait:
        action = input()
        if action == "new":
            reset()
            print(in_hand(first_player_cards, 4, True))
            print(in_hand(second_player_cards, hide = True))
            print("[0]: get Your starter cards\n")
            waittt = True
            while waittt:
                action = input()
                if action == "0" or action == "é":
                    clear_screen()
                    print(in_hand(first_player_cards, 4, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    draw_card(first_player_cards)
                    print(in_hand(first_player_cards, 3, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    draw_card(second_player_cards)
                    clear_screen()
                    print(in_hand(first_player_cards, 2, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    draw_card(first_player_cards)
                    clear_screen()
                    print(in_hand(first_player_cards, 1, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    draw_card(second_player_cards)
                    clear_screen()
                    print(in_hand(first_player_cards, 0, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    clear_screen()
                    print(in_hand(first_player_cards, 1, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    clear_screen()
                    print(in_hand(first_player_cards, 2, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    clear_screen()
                    waittt = False
            wait = False
        elif action == "restart":
            reset()
            print(pyfiglet.figlet_format("BLACKJACK"))
            print("Are you playing alone or with your friend?\n[1]: with friend\n[0]: alone")

            choosing_game_mode = True
            while choosing_game_mode == True:
                action = input()
                if action == "+" or action == "1":
                    two_players = True
                    choosing_game_mode = False
                elif action == "é" or action == "0":
                    two_players = False
                    just_stopped = True
                    choosing_game_mode = False
            print(in_hand(first_player_cards, 4, True))
            print(in_hand(second_player_cards, hide = True))
            print("[0]: get Your starter cards\n")
            waittt = True
            while waittt:
                action = input()
                if action == "0" or action == "é":
                    clear_screen()
                    print(in_hand(first_player_cards, 4, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    draw_card(first_player_cards)
                    print(in_hand(first_player_cards, 3, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    draw_card(second_player_cards)
                    clear_screen()
                    print(in_hand(first_player_cards, 2, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    draw_card(first_player_cards)
                    clear_screen()
                    print(in_hand(first_player_cards, 1, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    draw_card(second_player_cards)
                    clear_screen()
                    print(in_hand(first_player_cards, 0, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    clear_screen()
                    print(in_hand(first_player_cards, 1, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    clear_screen()
                    print(in_hand(first_player_cards, 2, True))
                    print(in_hand(second_player_cards, hide = True))
                    print("\n")
                    time.sleep(0.2)
                    clear_screen()
                    waittt = False
            first_player = True
            second_player = False
            wait = False
reset()
print(pyfiglet.figlet_format("BLACKJACK"))
print("Are you playing alone or with your friend?\n[1]: with friend\n[0]: alone")

choosing_game_mode = True
while choosing_game_mode == True:
    action = input()
    if action == "+" or action == "1":
        two_players = True
        choosing_game_mode = False
    elif action == "é" or action == "0":
        two_players = False
        just_stopped = True
        choosing_game_mode = False
clear_screen()
print(in_hand(first_player_cards, 4, True))
print(in_hand(second_player_cards, hide = True))
print("[0]: get Your starter cards\n")
wait = True
just_stopped = True
while wait:
    action = input()
    if action == "0" or action == "é":
        clear_screen()
        print(in_hand(first_player_cards, 4, True))
        print(in_hand(second_player_cards, hide = True))
        print("\n")
        time.sleep(0.2)
        draw_card(first_player_cards)
        print(in_hand(first_player_cards, 3, True))
        print(in_hand(second_player_cards, hide = True))
        print("\n")
        time.sleep(0.2)
        draw_card(second_player_cards)
        clear_screen()
        print(in_hand(first_player_cards, 2, True))
        print(in_hand(second_player_cards, hide = True))
        print("\n")
        time.sleep(0.2)
        draw_card(first_player_cards)
        clear_screen()
        print(in_hand(first_player_cards, 1, True))
        print(in_hand(second_player_cards, hide = True))
        print("\n")
        time.sleep(0.2)
        draw_card(second_player_cards)
        clear_screen()
        print(in_hand(first_player_cards, 0, True))
        print(in_hand(second_player_cards, hide = True))
        print("\n")
        time.sleep(0.2)
        clear_screen()
        print(in_hand(first_player_cards, 1, True))
        print(in_hand(second_player_cards, hide = True))
        print("\n")
        time.sleep(0.2)
        clear_screen()
        print(in_hand(first_player_cards, 2, True))
        print(in_hand(second_player_cards, hide = True))
        print("\n")
        time.sleep(0.2)
        clear_screen()
        wait = False
game = True
while game:
    while first_player:
        if two_players:
            print("\033[41m" + "First player's round" + "\033[0m")
        else:
            print("\033[42m" + "Your turn" + "\033[0m")
        if (not second_player_stop or just_stopped) and two_players or just_stopped:
            if just_stopped == True: just_stopped = False
            print(in_hand(first_player_cards, 3, True))
            print(in_hand(second_player_cards, hide = True))
            print("[0]: unhide your cards\n")
            wait = True
            while wait:
                action = input()
                just_stopped = False
                if action == "0" or action == "é":
                    wait = False
        clear_screen()
        if two_players:
            print("\033[41m" + "First player's round" + "\033[0m")
        else:
            print("\033[42m" + "Your turn" + "\033[0m")
        print(in_hand(first_player_cards, 3))
        print(in_hand(second_player_cards, hide = True))
        if not first_player_stop:
            print("[draw]: draw your card\n[stand]: stop drawing up another cards")
            action = input()
        first_player_sum = 0
        for i in first_player_cards:
            if first_player_sum + 11 <= 21 and i[1] == 1 :
                first_player_sum += 11
            elif i[1] == 11:
                first_player_sum += 10
            elif i[1] == 12:
                first_player_sum += 10
            elif i[1] == 13:
                first_player_sum += 10
            else: first_player_sum += i[1]
        if action == "quit":
            print("\033[?1049l")
            game = False
        if action == "draw":
            clear_screen()
            if first_player_stop == True:
                print("You cannot draw your card when you had standed!")
            draw_card(first_player_cards)
            print(in_hand(first_player_cards, 2))
            print(in_hand(second_player_cards, hide = True))
        if action == "stand":
            first_player_stop = True
            clear_screen()
            just_stopped = True
            print(in_hand(first_player_cards, 3))
            print(in_hand(second_player_cards, hide = True))
        if action == "sum":
            print(first_player_sum)
        if action == "reset":
            reset()
        if first_player_stop and second_player_stop:
            game_over()
        if not second_player_stop and two_players: wait = True
        if not two_players and first_player_stop:
            second_player = True
            first_player = False
        while wait:
            print("[0]: hide your cards\n")
            action = input()
            if action == "0" or action == "é":
                clear_screen()
                print(in_hand(first_player_cards, 3, True))
                wait = False
                second_player = True
                first_player = False
    while second_player:
        if two_players:
            if not first_player_stop or just_stopped:
                clear_screen()
                print("\033[44m" + "Second player's round" + "\033[0m")
                print(in_hand(first_player_cards, 3, True))
                print(in_hand(second_player_cards, hide = True))
                print("[0]: unhide your cards\n")
                wait = True
                just_stopped = False
                while wait:
                    action = input()
                    if action == "0" or action == "é":
                        wait = False
            clear_screen()
            print("\033[44m" + "Second player's round" + "\033[0m")
            print(in_hand(first_player_cards, 3, True))
            print(in_hand(second_player_cards))
            if not second_player_stop:
                print("[draw]: draw your card\n[stand]: stop drawing up another cards")
                action = input()
            second_player_sum = 0
            for i in second_player_cards:
                if second_player_sum + 11 <= 21 and i[1] == 1 :
                    second_player_sum += 11
                elif i[1] == 11:
                    second_player_sum += 10
                elif i[1] == 12:
                    second_player_sum += 10
                elif i[1] == 13:
                    second_player_sum += 10
                else: second_player_sum += i[1]
            if action == "quit":
                game = False
                print("\033[?1049l")
            if action == "draw":
                clear_screen()
                if second_player_stop == True:
                    print("You cannot draw your card when you had stoped!")
                draw_card(second_player_cards)
                print(in_hand(first_player_cards, 2, True))
                print(in_hand(second_player_cards))
            if action == "stand":
                second_player_stop = True
                clear_screen()
                just_stopped = True
                print(in_hand(first_player_cards, 3, True))
                print(in_hand(second_player_cards))
            if action == "sum":
                print(second_player_sum)
            if action == "reset":
                reset()
            if first_player_stop and second_player_stop:
                game_over()  
            if second_player and not first_player_stop == True:
                wait = True
                while wait:
                    print("[0]: hide your cards\n")
                    action = input()
                    if action == "0" or action == "é":
                        clear_screen()
                        wait = False
                        first_player = True
                        second_player = False
        else:
            time.sleep(1)
            clear_screen()
            print("\033[41mDealer's turn\033[0m")
            print(in_hand(first_player_cards, 3))
            print(in_hand(second_player_cards))
            print("\n\n")
            second_player_sum = 0
            for i in second_player_cards:
                if second_player_sum + 11 <= 21 and i[1] == 1 :
                    second_player_sum += 11
                elif i[1] == 11:
                    second_player_sum += 10
                elif i[1] == 12:
                    second_player_sum += 10
                elif i[1] == 13:
                    second_player_sum += 10
                else: second_player_sum += i[1]
            if second_player_sum < 17:
                clear_screen()
                draw_card(second_player_cards)
                print("\033[41mDealer's turn\033[0m")
                print(in_hand(first_player_cards, 2, False))
                print(in_hand(second_player_cards))
                print("\n\n")
            else:
                second_player_stop = True
            if second_player_stop:
                game_over()
                
                            
            
quit            
    
