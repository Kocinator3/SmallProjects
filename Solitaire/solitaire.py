import pyfiglet
import math
import random
import os
import sys
import colorama
import platform

if os.name == "nt" and int(platform.release()) < 10:
    highlight = "\033[33m"  
    grayed_highlight = "\033[33m"
else:
    highlight = "\033[38;5;208m"  
    grayed_highlight = "\033[38;5;137m"



colorama.init()
font = "delta_corps_priest_1"

if os.name == "nt":
    import msvcrt
else:
    import tty
    import termios
    import select

def get_key():
    if os.name == "nt":
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):
            ch2 = msvcrt.getch()
            keys_win = {b'H': 'up', b'P': 'down', b'M': 'right', b'K': 'left'}
            return keys_win.get(ch2, 'unknown')
            
        keys_win_base = {
            b'\x1b': 'esc',
            b'\r': 'enter',
            b' ': 'space',
            b'\x03': 'ctrl-c',
            b'q': 'q',
            b'\x08': 'backspace'
        }
        
        if ch in keys_win_base:
            return keys_win_base[ch]
        try:
            return ch.decode('utf-8').lower()
        except:
            return 'unknown'
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # Čteme "surové" byty přímo z operačního systému
            ch_bytes = os.read(fd, 1)
            ch = ch_bytes.decode('utf-8', errors='ignore')
            
            # Pokud přišel ESC znak, zkusíme počkat na zbytek sekvence (pro šipky)
            if ch == '\x1b':
                if select.select([fd], [], [], 0.05)[0]:
                    ch_bytes += os.read(fd, 2)
                    ch = ch_bytes.decode('utf-8', errors='ignore')
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
        keys_linux = {
            '\x1b[A': 'up',
            '\x1b[B': 'down',
            '\x1b[C': 'right',
            '\x1b[D': 'left',

            '\x1bOA': 'up',
            '\x1bOB': 'down',
            '\x1bOC': 'right',
            '\x1bOD': 'left',

            '\x1b': 'esc',
            '\r': 'enter',
            ' ': 'space',
            '\x03': 'ctrl-c',
            '\x7f': 'backspace',
            '\x08': 'backspace'
        }
        return keys_linux.get(ch, ch.lower())

rows_for_print = []
for i in range(37):
    rows_for_print.append("")
    

#┌┐ └┘-│

colors = {
    "heart" : "\033[31m♥\033[0m",
    "diamond": "\033[31m♦\033[0m",
    "club" : "♣",
    "spade" : "♠"
}
numbers = {
    1 : "A",
    2 : "2",
    3 : "3",
    4 : "4",
    5 : "5",
    6 : "6",
    7 : "7",
    8 : "8",
    9 : "9",
    10 : "10",
    11 : "J",
    12 : "Q",
    13 : "K"
}

class Card:
    cards = []
    def __init__(self, color:str, number:int, turned_over:bool = False, ghost:bool = False, dummy:bool = False):
        self.color = color
        self.number = number
        self.turned_over = turned_over
        self.ghost = ghost
        self.dummy = dummy
        Card.cards.append(self)
        self.text = []
        pad = "   " if len(numbers[number]) == 2 else "    "
        self.text.append("┌──────┐")
        self.text.append(f"│{numbers[number]}{pad}{colors[self.color]}│")
        for i in range(2):
            self.text.append("│      │")
        self.text.append(f"│{colors[self.color]}{pad}{numbers[number]}│")
        self.text.append("└──────┘")
        self.half_text = []
        self.half_text.append("┌──")
        self.half_text.append(f"│{numbers[number]}{pad}"[:3])
        self.half_text.append("│  ")
        self.half_text.append("│  ")
        self.half_text.append(f"│{colors[self.color]} ")
        self.half_text.append("└──")
        self.highlighted_text = [
            f"{highlight}┌──────┐\033[0m",
            f"{highlight}│\033[0m{numbers[number]}{pad}{colors[self.color]}{highlight}│\033[0m",
            f"{highlight}│      │\033[0m",
            f"{highlight}│      │\033[0m",
            f"{highlight}│\033[0m{colors[self.color]}{pad}{numbers[number]}{highlight}│\033[0m",
            f"{highlight}└──────┘\033[0m"
        ]

