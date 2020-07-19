import numpy as np

class Track():
    def __init__(self, start_point, end_point, id):
        self._is_initialized = False
        self._start_point = start_point
        self._end_point = end_point
        self._track_id = id
        self._cropped_image = None

    def crop_image_to_track_ROI(self, image):
        pass

    def pre_process_cropped_image(self):
        pass

    def update_track_position(self):
        pass

    def update_filter(self):
        pass

    def train_initial_filter(self):
        pass