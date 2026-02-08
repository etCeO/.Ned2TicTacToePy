# Ethan E. Lopez
# January 18, 2026
# Final Project - Tic Tac Toe Game

# References
# CHATGPT asssistance for find_winning_move() and difficult_mode() functions - https://chatgpt.com/
# code copied from assignment instructions

# README
# this script programs Ned to play a live tic tac toe game with a human player
# instructions are printed out in the terminal in each step of the game
# human player can choose easy or difficult mode via the button panel connected to the robot
# terminal tic tac toe board is printed out in terms of the ROBOT's POV

from pyniryo import * # imports NiryoRobot and all other robot functions
import numpy as np # imports numpy for arrays
import cv2 # imports openCV functions
import random # imports random number generation

robot = NiryoRobot('10.10.10.10') # establishes robot
robot.calibrate_auto() # calibrates axes

board = [['-','-','-'],['-','-','-'],['-','-','-']] # initializes an empty tic tac toe board
# in python, we'll represent this using a 3x3 2D list

markNum = 1 # keeps track of player turns

# ROBOT POSITIONS

# Board Positions - ROBOT POV
pos1 = [0.304, 0.036, 0.083, 2.949, 1.485, 2.772] # top left square
pos2 = [0.296, -0.008, 0.082, 2.695, 1.535, 2.64] # top middle square
pos3 = [0.302, -0.055, 0.082, 3.007, 1.498, 3.055] # top right square
pos4 = [0.258, 0.036, 0.084, 3.023, 1.399, 3.081] # middle left square
pos5 = [0.256, -0.007, 0.084, -2.946, 1.418, -2.946] # center square
pos6 = [0.253, -0.049, 0.085, -2.741, 1.453, -2.841] # middle right square
pos7 = [0.208, 0.035, 0.086, 2.944, 1.456, 2.937] # bottom left square
pos8 = [0.208, -0.007, 0.084, -3.071, 1.419, 3.127] # bottom middle square
pos9 = [0.205, -0.049, 0.085, -3.041, 1.464, 3.135] # bottom right square
grid = [[pos1, pos2, pos3], 
        [pos4, pos5, pos6], 
        [pos7, pos8, pos9]] # 2D list for robot position accessibility and visualization

# Main Positions
grab_pos = [0.165, 0.125, 0.062, -1.799, 1.384, -0.493] # pose coordinates used to grab discs
home_pos = [0.14, -0.0, 0.203, 0.0, 0.759, -0.001] # pose coordinates for home position

# Sad Positions
headshake_pos1 = [0.206, -0.044, 0.191, 0.06, 1.022, -0.228] # robot shakes head to the left
headshake_pos2 = [0.208, 0.023, 0.188, 0.054, 1.083, 0.081] # robot shakes head to the right
lookdown_pos = [0.158, -0.006, 0.156, -2.501, 0.781, -3.098] # robot looks down

# Happy Positions
happy_pos1 = [0.419, 0.336, 0.195, 0.982, 0.537, -2.522] # robot raises arm up
happy_pos2 = [1.419, 0.336, 0.195, 0.982, 0.537, -2.522] # partial spins on the bottom axis

grab_pos_initial = grab_pos[2] # stores original z coordinate for grab position
approach_height = 0.02 # 20 mm = 0.02 m
# this height is continuously adjusted throughout the program to ensure the robot doesn't collide with the board and discs

def print_board():
# a function to print a terminal version of the tic tac toe board
# borrowed from Assignment 4 instructions
    print('   0 1 2')
    for i, row in enumerate(board):
        print(f'{i}  {row[0]} {row[1]} {row[2]}')

def save_image(image_name):
# a function that saves an image from Ned's camera to the local folder
# takes in a parameter "image_name", a string specifying the image's title
    observation_pose1 = [0.150, 0.010, 0.220, 1.420, 1.500, 1.410] # first observation pose coordinates
    observation_pose2 = [0.152, 0.011, 0.224, 1.421, 1.507, 1.410] # second observation pose coordinates
    # two observations are needed for robot stability and accurate image capturing
    robot.move(PoseObject(*observation_pose1)) # move the robot to the first observation pose
    robot.move(PoseObject(*observation_pose2)) # move the robot to the second observation pose
    
    img_compressed = robot.get_img_compressed() # retrieve the image from the robot
    img = uncompress_image(img_compressed) # uncompress the image and store it in a variable

    cv2.imwrite(image_name, img) # save it to the local folder and begin processing

