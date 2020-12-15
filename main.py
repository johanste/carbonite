"""Example demonstrating how the public API surface area of the platinum (carbon python) prototype 
"""
import cv2 

import carbon
import carbon.face

session = carbon.Session(carbon.face.FaceDetectorConfiguration()) # TODO: I shouldn't have to specify a configuration unless I need to configure something...

with carbon.CameraStream() as stream:

    # I can analyze a single frame like this:
    # for event in session.analyze_frame(0, next(stream.frames())):
    #   print(f'Hello: {event}')

    # I can hook up a handler for FaceDetectedEvents like this:
    @session.handler(carbon.face.FacesDetectedEvent)
    def on_face_detected(face_event: carbon.face.FacesDetectedEvent):
        import cv2
        img = stream.get_frame(face_event.frame_no)
        for face in face_event.faces:
            cv2.rectangle(img, (face['x'],face['y']), (face['x'] + face['w'], face['y'] + face['w']), (0, 255, 0), 2)
            cv2.imshow('frame', img)
            cv2.waitKey(1)

    try:
        # And continously stream things like this:
        session.analyze(stream)
    except KeyboardInterrupt:
        print('Done - going away silently...')
        cv2.destroyAllWindows()
