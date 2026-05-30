import cv2
import mediapipe as mp
import numpy as np
from audio import VoiceAssistant
from test import test_vision

voice = VoiceAssistant('pl')

class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth=True, detection_conf=0.5, tracking_conf=0.5):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=mode,
            model_complexity=complexity,
            smooth_landmarks=smooth,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )

        self.BULGARIAN_LANDMARKS = {
            "tulow": [11, 12, 23, 24],
            "lewa_noga": {"hip": 23, "knee": 25, "ankle": 27, "heel": 29, "toe": 31},
            "prawa_noga": {"hip": 24, "knee": 26, "ankle": 28, "heel": 30, "toe": 32},
            "rece": [15, 16]
        }

        self.counter = 0
        self.stage = "up"
        self.errors = []

        self.results = None

    def detect(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        self.results = self.pose.process(image)
        image.flags.writeable = True
        if self.results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                self.results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )
        return frame

    def get_landmarks(self,frame):
        if not self.results or not self.results.pose_landmarks:
            return None

        h, w, _ = frame.shape
        landmarks = self.results.pose_landmarks.landmark

        extracted_data = {
            "tulow": {},
            "lewa_noga": {},
            "prawa_noga": {},
            "rece": {}
        }

        for idx in self.BULGARIAN_LANDMARKS["tulow"]:
            name = "lewe_ramie" if idx == 11 else "prawe_ramie" if idx == 12 else "lewe_biodro" if idx == 23 else "prawe_biodro"
            lm = landmarks[idx]
            extracted_data["tulow"][name] = (int(lm.x * w), int(lm.y * h), lm.visibility)

        for key, idx in self.BULGARIAN_LANDMARKS["lewa_noga"].items():
            lm = landmarks[idx]
            extracted_data["lewa_noga"][key] = (int(lm.x * w), int(lm.y * h), lm.visibility)

        for key, idx in self.BULGARIAN_LANDMARKS["prawa_noga"].items():
            lm = landmarks[idx]
            extracted_data["prawa_noga"][key] = (int(lm.x * w), int(lm.y * h), lm.visibility)

        for idx in self.BULGARIAN_LANDMARKS["rece"]:
            name = "lewy_nadgarstek" if idx == 15 else "prawy_nadgarstek"
            lm = landmarks[idx]
            extracted_data["rece"][name] = (int(lm.x * w), int(lm.y * h), lm.visibility)

        return extracted_data

    def calculate_angle(self, a, b, c):
        a = np.array(a[:2])
        b = np.array(b[:2])
        c = np.array(c[:2])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        return np.degrees(np.arccos(cosine_angle))

    def verify_bulgarian_split_squat(self, points, working_leg="lewa_noga"):
        if points is None:
            return {"counter": self.counter, "stage": self.stage, "errors": [], "angle": 180}

        hip_w = points[working_leg]["hip"]
        knee_w = points[working_leg]["knee"]
        ankle_w = points[working_leg]["ankle"]
        toe_w = points[working_leg]["toe"]
        shoulder = points["tulow"]["lewe_ramie"] if working_leg == "lewa_noga" else points["tulow"]["prawe_ramie"]

        angle_working_knee = self.calculate_angle(hip_w, knee_w, ankle_w)
        angle_working_hip = self.calculate_angle(shoulder, hip_w, knee_w)

        current_frame_errors = []

        if angle_working_knee <= 150:
            patrzy_w_prawo = toe_w[0] > points[working_leg]["heel"][0]
            tolerancja_palcow = 10

            if patrzy_w_prawo:
                if knee_w[0] > (toe_w[0] + tolerancja_palcow):
                    current_frame_errors.append("Kolano za daleko przed palcami!")
            else:
                if knee_w[0] < (toe_w[0] - tolerancja_palcow):
                    current_frame_errors.append("Kolano za daleko przed palcami!")

            if abs(knee_w[0] - ankle_w[0]) > 60:
                current_frame_errors.append("Kolano ucieka na boki!")

            if angle_working_hip < 80:
                current_frame_errors.append("Za mocne pochylenie tułowia!")

        is_down = angle_working_knee < 105 and angle_working_hip < 115
        is_up = angle_working_knee > 155

        if angle_working_knee < 145 and self.stage == "up":
            for err in current_frame_errors:
                if err not in self.errors:
                    self.errors.append(err)

        if is_down:
            if self.stage == "up":
                self.stage = "down"

            for err in current_frame_errors:
                if err not in self.errors:
                    self.errors.append(err)

        elif self.stage == "down":
            for err in current_frame_errors:
                if err not in self.errors:
                    self.errors.append(err)

            if is_up:
                self.stage = "up"
                if not self.errors:
                    self.counter += 1
                    print(f"Powtórzenie poprawne! Licznik: {self.counter}")
                    voice.speak("Powtórzenie poprawne!")
                else:
                    print(f"Powtórzenie odrzucone! Wykryte błędy w trakcie całego ruchu: {self.errors}")
                    voice.speak(self.errors)
                self.errors = []

        return {
            "counter": self.counter,
            "stage": self.stage,
            "errors": current_frame_errors,
            "angle": int(angle_working_knee)
        }

if __name__ == "__main__":
    test_vision