import cv2
import mediapipe as mp
import numpy as np

# Init MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

canvas = None
prev_x, prev_y = 0, 0

mode = 'draw'
draw_color = (255, 0, 0)  # Start with blue
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Blue, Green, Red
color_index = 0

def draw_buttons(frame):
    cv2.rectangle(frame, (10, 10), (110, 60), (255, 0, 0), -1)  # Draw
    cv2.rectangle(frame, (120, 10), (220, 60), (0, 0, 255), -1)  # Erase
    cv2.rectangle(frame, (230, 10), (330, 60), (0, 255, 0), -1)  # Color
    cv2.putText(frame, 'Draw', (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.putText(frame, 'Erase', (135, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv2.putText(frame, 'Color', (245, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if canvas is None:
        canvas = np.zeros_like(frame)

    index_pos, middle_pos = None, None

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            landmarks = {}
            h, w, _ = frame.shape
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks[id] = (cx, cy)

            index_pos = landmarks.get(8)
            middle_pos = landmarks.get(12)

            # Two-finger tap to activate buttons
            if index_pos and middle_pos:
                ix, iy = index_pos
                mx, my = middle_pos
                if 10 < ix < 110 and 10 < iy < 60 and 10 < mx < 110 and 10 < my < 60:
                    mode = 'draw'
                elif 120 < ix < 220 and 10 < iy < 60 and 120 < mx < 220 and 10 < my < 60:
                    mode = 'erase'
                elif 230 < ix < 330 and 10 < iy < 60 and 230 < mx < 330 and 10 < my < 60:
                    color_index = (color_index + 1) % len(colors)
                    draw_color = colors[color_index]

            # Drawing/erasing only if middle finger is down (index up only)
            if index_pos and middle_pos:
                cx, cy = index_pos
                mx, my = middle_pos
                if abs(cy - my) > 40:  # Only draw if fingers are not both up
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = cx, cy

                    if mode == 'draw':
                        cv2.line(canvas, (prev_x, prev_y), (cx, cy), draw_color, 5)
                    elif mode == 'erase':
                        cv2.line(canvas, (prev_x, prev_y), (cx, cy), (0, 0, 0), 50)

                    prev_x, prev_y = cx, cy
                else:
                    prev_x, prev_y = 0, 0  # Reset on double finger up

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
    else:
        prev_x, prev_y = 0, 0

    combined = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    draw_buttons(combined)

    cv2.imshow("AirText - Interactive Drawing", combined)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:
        break
    elif key == ord('c'):
        canvas = np.zeros_like(frame)
    elif key == ord('s'):
        filename = "airtext_output.png"
        cv2.imwrite(filename, canvas)
        print(f"✅ Canvas saved as {filename}")

cap.release()
cv2.destroyAllWindows()
