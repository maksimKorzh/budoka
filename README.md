# Budoka

A roguelike game dedicated to martial arts. Fight your way through
a dungeon, collect belts, and earn your black belt.

## What it does

You play as a martial artist working your way up through six disciplines:
Aikido, Judo, Karate, Ninjutsu, Sumo, and Taido. Beat enemies to gain
experience. Grab the right belt to rank up. Get out of the dungeon
before you get overwhelmed.

Once you hit black belt + 1 dan, you unlock "sensitivity" — the ability
to see every enemy on the map. Turns the game on its head.

## Running it

No dependencies. Just Python 3.

```
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `h` `j` `k` `l` `y` `u` `b` `n` | Move (vi-style) |
| `H` `J` `K` `L` `Y` `U` `B` `N` | Run |
| `,` | Pick up a belt |
| `Space` | Skip one turn |
| `p` | Practice (skip 50 turns) |
| `i` | List your belts |

## How it works

**Belts are keys.** Each belt lets you go back up to earlier dungeon
levels. Sometimes it pays to fight weaker enemies there for extra
experience before tackling the next rank.

**Enemies have memory.** Hit someone and the whole floor comes after you.
Get hit and only nearby enemies notice. Skipping turns or wandering
around will occasionally spawn new opponents — the dungeon doesn't
wait for you.

**Six martial art classes**, each with their own belt progression
from white to black.

## Goals

- **Primary:** Collect every belt and escape. You open your own dojo.
- **Secondary:** Gain experience and get out early. Live to fight
  another day.

## Project structure

```
main.py        Entry point
command.py     Input handling
dice.py        RNG
enemies.py     Enemy logic
globals.py     Shared state
level.py       Dungeon generation
move.py        Movement system
render.py      ASCII display
room.py        Room logic
colors.py      Terminal colors
```

Nothing to install. Nothing to configure. Run it and start hitting things.

---

Found a bug or got an idea? Open an issue. PRs are welcome.
