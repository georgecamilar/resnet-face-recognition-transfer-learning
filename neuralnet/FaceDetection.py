import cv2
import dlib
import numpy
import os

class FaceCropper:
    def __init__(self) -> None:

        self.detector = dlib.get_frontal_face_detector()

    def crop_faces_from_video(self, video_path, output_directory):
        starting_index = len(os.listdir(output_directory)) + 1
        # Detects faces from the video at given path and creates new dataset entry
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.detector(gray, 1)
            for i, face in enumerate(faces):
                filename = f"{output_directory}/frame_{frame_count}_face_{i}_index_{starting_index}.jpg"
                cv2.imwrite(filename, frame)
            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()


    def resize_video(self, path, output_dir):
        cap = cv2.VideoCapture(path)
        frame_count=0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            b = cv2.resize(frame, (224, 224))
            gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)

            faces = self.detector(gray, 1)
            for i, face in enumerate(faces):
                filename = f"{output_dir}/frame_{frame_count}_face_{i}.jpg"
                cv2.imwrite(filename, frame)
            frame_count += 1
        cap.release()
        # out.release()
        cv2.destroyAllWindows()
        return "/Users/georgecamilar/Personal/licenta/experiments/resized/output.webm"


    def crop_faces_from_video_eval(self, video_path, output_dir):
        # Detects faces from the video at given path and creates new dataset entry
        images = []
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.detector(gray, 1)
            for i, face in enumerate(faces):
                filename = f"{output_dir}/frame_{frame_count}_face_{i}.jpg"
                cv2.imwrite(filename, frame)
                images.append(frame)
            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()

    def crop_faces_only_from_video(self, video_path, output_directory):
        video_capture = cv2.VideoCapture(video_path)
        frame_count = 0
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.detector(gray, 1)
            for i, face in enumerate(faces):
                filename = f"{output_directory}/frame_{frame_count}_face_{i}.jpg"
                cv2.imwrite(filename, frame)
            frame_count += 1

        video_capture.release()
        cv2.destroyAllWindows()