# Globals
from globals import *

# Get tiles of certain type
def get_tiles(cells):
  tiles = []
  for row in range(ROWS):
    for col in range(COLS):
      if game['dungeon'][row][col] in cells:
        tiles.append([row, col])
  return tiles

# Whether player is in room or not
def current_room(y, x, room):
  if [y, x] in room['v_walls'] + room['h_walls'] or \
     [y, x] in room['floors']: return True
  else: return False

# Create a single room in the dungeon
def make_room(row, col, height, width, doors, sector, light):
  # Room reference
  room = {
    'sector': sector,
    'light': light,
    'v_walls': [],
    'h_walls': [],
    'floors': [],
    'doors': [[]]*4
  }
  
  # Dig room in the dungeon
  for r in range(height):
    for c in range(width):
      if r == 0 or r == height-1:
        if doors[0] and r == 0 and c == doors[0]:
          room['doors'][0] = [row+r, col+c]
          room['h_walls'].append([row+r, col+c])
          cell = DOOR
        elif doors[1] and r == height-1 and c == doors[1]:
          room['doors'][1] = [row+r, col+c]
          room['h_walls'].append([row+r, col+c])
          cell = DOOR
        else:
          room['h_walls'].append([row+r, col+c])
          cell = H_WALL
      elif c == 0 or c == width-1:
        if doors[2] and c == 0 and r == doors[2]:
          room['doors'][2] = [row+r, col+c]
          room['v_walls'].append([row+r, col+c])
          cell = DOOR
        elif doors[3] and c == width-1 and r == doors[3]:
          room['doors'][3] = [row+r, col+c]
          room['v_walls'].append([row+r, col+c])
          cell = DOOR
        else:
          room['v_walls'].append([row+r, col+c])
          cell = V_WALL
      else:
        room['floors'].append([row+r, col+c])
        cell = FLOOR
      game['dungeon'][row+r][col+c] = cell
  
  # Store global room reference
  game['rooms'].append(room)

# Dig horizontal passage between rooms
def make_horizontal_passage(room1, room2, door1, door2):
  row, col = room1['doors'][door1]
  step_x = col+1
  step_y = row
  dir_x = 1
  distance_x = abs(step_x-room2['floors'][0][1])
  for i in range(int(distance_x/2)):
    game['dungeon'][row][step_x] = PASSAGE
    step_x += dir_x
  if row != room2['doors'][door2][0]:
    dir_y = 1 if row < room2['doors'][door2][0] else -1
    distance_y = abs(row-room2['doors'][door2][0])
    for i in range(distance_y):
      game['dungeon'][step_y][step_x] = PASSAGE
      step_y += dir_y
  for i in range(int(distance_x/2)):
    if game['dungeon'][step_y][step_x] == DOOR: break
    game['dungeon'][step_y][step_x] = PASSAGE
    step_x += 1
  room1['doors'][door1] = []
  room2['doors'][door2] = []

# Dig vertical passage between rooms
def make_vertical_passage(room1, room2, door1, door2):
  row, col = room1['doors'][door1]
  step_x = col
  step_y = row+1
  dir_y = 1
  distance_y = abs(step_y-room2['floors'][0][0])
  for i in range(int(distance_y/2)-1):
    game['dungeon'][step_y][col] = PASSAGE
    step_y += dir_y
  if col != room2['doors'][door2][1]:
    dir_x = 1 if col < room2['doors'][door2][1] else -1
    distance_x = abs(col-room2['doors'][door2][1])
    for i in range(distance_x):
      game['dungeon'][step_y][step_x] = PASSAGE
      step_x += dir_x
  for i in range(int(distance_y/2)+1):
    if game['dungeon'][step_y][step_x] == DOOR: break
    game['dungeon'][step_y][step_x] = PASSAGE
    step_y += 1
  room1['doors'][door1] = []
  room2['doors'][door2] = []

# Create dead ends
def dead_end():
  passages = get_tiles(PASSAGE)
  for i in range(game['level']-1):
    entry = choice(passages)
    len_y = randrange(5, 21)
    len_x = randrange(5, 21)
    step_y = 0
    step_x = 0
    dir_x = 1 if coin_toss() else -1
    dir_y = 1 if coin_toss() else -1
    for i in range(len_y):
      step_y += dir_y
      if entry[0]+step_y not in range (2, ROWS-2): break
      if game['dungeon'][entry[0]+step_y][entry[1]] != EMPTY: break
      if game['dungeon'][entry[0]+step_y+dir_y][entry[1]] in [V_WALL, H_WALL, DOOR]: break
      game['dungeon'][entry[0]+step_y][entry[1]] = PASSAGE
    for i in range(len_x):
      step_x += dir_x
      if entry[1]+step_x not in range (2, COLS-2): break
      if game['dungeon'][entry[0]+step_y-dir_y][entry[1]+step_x] != EMPTY: break
      if game['dungeon'][entry[0]+step_y-dir_y][entry[1]+step_x+dir_x] in [V_WALL, H_WALL, DOOR]: break
      game['dungeon'][entry[0]+step_y-dir_y][entry[1]+step_x] = PASSAGE

