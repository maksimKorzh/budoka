# Packages
from globals import *

# Regenerate HP
def regenerate_hp():
  game['steps'] += 1
  if not game['steps'] % (30-game['level']):
    if game['player']['hp'] < game['player']['max_hp']:
      game['player']['hp'] += 1
  if not game['steps'] % 200:
    if coin_toss():
      player_pos = [game['player']['y'], game['player']['x']]
      place_enemies(player_pos, 2, game['level'])
      message('New challengers enter the dungeon')

# Move player
def move(ch):
  # Current player position
  player_y = game['player']['y']
  player_x = game['player']['x']
  
  # Obstacles
  obstacles = [V_WALL, H_WALL, EMPTY]

  # Motion control
  if ch == ord('h'):
    if game['dungeon'][player_y][player_x-1] not in obstacles:
      enemy = encounter(player_y, player_x-1)
      if enemy is not None: player_hit(enemy)
      else: player_x -= 1
  elif ch == ord('j'):
    if game['dungeon'][player_y+1][player_x] not in obstacles:
      enemy = encounter(player_y+1, player_x)
      if enemy is not None: player_hit(enemy)
      else: player_y += 1
  elif ch == ord('k'):
    if game['dungeon'][player_y-1][player_x] not in obstacles:
      enemy = encounter(player_y-1, player_x)
      if enemy is not None: player_hit(enemy)
      else: player_y -= 1
  elif ch == ord('l'):
    if game['dungeon'][player_y][player_x+1] not in obstacles:
      enemy = encounter(player_y, player_x+1)
      if enemy is not None: player_hit(enemy)
      else: player_x += 1
  elif ch == ord('y'):
    if game['dungeon'][player_y-1][player_x-1] not in obstacles:
      enemy = encounter(player_y-1, player_x-1)
      if enemy is not None: player_hit(enemy)
      else: player_x -= 1; player_y -= 1
  elif ch == ord('b'):
    if game['dungeon'][player_y+1][player_x-1] not in obstacles:
      enemy = encounter(player_y+1, player_x-1)
      if enemy is not None: player_hit(enemy)
      else: player_x -=1; player_y += 1
  if ch == ord('u'):
    if game['dungeon'][player_y-1][player_x+1] not in obstacles:
      enemy = encounter(player_y-1, player_x+1)
      if enemy is not None: player_hit(enemy)
      else: player_x += 1; player_y -= 1
  if ch == ord('n'):
    if game['dungeon'][player_y+1][player_x+1] not in obstacles:
      enemy = encounter(player_y+1, player_x+1)
      if enemy is not None: player_hit(enemy)
      else: player_x += 1; player_y += 1
  
  # Update player position
  game['player']['y'] = player_y
  game['player']['x'] = player_x

  # HP regeneration
  regenerate_hp()

  # Fog of war
  for off in [
    (0, 0),
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (-1,-1), (1,-1), (-1, 1)
  ]:
    explore([player_y+off[1], player_x+off[0]])
  
  # Update enemy position
  if game['player']['chased'] == True: move_all_enemies()
  else: move_local_enemies()
  
# Run player
def run(ch):
  # Destination offset
  y = 0
  x = 0

  # Init direction
  if ch == 'H': y = 0; x = -1
  elif ch == 'J': y = 1; x = 0
  elif ch == 'K': y = -1; x = 0
  elif ch == 'L': y = 0; x = 1
  elif ch == 'Y': y = -1; x = -1
  elif ch == 'U': y = -1; x = 1
  elif ch == 'B': y = 1; x = -1
  elif ch == 'N': y = 1; x = 1
  
  # Passable objects
  passable = [
    FLOOR, PASSAGE, DOOR, STAIRS, ELIXIR,
    MAGENTA_BELT, CYAN_BELT, BLUE_BELT, GREEN_BELT, RED_BELT, BLACK_BELT
  ]
  
  # Stoppable objects
  stoppable = [
    DOOR, STAIRS, ELIXIR,
    MAGENTA_BELT, CYAN_BELT, BLUE_BELT, GREEN_BELT, RED_BELT, BLACK_BELT
  ]
  
  # Move along direction
  player_y = game['player']['y']
  player_x = game['player']['x']
  while game['dungeon'][player_y+y][player_x+x] in passable:
    move(ord(ch.lower()))
    player_y = game['player']['y']
    player_x = game['player']['x']
    if game['dungeon'][player_y][player_x] in stoppable: break
    if encounter(player_y+y, player_x+x): break

# Whether a given cell is blocked
def blocked(row, col):
  # Blocked by enemy
  for enemy in game['enemies']:
    if enemy['position']['y'] == row and enemy['position']['x'] == col:
      if enemy['hp']: return True
      else: return False
  
  # Blocked by dungeon
  if game['dungeon'][row][col] in [FLOOR, DOOR, PASSAGE, STAIRS, ELIXIR]: return False
  else: return True

# Entities chase player
def move_towards(py, px, ey, ex, enemy):
  # Init move offset
  dy = py - ey
  dx = px - ex
  
  # Prevent jitter
  if dy == 0 and dx == 0: return
  
  # Possible enemy moves
  moves = []

  # Choose primaty direction
  if abs(dx) > abs(dy):
    step_x = 1 if dx > 0 else -1
    step_y = 0
    moves.append((step_y, step_x))
    step_y = 1 if dy > 0 else -1 if dy < 0 else 0
    moves.append((step_y, 0))
  else:
    step_y = 1 if dy > 0 else -1
    step_x = 0
    moves.append((step_y, step_x))
    step_x = 1 if dx > 0 else -1 if dx < 0 else 0
    moves.append((0, step_x))

  # Try moves in order
  for my, mx in moves:
    if my == 0 and mx == 0: continue
    if not blocked(ey + my, ex + mx):
      enemy['position']['y'] += my
      enemy['position']['x'] += mx
      return

# Aggravate enemies
def move_all_enemies():
  player_y = game['player']['y']
  player_x = game['player']['x']
  for enemy in game['enemies']:
    if enemy['hp'] == 0: continue
    player_y = game['player']['y']
    player_x = game['player']['x']
    if distance_to(player_y, player_x, enemy['position']['y'], enemy['position']['x']) >= 2:
      move_towards(player_y, player_x, enemy['position']['y'], enemy['position']['x'], enemy)
    else: enemy_hit(enemy)

# Local monsters chase player
def move_local_enemies():
  player_y = game['player']['y']
  player_x = game['player']['x']
  for enemy in game['enemies']:
    if enemy['hp'] == 0: continue
    enemy_y = enemy['position']['y']
    enemy_x = enemy['position']['x']
    if [enemy_y, enemy_x] in game['visited_tiles']:
      if distance_to(player_y, player_x, enemy['position']['y'], enemy['position']['x']) >= 2:
        move_towards(player_y, player_x, enemy['position']['y'], enemy['position']['x'], enemy)
      else: enemy_hit(enemy)
