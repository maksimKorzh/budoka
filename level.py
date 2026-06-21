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
    stairs_pos = choice(tiles)
  else:
    tiles = get_tiles([FLOOR, PASSAGE])
    stairs_pos = choice(tiles)
  
  game['dungeon'][stairs_pos[0]][stairs_pos[1]] = STAIRS

  # Place player
  tiles = get_tiles([FLOOR])
  player_pos = choice(tiles)
  game['player']['y'] = player_pos[0]
  game['player']['x'] = player_pos[1]

  # Place enemies
  tiles = get_tiles([FLOOR])
  for i in range(10):
    pos = choice(tiles)
    if pos == player_pos: continue
    hp = game['level']*2
    attack = game['level']
    defense = game['level']
    level = randrange(game['level'], game['level']+3)
    style = choice(list(EMEMIES.keys()))
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
  
  # Create rooms
  for sector in sectors:
    if sector == 0: place_room(SECTORS_COL1_OFFSET_MAX, SECTORS_COL1_OFFSET_MIN, SECTORS_ROW1_OFFSET_MAX, SECTORS_ROW1_OFFSET_MIN, sector, True)
    elif sector == 1: place_room(SECTORS_COL1_OFFSET_MAX, SECTORS_COL1_OFFSET_MIN, SECTORS_ROW2_OFFSET_MAX, SECTORS_ROW2_OFFSET_MIN, sector, True)
    elif sector == 2: place_room(SECTORS_COL1_OFFSET_MAX, SECTORS_COL1_OFFSET_MIN, SECTORS_ROW3_OFFSET_MAX, SECTORS_ROW3_OFFSET_MIN, sector, True)
    elif sector == 3: place_room(SECTORS_COL2_OFFSET_MAX, SECTORS_COL2_OFFSET_MIN, SECTORS_ROW1_OFFSET_MAX, SECTORS_ROW1_OFFSET_MIN, sector, True)
    elif sector == 4: place_room(SECTORS_COL2_OFFSET_MAX, SECTORS_COL2_OFFSET_MIN, SECTORS_ROW2_OFFSET_MAX, SECTORS_ROW2_OFFSET_MIN, sector, True)
    elif sector == 5: place_room(SECTORS_COL2_OFFSET_MAX, SECTORS_COL2_OFFSET_MIN, SECTORS_ROW3_OFFSET_MAX, SECTORS_ROW3_OFFSET_MIN, sector, True)
    elif sector == 6: place_room(SECTORS_COL3_OFFSET_MAX, SECTORS_COL3_OFFSET_MIN, SECTORS_ROW1_OFFSET_MAX, SECTORS_ROW1_OFFSET_MIN, sector, True)
    elif sector == 7: place_room(SECTORS_COL3_OFFSET_MAX, SECTORS_COL3_OFFSET_MIN, SECTORS_ROW2_OFFSET_MAX, SECTORS_ROW2_OFFSET_MIN, sector, True)
    elif sector == 8: place_room(SECTORS_COL3_OFFSET_MAX, SECTORS_COL3_OFFSET_MIN, SECTORS_ROW3_OFFSET_MAX, SECTORS_ROW3_OFFSET_MIN,  sector, True)
  
  # Connect rooms
  connect_rooms()
  dead_end()

  # Fill dungeon
  fill_dungeon()
