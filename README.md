# 🛰️ Rover Navigation and Mine Disarmament Simulator

This project simulates a rover navigating a 2D terrain scattered with hidden mines. The rover must interpret movement commands, avoid obstacles, and safely disarm mines using a brute-force hashing strategy.

## 🚀 Project Description

The rover receives a sequence of commands to navigate the environment. Its mission is to move safely across the grid while detecting and disarming any mines it encounters.

### Supported Commands

- `L` — Turn the rover left
- `R` — Turn the rover right
- `M` — Move one step forward in the current direction
- `D` — Dig and attempt to disarm a mine at the current location

## 💣 Mine Disarmament Mechanism

Each mine is assigned a unique **serial number**. To disarm a mine, the rover must:

1. Generate a **PIN** and prepend it to the serial number.
2. Hash the combined string using **SHA-256**.
3. Check whether the hash starts with **six leading zeros (`000000`)**.
4. Repeat with new PINs until a valid one is found.

This mechanism simulates a **proof-of-work** style brute-force process.
