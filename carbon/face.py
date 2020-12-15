import typing

import cv2

import carbon
import carbon.base

class Face(typing.TypedDict):
    x: int
    y: int
    h: int
    w: int


class FacesDetectedEvent:
    
    def __init__(self, frame_no: int, faces:typing.List[Face]):
        self.frame_no = frame_no
        self.faces = faces


class FaceDetector(carbon.base.BaseDetector):

    def __init__(self, configuration=None):
        super().__init__()
        self._face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self._eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    def start(self, session: carbon.Session):
        ...

    def analyze_frame(self, session, frame_no, org_frame):
        frame = cv2.cvtColor(org_frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.detectMultiScale(
            frame, scaleFactor=1.3,
            minNeighbors=5)
        events = []

        event = FacesDetectedEvent(
            frame_no,
            [{
                'x': x,
                'y': y,
                'w': w,
                'h': h
            } for x, y, w, h in faces]
        )
        if session:
            session.emit(event)
        events.append(event)
        return events

class FaceDetectorConfiguration:

    def create_detector(self):
        return FaceDetector(configuration = self)

