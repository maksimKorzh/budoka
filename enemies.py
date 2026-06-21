# Globals
from globals import *

# Identify enemy
def encounter(row, col):
  for enemy in game['enemies']:
    if enemy['position']['y'] == row and enemy['position']['x'] == col:
      if enemy['hp']: return enemy
  return None

# Create enemy
def create_enemy(row, col, hp, attack, defense, level, style):
  return {
    'position': {'y': row, 'x': col},
    'hp': hp,
    'attack': attack,
    'defense': defense,
    'level': level,
    'style': style
  }

# Player hits enemy
def player_hit(enemy):
  style = ENEMIES[enemy['style']]
  rank = RANKS[str(enemy['level'])]['degree']
  hp = enemy['hp']
  name = rank + ' ' + style + ' practitioner'
  player_chance = game['player']['attack'] * game['player']['level']
  enemy_chance = enemy['defense'] * enemy['level']
  hit_chance = player_chance + roll_dice(1, 6) >= enemy_chance + roll_dice(1, 6)
  if hit_chance:
    damage = game['player']['attack'] * game['player']['level'] + roll_dice(1, 6) - enemy['defense']
    enemy['hp'] -= damage
    enemy['hp'] = max(0, enemy['hp'])
    if not enemy['hp']:
      enemy['style'] = game['dungeon'][enemy['position']['y']][enemy['position']['x']]
      message(f'You defeated {name}')
      game['player']['experience'] += enemy['attack'] * enemy['level']
      if game['player']['experience'] >= game['player']['level'] * 10:
        game['player']['level'] += 1
        game['player']['attack'] += 1
        game['player']['defense'] += 1
        game['player']['hp'] = game['player']['level'] * 2
        new_rank = RANKS[str(game['player']['level'])]['degree']
        message(f'Congratulations! You were awarded {new_rank}')
    else: message(f'You hit {name}({hp}) by {damage} points')
  else: message(f'You missed {name}({hp})')

# Enemy hits player
def enemy_hit(enemy):
  style = ENEMIES[enemy['style']]
  rank = RANKS[str(enemy['level'])]['degree']
  hp = enemy['hp']
  name = rank + ' ' + style + ' practitioner'
  enemy_chance = enemy['attack'] * enemy['level']
  player_chance = game['player']['defense'] * game['player']['level']
  hit_chance = enemy_chance + roll_dice(1, 6) >= player_chance + roll_dice(1, 6)
  if hit_chance:
    damage = enemy['attack'] * enemy['level'] + roll_dice(1, 6) - game['player']['defense']
    game['player']['hp'] -= damage
    #game['player']['hp'] = max(0, game['player']['hp'])
    
    message(f'{name}({hp}) hits you by {damage} points')
  else: message(f'{name} missed you')
