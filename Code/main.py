import argparse
import cv2
from Tracker.TrackerClass import Tracker
from GUI.GuiClass import GUI
from SequenceReader.SequenceReaderClass import SequenceReaderClass

def run_dcf(sequence_path):
    gui = GUI()
    sequence_reader = SequenceReaderClass(sequence_path)
    tracker = Tracker()

    if sequence_reader.sequence_is_available():
        # tracker.initialize_tracks(gui.get_track_ROIs())
        paused_video = False
        image_available = sequence_reader.image_is_available()
        while image_available:
            image = sequence_reader.get_current_image()

            if not paused_video or image is None:
                image_available, image = sequence_reader.get_new_image()

            if image_available:
                gui.update_window(image)
                gui.update_rectangles()

                key = cv2.waitKey(10) & 0xFF

                if key == 27: # 27 is the escape key
                    break
                if key == 32: # 32 is the space key
                    if paused_video:
                        paused_video = False
                    else:
                        paused_video = True
                elif key == ord("p"):
                    key = cv2.waitKey(0)
                elif key == ord("z"):
                    sequence_reader.jump_back_one_frame()
                    gui.update_window(sequence_reader.get_current_image())
                elif key == ord("x"):
                    sequence_reader.jump_forward_one_frame()
                    gui.update_window(sequence_reader.get_current_image())
                elif key == ord("b"):
                    gui.clear_rectangles()

            # tracker.run_translation_tracker(sequence_reader.get_new_image())

        gui.close_window()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("sequence_path", help="Path to where sequence to run DCF on is located.")
    a = p.parse_args()

    run_dcf(a.sequence_path)