import argparse
from Tracker.TrackerClass import Tracker
from GUI.GuiClass import GUI
from SequenceReader.SequenceReaderClass import SequenceReaderClass

def run_dcf(sequence_path):
    gui = GUI()
    sequence_reader = SequenceReaderClass(sequence_path)
    tracker = Tracker()

    if sequence_reader.sequence_is_available():
        # tracker.initialize_tracks(gui.get_track_ROIs())

        while sequence_reader.image_is_available():
            event, values = gui.update_window()
            if event == "OK" or event == None:
                break
            # tracker.run_translation_tracker(sequence_reader.get_new_image())

        gui.close_window()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("sequence_path", help="Path to where sequence to run DCF on is located.")
    a = p.parse_args()

    run_dcf(a.sequence_path)