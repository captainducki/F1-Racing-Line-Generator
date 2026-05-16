import numpy as np


CORNER_THRESHOLD = 0.001  # 1/m — curvature above this is classified as a corner


def detect_corners(kappa: np.ndarray) -> np.ndarray:
    return kappa > CORNER_THRESHOLD


def get_corner_segments(kappa: np.ndarray):
    is_corner = detect_corners(kappa)
    segments = []
    n = len(is_corner)
    i = 0

    while i < n:
        if is_corner[i]:
            start = i
            while i < n and is_corner[i]:
                i += 1
            end = i - 1
            segments.append((start, end))
        else:
            i += 1

    return segments