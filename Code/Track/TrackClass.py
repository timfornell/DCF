import numpy as np

class Track():
    def __init__(self, roi):
        self._is_initialized = False
        self._roi = roi
        self._cropped_image = None
