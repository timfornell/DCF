import numpy as np

class Track():
    def __init__(self, start_point, end_point, id):
        self._is_initialized = False
        self._start_point = start_point
        self._end_point = end_point
        self._track_id = id
        self._cropped_image = None
