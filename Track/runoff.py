import numpy as np


RUNOFF_WIDTH = 5.0  # metres beyond each track edge


def generate_runoff(left_edge: np.ndarray, right_edge: np.ndarray) -> tuple:
    n = len(left_edge)
    left_runoff  = np.zeros((n, 2))
    right_runoff = np.zeros((n, 2))

    for i in range(n):
        # Left runoff — offset further left from left edge
        prev = left_edge[(i - 1) % n]
        next = left_edge[(i + 1) % n]
        tangent = next - prev
        tangent = tangent / np.linalg.norm(tangent)
        normal = np.array([-tangent[1], tangent[0]])
        left_runoff[i] = left_edge[i] + RUNOFF_WIDTH * normal

        # Right runoff — offset further right from right edge
        prev = right_edge[(i - 1) % n]
        next = right_edge[(i + 1) % n]
        tangent = next - prev
        tangent = tangent / np.linalg.norm(tangent)
        normal = np.array([-tangent[1], tangent[0]])
        right_runoff[i] = right_edge[i] - RUNOFF_WIDTH * normal

    return left_runoff, right_runoff