from typing import Tuple
import cv2

class CameraStream:
    
    def __init__(self, *, camera_no:int=0, buffer_frames=1024):
        self._video_capture = cv2.VideoCapture(camera_no)
        self.last_frame = None
        self.buffer_frames = buffer_frames
        self.frame_buf = [None] * buffer_frames
        self.frame_buf_no = 0
        self.frames_per_second = self._video_capture.get(cv2.CAP_PROP_FPS) 

    def get_frame(self, frame_no):
        return self.frame_buf[frame_no]

    def frames(self):
        while True:
            ret, frame = self._video_capture.read()
            frame_buf_no = (self.frame_buf_no + 1) % self.buffer_frames
            self.frame_buf_no = frame_buf_no
            self.frame_buf[frame_buf_no] = frame
            if ret:
                yield frame_buf_no, frame

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self._video_capture.release()
        self._video_capture = None

class Session:

    def __init__(self, *configurations):
        self._detectors = []
        self._handlers = {}
        self._closed = True

        for configuration in configurations:
            try:
                self._detectors.append(configuration.create_detector())
            except AttributeError:
                configuration.session = self
                self._detectors.append(configuration)

    def close(self):
        print('Closing')
        self._closed = True

    def open(self):
        ...

    def emit(self, event):
        try:
            self._handlers[type(event)](event)
        except KeyError:
            print(f'No handler for {type(event)}')

    def handler(self, event_type: type):
        """Used as a decorator for functions that want to handle a specific event type

        :param event_type type: The type of event to handle
        """
        def wrapped(func):
            self._handlers[event_type] = func
            return func

        return wrapped

    def analyze_frame(self, frame_no, frame):
        events = []
        for analyzer in self._detectors:
            for detected_event in analyzer.analyze_frame(self, frame_no, frame):
                events.append(detected_event)
        return events

    def analyze(self, stream):
        self._closed = False
        for frame_no, frame in stream.frames():
            if self._closed:
                return

            self.analyze_frame(frame_no, frame)

