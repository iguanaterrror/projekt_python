import cv2
import os
import numpy as np
from colorDetection import detect_piece_colors
from PIL import Image, ImageDraw
from boardDetection import find_board

# function that is setting up camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)


red_det = []
blue_det = []
prev_red, prev_blue = [], []

center_coords = []

# function that is calculating coordinates of the center of the black fields
def centerCoords():
    for i in range(50, 800, 100):
        for j in range(50, 800, 100):
            if (i // 100 + j // 100) % 2 == 1:
                center_coords.append((j, i))
    
    return center_coords
       
# defining board parameters
board_size = (800, 800)
square_size = 100
piece_radius = 40

# setting up board
board = Image.new("RGB", board_size, "white")

white = "white"
black = "black"
red = "red"
blue = "blue"

draw = ImageDraw.Draw(board)

# function that finds coordinates of the pieces
def pieces_positions():
    while True:
        # reading the camera input
        ret, frame = cam.read()
        
        if not ret:
            break
        
        # showing live input
        cv2.namedWindow("live", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("live", 800, 800)  
        cv2.imshow("live", frame)
        
        # if u press esc function will stop 
        k = cv2.waitKey(1) 
        if k == 27:
            cam.release()
            cv2.destroyAllWindows()
            return None
        
        # if u press space function will proceed to finding pieces
        elif k == 32:
            # finding board and showing it then detect pieces on a cropped out image
            img_name = "frame.png"
            cv2.imwrite(img_name, frame)
            img = cv2.imread(img_name)
            board = find_board(img)
            cv2.imshow('board', board)
            detect_piece_colors(board, red_det, blue_det)

            try:
                os.remove(img_name)
            except: pass
            
            # function returns detectes pieces coordniates
            return red_det, blue_det
    return None

# function that draws piece in given color in a given coordinates
def drawPiece(draw, x, y, color):
    draw.ellipse([x - piece_radius, y - piece_radius, x + piece_radius, y + piece_radius], fill = color)
    
# function that draws board with pieces in given coordinates
def drawBoard(red_pieces, blue_pieces):
    for y in range(0, board_size[0], square_size):
        for x in range(0, board_size[1], square_size):
            if((x // square_size + y // square_size )%2 == 1):
                draw.rectangle([(x, y), (x + square_size, y + square_size)], fill = black)
            else:
                draw.rectangle([(x, y), (x + square_size, y + square_size)], fill = white)
                
            for piece in red_pieces:
                drawPiece(draw, piece[0], piece[1], red)
            
            for piece in blue_pieces:
                drawPiece(draw, piece[0], piece[1], blue)

cv2.namedWindow("warca.py", cv2.WINDOW_NORMAL)
cv2.resizeWindow("warca.py", 800, 800)   
# main loop
def main():
    center_coords = centerCoords()
                   
    while True:
        red_on_board, blue_on_board = [], []
        red_det, blue_det = pieces_positions()
        if red_det == blue_det == []:
            print("zero pieces found")
        # comapring coordinates of found pieces with the centers of a black fields on board if in range it will draw piece there
        for red_piece in red_det:
            for center in center_coords:
                if abs(red_piece[0] - center[0]) <= 65 and abs(red_piece[1] - center[1]) <= 65:
                    red_on_board.append(center)
                            
        for blue_piece in blue_det:
            for center in center_coords:
                if abs(blue_piece[0] - center[0]) <= 65 and abs(blue_piece[1] - center[1]) <= 65:
                    blue_on_board.append(center)
        
        # drawing board with found pieces on it        
        drawBoard(red_on_board, blue_on_board)

        red_det.clear()
        red_on_board.clear()
        blue_on_board.clear()
        blue_det.clear()
        
        # switching to rgb display and showing board
        realBoard = cv2.cvtColor(np.array(board), cv2.COLOR_BGR2RGB)
        cv2.imshow("warca.py", np.array(realBoard))
        

if __name__ == "__main__":
    main()