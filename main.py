from random import randint
from os import system
import enum

def clear_screen():
    ''' Clear screen '''
    system('cls')

class Status(enum.Enum):
    ''' Difficult class
    
    Is an enumeration of possible cell states
    '''
    closed = 0
    flag = 1
    open = 2

class Cell:
    ''' Cell class
    
    It is the main object on the playing field.

    Each object stores its value of bombs around (9 means this is the bomb) and status (open, flag, closed)
    '''
    BOMB = 9

    def __init__(self, value:int=0, status=Status.closed) -> None:
        ''' Constructor 
        
        :value: Cell value, displays the number of bombs around the cell

        :status: Cell status (open, flag, closed)
        '''
        self.value = value
        self.status = status
    
    def open(self):
        ''' Open the cell (change cell status to "open") '''
        if self.status == Status.closed:
            self.status = Status.open

    def mark(self):
        ''' Flag the cell (change cell status to "flag") '''
        if self.status == Status.closed:
            self.status = Status.flag
            Game.closed_cell_count -= 1
            Game.bomb_count -=1
        elif self.status == Status.flag:
            self.status = Status.closed
            Game.bomb_count +=1
            Game.closed_cell_count += 1
    
    def __str__(self) -> str:
        ''' Returns the value of the cell when trying to access
        the string representation of the object
        '''
        return str(self.value)
    

class Game:
    ''' Game class
    
    A class that describes the state of the game, the number of bombs, the playing field itself, etc.
    '''
    field = []
    game_mode = 'game'
    bomb_count = 9
    closed_cell_count = 81
    field_width = 9
    field_height = 9

    @staticmethod
    def init_game():
        ''' Initialization game '''
        Game.generate_field()
        Game.generate_bombs()
        
    @staticmethod
    def generate_field():
        ''' Generate field before game '''
        for y in range(Game.field_height):
            Game.field.append([])
            for x in range(Game.field_width):
                Game.field[y].append(Cell())
        
    @staticmethod
    def generate_bombs():
        ''' Generate bombs on field '''
        for _ in range(Game.bomb_count):
            Game.place_bomb()

    @staticmethod
    def place_bomb():
        ''' Place bomb on random cell '''
        x = randint(0, Game.field_width-1)
        y = randint(0, Game.field_height-1)
        if not Game.field[y][x].value == Cell.BOMB:
            Game.field[y][x].value = Cell.BOMB
            Game.update_cells_value(x, y)
        else:
            Game.place_bomb()
    
    @staticmethod
    def update_cells_value(x, y):
        ''' Update cells value adjacent to the bomb 
        
        :x: Cell index by x (width)
        
        :y: Cell index by y (height)
        '''
        Game.execute_with_adjacent_cells(x, y, Game.increase_value)
    
    @staticmethod
    def increase_value(x, y):
        ''' Increase the value in a cell with [x,y] coordinates 
        
        :x: Cell index by x (width)
        
        :y: Cell index by y (height)
        '''
        if not Game.field[y][x].value == Cell.BOMB:
            Game.field[y][x].value += 1

    @staticmethod
    def execute_with_adjacent_cells(x, y, method):
        ''' Does some action with all neighboring cells 
        
        :x: Cell index by x (width)
        
        :y: Cell index by y (height)

        :method: Action to be performed on all adjacent cells
        '''
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if 0 <= x+j < Game.field_width and 0 <= y+i < Game.field_height:
                        method(x+j, y+i)
                    else:
                        continue

    @staticmethod
    def draw_map():
        ''' Draw field on screen '''
        for row in Game.field:
            for element in row:
                symbol = Game.get_cell_symbol(element)
                print(symbol, end=' ')
            print()
    
    @staticmethod
    def get_cell_symbol(element):
        ''' Return a character describing the value of the cell 
        
        :element: Cell object whose symbol is to be retrieved
        '''
        symbol = ''
        match element.status:
            case Status.open:
                match element.value:
                    case 0: 
                        symbol = ' •'
                    case 9: 
                        symbol = '💣'
                    case _:
                        symbol = f' {element}'
            case Status.flag:
                if Game.game_mode == 'game':
                    symbol = '🏴'
                elif Game.game_mode == 'end':
                    if element.value == 9:
                        symbol = '🏴'
                    else:
                        symbol = '🚩'
            case Status.closed:
                symbol = '⬜'
        return symbol

    @staticmethod
    def draw_map_debug():
        ''' Draw field on screen with values '''
        for row in Game.field:
            for element in row:
                print(element, end=" ")
            print()

    @staticmethod
    def mark_cell(x : int, y : int):
        ''' Mark cell as flag

        :x: Cell index by x (width)
        
        :y: Cell index by y (height)
        '''
        Game.field[y][x].mark()

    @staticmethod
    def open_cell(x : int, y : int):
        ''' Open cell [x, y] on field 
        
        :x: Cell index by x (width)
        
        :y: Cell index by y (height)
        '''

        cell = Game.field[y][x]
        if not cell.status == Status.closed:
            return
        
        cell.open()
        if cell.value == 0:
            Game.execute_with_adjacent_cells(x, y, Game.open_cell)
        if cell.value == 9:
            Game.game_over()
        
        Game.closed_cell_count -= 1
        
    @staticmethod
    def game_over():
        ''' Game over, player loose '''
        Game.game_mode = 'end'
        clear_screen()
        Game.draw_map()

    
    @staticmethod
    def user_input():
        ''' Read user input '''
        user_choice = input("Enter cell coordinates and action separated by a space: ")
        user_choice = user_choice.split(' ')
        action = user_choice[0]
        y = int(user_choice[1]) - 1
        x = int(user_choice[2]) - 1
        if action == 'open':
            Game.open_cell(x, y)
        elif action == 'flag':
            Game.mark_cell(x, y)

    @staticmethod
    def check_win():
        ''' Check the successful completion of the game '''
        if Game.bomb_count == 0 and Game.closed_cell_count == 0:
            Game.game_mode = 'end'
            clear_screen()
            Game.draw_map()
            print("You win!")

if (__name__ == '__main__'):
    Game.init_game()
    while not Game.game_mode == 'end':
        clear_screen()
        Game.draw_map()
        Game.user_input()
        Game.check_win()