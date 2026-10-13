import numpy as np

from pose.pose_detector import get_keypoints


def test_blank_frame_has_no_pose():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    assert get_keypoints(frame) is None


def test_empty_frame_is_rejected():
    assert get_keypoints(None) is None
    assert get_keypoints(np.zeros((0, 0, 3), dtype=np.uint8)) is None
