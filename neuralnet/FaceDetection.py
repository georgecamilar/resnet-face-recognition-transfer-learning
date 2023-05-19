import cv2
import dlib


class FaceCropper:
    def __init__(self) -> None:
        # self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.detector = dlib.get_frontal_face_detector()

    def crop_faces_from_video(self, video_path, output_directory):
        # Detects faces from the video at given path and creates new dataset entry
        cap = cv2.VideoCapture(video_path)
        # self.detector = dlib.get_frontal_face_detector()
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.detector(gray, 1)
            for i, face in enumerate(faces):
                filename = f"{output_directory}/frame_{frame_count}_face_{i}.jpg"
                cv2.imwrite(filename, frame)
            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()