class Column:
    columns = []
    def __init__(self, cards:list):
        self.cards = cards
        Column.columns.append(self)
        self.index = Column.columns.__len__()
    def draw(self):
        global highlighted, rows_for_print
        current_y = 7
        for i, card in enumerate(self.cards):
            if card.dummy:
                rows_for_print[current_y] += "        "
                current_y += 1
            elif card.turned_over:
                if card.ghost:
                    rows_for_print[current_y] += "│      │"
                    current_y += 1
                #if card is turned over and the last one
                elif i == len(self.cards) - 1:
                    if card == highlighted:
                        for text in card.highlighted_text:
                            rows_for_print[current_y] += (text)
                            current_y += 1                        
                    else:
                        for text in card.text:
                            rows_for_print[current_y] += (text)
                            current_y += 1
                #if card is turned over and isn't the last one
                else:
                    if card == highlighted:
                        for i in range(2):
                            rows_for_print[current_y] += (card.highlighted_text[i])
                            current_y += 1                        
                    else:
                        for i in range(2):
                            rows_for_print[current_y] += (card.text[i])
                            current_y += 1
            else:
                #if card isn't turned over:
                if card.ghost:
                    rows_for_print[current_y] += "│xxxxxx│"
                else:
                    rows_for_print[current_y] += "┌──────┐"
                current_y += 1
        while current_y < len(rows_for_print):
            rows_for_print[current_y] += "        "
            current_y += 1
    def update(self):
        if self.cards.__len__() > 0:
            if self.cards[-1].turned_over == False:
                self.cards[-1].turned_over = True

    @classmethod
    def draw_all(cls):
        for i in cls.columns:
            i.draw()
    @classmethod
    def update_all(cls):
        for i in cls.columns:
            i.update()
    @classmethod
    def kill_dummies(cls):
        for i in cls.columns:
            i.cards = [card for card in i.cards if not (card.dummy or card.ghost)]
class Stock:
    stock = None
    def __init__(self, cards:list):
        self.cards = cards
        self.text = []
        self.text.append("┌──────┐")
        for i in range(4):
            self.text.append("│xxxxxx│")
        self.text.append("└──────┘")
        Stock.stock = self
        self.refills = 3
    def draw(self):
        if len(self.cards) > 0:
            if highlighted == "stock":
                rows_for_print[0] += f"{highlight}┌──────┐\033[0m"
                rows_for_print[1] += f"{highlight}│xxxxxx│\033[0m"
                rows_for_print[2] += f"{highlight}│xxxxxx│\033[0m"
                rows_for_print[3] += f"{highlight}│xxxxxx│\033[0m"
                rows_for_print[4] += f"{highlight}│xxxxxx│\033[0m"
                rows_for_print[5] += f"{highlight}└──────┘\033[0m"
            else:
                for i, text in enumerate(self.text):
                    rows_for_print[i] += text
        else:
            if highlighted == "stock":
                if self.refills > 0:
                    rows_for_print[0] += f"{highlight}┌──────┐\033[0m"
                    rows_for_print[1] += f"{highlight}│\033[0mREFILL{highlight}│\033[0m"
                    rows_for_print[2] += f"{highlight}│\033[0m [R]  {highlight}│\033[0m"
                    rows_for_print[3] += f"{highlight}│\033[0m LEFT:{highlight}│\033[0m"
                    rows_for_print[4] += f"{highlight}│\033[0m  {self.refills}   {highlight}│\033[0m"
                    rows_for_print[5] += f"{highlight}└──────┘"           
                else:
                    rows_for_print[0] += "\033[31m┌──────┐\033[0m"
                    rows_for_print[1] += "\033[31m│REFILL│\033[0m"
                    rows_for_print[2] += "\033[31m│ [R]  │\033[0m"
                    rows_for_print[3] += "\033[31m│ LEFT:│\033[0m"
                    rows_for_print[4] += "\033[31m│  0   │\033[0m"
                    rows_for_print[5] += "\033[31m└──────┘\033[0m"
            else:
                rows_for_print[0] += "┌──────┐"
                rows_for_print[1] += "│REFILL│"
                rows_for_print[2] += "│ [R]  │"
                rows_for_print[3] += "│ LEFT:│"
                rows_for_print[4] += f"│  {self.refills}   │"
                rows_for_print[5] += "└──────┘"
    def refill(self):
        if self.refills > 0 and self.cards.__len__() <= 0:
            self.cards = Waste.waste.cards[::-1]
            Waste.waste.cards.clear()
            self.refills -= 1
            