# Place random room
def place_room(y_max, y_min, x_max, x_min, sector, light):
  # Room layout
  rand_row = randrange(y_min, y_max-MIN_ROOM_HEIGHT)
  rand_col = randrange(x_min, x_max-MIN_ROOM_WIDTH)
  rand_height = min(MAX_ROOM_HEIGHT, randrange(MIN_ROOM_HEIGHT, y_max-rand_row))
  rand_width = min(MAX_ROOM_WIDTH, randrange(MIN_ROOM_WIDTH, x_max-rand_col+1))
  
  # Doors layout
  rand_x1 = randrange(1, rand_height-1)
  rand_x2 = randrange(1, rand_height-1)
  rand_y1 = randrange(1, rand_width-1)
  rand_y2 = randrange(1, rand_width-1)
  room_doors = [
    [0, rand_y2, 0, rand_x2],
    [0, rand_y2, rand_x1, rand_x2],
    [0, rand_y2, rand_x1, 0],
    [rand_y1, rand_y2, 0, rand_x2],
    [rand_y1, rand_y2, rand_x1, rand_x2],
    [rand_y1, rand_y2, rand_x1, 0],
    [rand_y1, 0, 0, rand_x2],
    [rand_y1, 0, rand_x1, rand_x2],
    [rand_y1, 0, rand_x1, 0]
  ]
  
  # Create room  
  make_room(rand_row, rand_col, rand_height, rand_width, room_doors[sector], sector, light)

# Connect rooms with passages
def connect_rooms():
  rooms = {}
  for room in game['rooms']: rooms[str(room['sector'])] = room
  for room in game['rooms']:
    if room['sector'] == 0 and '1' in rooms.keys(): make_horizontal_passage(room, rooms['1'], 3, 2)
    elif room['sector'] == 0 and '2' in rooms.keys(): make_horizontal_passage(room, rooms['2'], 3, 2)
    elif room['sector'] == 1 and '2' in rooms.keys(): make_horizontal_passage(room, rooms['2'], 3, 2)
    elif room['sector'] == 3 and '4' in rooms.keys(): make_horizontal_passage(room, rooms['4'], 3, 2)
    elif room['sector'] == 3 and '5' in rooms.keys(): make_horizontal_passage(room, rooms['5'], 3, 2)
    elif room['sector'] == 4 and '5' in rooms.keys(): make_horizontal_passage(room, rooms['5'], 3, 2)
    elif room['sector'] == 6 and '7' in rooms.keys(): make_horizontal_passage(room, rooms['7'], 3, 2)
    elif room['sector'] == 6 and '8' in rooms.keys(): make_horizontal_passage(room, rooms['8'], 3, 2)
    elif room['sector'] == 7 and '8' in rooms.keys(): make_horizontal_passage(room, rooms['8'], 3, 2)
    if room['sector'] == 0 and '3' in rooms.keys(): make_vertical_passage(room, rooms['3'], 1, 0)
    elif room['sector'] == 0 and '6' in rooms.keys(): make_vertical_passage(room, rooms['6'], 1, 0)
    elif room['sector'] == 3 and '6' in rooms.keys(): make_vertical_passage(room, rooms['6'], 1, 0)
    elif room['sector'] == 1 and '4' in rooms.keys(): make_vertical_passage(room, rooms['4'], 1, 0)
    elif room['sector'] == 1 and '7' in rooms.keys(): make_vertical_passage(room, rooms['7'], 1, 0)
    elif room['sector'] == 4 and '7' in rooms.keys(): make_vertical_passage(room, rooms['7'], 1, 0)
    elif room['sector'] == 2 and '5' in rooms.keys(): make_vertical_passage(room, rooms['5'], 1, 0)
    elif room['sector'] == 2 and '8' in rooms.keys(): make_vertical_passage(room, rooms['8'], 1, 0)
    elif room['sector'] == 5 and '8' in rooms.keys(): make_vertical_passage(room, rooms['8'], 1, 0)

  # Remove doors not in use
  for key in rooms.keys():
    for door in rooms[key]['doors']:
      if len(door):
        if game['dungeon'][door[0]+1][door[1]] == FLOOR or \
           game['dungeon'][door[0]-1][door[1]] == FLOOR:
          game['dungeon'][door[0]][door[1]] = H_WALL
        if game['dungeon'][door[0]][door[1]+1] == FLOOR or \
           game['dungeon'][door[0]][door[1]-1] == FLOOR:
          game['dungeon'][door[0]][door[1]] = V_WALL
