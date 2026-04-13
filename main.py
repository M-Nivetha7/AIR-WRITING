import cv2
from src.hand_tracker import HandTracker
from src.drawing_utils import AirCanvas
def fingers_up(lm_list):
    if len(lm_list) == 0:
        return []

    fingers = []

    # Index
    fingers.append(lm_list[8][2] < lm_list[6][2])
    # Middle
    fingers.append(lm_list[12][2] < lm_list[10][2])
    # Ring
    fingers.append(lm_list[16][2] < lm_list[14][2])
    # Pinky
    fingers.append(lm_list[20][2] < lm_list[18][2])

    return fingers


def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    canvas = AirCanvas()

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        canvas.initialize_canvas(frame)

        tracker.find_hands(frame)
        lm_list = tracker.get_landmarks(frame)
        tracker.draw_hands(frame)

        if len(lm_list) != 0:
            x1, y1 = lm_list[8][1], lm_list[8][2]

            fingers = fingers_up(lm_list)

    # ✊ Fist → Clear screen
            if fingers == [False, False, False, False]:
                canvas.canvas = frame.copy() * 0

    # ✋ Two fingers → Stop drawing (move freely)
            elif fingers[0] and fingers[1]:
                canvas.reset_position()

    # ✍️ Only index → Draw
            elif fingers[0] and not fingers[1]:
                canvas.draw(frame, x1, y1)

        frame = canvas.merge_canvas(frame)

        cv2.imshow("Air Writing", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()