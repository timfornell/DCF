import numpy as np
import Defs.GlobalVariables as glob
from Track.TrackClass import Track

class Tracker():
    def __init__(self):
        self._tracks = []

    def initialize_tracks(self, list_of_track_rois):
        """
        The ROIs from the GUI come as a list where each object contains (top_left_x, top_left_y),
        (bottom_right_x, bottom_right_y) and track id. This function is run each frame to catch any possible new
        tracks that have been drawn.
        """
        internal_track_ids = [track._track_id for track in self._tracks]
        incoming_track_ids = [track.id for track in list_of_track_rois]
        for track_roi in list_of_track_rois:
            if track_roi.id not in internal_track_ids:
                self._tracks.append(Track(track_roi.start_point, track_roi.end_point, track_roi.id))

        for i, track in enumerate(self._tracks):
            if track._track_id not in incoming_track_ids:
                del self._tracks[i]

    def run_translation_tracker(self, current_image):
        """
        This is the part of the DCF tracker where it looks for the object in the image using the filter that it has
        from the previous frame. To do this a search window is used that is centered around the last known position of
        the track and the last known ROI increased by X percent (this is a tunable parameter). The image is then
        preprocessed by applying a window (tunable). Then the filter is correlated with the resulting image. If there
        is a clear enough peak in the resulting correlation the track is moved to this position. After that a new
        cropped image is calculated, this image is used to update the filter so that it can be used to find the object
        in the next frame.

        The first frame a track exists is a bit special since the filter is trained. It is trained be perbutating the
        cropped image X (tunable) amount of times.
        """
        for track in self._tracks:
            # Get the image patch from original image
            track.crop_image_to_track_ROI(current_image)
            # Preprocess image patch to prepare for DCF tracker
            track.pre_process_cropped_image()

            if track._is_initialized:
                # Correlate image with filter
                track.calculate_correlation()
                # Find location of maximum correlation and if clear enough, move track ROI
                track.update_track_position()
                # Get the image patch from original image for the new location
                track.crop_image_to_track_ROI(current_image)
                # Preprocess image patch to prepare for DCF tracker
                track.pre_process_cropped_image()
                # Update the filter
                track.update_filter()
            else:
                # Train the filter using x amount of pertubations
                track.train_initial_filter()