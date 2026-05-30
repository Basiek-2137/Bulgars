import cv2
from audio import VoiceAssistant
from vision import PoseDetector, CameraManager

#video_capture = 0
video_capture = "../8262c14ce5cf4128a5b0db20f52956701777999730610761.mp4";
#video_capture = "../20260415_102333.mp4"

cam = CameraManager(0,video_capture)
voice = VoiceAssistant('pl')

posse = PoseDetector()

while cam.cap.isOpened():
    ret, frame = cam.cap.read()
    if not ret:
        voice.speak("Kończenie pracy.")
        break

    frame = posse.detect(frame)
    punkty_bulgarskie = posse.get_landmarks(frame)
    raport = posse.verify_bulgarian_split_squat(punkty_bulgarskie, working_leg='prawa_noga')

    frame = cam.draw_trainer_hud(frame,raport)
    cv2.imshow('image', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.stop()
cv2.destroyAllWindows()
