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

# Player hits enemy
def player_hit(enemy):
  bonuses = BONUSES[game['player']['style']]
  game['player']['aggravate'] = True
  style = ENEMIES[enemy['name']]
  rank = RANKS[str(enemy['level'])]['degree']
  hp = enemy['hp']
  status = 'Deshi' if enemy['level'] < 8 else 'Sensei'
  name = rank + ' ' + style + ' ' + status
  for i in range(bonuses['multiple_attacks']):
    message(f'You attempt attack {i+1}')
    player_chance = game['player']['attack'] * game['player']['level']
    enemy_chance = enemy['defense'] * enemy['level']
    hit_chance = player_chance + roll_dice(1, 6) >= enemy_chance + roll_dice(1, 6)
    if bonuses['always_hit']:
      hit_chance = 1
      message('You attack first')
    if hit_chance:
      damage = roll_dice(1, game['player']['attack'] * game['player']['level']) + roll_dice(1, 6) - enemy['defense']
      if bonuses['max_damage']:
        damage = game['player']['attack'] * game['player']['level'] - enemy['defense']
        message('You attack with maximum damage')
      enemy['hp'] -= damage
      enemy['hp'] = max(0, enemy['hp'])
      if not enemy['hp']:
        enemy['name'] = game['dungeon'][enemy['position']['y']][enemy['position']['x']]
        message(f'You defeated {name}')
        game['player']['experience'] += enemy['attack'] * enemy['level']
        bonuses = BONUSES[game['player']['style']]
        if game['player']['experience'] >= game['player']['level'] ** 2 * 10:
          game['player']['level'] += 1
          game['player']['attack'] += 1 + bonuses['attack']
          game['player']['defense'] += 1 + bonuses['defense']
          game['player']['max_hp'] = game['player']['level'] * 10 + bonuses['hp']
          new_rank = RANKS[str(game['player']['level'])]['degree']
          if game['player']['level'] >= 8: game['player']['sensivity'] = True
          message(f'Congratulations! You were awarded {new_rank}')
        break
      else: message(f'You hit {name}({hp}) by {damage} points')
    else: message(f'You missed {name}({hp})')

# Enemy hits player
def enemy_hit(enemy):
  bonuses = BONUSES[ENEMIES[enemy['name']]]
  game['player']['aggravate'] = False
  style = ENEMIES[enemy['name']]
  rank = RANKS[str(enemy['level'])]['degree']
  hp = enemy['hp']
  status = 'Deshi' if enemy['level'] < 8 else 'Sensei'
  name = rank + ' ' + style + ' ' + status
  for i in range(bonuses['multiple_attacks']):
    message(f'{name} attempts attack {i+1}')
    enemy_chance = enemy['attack'] * enemy['level']
    player_chance = game['player']['defense'] * game['player']['level']
    hit_chance = enemy_chance + roll_dice(1, 6) >= player_chance + roll_dice(1, 6)
    if bonuses['always_hit']:
      hit_chance = 1
      message(f'{name} attacks first')
    if hit_chance:
      damage = roll_dice(1, enemy['attack'] * enemy['level'] + roll_dice(1, 6)) + roll_dice(1, 6) - game['player']['defense']
      if bonuses['max_damage']:
        damage = enemy['attack'] * enemy['level'] + roll_dice(1, 6) - game['player']['defense']
        message(f'{name} attacks with maximum damage')
      game['player']['hp'] -= damage
      game['player']['hp'] = max(0, game['player']['hp'])
      if not game['player']['hp']:
        message(f'You were defeated by {name}')
        curses.endwin()
        sys.exit()
        break
      message(f'{name}({hp}) hits you by {damage} points')
    else: message(f'{name} missed you')