class Waste:
    waste = None
    def __init__(self, cards:list = list()):
        self.cards = cards
        Waste.waste = self
    def draw(self):
        if self.cards.__len__() == 0:
            for i in range(6):
                rows_for_print[i] += "                "
        elif self.cards.__len__() == 1:
            for i in range(6):
                rows_for_print[i] += "       "
            if self.cards[-1] == highlighted:
                for i, text in enumerate(self.cards[-1].highlighted_text):
                    rows_for_print[i] += text
            else:
                for i, text in enumerate(self.cards[-1].text):
                    rows_for_print[i] += text
            for i in range(6):
                rows_for_print[i] += " "
        elif self.cards.__len__() == 2:
            for i in range(6):
                rows_for_print[i] += "    "
            for i, text in enumerate(self.cards[-2].half_text):
                rows_for_print[i] += text
            if self.cards[-1] == highlighted:
                for i, text in enumerate(self.cards[-1].highlighted_text):
                    rows_for_print[i] += text
            else:
                for i, text in enumerate(self.cards[-1].text):
                    rows_for_print[i] += text
            for i in range(6):
                rows_for_print[i] += " "
        else:
            for i in range(6):
                rows_for_print[i] += " "
            for i, text in enumerate(self.cards[-3].half_text):
                rows_for_print[i] += text
            for i, text in enumerate(self.cards[-2].half_text):
                rows_for_print[i] += text
            if self.cards[-1] == highlighted:
                for i, text in enumerate(self.cards[-1].highlighted_text):
                    rows_for_print[i] += text
            else:
                for i, text in enumerate(self.cards[-1].text):
                    rows_for_print[i] += text
            for i in range(6):
                rows_for_print[i] += " "


class Foundation:
    foundations = []
    def __init__(self, cards:list = list()):
        self.cards = cards
        Foundation.foundations.append(self)
    def draw(self):
        if self.cards.__len__() < 1:
            if highlighted == Foundation.foundations.index(self):
                rows_for_print[0] += f"{grayed_highlight}┌──────┐\033[0m"
                rows_for_print[1] += f"{grayed_highlight}│[A]   │\033[0m"
                rows_for_print[2] += f"{grayed_highlight}│      │\033[0m"
                rows_for_print[3] += f"{grayed_highlight}│      │\033[0m"
                rows_for_print[4] += f"{grayed_highlight}│   [A]│\033[0m"
                rows_for_print[5] += f"{grayed_highlight}└──────┘\033[0m"
            else:
                rows_for_print[0] += "\033[38;5;244m┌──────┐\033[0m"
                rows_for_print[1] += "\033[38;5;244m│[A]   │\033[0m"
                rows_for_print[2] += "\033[38;5;244m│      │\033[0m"
                rows_for_print[3] += "\033[38;5;244m│      │\033[0m"
                rows_for_print[4] += "\033[38;5;244m│   [A]│\033[0m"
                rows_for_print[5] += "\033[38;5;244m└──────┘\033[0m"
        else:
            if highlighted == Foundation.foundations.index(self):
                for i, text in enumerate(self.cards[-1].highlighted_text):
                    rows_for_print[i] += text
            else:
                for i, text in enumerate(self.cards[-1].text):
                    rows_for_print[i] += text
    @classmethod
    def draw_all(cls):
        for i in cls.foundations:
            i.draw()

def time(play_time:str="0:0"):
    texts = pyfiglet.figlet_format(play_time, font="double_blocky", width=200).splitlines()
    for i,text in enumerate(texts):
        rows_for_print[i+2] += f"\t{text}"
def score(score:str="9999"):
    texts = pyfiglet.figlet_format(score, font="double_blocky", width=200).splitlines()
    for i,text in enumerate(texts):
        rows_for_print[i+2] += f"\t{text}"
def reset():
    global highlighted, moving
    Card.cards.clear()
    Column.columns.clear()
    Stock.stock = None
    high_x, high_y = 0, 1
    cards = []
    moving = False
    for number in range(1,14):
        for color in ["heart", "club", "diamond", "spade"]:
            cards.append(Card(color, number, False, False))

    random.shuffle(Card.cards)

    for i in range(1,8):
        column = []
        for ii in range(i):
            column.append(Card.cards[0])
            Card.cards.remove(Card.cards[0])
        Column(column)
    for i in range(4):
        Foundation()
    print("\n")
    print(pyfiglet.figlet_format("SOLITAIRE", font=font, width=200))
    Stock(Card.cards)
    cards.clear
    Waste()
    
    highlighted = Column.columns[0].cards[0]

