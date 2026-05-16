import numpy as np
from scipy.interpolate import splprep, splev
 
 
def fit_spline(centerline: np.ndarray):
    x = centerline[:, 0]
    y = centerline[:, 1]
 
    tck, u = splprep([x, y], s=0, per=True, k=3)
 
    return tck, u
 
 
def resample(tck, spacing_m: float) -> np.ndarray:
    u_dense = np.linspace(0, 1, 10000)
    x_dense, y_dense = splev(u_dense, tck)
 
    points = np.stack([x_dense, y_dense], axis=1)
    diffs = np.diff(points, axis=0)
    seg_lengths = np.linalg.norm(diffs, axis=1)
    arc_length = np.concatenate([[0.0], np.cumsum(seg_lengths)])
 
    total_length = arc_length[-1]
 
    distances = np.arange(0, total_length, spacing_m)
 
    u_uniform = np.interp(distances, arc_length, u_dense)
 
    x_resampled, y_resampled = splev(u_uniform, tck)
 
    return np.stack([x_resampled, y_resampled], axis=1)

 
def compute_edges(centerline: np.ndarray, track_width_m: float):
    half_width = track_width_m / 2.0
 
    n = len(centerline)
    left_edge = np.zeros((n, 2))
    right_edge = np.zeros((n, 2))
 
    for i in range(n):
        prev = centerline[(i - 1) % n]
        next = centerline[(i + 1) % n]
 
        tangent = next - prev
        tangent = tangent / np.linalg.norm(tangent)
 
        normal = np.array([-tangent[1], tangent[0]])
 
        left_edge[i] = centerline[i] + half_width * normal
        right_edge[i] = centerline[i] - half_width * normal
 
    return left_edge, right_edge
