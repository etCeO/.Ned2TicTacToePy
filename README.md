# NED Robot Tic-Tac-Toe Automation

- Developed a fully autonomous Tic-Tac-Toe system for NED robots using Python, integrating HSV-based computer vision, state-driven control logic, coordinated motion planning, and real-time game tracking within an academic robotics lab environment.

## Author Info

- Full Name: Ethan E. Lopez
- Chapman Email: etlopez@chapman.edu

## Usage

- This program enables a NED robot to autonomously play a game of Tic-Tac-Toe against a human player.
- Once initialized, it detects game pieces, finds valid moves, performs physical moves of placing discs, and keeps track of the game state until a winning or draw condition is reached.
- Game progress and results are depicted by the real-time logs in the terminal.

## Input Format

1. Physical Input:
- The red and blue circular discs on a 3×3 Tic-Tac-Toe board
- Buttons: "Finished", "Easy", or "Difficult" to indicate human decisions for level selection and turn recognition
- Human player moves are visually detected by the robot's camera

2. Visual Input:
- Processing of live camera feed using HSV color space to differentiate the colors of the discs

3. Configuration Parameters:
- HSV threshold values for color detection
- Predefined robot coordinates for board positions and pickup locations

## Implementation Details

- Implemented in Python with robotics control, computer vision, and game logic
- Applies HSV-based image processing for robust detection and classification of red and blue game pieces under changing light conditions
- Utilizes state-based control logics to manage turn order, legitimate movements, and signaling game completion
- Motion sequences of disk pick-up, place, and reset are executed by coordinated motion loops
- Terminal logging gives insight into robot decisions, detected moves, and match outcomes
- Designed and tested in an academic robotics lab environment using NED hardware
