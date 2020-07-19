import pytest
from pathlib import Path
from SequenceReader.SequenceReaderClass import SequenceReaderClass

sequence_path = Path.joinpath(Path.cwd(), "Code/SequenceReader/file_example_MP4_640_3MG.mp4")
invalid_sequence_path = Path.joinpath(Path.cwd(), "Code/SequenceReader/invalid/file_example_MP4_640_3MG.mp4")
seq_reader = SequenceReaderClass(sequence_path)
seq_reader_invalid_path = SequenceReaderClass(invalid_sequence_path)

def test_initialise_with_invalid_sequence():
    assert seq_reader_invalid_path.sequence_is_available() == False

    for _ in range(0, 10):
        image_is_available, image = seq_reader_invalid_path.get_new_image()
        assert image is None
        assert image_is_available == False
        assert seq_reader_invalid_path.get_current_image() is None
        assert seq_reader_invalid_path.image_is_available() == False

def test_that_sequence_frames_are_read_correctly():
    assert seq_reader.sequence_is_available() == True

    for _ in range(0, 10):
        image_is_available, image = seq_reader.get_new_image()
        assert image is not None
        assert image_is_available == True
        assert seq_reader.get_current_image() is not None
        assert seq_reader.image_is_available() == True

def test_jump_backward():
    current_frame_number = seq_reader.get_current_frame_number()

    for _ in range(0, 5):
        seq_reader.jump_back_one_frame()
        new_frame_number = seq_reader.get_current_frame_number()
        assert new_frame_number == current_frame_number - 1
        current_frame_number = new_frame_number

def test_jump_forward():
    current_frame_number = seq_reader.get_current_frame_number()

    for _ in range(0, 5):
        seq_reader.jump_forward_one_frame()
        new_frame_number = seq_reader.get_current_frame_number()
        assert new_frame_number == current_frame_number + 1
        current_frame_number = new_frame_number
