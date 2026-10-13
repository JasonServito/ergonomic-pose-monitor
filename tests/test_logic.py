import math

import pytest

from logic.posture_logic import (
    BACK_ANGLE_THRESHOLD,
    NECK_ANGLE_THRESHOLD,
    classify_posture,
)


def make_keypoints(neck_deg=0.0, back_deg=0.0):
    """Build keypoints whose neck/back segments lean by the given angles from vertical."""
    shoulder_mid = (450.0, 300.0)
    back_len, neck_len = 150.0, 60.0
    hip_mid = (
        shoulder_mid[0] - back_len * math.sin(math.radians(back_deg)),
        shoulder_mid[1] + back_len * math.cos(math.radians(back_deg)),
    )
    nose = (
        shoulder_mid[0] + neck_len * math.sin(math.radians(neck_deg)),
        shoulder_mid[1] - neck_len * math.cos(math.radians(neck_deg)),
    )
    return {
        "left_shoulder": (shoulder_mid[0] - 50, shoulder_mid[1]),
        "right_shoulder": (shoulder_mid[0] + 50, shoulder_mid[1]),
        "left_hip": (hip_mid[0] - 30, hip_mid[1]),
        "right_hip": (hip_mid[0] + 30, hip_mid[1]),
        "nose": nose,
    }


def test_upright_posture_is_good():
    result = classify_posture(make_keypoints())
    assert result == {"neck_angle": 0.0, "back_angle": 0.0, "is_good": True}


@pytest.mark.parametrize("neck_deg", [10.0, 35.0])
def test_neck_angle_is_measured(neck_deg):
    assert classify_posture(make_keypoints(neck_deg=neck_deg))["neck_angle"] == pytest.approx(neck_deg, abs=0.1)


@pytest.mark.parametrize("back_deg", [5.0, 25.0])
def test_back_angle_is_measured(back_deg):
    assert classify_posture(make_keypoints(back_deg=back_deg))["back_angle"] == pytest.approx(back_deg, abs=0.1)


def test_forward_head_is_bad():
    assert classify_posture(make_keypoints(neck_deg=NECK_ANGLE_THRESHOLD + 1))["is_good"] is False


def test_slouched_back_is_bad():
    assert classify_posture(make_keypoints(back_deg=BACK_ANGLE_THRESHOLD + 1))["is_good"] is False


def test_just_inside_both_thresholds_is_good():
    keypoints = make_keypoints(neck_deg=NECK_ANGLE_THRESHOLD - 1, back_deg=BACK_ANGLE_THRESHOLD - 1)
    assert classify_posture(keypoints)["is_good"] is True