def redraw():
    global highlighted, high_x, high_y
    Column.update_all()
    global rows_for_print
    rows_for_print = ["" for _ in range(40)]
    if high_y == 0:
        if high_x == 0:
            highlighted = "stock"
        elif high_x < 3:
            if Waste.waste.cards.__len__() > 0:
                highlighted = Waste.waste.cards[-1]
            else:
                high_x = 3
                highlighted = 0
        elif high_x >= 3:
            highlighted = high_x - 3
    elif Column.columns[high_x].cards.__len__() == 0:
        high_y = 0
    else:
        while True:
            if Column.columns[high_x].cards[high_y-1].turned_over:
                highlighted = Column.columns[high_x].cards[high_y-1]
                break
            high_y += 1
            if high_y >= 20: 
                high_x += 1
                high_y = 1
    Stock.stock.draw()
    Waste.waste.draw()
    Column.draw_all()
    Foundation.draw_all()
    score()
    time()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n")
    print(pyfiglet.figlet_format("SOLITAIRE", font=font, width=200))
    for row in rows_for_print:
        print(row)

def draw_card():
    if Stock.stock.cards.__len__() > 0:
        Waste.waste.cards.append(Stock.stock.cards[-1])
        Stock.stock.cards.remove(Stock.stock.cards[-1])

reset()
for i in rows_for_print:
    print(i)

try:
    print('\033[?25l', end="")
    run = True
    high_x, high_y = 0, 1

    while run:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n")
        print(pyfiglet.figlet_format("SOLITAIRE", font=font , width=200))
        print("press [enter] to start a new round")
        key = get_key() 
        if key in ['q', 'esc', 'ctrl-c']:
            break
        redraw()
        game = True
        while game:
            key = get_key()

            if key in ['q', 'esc', 'ctrl-c']:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Hra ukončena.")
                run = False
                game = False

            if key == "d":
                draw_card()
            if key == "r":
                Stock.stock.refill()
            if key == "up":
                if high_y > 1:
                    if Column.columns[high_x].cards[high_y-2].turned_over:
                        high_y -= 1
                    else:
                        high_y = 0
                elif high_y == 1:
                    high_y = 0
            if key == "down" and high_y < Column.columns[high_x].cards.__len__():
                high_y += 1
            if key == "right" and high_x <= 5:
                high_x += 1
                if high_y > Column.columns[high_x].cards.__len__():
                    high_y = Column.columns[high_x].cards.__len__()

                if high_y == 0:
                    if Waste.waste.cards.__len__() == 0 and high_x == 0:
                        high_x = 3
                    elif high_x == 2:
                        high_x = 3
            if key == "left" and high_x >= 1:
                high_x -= 1
                if high_y > Column.columns[high_x].cards.__len__():
                    high_y = Column.columns[high_x].cards.__len__()
                
                if high_y == 0:
                    if high_x == 2:
                        high_x = 1 if Waste.waste.cards.__len__() > 0 else 0
                    elif high_x == 1 and Waste.waste.cards.__len__() == 0:
                        high_x = 0
            if key == "space" or key == "enter":
                if highlighted == "stock":
                    draw_card()
                if high_y > 0:
                    if moving == False:
                        if high_y > 1:
                            Column.columns[high_x].cards.insert(high_y - 1, Card("heart", 1, Column.columns[high_x].cards[high_y - 1].turned_over, ghost=True))
                            high_y += 1
                            move = (Column.columns[high_x].cards[high_y-1], high_x, high_y)
                            moving = True
                        else:
                            Column.columns[high_x].cards.insert(high_y - 1, Card("heart", 1, False, False, True))
                            high_y += 1
                            move = (Column.columns[high_x].cards[high_y-1], high_x, high_y)
                            moving = True
                    else:
                        choosed = Column.columns[high_x].cards[high_y-1]
                        if (choosed.color == "club" or choosed.color == "spade") and (move[0].color == "diamond" or move[0].color == "heart") and (choosed.number == move[0].number + 1):
                            for i in Column.columns[move[1]].cards[move[2]-1:]:
                                Column.columns[high_x].cards.append(i)
                                Column.columns[move[1]].cards.remove(i)
                        if (move[0].color == "club" or move[0].color == "spade") and (choosed.color == "diamond" or choosed.color == "heart") and (choosed.number == move[0].number + 1):
                            for i in Column.columns[move[1]].cards[move[2]-1:]:
                                Column.columns[high_x].cards.append(i)
                                Column.columns[move[1]].cards.remove(i)
                        Column.kill_dummies()
                        moving = False            
            if key == "backspace":
                Column.kill_dummies()
                moving = False                     

            redraw()
finally:
    print('\033[?25h', end="")