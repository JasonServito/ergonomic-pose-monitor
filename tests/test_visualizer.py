import numpy as np
import pytest

from ui.visualizer import draw_feedback


@pytest.mark.parametrize("is_good", [True, False])
def test_draw_feedback_renders_onto_frame(is_good):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    draw_feedback(frame, {"neck_angle": 25.0, "back_angle": 18.0, "is_good": is_good})
    assert frame.any(), "expected status text to be drawn on the frame"