def scan_image(image):
# a function that scans Ned's tic tac board image, updating the terminal tic tac toe board based on hsv color detection
# takes in a parameter "image", retrieving the saved image from the local folder
    img = cv2.imread(image) # read the saved image
    im_work = extract_img_workspace(img, workspace_ratio=1.0) # extract the center workspace (tic tac toe board) from the image

    # resize workspace to 300x300 for clearer viewing and cropping options
    im_work = cv2.resize(im_work, (300,300), interpolation=cv2.INTER_NEAREST)

    for i in range(0, 9):
    # for all 9 tic tac toe sections
        if i < 3: # if in the first three iterations
            img_cropped = im_work[10:100, (10+i*95):(100+i*95)]
            # crop the image sections from the top row
        elif i < 6: # if in the middle three iterations
            img_cropped = im_work[105:195, (10+(i-3)*95):(100+(i-3)*95)]
            # crop the image sections from the middle row
        else: # if for the last three iterations
            img_cropped = im_work[200:290, (10+(i-6)*95):(100+(i-6)*95)]
            # crop the image sections from the bottom row
                    
        # BLUE COLOR DETECTION

        hsv_image = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2HSV) # create an HSV from the cropped image

        blue_lower = np.array([100, 100, 100]) # define lower blue range
        blue_upper = np.array([130, 255, 255]) # define upper blue range
        blue_mask = cv2.inRange(hsv_image, blue_lower, blue_upper) # create blue mask

        total_pixels = im_work.shape[0] * im_work.shape[1] # calculate total workspace pixels (300x300)
        blue_pixels = cv2.countNonZero(blue_mask) # count blue pixels in the cropped image
        percent_blue = (blue_pixels/total_pixels) * 100 # calculate the percent of blue pixels

        if percent_blue > 3:
        # if the blue pixel percentage is greater than 3, this means there's a blue marker (o) in the section
            if i < 3:
            # if the iteration is less than 3
                board[0][i%3] = 'o' # assign terminal board coordinates in the top row
            elif i < 6:
            # if the iteration is less than 6
                board[1][i%3] = 'o' # assign terminal board coordinates in the middle row
            else:
            # otherwise
                board[2][i%3] = 'o' # the terminal marker is located in the bottom row

        # RED COLOR DETECTION
        
        # define lower red ranges
        red_lower1 = np.array([0,100,100])
        red_upper1 = np.array([10,255,255])

        # define upper red ranges
        red_lower2 = np.array([160,100,100])
        red_upper2 = np.array([179,255,255])

        mask1 = cv2.inRange(hsv_image, red_lower1, red_upper1) # create a mask for the lower red range
        mask2 = cv2.inRange(hsv_image, red_lower2, red_upper2) # create a mask for the upper red range
        red_mask = cv2.bitwise_or(mask1, mask2) # combine the masks together to create an absolute red mask

        red_pixels = cv2.countNonZero(red_mask) # count red pixels in the cropped image
        percent_red = (red_pixels/total_pixels) * 100 # calculate the percent of red pixels

        if percent_red > 3:
        # if the red pixel percentage is greater than 3, this means there's a red marker (x) in the section
            if i < 3:
            # if the iteration is less than 3
                board[0][i%3] = 'x' # assign terminal board coordinates in the top row
            elif i < 6:
            # if the iteration is less than 6
                board[1][i%3] = 'x' # assign terminal board coordinates in the middle row
            else:
            # otherwise
                board[2][i%3] = 'x' # the terminal marker is located in the bottom row

def easy_mode():
# a function displaying the robot's decision making in easy mode
# this logic is randomized rather than strategic so the human can easily win
    while True:
    # while it is Ned's turn
        row = random.randint(0,2) # assign robot's row choice to a random index between 0 and 2
        col = random.randint(0,2) # assign robot's column choice to a random index between 0 and 2
        if board[row][col] == '-': # if there is a dash present in the terminal tic tac toe board
        # this means Ned can go here
            move_robot(row, col) # call the move_robot function to grab the disc and place it in this spot
            break # break out of the robot's turn and continue with game play
        # if a row/column combination isn't valid because someone already went there, the loop continues until a spot is found

