# Globals
from globals import *

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
