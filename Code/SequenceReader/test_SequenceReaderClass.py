import pytest
from pathlib import Path
from SequenceReader.SequenceReaderClass import SequenceReaderClass

def test_that_sequence_frames_are_read_correctly():
    sequence_path = Path.joinpath(Path.cwd(), "Code/SequenceReader/file_example_MP4_640_3MG.mp4")
    seq_reader = SequenceReaderClass(sequence_path)

    assert seq_reader.sequence_is_available() == True

    for _ in range(0, 10):
        assert seq_reader.get_new_image() is not None
        assert seq_reader.get_current_image() is not None
        assert seq_reader.image_is_available() == True


test_that_sequence_frames_are_read_correctly()