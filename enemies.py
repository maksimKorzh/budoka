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
    else: message(f'You hit {name}({hp}) by {damage} points')
  else: message(f'You missed {name}({hp})')
