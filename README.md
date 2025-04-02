# StarCraft Tower Defense: Terran vs Zerg

A tower defense game inspired by StarCraft's Terran vs Zerg theme.

## Description

Defend your base against waves of Zerg units by strategically placing Terran defensive structures. The game features distinct build and wave phases - build your defenses during the build phase, then watch them fight off the Zerg invasion during the wave phase!

## Features

- **Phase-based gameplay:**
  - Build Phase: 30 seconds to place and upgrade defensive structures
  - Wave Phase: Fixed number of Zerg units attack in waves

- **Three Terran tower types:**
  - Marine (cheap, balanced attack speed and damage)
  - Firebat (medium cost, high damage, shorter range)
  - Tank (expensive, high damage, long range, slow fire rate)

- **Three Zerg enemy types:**
  - Zergling (fast, low health)
  - Hydralisk (medium speed, medium health)
  - Ultralisk (slow, high health, deals more damage)

- **Resource management:**
  - Minerals (primary resource)
  - Gas (advanced resource for better towers)

- **Tower management:**
  - Upgrade towers to increase their damage, range, and fire rate
  - Sell towers to reclaim some resources

## Controls

- **Left Mouse Button:** Place towers, select towers, upgrade/sell towers
- **1, 2, 3 Keys:** Select Marine, Firebat, or Tank tower type
- **Space:** Pause/Resume game
- **ESC:** Quit game
- **Start Wave Button:** Start the wave phase early (before timer expires)

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Ensure Python is installed on your system
2. Install Pygame: `pip install pygame`
3. Run the game: `python game.py`

## Tips for Success

- Use the build phase to strategically place your defenses
- Start with Marines for early defense
- Save gas for Tanks to handle large waves
- Upgrade your towers strategically during build phases
- Place Firebats at chokepoints
- You can start waves early if your defenses are ready
- Higher waves bring tougher enemies - prepare accordingly!