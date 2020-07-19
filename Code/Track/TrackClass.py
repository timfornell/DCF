import numpy as np

class Track():
    def __init__(self, roi):
        self._is_initialized = False
        self._start_point = (0, 0)
        self._end_point = (0, 0)
        self._cropped_image = None
