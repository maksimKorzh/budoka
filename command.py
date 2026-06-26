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
  elif ch == ord('p'):
    if game['player']['hp'] < game['player']['max_hp']:
      message(f'You practice {game["player"]["style"]} and start to feel better')
    else: message(f'You practice {game["player"]["style"]} but it gives no effect')
    for i in range(50):
      player_y = game['player']['y']
      player_x = game['player']['x']
      for enemy in game['enemies']:
        if enemy['hp'] == 0: continue
        player_y = game['player']['y']
        player_x = game['player']['x']
        if distance_to(player_y, player_x, enemy['position']['y'], enemy['position']['x']) <= 4:
          message(f'Enemy approaches while you practicing {game["player"]["style"]}')
          return
      regenerate_hp()
      move_all_enemies()
  elif ch == ord(','):
    item = game['dungeon'][game['player']['y']][game['player']['x']]
    if item in list(RANKS.keys()):
      belt = RANKS[item]['belt']
      if belt in game['player']['belts']:
        message(f'You already have a {belt} belt')
        return
      game['player']['belts'].append(belt)
      game['dungeon'][game['player']['y']][game['player']['x']] = FLOOR
      message(f'You picked up {belt} belt')
      if game['player']['experience'] < game['player']['level'] ** 2 * 10:
        message(f'You don\'t deserve to wear {belt} belt yet')
      else: promote()
    elif item == ELIXIR:
      if game['player']['hp'] < game['player']['max_hp']:
        game['player']['hp'] = game['player']['max_hp']
        message('You drank the elixir of health and fully recovered')
      else: message('You drank the elixir of health but it gives no effect')
      game['dungeon'][game['player']['y']][game['player']['x']] = FLOOR
  elif ch == ord('i'):
    belts = game['player']['belts']
    message(f'Belts you have: {", ".join(belts)}')
  elif ch == ord('f'):
    fight()
    move_local_enemies()
  elif ch == ord('>'):
    if game['dungeon'][game['player']['y']][game['player']['x']] == STAIRS:
      if game['level'] == max([int(i) for i in list(RANKS.keys())])-1:
        message('You have reached the deepest level')
        return
      game['level'] += 1
      make_level()
  elif ch == ord('<'):
    if game['dungeon'][game['player']['y']][game['player']['x']] == STAIRS:
      required_belt = RANKS[str(game['level']-(1 if game['level'] > 1 else 0))]['belt']
      if required_belt in game['player']['belts']:
        game['level'] -= 1
        if game['level'] == 0:
          screen.clear()
          if len(game['player']['belts']) == 7:
            screen.addstr(10, 25, 'You have been accepted by the martial art')
            screen.addstr(11, 25, f'community as an acknowledged {game["player"]["style"]} sensei')
            screen.addstr(12, 30, 'You may now start your own dojo')
          else: 
            screen.addstr(10, 25, f'You have escaped with {", ".join(game["player"]["belts"])} belt(s)')
            screen.addstr(11, 27, f'and earned {game["player"]["experience"]} experience points')
          read_key()
          curses.endwin()
          sys.exit()
        else: make_level()
      else: message(f'You need to have {required_belt} belt to ascend')
  elif ch == ord('q'):
    curses.endwin()
    sys.exit()
