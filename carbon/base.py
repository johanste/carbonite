"""Base classes for developers extending the carbon APIs (e.g. implement custom detectors etc.)
"""

import abc

import carbon

class BaseDetector:
    """Base class for all detectors.
    
    :ivar session: Session associated with the detector.
    """

    def initialize(self, session: carbon.Session) -> None:
        """Initialize the detector for the given session.
        

        """
        self.session = session

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...