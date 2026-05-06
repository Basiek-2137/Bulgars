from ultralytics import YOLO
import numpy as np

class PoseDetector:
    def __init__(self, model_type="yolov8n-pose.pt"):
        self.model = YOLO(model_type)
        self.device = 'cpu'
        # Bufor na poprzednie punkty i współczynnik wygładzania dla stabilności
        self.prev_keypoints = None
        self.alpha = 0.8  # Wartość od 0.1 (bardzo płynne) do 1.0 (surowe dane)
        self.front_leg = "RIGHT"

    def get_keypoints(self, frame):
        results = self.model.track(frame, persist=True, verbose=False, device=self.device, conf=0.5)

        if not results or not results[0].boxes or len(results[0].boxes) == 0:
            return None

        boxes = results[0].boxes.xywh.cpu().numpy()
        areas = boxes[:, 2] * boxes[:, 3]
        biggest_user_idx = np.argmax(areas)
        current_keypoints = results[0].keypoints.data[biggest_user_idx].cpu().numpy()

        if self.prev_keypoints is None:
            self.prev_keypoints = current_keypoints
            return current_keypoints

        smoothed_keypoints = current_keypoints.copy()

        # 1. NAJPIERW STABILIZUJEMY KOSTKI (Kotwice)
        # Kostki (15, 16) niemal się nie ruszają w bułgarze, więc wygładzamy je ekstremalnie
        for ankle_idx in [15, 16]:
            if current_keypoints[ankle_idx][2] > 0.5:
                smoothed_keypoints[ankle_idx][0] = (0.1 * current_keypoints[ankle_idx][0] +
                                                    0.9 * self.prev_keypoints[ankle_idx][0])
                smoothed_keypoints[ankle_idx][1] = (0.1 * current_keypoints[ankle_idx][1] +
                                                    0.9 * self.prev_keypoints[ankle_idx][1])

        # 2. TERAZ RESZTA CIAŁA I KOLANA
        for i in range(len(current_keypoints)):
            if current_keypoints[i][2] > 0.5:
                # Jeśli to kostka, już ją obsłużyliśmy wyżej
                if i in [15, 16]: continue

                is_knee = i in [13, 14]
                current_alpha = 0.2 if is_knee else 0.6  #

                new_x = (current_alpha * current_keypoints[i][0] + (1 - current_alpha) * self.prev_keypoints[i][0])
                new_y = (current_alpha * current_keypoints[i][1] + (1 - current_alpha) * self.prev_keypoints[i][1])
                if is_knee:
                    # 1. Zwiększamy responsywność (mniej "pamięci" poprzedniej klatki)
                    # Zmiana z 0.2 na 0.4 sprawi, że kropka będzie szybciej reagować na ruch.
                    current_alpha = 0.4
                    new_x = (current_alpha * current_keypoints[i][0] + (1 - current_alpha) * self.prev_keypoints[i][0])
                    new_y = (current_alpha * current_keypoints[i][1] + (1 - current_alpha) * self.prev_keypoints[i][1])

                    hip_y = self.prev_keypoints[i - 2][1]
                    stable_ankle_y = smoothed_keypoints[i + 2][1]
                    leg_full_dist = abs(stable_ankle_y - hip_y)

                    is_back_knee = (i == 13 and self.front_leg == "RIGHT") or \
                                   (i == 14 and self.front_leg == "LEFT")

                    if is_back_knee:
                        # NOGA TYLNA: Zmniejszamy wagę poprawki (z 0.7 na 0.4)
                        # Teraz YOLO ma 60% wpływu, a nasza "matematyka" tylko 40% asysty.
                        f_hip_idx = 12 if self.front_leg == "RIGHT" else 11
                        f_ankle_idx = 16 if self.front_leg == "RIGHT" else 15
                        ref_height = abs(smoothed_keypoints[f_ankle_idx][1] - smoothed_keypoints[f_hip_idx][1])

                        target_y = hip_y + (ref_height * 0.54)
                        new_y = (0.6 * new_y) + (0.4 * target_y)
                        new_x += 2  # Lekkie odsunięcie od uda[cite: 2]
                    else:
                        # NOGA PRZEDNIA: Utrzymujemy 45% wysokości dla poprawnego kąta[cite: 1, 3]
                        target_y = hip_y + (leg_full_dist * 0.45)
                        new_y = (0.5 * new_y) + (0.5 * target_y)

                smoothed_keypoints[i][0] = new_x
                smoothed_keypoints[i][1] = new_y
            else:
                smoothed_keypoints[i] = self.prev_keypoints[i]

        self.prev_keypoints = smoothed_keypoints
        return smoothed_keypoints

    def calculate_angle(self, a, b, c):
        a, b, c = np.array(a[:2]), np.array(b[:2]), np.array(c[:2])
        rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(rad * 180.0 / np.pi)
        return 360 - angle if angle > 180 else angle

