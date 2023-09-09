import cv2
import numpy as np

# function to detect pieces color
def detect_piece_colors(image, red, blue):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # lower and upper bounds for red and blue in hsv scale
    lower_red = np.array([159, 50, 70])
    upper_red = np.array([180, 255, 255])

    lower_blue = np.array([90, 50, 70])
    upper_blue = np.array([128, 255, 255])

    ranges = [(lower_red, upper_red, red), (lower_blue, upper_blue, blue)]

    for lower, upper, color_list in ranges:
        # finding contours of detected pieces
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # checking if found piece is big enough to be a piece and if its a circle shaped
            area = cv2.contourArea(contour)
            if area > 80:
                x, y, w, h = cv2.boundingRect(contour)
                ratio = float(w) / h
                circularity_threshold = 0.9

                if circularity_threshold <= ratio <= 1 / circularity_threshold:
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        color_list.append((cX, cY))
    
    # returnig coordinates of detected pieces                
    return image, red, blue

