#!/usr/bin/env python3
"""
Manual eigenvalue calculation versus NumPy's `linalg.eig`.

The manual method follows the characteristic-polynomial approach shown in the
LucasBN reference repository:
https://github.com/LucasBN/Eigenvalues-and-Eigenvectors
"""

from __future__ import annotations

from time import perf_counter

import numpy as np

RESEARCH_SOURCES = {
    "numpy_docs": "https://numpy.org/doc/2.1/reference/generated/numpy.linalg.eig.html",
    "numpy_source": "https://github.com/numpy/numpy/blob/v2.1.3/numpy/linalg/_linalg.py",
    "lucasbn_repo": "https://github.com/LucasBN/Eigenvalues-and-Eigenvectors",
    "mlm_eigen_intro": "https://machinelearningmastery.com/introduction-to-eigendecomposition-eigenvalues-and-eigenvectors/",
    "sklearn_pca": "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html",
    "sklearn_clustering": "https://scikit-learn.org/stable/modules/clustering.html#spectral-clustering",
}

MATRIX_CASES = [
    (
        "3x3 reference matrix",
        np.array(
            [
                [6.0, 1.0, -1.0],
                [0.0, 7.0, 0.0],
                [3.0, -1.0, 2.0],
            ]
        ),
        300,
    ),
    (
        "4x4 matrix with complex conjugate pair",
        np.array(
            [
                [4.0, 2.0, 1.0, 0.0],
                [0.0, 3.0, -1.0, 1.0],
                [2.0, 0.0, 1.0, 2.0],
                [1.0, 1.0, 0.0, 2.0],
            ]
        ),
        150,
    ),
    (
        "5x5 dense matrix",
        np.array(
            [
                [5.0, 1.0, 0.0, -1.0, 2.0],
                [2.0, 4.0, 1.0, 0.0, 1.0],
                [0.0, 1.0, 3.0, 1.0, 0.0],
                [1.0, 0.0, 2.0, 2.0, -1.0],
                [2.0, 1.0, 0.0, 1.0, 4.0],
            ]
        ),
        30,
    ),
]


def list_multiply(a, b):
    """Multiply polynomial coefficient lists."""
    if not isinstance(a, list):
        a = [a]
    if not isinstance(b, list):
        b = [b]

    result = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            result[i + j] += ai * bj
    return result


def poly_add(a, b):
    """Add two polynomial coefficient lists."""
    size = max(len(a), len(b))
    a = a + [0] * (size - len(a))
    b = b + [0] * (size - len(b))
    return [x + y for x, y in zip(a, b)]


def det_poly(matrix):
    """
    Recursively build the characteristic polynomial via Laplace expansion.

    Each matrix element is stored as polynomial coefficients. For example,
    [6, -1] represents (6 - lambda).
    """

    size = len(matrix)
    if size == 1:
        return matrix[0][0]

    result = [0]
    for col in range(size):
        coefficient = matrix[0][col]
        submatrix = [
            [matrix[row][k] for k in range(size) if k != col]
            for row in range(1, size)
        ]
        sub_det = det_poly(submatrix)
        product = list_multiply(coefficient, sub_det)
        if col % 2 == 1:
            product = [-value for value in product]
        result = poly_add(result, product)
    return result


def manual_eigenvalues(matrix):
    """Return eigenvalues using the LucasBN-style characteristic polynomial."""
    size = len(matrix)
    characteristic_matrix = [
        [[matrix[i][j], -1 if i == j else 0] for j in range(size)]
        for i in range(size)
    ]
    polynomial = det_poly(characteristic_matrix)
    return np.roots(polynomial[::-1])


def sort_eigenvalues(values):
    """Sort real and complex eigenvalues for deterministic comparisons."""
    return np.array(
        sorted(
            values,
            key=lambda z: (
                round(float(np.real(z)), 12),
                round(float(np.imag(z)), 12),
            ),
        )
    )


def format_eigenvalues(values):
    """Pretty-print eigenvalues with stable precision."""
    formatted = []
    for value in values:
        real = float(np.real(value))
        imag = float(np.imag(value))
        if abs(imag) < 1e-10:
            formatted.append(f"{real:.6f}")
        else:
            formatted.append(f"{real:.6f}{imag:+.6f}j")
    return "[" + ", ".join(formatted) + "]"


def average_runtime(callback, repeats):
    """Return average runtime in milliseconds."""
    start = perf_counter()
    for _ in range(repeats):
        callback()
    total_seconds = perf_counter() - start
    return (total_seconds / repeats) * 1000.0


def compare_case(name, matrix, repeats):
    """Compare manual eigenvalues with `numpy.linalg.eig` on one matrix."""
    manual_values = sort_eigenvalues(manual_eigenvalues(matrix.tolist()))
    raw_numpy_values, numpy_vectors = np.linalg.eig(matrix)
    numpy_values = sort_eigenvalues(raw_numpy_values)

    residual_norms = [
        float(np.linalg.norm(matrix @ numpy_vectors[:, i] - raw_numpy_values[i] * numpy_vectors[:, i]))
        for i in range(matrix.shape[0])
    ]
    manual_avg_ms = average_runtime(
        lambda: manual_eigenvalues(matrix.tolist()),
        repeats=repeats,
    )
    numpy_avg_ms = average_runtime(
        lambda: np.linalg.eig(matrix),
        repeats=repeats,
    )
    return {
        "name": name,
        "shape": matrix.shape,
        "matrix": matrix,
        "manual_eigenvalues": manual_values,
        "numpy_eigenvalues": numpy_values,
        "max_abs_difference": float(np.max(np.abs(manual_values - numpy_values))),
        "manual_avg_ms": manual_avg_ms,
        "numpy_avg_ms": numpy_avg_ms,
        "slowdown_ratio": manual_avg_ms / numpy_avg_ms,
        "max_residual_norm": max(residual_norms),
    }


def run_analysis():
    """Run all matrix comparisons and return structured results."""
    return [compare_case(name, matrix, repeats) for name, matrix, repeats in MATRIX_CASES]


def print_report(results):
    """Print a console-friendly summary."""
    print("1.3 EigenVectorValues - manual versus NumPy comparison")
    print(f"NumPy documentation: {RESEARCH_SOURCES['numpy_docs']}")
    print(f"NumPy source: {RESEARCH_SOURCES['numpy_source']}")
    print(f"Manual reference: {RESEARCH_SOURCES['lucasbn_repo']}")
    print()

    for result in results:
        print("=" * 72)
        print(result["name"])
        print(f"Shape: {result['shape']}")
        print("Matrix:")
        print(result["matrix"])
        print(f"Manual eigenvalues: {format_eigenvalues(result['manual_eigenvalues'])}")
        print(f"NumPy eigenvalues:  {format_eigenvalues(result['numpy_eigenvalues'])}")
        print(f"Max abs difference: {result['max_abs_difference']:.3e}")
        print(f"Manual avg runtime: {result['manual_avg_ms']:.6f} ms")
        print(f"NumPy avg runtime:  {result['numpy_avg_ms']:.6f} ms")
        print(f"Manual / NumPy:     {result['slowdown_ratio']:.2f}x")
        print(f"Max eigenvector residual norm: {result['max_residual_norm']:.3e}")


if __name__ == "__main__":
    print_report(run_analysis())
