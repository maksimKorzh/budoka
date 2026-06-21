# Packages
from globals import *

# Move player
def move(ch):
  # clear previous message
  screen.move(0, 0)
  screen.clrtoeol()

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
  
  # Fog of war
  for off in [
    (0, 0),
    (1, 0), (-1, 0), (0, 1), (0, -1),
  ]:
    explore([player_y+off[1], player_x+off[0]])
  
  # Update enemy position
  if game['player']['aggravate'] == True: move_all_enemies()
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

  # Move along direction
  player_y = game['player']['y']
  player_x = game['player']['x']
  while game['dungeon'][player_y+y][player_x+x] in [FLOOR, PASSAGE, DOOR, STAIRS]:
    move(ord(ch.lower()))
    player_y = game['player']['y']
    player_x = game['player']['x']
    if game['dungeon'][player_y][player_x] in [DOOR, STAIRS]: break
    if encounter(player_y+y, player_x+x): break

# Whether a given cell is blocked
def blocked(row, col):
  # Blocked by enemy
  for enemy in game['enemies']:
    if enemy['position']['y'] == row and enemy['position']['x'] == col:
      return True
  
  # Blocked by dungeon
  if game['dungeon'][row][col] in [FLOOR, DOOR, PASSAGE]: return False
  else: return True

# Get distance between two cells
def distance_to(py, px, ey, ex):
  dy = ey - py
  dx = ex - px
  return math.sqrt(dx**2 + dy**2)

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

# Aggravate monster
def move_all_enemies():
  for enemy in game['enemies']:
    if enemy['hp'] == 0: continue
    player_y = game['player']['y']
    player_x = game['player']['x']
    if distance_to(player_y, player_x, enemy['position']['y'], enemy['position']['x']) >= 2:
      move_towards(player_y, player_x, enemy['position']['y'], enemy['position']['x'], enemy)

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