def find_winning_move(player):
# a helper function for difficult_mode()
# takes in parameter "player", to identify if we're checking robot or human winning moves
# CHATGPT assistance: "this is a function showing easy mode for a ned robot playing tic tac toe... 
# how do i update this to difficult mode so that the human player rarely wins?"
    for r in range(3): # for each row in board
        for c in range(3): # for each column in board
            if board[r][c] == '-': # if there is a blank spot
                board[r][c] = player # test this move to see if the robot or human wins
                result = check_win() # evaluate check_win() result
                board[r][c] = '-' # undo test move to carry on with actual game play

                if player == 'o' and result == "The ROBOT won!":
                # if the robot is the player and this move results in a win
                    return (r, c) # return the row and column so the robot can play here

                if player == 'x' and result == "You won!":
                # if the human is the player and this move results in a win
                    return (r, c) # return the row and column so the robot can block the human here

    return None # if there are no winning moves, return None

def difficult_mode():
# a function displaying the robot's decision making in difficult mode
# this logic is strategic so the human rarely wins
# CHATGPT assistance: "this is a function showing easy mode for a ned robot playing tic tac toe... 
# how do i update this to difficult mode so that the human player rarely wins?"
    
    # ROBOT checks if they have any winning moves
    move = find_winning_move('o') # call helper function to see if there are any spots to win
    if move: # if a win exists
        move_robot(move[0], move[1]) # move the robot to this position to win
        return # stop the function

    # ROBOT checks if the HUMAN has any winning moves
    move = find_winning_move('x') # call helper function to see if there are any spots for the human to win
    if move: # if a win exists for the human
        move_robot(move[0], move[1]) # move the robot to this position to block the human
        return # stop the function

    # ROBOT checks if the center is available
    if board[1][1] == '-': # if the center spot is blank
        move_robot(1, 1) # move the robot here to follow optimal strategy
        return # stop the function

    # ROBOT checks if any corner spots are available
    corners = [(0,0), (0,2), (2,0), (2,2)] # coordinates for corner spots
    random.shuffle(corners) # shuffle corners
    for r, c in corners: # for every corner spot in the board
        if board[r][c] == '-': # if there is a blank corner spot
            move_robot(r, c) # move the robot here
            return # stop the function

    # If there are no winning/blocking options, or if there are no center/corner spots
    for r in range(3): # for every row in board
        for c in range(3): # for every column in board
            if board[r][c] == '-': # simply take the first blank spot available
                move_robot(r, c) # move the robot here
                return # stop the function

def sad_motion():
# a function to express the robot's sadness when it loses or draws the game
    robot.move(PoseObject(*headshake_pos1)) # headshake left
    robot.move(PoseObject(*headshake_pos2)) # headshake right
    robot.move(PoseObject(*lookdown_pos)) # look down

def happy_motion():
# a function to express the robot's happiness when it wins
    robot.move(JointsPosition(*happy_pos1)) # raise arm up
    robot.move(JointsPosition(*happy_pos2)) # partially rotate base
    robot.move(JointsPosition(*happy_pos1)) # rotate base back

def move_robot(row, col):
# a function that picks up and places a disc in a specified spot on the tic tac toe board
# takes in 2 parameters, "row" and "col", that identify board coordinates
    pose = grid[row][col] # retrieve the robot's pose for disc placement
    pose_initial = pose[2] # store z coordinates for spot
    
    # GRABBING THE DISC
    grab1 = grab_pos_initial + (approach_height/2) # position the robot to move slightly above the selected disc
    grab_pos[2] = grab1 # assign this position to the grab sequence
    robot.move(PoseObject(*grab_pos)) # move Ned above the disc
    grab2 = grab_pos_initial # position the robot to move towards the disc
    grab_pos[2] = grab2 # assign this new position to the grab sequence
    robot.move(PoseObject(*grab_pos)) # move Ned to touch the disc
    robot.grasp_with_tool() # Ned grasps the disc
    grab_pos[2] = grab1 + approach_height # position the robot to lift the disc from the pile
    robot.move(PoseObject(*grab_pos)) # move Ned to this new position to avoid collision
    
    # PLACING THE DISC IN THE SPOT
    tac1 = pose_initial + approach_height # position the robot to move slightly above the selected spot
    pose[2] = tac1 # assign this position to the placement sequence
    robot.move(PoseObject(*pose)) # move Ned above the spot
    tac2 = pose_initial + (approach_height/2) # position the robot to move towards the spot
    pose[2] = tac2 # assign this new position to the placement sequence
    robot.move(PoseObject(*pose)) # move Ned to touch the spot
    robot.release_with_tool() # Ned releases the disc
    pose[2] = tac1 # position the robot to lift away from the disc
    robot.move(PoseObject(*pose)) # move Ned to this new position to avoid collision
    robot.move(PoseObject(*home_pos)) # move Ned to the home position to signal turn completion

