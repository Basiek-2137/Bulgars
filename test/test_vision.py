import cv2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vision import PoseDetector, CameraManager


def run_test():
    detector = PoseDetector()
    cam_manager = CameraManager(detector)
    frame_count = 0
    last_keypoints = None

    video_path = "../8262c14ce5cf4128a5b0db20f52956701777999730610761.mp4"
    # video_path = "../20260415_102333.mp4"
    cam_manager.cap = cv2.VideoCapture(video_path)

    # 1. WYBÓR NOGI
    front_leg_locked = "RIGHT"

    EDGES = [
        (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
        (11, 12), (5, 11), (6, 12),
        (11, 13), (13, 15), (12, 14), (14, 16)
    ]

    cv2.namedWindow('Cyber Trener - Stabilizacja', cv2.WINDOW_NORMAL)

    while True:
        success, frame = cam_manager.cap.read()
        if not success: break

        # Skalowanie filmu
        target_width = 800
        h, w = frame.shape[:2]
        target_height = int(h * (target_width / w))
        frame = cv2.resize(frame, (target_width, target_height))

        frame_count += 1

        # Analiza co 1 klatke
        if frame_count % 1 == 0:
            new_keypoints = detector.get_keypoints(frame)
            if new_keypoints is not None:
                last_keypoints = new_keypoints

        if last_keypoints is not None:
            # 2. PRZYPISANIE INDEKSÓW (na sztywno zablokowane)
            if front_leg_locked == "RIGHT":
                front_leg, back_leg_idx = (12, 14, 16), 15
                shoulder_idx, hip_idx = 6, 12
            else:
                front_leg, back_leg_idx = (11, 13, 15), 16
                shoulder_idx, hip_idx = 5, 11

            # 3. OBLICZENIA
            angle_front = detector.calculate_angle(
                last_keypoints[front_leg[0]],
                last_keypoints[front_leg[1]],
                last_keypoints[front_leg[2]]
            )

            back_tilt = abs(last_keypoints[shoulder_idx][0] - last_keypoints[hip_idx][0])

            # WERYFIKACJA
            errors = []
            if angle_front > 105:
                errors.append("ZA PLYTKO!")
            elif angle_front < 75:
                errors.append("ZA GLEBOKO!")

            if back_tilt > 60:  # Zwiększono z 50 dla pleców
                errors.append("PROSTUJ PLECY!")

            # 4. RYSOWANIE
            color = (0, 255, 0) if not errors else (0, 0, 255)
            cv2.putText(frame, f"Kat: {int(angle_front)}st", (20, 50), 0, 1.0, color, 2)
            cv2.putText(frame, f"Noga: {front_leg_locked}", (20, 130), 0, 0.7, (255, 255, 0), 1)

            if errors:
                cv2.putText(frame, errors[0], (20, 90), 0, 1.0, (0, 0, 255), 2)

            for edge in EDGES:
                p1, p2 = last_keypoints[edge[0]], last_keypoints[edge[1]]
                if p1[2] > 0.5 and p2[2] > 0.5:
                    pt1, pt2 = (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1]))
                    cv2.line(frame, pt1, pt2, (255, 255, 255), 2)
                    cv2.circle(frame, pt1, 4, (0, 255, 255), -1)

        cv2.imshow('Cyber Trener - Stabilizacja', frame)

        key = cv2.waitKey(15) & 0xFF
        if key == ord('q'): break

    cam_manager.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_test()