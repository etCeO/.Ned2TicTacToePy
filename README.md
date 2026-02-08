# NED Robot Tic-Tac-Toe Automation

- Developed a fully autonomous Tic-Tac-Toe system for NED robots using Python, integrating HSV-based computer vision, state-driven control logic, coordinated motion planning, and real-time game tracking within an academic robotics lab environment.

## Author Info

- Full Name: Ethan E. Lopez
- Chapman Email: etlopez@chapman.edu

## Usage

- This program enables a NED robot to autonomously play a game of Tic-Tac-Toe against a human player.
- Once initialized, the robot detects game pieces, determines valid moves, executes physical actions to place discs, and tracks the game state until a win or draw condition is reached.
- Game progress and results are displayed through real-time terminal logs.

## Input Format

1. Physical Input:
- Red and blue circular discs placed on a 3×3 Tic-Tac-Toe board
- Human player moves are detected visually via the robot’s camera

2. Visual Input:
- Live camera feed processed using HSV color space to distinguish disc colors

3. Configuration Parameters:
- HSV threshold values for color detection
- Predefined robot coordinates for board positions and pickup locations

## Implementation Details

- Implemented in Python, combining robotics control, computer vision, and game logic
- Uses HSV-based image processing to reliably detect and classify red and blue game pieces in varying lighting conditions
- Employs state-based control logic to manage turn order, move validation, and game completion
- Motion sequences are executed through coordinated movement loops for disc pickup, placement, and reset actions
- Terminal logging provides visibility into robot decisions, detected moves, and match outcomes
- Designed and tested in an academic robotics lab environment using NED hardware