def mode_selection():
# a function to define game modes based on button selection
    while True: # while the robot is waiting for mode selection
        button1 = robot.digital_read('DI3') # define the location of button 1
        button2 = robot.digital_read('DI1') # define the location of button 2
        if button1==PinState.HIGH: # if button 1 is activated
            return 'EASY' # this means the player chose easy mode
        elif button2==PinState.HIGH: # if button 2 is activated
            return 'DIFFICULT' # this means the player chose difficult mode
    # CAUTION: this function will not deactivate until one of these 2 buttons are pressed

def finished():
# a function signaling when the human player has finished their turn
    while True: # while the robot is waiting for turn completion
        button = robot.digital_read('DI2') # define the location of the "finished" button
        if button==PinState.HIGH: # if this button is activated
            return 'finished' # this means the human player is done and game play can continue
    # CAUTION: this function will not deactivate until this button is pressed
        
def check_win():
# a function to check if you or the robot won the game
# checks if anyone won using the normal rules of tic tac toe for rows, columns, and diagonals

    # VERTICAL / HORIZONTAL CASES
    for i in range(0,3): # for valid board indices 0 through 2
        if (board[i][0] == 'x') and (board[i][1] == 'x') and (board[i][2] == 'x'):
        # if there is a row of x's
            return "You won!" # we won the game
        elif (board[0][i] == 'x') and (board[1][i] == 'x') and (board[2][i] == 'x'):
        # if there is a column of x's
            return "You won!" # we also won the game
        elif (board[i][0] == 'o') and (board[i][1] == 'o') and (board[i][2] == 'o'):
        # if there is a row of o's
            return "The ROBOT won!" # the robot won the game
        elif (board[0][i] == 'o') and (board[1][i] == 'o') and (board[2][i] == 'o'):
        # if there is a column of o's
            return "The ROBOT won!" # the robot also won the game

    # DIAGONAL CASES
    if (board[0][0] == 'x') and (board[1][1] == 'x') and (board[2][2] == 'x'):
    # if there's a left diagonal of x's
        return "You won!" # we won
    elif (board[0][0] == 'o') and (board[1][1] == 'o') and (board[2][2] == 'o'):
    # if there's a left diagonal of o's
        return "The ROBOT won!" # the robot won
    elif (board[0][2] == 'x') and (board[1][1] == 'x') and (board[2][0] == 'x'):
    # if there's a right diagonal of x's
        return "You won!" # we won
    elif (board[0][2] == 'o') and (board[1][1] == 'o') and (board[2][0] == 'o'):
    # if there's a right diagonal of o's
        return "The ROBOT won!" # the robot won
    else:
    # otherwise this could mean two things
    # 1) we both lost the game / CAT(draw)
    # 2) the game is still in play
        draw = True # let's assume there is a draw / CAT game first
        # to debunk a draw, we have to prove there are dashes still on the board
        for row in board:
        # for every row in the board
            for tac in row:
            # for every character in row
                if tac == '-':
                # if there is at least one dash, that means the game is still in play
                    draw = False # set draw equal to false
                    return draw # return this value

        # if there are no dashes found        
        if draw == True: # all players filled the board and no one won
            return "Draw! Game over!" # return there is a draw to conclude the game

