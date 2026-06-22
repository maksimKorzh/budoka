# Globals
from globals import *

# Identify enemy
def encounter(row, col):
  for enemy in game['enemies']:
    if enemy['position']['y'] == row and enemy['position']['x'] == col:
      if enemy['hp']: return enemy
  return None

# Create enemy
def create_enemy(row, col, hp, attack, defense, level, name):
  bonuses = BONUSES[ENEMIES[name]]
  return {
    'position': {'y': row, 'x': col},
    'hp': hp + bonuses['hp'],
    'attack': attack + bonuses['attack'],
    'defense': defense + bonuses['defense'],
    'level': level,
    'name': name
  }

# Promote to the next rank
def promote():
  new_belt = RANKS[str(game['player']['level']+1)]['belt']
  if new_belt not in game['player']['belts']:
    message(f'You deserve to wear {new_belt} but you need to find it first')
    return
  game['player']['level'] += 1
  game['player']['attack'] += 1
  game['player']['defense'] += 1
  game['player']['max_hp'] += game['player']['level']
  if game['player']['level'] >= 8: game['player']['sensivity'] = True
  message(f'Congratulations! You are now wearing a {new_belt} belt!')

# Player hits enemy
def player_hit(enemy):
  bonuses = BONUSES[game['player']['style']]
  game['player']['chased'] = True
  style = ENEMIES[enemy['name']]
  rank = RANKS[str(enemy['level'])]['degree']
  hp = enemy['hp']
  status = 'deshi' if enemy['level'] < 8 else 'sensei'
  name = rank + ' ' + style + ' ' + status
  for i in range(bonuses['multiple_attacks']):
    message(f'You attempt attack {i+1}')
    player_chance = game['player']['attack'] + game['player']['level']
    enemy_chance = enemy['defense'] + enemy['level']
    hit_chance = player_chance + roll_dice(1, 6) >= enemy_chance + roll_dice(1, 6)
    if bonuses['always_hit']:
      hit_chance = 1
      message('You attack first')
    if hit_chance:
      damage = roll_dice(1, game['player']['attack'] + game['player']['level']) + roll_dice(1, 6) - enemy['defense']
      if bonuses['max_damage']:
        damage = game['player']['attack'] + game['player']['level'] + roll_dice(1, 6)- enemy['defense']
        message('You attack with maximum damage')
      damage = max(1, damage)
      enemy['hp'] -= damage
      enemy['hp'] = max(0, enemy['hp'])
      if not enemy['hp']:
        enemy['name'] = game['dungeon'][enemy['position']['y']][enemy['position']['x']]
        message(f'You defeated {name}')
        game['player']['experience'] += enemy['attack'] * enemy['level']
        bonuses = BONUSES[game['player']['style']]
        if game['player']['experience'] >= game['player']['level'] ** 2 * 10: promote()
        break
      else: message(f'You hit {name}({enemy["hp"]}) by {damage} points')
    else: message(f'You missed {name}({enemy["hp"]})')

# Enemy hits player
def enemy_hit(enemy):
  bonuses = BONUSES[ENEMIES[enemy['name']]]
  game['player']['chased'] = False
  style = ENEMIES[enemy['name']]
  rank = RANKS[str(enemy['level'])]['degree']
  hp = enemy['hp']
  status = 'deshi' if enemy['level'] < 8 else 'sensei'
  name = rank + ' ' + style + ' ' + status
  for i in range(bonuses['multiple_attacks']):
    message(f'{name} attempts attack {i+1}')
    enemy_chance = enemy['attack'] + enemy['level']
    player_chance = game['player']['defense'] + game['player']['level']
    hit_chance = enemy_chance + roll_dice(1, 6) >= player_chance + roll_dice(1, 6)
    if bonuses['always_hit']:
      hit_chance = 1
      message(f'{name} attacks first')
    if hit_chance:
      damage = roll_dice(1, enemy['attack'] + enemy['level']) + roll_dice(1, 6) - game['player']['defense']
      if bonuses['max_damage']:
        damage = enemy['attack'] + enemy['level'] + roll_dice(1, 6) - game['player']['defense']
        message(f'{name} attacks with maximum damage')
      damage = max(1, damage)
      game['player']['hp'] -= damage
      game['player']['hp'] = max(0, game['player']['hp'])
      if not game['player']['hp']:
        message(f'You were defeated by {name}')
        curses.endwin()
        print(f'You need to study {game["player"]["style"].lower()} harder!')
        sys.exit()
        break
      message(f'{name}({enemy["hp"]}) hits you by {damage} points')
    else: message(f'{name} missed you')
