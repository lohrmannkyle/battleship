# 🛳️ Battleship Game Simulation (`battleship.py`)

This Python program simulates a simplified version of the classic game **Battleship**, allowing Player 2 to attempt to sink all of Player 1’s ships using guesses read from a file.

---

## 📌 Overview

The program reads:
- A **placement file** describing Player 1's ship positions
- A **guess file** containing Player 2’s firing attempts

It then processes each guess and provides feedback based on whether it results in a hit, miss, repeated guess, ship sunk, or all ships being sunk.

---

## 🔧 Usage

Run the program and enter the filenames when prompted:

```bash
$ python battleship.py
example-placement.txt
example-guess.txt
