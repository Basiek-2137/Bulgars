import cv2

class CameraManager:
    def __init__(self, detector):
        self.cap = cv2.VideoCapture(0)
        self.detector = detector
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.detector = detector
    def stop(self):
        self.cap.release()