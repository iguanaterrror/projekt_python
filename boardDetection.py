import cv2

# function that cuts out checkers board out from the image
def find_board(img):
    # finding all squares on a picture
    squares = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        eps = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, eps, True)
        
        if len(approx) == 4:
            squares.append(approx)
    
    # choosing the biggest square        
    if squares:
        largest = max(squares, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        
        crop = img[y:y+h, x:x+w]
        
        dim = (800, 800)
        
        # scaling board cutted of from image to size of virtual board
        resized = cv2.resize(crop, dim, interpolation = cv2.INTER_AREA)
          
    return resized