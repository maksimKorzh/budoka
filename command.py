# Packages
from globals import *

# Process user command
def parse_command():
  screen.move(0, 0)
  screen.clrtoeol()
  render_player()
  ch = read_key()
  if ch in [ord(c) for c in 'hjklyubn']: move(ch)
  if chr(ch) in 'HJKLYUBN': run(chr(ch))
  elif ch == ord(' '):
    regenerate_hp()
    move_all_enemies()
  elif ch == ord('w'):
    for i in range(50):
      regenerate_hp()
      move_all_enemies()
  elif ch == ord(','):
    item = game['dungeon'][game['player']['y']][game['player']['x']]
    if item in list(RANKS.keys()):
      belt = RANKS[item]['belt']
      game['player']['belts'].append(belt)
    game['dungeon'][game['player']['y']][game['player']['x']] = FLOOR
    message(f'You picked up {belt} belt')
    if game['player']['experience'] < game['player']['level'] ** 2 * 10:
      message(f'You don\'t deserve to wear a {belt} belt yet.')
    else: promote()
  elif ch == ord('i'):
    belts = game['player']['belts']
    message(f'Belts you have: {", ".join(belts)}')
  elif ch == ord('>'):
    if game['dungeon'][game['player']['y']][game['player']['x']] == STAIRS:
      game['level'] += 1
      make_level()
  elif ch == ord('<'):
    if game['dungeon'][game['player']['y']][game['player']['x']] == STAIRS:
      required_belt = RANKS[str(game['level']-(1 if game['level'] > 1 else 0))]['belt']
      if required_belt in game['player']['belts']:
        game['level'] -= 1
        if game['level'] == 0:
          curses.endwin()
          print('You escaped')
          sys.exit()
        else: make_level()
      else: message(f'You need to have {required_belt} belt to ascend')
  elif ch == ord('q'):
    curses.endwin()
    sys.exit()
