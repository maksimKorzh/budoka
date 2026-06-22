# Globals
from globals import *

# Keep track of visited places
def explore(tile):
  if tile not in game['visited_tiles']:
    game['visited_tiles'].append(tile)

# Add enemies and items
def fill_dungeon():
  # Place stairs
  if game['level'] < 6:
    tiles = get_tiles([FLOOR])
    stairs = choice(tiles)
  else:
    tiles = get_tiles([FLOOR, PASSAGE])
    stairs = choice(tiles)
  game['dungeon'][stairs[0]][stairs[1]] = STAIRS
  
  # Place belt
  belt = choice(get_tiles([FLOOR]))
  game['dungeon'][belt[0]][belt[1]] = str(game['level']+1)

  # Place player
  tiles = get_tiles([FLOOR])
  player_pos = choice(tiles)
  game['player']['y'] = player_pos[0]
  game['player']['x'] = player_pos[1]

  # Place enemies
  tiles = get_tiles([FLOOR])
  for i in range(roll_dice(2, game['level'])):
    pos = choice(tiles)
    if pos == player_pos: continue
    occupied = False
    for enemy in game['enemies']:
      if enemy['position']['y'] == pos[0] and \
         enemy['position']['x'] == pos[1]:
        occupied = True
    if occupied: break
    hp = game['level']*2
    attack = game['level']
    defense = game['level']
    level = randrange(game['level'], game['level']+2)
    style = choice(list(ENEMIES.keys()))
    enemy = create_enemy(pos[0], pos[1], hp, attack, defense, level, style)
    game['enemies'].append(enemy)

# Create a single dungeon level
def make_level():
  # Clear dungeon
  for row in range(ROWS):
    for col in range(COLS):
      game['dungeon'][row][col] = EMPTY
  
  # Clear rooms
  game['rooms'] = []
  
  # Clear enemies
  game['enemies'] = []
  
  # Clear visited tiles
  game['visited_tiles'] = []
  
  # Clear old level screen
  screen.clear()

  # Pick up random number of rooms
  num_rooms = randrange(MINROOMS, MAXROOMS+1)

  # Pick up random sectors
  sectors = []
  for i in range(num_rooms):
    rand_sector = randrange(9)
    while rand_sector in sectors:
      rand_sector = randrange(9)
    sectors.append(rand_sector)

  # Random dark rooms
  light_rooms = [True for i in range(9)]
  if game['level'] > 2:
    num_dark = roll_dice(1, 6)
    for i in range(num_dark):
      light_rooms[i] = False
  shuffle(light_rooms)

  # Create rooms
  for sector in sectors:
    if sector == 0: place_room(SECTORS_COL1_OFFSET_MAX, SECTORS_COL1_OFFSET_MIN, SECTORS_ROW1_OFFSET_MAX, SECTORS_ROW1_OFFSET_MIN, sector, light_rooms[0])
    elif sector == 1: place_room(SECTORS_COL1_OFFSET_MAX, SECTORS_COL1_OFFSET_MIN, SECTORS_ROW2_OFFSET_MAX, SECTORS_ROW2_OFFSET_MIN, sector, light_rooms[1])
    elif sector == 2: place_room(SECTORS_COL1_OFFSET_MAX, SECTORS_COL1_OFFSET_MIN, SECTORS_ROW3_OFFSET_MAX, SECTORS_ROW3_OFFSET_MIN, sector, light_rooms[2])
    elif sector == 3: place_room(SECTORS_COL2_OFFSET_MAX, SECTORS_COL2_OFFSET_MIN, SECTORS_ROW1_OFFSET_MAX, SECTORS_ROW1_OFFSET_MIN, sector, light_rooms[3])
    elif sector == 4: place_room(SECTORS_COL2_OFFSET_MAX, SECTORS_COL2_OFFSET_MIN, SECTORS_ROW2_OFFSET_MAX, SECTORS_ROW2_OFFSET_MIN, sector, light_rooms[4])
    elif sector == 5: place_room(SECTORS_COL2_OFFSET_MAX, SECTORS_COL2_OFFSET_MIN, SECTORS_ROW3_OFFSET_MAX, SECTORS_ROW3_OFFSET_MIN, sector, light_rooms[5])
    elif sector == 6: place_room(SECTORS_COL3_OFFSET_MAX, SECTORS_COL3_OFFSET_MIN, SECTORS_ROW1_OFFSET_MAX, SECTORS_ROW1_OFFSET_MIN, sector, light_rooms[6])
    elif sector == 7: place_room(SECTORS_COL3_OFFSET_MAX, SECTORS_COL3_OFFSET_MIN, SECTORS_ROW2_OFFSET_MAX, SECTORS_ROW2_OFFSET_MIN, sector, light_rooms[7])
    elif sector == 8: place_room(SECTORS_COL3_OFFSET_MAX, SECTORS_COL3_OFFSET_MIN, SECTORS_ROW3_OFFSET_MAX, SECTORS_ROW3_OFFSET_MIN,  sector, light_rooms[8])
  
  # Connect rooms
  connect_rooms()
  dead_end()

  # Fill dungeon
  fill_dungeon()
