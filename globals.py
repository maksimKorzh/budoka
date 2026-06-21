# Packages
import sys
import math
import curses
from random import randrange, choice

# Constants
ROWS = 24
COLS = 80

MAXROOMS = 9
MINROOMS = 6

MAX_ROOM_WIDTH = 18
MIN_ROOM_WIDTH = 5
MAX_ROOM_HEIGHT = 6
MIN_ROOM_HEIGHT = 4

SECTORS_ROW1_OFFSET_MAX = 26
SECTORS_ROW1_OFFSET_MIN = 10
SECTORS_ROW2_OFFSET_MAX = 45
SECTORS_ROW2_OFFSET_MIN = 32
SECTORS_ROW3_OFFSET_MAX = 69
SECTORS_ROW3_OFFSET_MIN = 54

SECTORS_COL1_OFFSET_MAX = 9
SECTORS_COL1_OFFSET_MIN = 2
SECTORS_COL2_OFFSET_MAX = 16
SECTORS_COL2_OFFSET_MIN = 9
SECTORS_COL3_OFFSET_MAX = 23
SECTORS_COL3_OFFSET_MIN = 16

DOOR = '+'
EMPTY = ' '
FLOOR = '.'
V_WALL = '|'
H_WALL = '-'
STAIRS = '%'
PLAYER = '@'
PASSAGE = '#'

ENEMIES = {
 'A': 'Aikido',
 'B': 'Boxing',
 'C': 'Capoeira',
 'G': 'Grappling',
 'H': 'Hapkido',
 'J': 'Judo',
 'K': 'Karate',
 'M': 'Muay Thai',
 'R': 'Russian style',
 'S': 'Sumo',
 'T': 'Taekwondo',
 'W': 'Wing Chun',
}

RANKS = {
  '1': { 'degree': '7 kyu', 'belt': 'white' },
  '2': { 'degree': '6 kyu', 'belt': 'yellow' },
  '3': { 'degree': '5 kyu', 'belt': 'magenta' },
  '4': { 'degree': '4 kyu', 'belt': 'cyan' },
  '5': { 'degree': '3 kyu', 'belt': 'blue' },
  '6': { 'degree': '2 kyu', 'belt': 'green' },
  '7': { 'degree': '1 kyu', 'belt': 'red' },
  '8': { 'degree': '1 dan', 'belt': 'black' },
  '9': { 'degree': '2 dan', 'belt': 'black' },
  '10': { 'degree': '3 dan', 'belt': 'black' },
  '11': { 'degree': '4 dan', 'belt': 'black' },
  '12': { 'degree': '5 dan', 'belt': 'black' },
  '13': { 'degree': '6 dan', 'belt': 'black' },
  '14': { 'degree': '7 dan', 'belt': 'black' },
  '15': { 'degree': '8 dan', 'belt': 'black' },
  '16': { 'degree': '9 dan', 'belt': 'black' },
}

MAX_LEVEL = len(RANKS)

# Variables
game = {
  'dungeon': [[' ']*COLS for i in range(ROWS)],
  'rooms': [],
  'visited_tiles': [],
  'level': 1,
  'player': {
    'y': 0,
    'x': 0,
    'hp': 2,
    'attack': 1,
    'defense': 1,
    'level': 1,
    'style': 'Aikido',
    'experience': 0,
    'sensitivity': False,
    'aggravate': False
  },
  'enemies': []
}

# Curses screen
screen = curses.initscr()
screen.nodelay(1)
curses.noecho()
curses.raw()
screen.keypad(1)
curses.start_color()
curses.use_default_colors()

# Read key from keyboard
def read_key():
  ch = -1
  while ch == -1: ch = screen.getch()
  return ch

# Print message
def message(text):
  screen.addstr(0, 1, text + ' --PRESS ANY KEY--')
  screen.clrtoeol()
  render_screen()
  read_key()

# Packages
from colors import *
from dice import *
from room import *
from enemies import *
from level import *
from render import *
from move import *
from command import *
