import cv2
from pathlib import Path

class SequenceReaderClass():
    def __init__(self, sequence_path):
        self._sequence_is_available = False
        self._image_is_available = False
        self._max_frame_nr = 0
        self._current_image = None
        sequence_path = Path(sequence_path)
        if sequence_path.exists():
            self._sequence_is_available = True
            self._image_is_available = True
            self._video = cv2.VideoCapture(str(sequence_path))
            self._max_frame_nr = self._video.get(cv2.CAP_PROP_FRAME_COUNT)

    def sequence_is_available(self):
        return self._sequence_is_available

    def get_new_image(self):
        return_image = None
        if self._video.isOpened():
            self._image_is_available, self._current_image = self._video.read()
            return_image = self._current_image
            print("Current frame: {}".format(self._video.get(cv2.CAP_PROP_POS_FRAMES)))

        return self._image_is_available, return_image

    def get_current_image(self):
        return self._current_image

    def image_is_available(self):
        return self._image_is_available

    def jump_back_one_frame(self):
        current_frame_nr = self._video.get(cv2.CAP_PROP_POS_FRAMES)
        self._video.set(cv2.CAP_PROP_POS_FRAMES, current_frame_nr - 1)
        self.get_new_image()
        self._video.set(cv2.CAP_PROP_POS_FRAMES, current_frame_nr - 1)

    def jump_forward_one_frame(self):
        current_frame_nr = self._video.get(cv2.CAP_PROP_POS_FRAMES)
        self._video.set(cv2.CAP_PROP_POS_FRAMES, current_frame_nr + 1)
        self.get_new_image()