def ticTacToe():
# the "main" function simulating the final game play
    robot.move(PoseObject(*home_pos)) # Ned goes to the home position first
    global markNum # calls the markNum variable to check player turns
    print() # newline for readability
    print("Let's play tic tac toe!", end='\n\n') # greeting message
    print("Choose your mode... Easy or Difficult?", end='\n\n') # prompt for mode selection
    mode = mode_selection() # store mode selected in a variable
    print("MODE SELECTED --> ", mode) # print mode selection
    print() # newline for neatness
    if mode == 'EASY':
        # if the mode chosen was EASY
        print("Let's begin!", end='\n\n') # begin easy game play
        # EASY GAME LOOP
        while True: # while the game is in play
            print("Your Move... Push 'Finished' When Done...", end='\n\n') # tell the human to make their move
            turn = finished() # store the result of the human turnn
            if turn == 'finished': # if the human pressed the 'finished' button
                save_image(f"mark{markNum}_.png") # allow Ned to capture the board's image
                scan_image(f"mark{markNum}_.png") # update the terminal tic tac toe board to include the latest moves
                markNum += 1 # increment marks for human turn
                if (check_win() != False): # analyze board (False means the game is not over)
                # if the game is over
                    print_board() # display the final tic tac toe board
                    print() # newline for neatness
                    print(check_win()) # print the result of the game, either human winning or draw in this case
                    sad_motion() # have the robot do a sad motion to indicate they lost
                    break # break from the game loop
                print_board() # otherwise, display the tic tac toe board
                print() # newline for neatness
                print("Robot's Move...", end='\n\n') # tell the robot to make their move
                easy_mode() # robot makes move
                save_image(f"mark{markNum}_.png") # allow Ned to capture the board's image
                scan_image(f"mark{markNum}_.png") # update the terminal tic tac toe board to include the latest moves
                markNum += 1 # increment marks for robot turn
                if (check_win() != False): # analyze board (False means the game is not over)
                # if the game is over
                    print_board() # display the final tic tac toe board
                    print() # newline for neatness
                    print(check_win()) # print the result of the game, in this case the robot winning
                    happy_motion() # have the robot do a happy motion to indicate they won
                    break # break from the game loop
            print_board() # otherwise, display the tic tac toe board
            print() # newline for neatness

    if mode == 'DIFFICULT':
        # if the mode chosen was DIFFICULT
        print("Let's begin!", end='\n\n') # begin easy game play
        # DIFFICULT GAME LOOP
        while True: # while the game is in play
            print("Your Move... Push 'Finished' When Done...", end='\n\n') # tell the human to make their move
            turn = finished() # store the result of the human turn
            if turn == 'finished': # if the human pressed the 'finished' button
                save_image(f"mark{markNum}_.png") # allow Ned to capture the board's image
                scan_image(f"mark{markNum}_.png") # update the terminal tic tac toe board to include the latest moves
                markNum += 1 # increment marks for human turn
                if (check_win() != False): # analyze board (False means the game is not over)
                # if the game is over
                    print_board() # display the final tic tac toe board
                    print() # newline for neatness
                    print(check_win()) # print the result of the game, either human winning or draw in this case
                    sad_motion() # have the robot do a sad motion to indicate they lost
                    break # break from the game loop
                print_board() # otherwise, display the tic tac toe board
                print() # newline for neatness
                print("Robot's Move...", end='\n\n') # tell the robot to make their move
                difficult_mode() # robot makes move
                save_image(f"mark{markNum}_.png") # allow Ned to capture the board's image
                scan_image(f"mark{markNum}_.png") # update the terminal tic tac toe board to include the latest moves
                markNum += 1 # increment marks for robot turn
                if (check_win() != False): # analyze board (False means the game is not over)
                # if the game is over
                    print_board() # display the final tic tac toe board
                    print() # newline for neatness
                    print(check_win()) # print the result of the game, in this case the robot winning
                    happy_motion() # have the robot do a happy motion to indicate they won
                    break # break from the game loop
            print_board() # otherwise, display the tic tac toe board
            print() # newline for neatness
            
    # when game play is over
    print() # newline for neatness
    print("Thanks for playing :>", end='\n\n') # farewell message
    robot.move(PoseObject(*home_pos)) # move robot back to home position when the game is completed

ticTacToe() # call the main function to start the game