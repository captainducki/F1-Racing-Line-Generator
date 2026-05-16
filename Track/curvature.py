import numpy as np


def compute_curvature(path: np.ndarray) -> np.ndarray:
    n = len(path)
    kappa = np.zeros(n)

    for i in range(n):
        A = path[(i - 1) % n]
        B = path[i]
        C = path[(i + 1) % n]

        AB = np.linalg.norm(B - A)
        BC = np.linalg.norm(C - B)
        AC = np.linalg.norm(C - A)

        area = abs((B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1])) / 2.0

        denominator = AB * BC * AC
        if denominator < 1e-10:
            kappa[i] = 0.0
        else:
            kappa[i] = (2.0 * area) / denominator

    return kappa