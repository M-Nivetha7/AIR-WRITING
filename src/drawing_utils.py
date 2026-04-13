import cv2
import numpy as np
from utils.constants import BLUE, BLACK

class AirCanvas:
    def __init__(self):
        self.prev_x, self.prev_y = 0, 0
        self.canvas = None
        self.color = BLUE
        self.brush_thickness = 8
        self.eraser_thickness = 30

    def initialize_canvas(self, frame):
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

    def draw(self, frame, x, y):
        # If starting new stroke
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = x, y

        # Draw smooth line
        cv2.line(
            self.canvas,
            (self.prev_x, self.prev_y),
            (x, y),
            self.color,
            self.brush_thickness
        )

        self.prev_x, self.prev_y = x, y

    def erase(self, x, y):
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = x, y

        cv2.line(
            self.canvas,
            (self.prev_x, self.prev_y),
            (x, y),
            BLACK,
            self.eraser_thickness
        )

        self.prev_x, self.prev_y = x, y

    def reset_position(self):
        # Lift pen (important to stop unwanted lines)
        self.prev_x, self.prev_y = 0, 0

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas[:] = 0

    def merge_canvas(self, frame):
        # Convert canvas to grayscale
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)

        # Create mask
        _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # Convert to 3 channel
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask_inv = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR)

        # Black-out area on frame
        frame_bg = cv2.bitwise_and(frame, mask_inv)

        # Take only drawing
        canvas_fg = cv2.bitwise_and(self.canvas, mask)

        # Combine
        combined = cv2.add(frame_bg, canvas_fg)

        return combined