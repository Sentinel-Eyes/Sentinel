import threading
import cv2

# IP Camera
url = "http://100.82.7.117:3636/video"
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(url)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.lock = threading.Lock()  # Create a lock
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

        flipped_image = cv2.flip(image, 1)
        _, jpeg = cv2.imencode('.jpg', flipped_image)

        return jpeg.tobytes()

    def update(self):
        while True:
            with self.lock:  # Acquire the lock
                (self.grabbed, self.frame) = self.video.read()

    def get_detected_faces_frame(self):
        with self.lock:
            image = self.frame.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        detected_faces = []

        for i, (x, y, w, h) in enumerate(faces):
            face = image[y:y + h, x:x + w]  # Crop the detected face region
            flipped_face_image = cv2.flip(face, 1)
            detected_faces.append(flipped_face_image)

            # Only create a single image from the detected faces
        if detected_faces:
            combined_image = cv2.hconcat(detected_faces)
            _, jpeg = cv2.imencode('.jpg', combined_image)
            return jpeg.tobytes()
        else:
            return None  # Return None when no faces are detected


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
