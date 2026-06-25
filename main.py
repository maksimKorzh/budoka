# Globals
from globals import *

# Character selection menu
menu = '                               Pick up your style:\n\n'
menu += '           a) Aikido   (tripple attack, always hit)\n'
menu += '           j) Judo     (defense +2, always_hit, max damage, HP +5)\n'
menu += '           k) Karate   (attack +2, max damage)\n'
menu += '           n) Ninjutsu (attack +1, defense +1, always hit, max damage)\n'
menu += '           s) Sumo     (attack +2, defense+2, HP +15)\n'
menu += '           t) Taido    (double attack, always hit, attack +1)\n\n'

# Pick up your style
try:
  screen.addstr(7, 0, menu)
  ch = chr(read_key()).upper()
  game['player']['style'] = ENEMIES[ch]
  bonuses = BONUSES[game['player']['style']]
  game['player']['max_hp'] += bonuses['hp']
  game['player']['hp'] = game['player']['max_hp']
  game['player']['attack'] += bonuses['attack']
  game['player']['defense'] += bonuses['defense']
except: pass

# Create initial level
make_level()

# Game loop
while True:
  render_screen()
  parse_command()
