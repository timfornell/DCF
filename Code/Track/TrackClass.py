import numpy as np
import cv2
import Defs.GlobalVariables as glob

class Track():
    def __init__(self, start_point, end_point, id):
        self._is_initialized = False
        self._start_point = start_point
        self._end_point = end_point
        self._track_id = id
        self._cropped_image = None

    def crop_image_to_track_ROI(self, image):
        self._cropped_image = image[self._start_point[1]:self._end_point[1],
                                    self._start_point[0]:self._end_point[0]]

    def pre_process_cropped_image(self):
        self._cropped_image = cv2.cvtColor(self._cropped_image, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow("Cropped {} grayscale".format(self._track_id))
        cv2.imshow("Cropped {} grayscale".format(self._track_id), self._cropped_image)

        image_size = self._cropped_image.shape
        self._cropped_image = cv2.resize(self._cropped_image, glob.TRANLSATION_FILTER_SIZE,
                                         interpolation=cv2.INTER_LINEAR)
        cv2.namedWindow("Cropped {} resampled".format(self._track_id))
        cv2.imshow("Cropped {} resampled".format(self._track_id), self._cropped_image)

    def update_track_position(self):
        pass

    def update_filter(self):
        pass

    def train_initial_filter(self):
        pass