import cv2

class CameraManager:
    def __init__(self, detector, video_capture):
        self.cap = cv2.VideoCapture(video_capture)
        self.detector = detector
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.detector = detector
    def stop(self):
        self.cap.release()

    def draw_coordinates_panel(self, frame, points_dict):
        if points_dict is None:
            return frame

        start_x = 20
        start_y = 30
        line_height = 25

        cv2.rectangle(frame, (10, 10), (320, 300), (0, 0, 0), -1)

        cv2.putText(frame, "PANEL DIAGNOSTYCZNY COORD", (start_x, start_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        start_y += line_height

        strony = ["lewa_noga", "prawa_noga"]
        stawy_do_wypisania = ["hip", "knee", "ankle"]

        for strona in strony:
            kolor_sekcji = (0, 255, 0) if strona == "lewa_noga" else (0, 165, 255)
            cv2.putText(frame, f"{strona.upper()}:", (start_x, start_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, kolor_sekcji, 1, cv2.LINE_AA)
            start_y += line_height

            for staw in stawy_do_wypisania:
                if staw in points_dict[strona]:
                    x, y, vis = points_dict[strona][staw]

                    tekst_wspolrzednych = f"  {staw}: X: {x}, Y: {y} (vis: {vis:.2f})"

                    cv2.putText(frame, tekst_wspolrzednych, (start_x, start_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
                    start_y += line_height

            start_y += 5

        return frame

    def draw_trainer_hud(self, frame, evaluation):
        counter = evaluation["counter"]
        stage = evaluation["stage"]
        errors = evaluation["errors"]
        angle = evaluation["angle"]

        cv2.rectangle(frame, (0, 0), (640, 60), (20, 20, 20), -1)

        cv2.putText(frame, f"POWTORZENIA: {counter}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        kolor_fazy = (0, 165, 255) if stage == "down" else (255, 255, 255)
        cv2.putText(frame, f"FAZA: {stage.upper()} ({angle} deg)", (280, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, kolor_fazy, 2, cv2.LINE_AA)

        if errors:
            cv2.rectangle(frame, (0, 420), (640, 480), (0, 0, 139), -1)  # Dark Red

            cv2.putText(frame, f"BLAD: {errors[0]}", (20, 455),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        return frame