import cv2

class CameraManager:
    def __init__(self, detector, video_capture):
        self.cap = cv2.VideoCapture(video_capture)
        self.detector = detector
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def stop(self):
        self.cap.release()

    def draw_trainer_hud(self, frame, evaluation, target_reps=10):
        counter = evaluation["counter"]
        stage = evaluation["stage"]
        errors = evaluation["errors"]
        angle = evaluation["angle"]

        cv2.rectangle(frame, (0, 0), (640, 60), (20, 20, 20), -1)

        cv2.putText(frame, f"POWTORZENIA: {counter} / {target_reps}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        kolor_fazy = (0, 165, 255) if stage == "down" else (255, 255, 255)
        cv2.putText(frame, f"FAZA: {stage.upper()} ({angle} deg)", (350, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, kolor_fazy, 2, cv2.LINE_AA)

        if errors:
            cv2.rectangle(frame, (0, 420), (640, 480), (0, 0, 139), -1)
            cv2.putText(frame, f"BLAD: {errors[0]}", (20, 455),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        return frame