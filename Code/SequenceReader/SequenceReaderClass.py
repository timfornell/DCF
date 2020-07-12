import cv2
from pathlib import Path

class SequenceReaderClass():
    def __init__(self, sequence_path):
        self._sequence_is_available = False
        sequence_path = Path(sequence_path)
        if sequence_path.exists():
            self._sequence_is_available = True
            self._video = cv2.VideoCapture(sequence_path)

    def sequence_is_available(self):
        return self._sequence_is_available

    def get_new_image(self):
        self._image_is_available, self._current_image = self._video.read()
        return self._current_image

    def get_current_image(self):
        return self._current_image

    def image_is_available(self):
        return self._image_is_available
