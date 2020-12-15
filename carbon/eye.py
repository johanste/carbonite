import carbon
import carbon.base
import carbon.face

import cv2

class EyeDetectedEvent:

    def __init__(self, frame, eyes):
        self.frame = frame
        self.eyes = eyes

class EyeDetector(carbon.base.BaseDetector):

    def __init__(self, configuration=None):
        super().__init__()
        self._eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    def start(self, session: carbon.Session):
        session.handler(carbon.face.FacesDetectedEvent)(self.analyze_face_detected_event)


    def analyze_face_detected_event(self, event: carbon.face.FacesDetectedEvent):
        frame = cv2.cvtColor(org_frame, cv2.COLOR_BGR2GRAY) # type: ignore
        events = []
        for (x,y,w,h) in event.faces:
            roi_frame = frame[y:y+h, x:x+w]
            eyes = self._eye_cascade.detectMultiScale(roi_frame)
            recognized_event = EyeDetectedEvent(
                event.frame_no,
                eyes
            )
            events.append(recognized_event)
            if self.session:
                self.session.emit(recognized_event)
        return events
