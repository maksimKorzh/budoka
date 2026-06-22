# Packages
from globals import *

# Render single character in dungeon
def render_char(row, col, dark_room=False):
  if [row, col] not in game['visited_tiles'] and not dark_room: return
  if game['dungeon'][row][col] == FLOOR:
    screen.addch(row, col, game['dungeon'][row][col], paint('white'))
  elif game['dungeon'][row][col] == DOOR:
    screen.addch(row, col, game['dungeon'][row][col], paint('darkyellow'))
  elif game['dungeon'][row][col] == STAIRS:
    screen.addch(row, col, game['dungeon'][row][col], paint('yellow'))
  elif game['dungeon'][row][col] == PASSAGE:
    screen.addch(row, col, game['dungeon'][row][col], paint('darkwhite'))
  else: screen.addch(row, col, game['dungeon'][row][col], paint('white'))

# Render enemies
def render_enemies():
  player_y = game['player']['y']
  player_x = game['player']['x']
  for enemy in game['enemies']:
    if enemy['hp'] == 0: continue
    enemy_y = enemy['position']['y']
    enemy_x = enemy['position']['x']
    belt = RANKS[str(enemy['level'])]['belt']
    if [enemy_y, enemy_x] in game['visited_tiles']:
      for room in game['rooms']:
        if game['dungeon'][enemy_y][enemy_x] == FLOOR:
          if current_room(player_y, player_x, room):
            if current_room(enemy_y, enemy_x, room):
              screen.addch(enemy_y, enemy_x, enemy['name'], paint(belt))
        elif game['dungeon'][enemy_y][enemy_x] in [PASSAGE, DOOR]:
          if abs(enemy_y-player_y) <= 1 and abs(enemy_x-player_x) <= 1:
            screen.addch(enemy_y, enemy_x, enemy['name'], paint(belt))

# Render enemies
def render_all_enemies():
  for enemy in game['enemies']:
    if enemy['hp'] == 0: continue
    enemy_y = enemy['position']['y']
    enemy_x = enemy['position']['x']
    belt = RANKS[str(enemy['level'])]['belt']
    screen.addch(enemy_y, enemy_x, enemy['name'], paint(belt))

# Render player
def render_player():
  player_y = game['player']['y']
  player_x = game['player']['x']
  belt = RANKS[str(game['player']['level'])]['belt']
  screen.addch(player_y, player_x, PLAYER, paint(belt))
  screen.move(player_y, player_x)

# Render single room
def render_room(room):
  tiles = room['floors'] + room['v_walls'] + room['h_walls']
  for tile in tiles:
    if room['light']:
      explore(tile)
      render_char(tile[0], tile[1])
    else:
      if game['dungeon'][tile[0]][tile[1]] == FLOOR:
        screen.addch(tile[0], tile[1], ' ')
      for tile in tiles:
        if tile[0] == game['player']['y'] and tile[1] == game['player']['x']:
          for dir in [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1,-1), (1,-1), (-1, 1)
          ]: render_char(tile[0]+dir[0], tile[1]+dir[1], True)

# A room without a player
def render_abandoned_room(room):
  floors = room['floors']
  walls = room['v_walls'] + room['h_walls']
  for tile in floors:
    if game['dungeon'][tile[0]][tile[1]] == FLOOR:
      if tile in game['visited_tiles']:
        if room['light']: screen.addch(tile[0], tile[1], FLOOR, paint('darkwhite'))
        else: screen.addch(tile[0], tile[1], ' ')
    else: render_char(tile[0], tile[1])
  for tile in walls: render_char(tile[0], tile[1])

# Render game level
def render_dungeon():
  # Current player position
  player_y = game['player']['y']
  player_x = game['player']['x']
  
  # Draw passages
  for tile in game['visited_tiles']:
    render_char(tile[0], tile[1])
  
  # Draw current room
  for room in game['rooms']:
    if current_room(player_y, player_x, room):
      render_room(room)

  # Draw visited rooms
  for room in game['rooms']:
    if not current_room(player_y, player_x, room):
      render_abandoned_room(room)

# Render player stats
def render_stats():
  level = game['level']
  hp = game['player']['hp']
  max_hp = game['player']['max_hp']
  attack = game['player']['attack']
  defense = game['player']['defense']
  style = game['player']['style']
  rank = RANKS[str(game['player']['level'])]['degree']
  status = 'deshi' if game['player']['level'] < 8 else 'sensei'
  exp = game['player']['experience']
  up = game['player']['level'] ** 2 * 10
  screen.addstr(23, 1, f'Level: {level}  HP: {hp}({max_hp})  XP: {exp}/{up}  Attack: {attack}  Defense: {defense} -> {rank} {style} {status}')
  screen.clrtoeol()

# Clear screen
def clear_screen():
  for i in range(1, 23):
    screen.move(i, 0)
    screen.clrtoeol()

# Render screen
def render_screen():
  render_dungeon()
  if game['player']['sensivity']:
    clear_screen()
    render_dungeon()
    render_all_enemies()
  else: render_enemies()
  render_stats()
  render_player()
