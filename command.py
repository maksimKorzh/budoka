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
  elif ch == ord('>'):
    if game['dungeon'][game['player']['y']][game['player']['x']] == STAIRS:
      game['level'] += 1
      make_level()
  elif ch == ord('<'):
    if game['dungeon'][game['player']['y']][game['player']['x']] == STAIRS:
      game['level'] -= 1
      make_level()
  elif ch == ord('q'):
    curses.endwin()
    sys.exit()
