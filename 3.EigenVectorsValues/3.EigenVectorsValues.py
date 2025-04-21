#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eigen_manual_vs_numpy_timing.py

– Manuel özdeğer bulma ile NumPy karşılaştırması
– Süre ölçümü için time.time() kullanılır
"""

import numpy as np
import time

# --- Manuel özdeğer hesaplama fonksiyonları ---
def list_multiply(a, b):
    if not isinstance(a, list):
        a = [a]
    if not isinstance(b, list):
        b = [b]
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            res[i + j] += ai * bj
    return res

def poly_add(a, b):
    n = max(len(a), len(b))
    a = a + [0] * (n - len(a))
    b = b + [0] * (n - len(b))
    return [x + y for x, y in zip(a, b)]

def det_poly(mat):
    n = len(mat)
    if n == 1:
        return mat[0][0]
    result = [0]
    for j in range(n):
        coeff = mat[0][j]
        submat = [
            [mat[i][k] for k in range(n) if k != j]
            for i in range(1, n)
        ]
        sub_det = det_poly(submat)
        prod = list_multiply(coeff, sub_det)
        if j % 2 == 1:
            prod = [-c for c in prod]
        result = poly_add(result, prod)
    return result

def find_eigenvalues_manual(matrix):
    n = len(matrix)
    # Karakteristik matris: A - λI
    char_mat = [
        [[matrix[i][j], -1 if i == j else 0] for j in range(n)]
        for i in range(n)
    ]
    poly = det_poly(char_mat)
    return np.roots(poly[::-1])

# --- Ana program ---
if __name__ == "__main__":
    # Örnek kare matris
    A = [
        [6,  1, -1],
        [0,  7,  0],
        [3, -1,  2]
    ]
    A_np = np.array(A)

    # 1) Manuel yöntem zamanı
    t0 = time.time()
    manual_vals = find_eigenvalues_manual(A)
    t1 = time.time()
    manuel_zaman = t1 - t0

    # 2) NumPy yöntemi zamanı
    t0 = time.time()
    np_vals, np_vecs = np.linalg.eig(A_np)
    t1 = time.time()
    numpy_zaman = t1 - t0

    # Sonuçları yazdır
    print(f"Manual özdeğerler: {manual_vals}")
    print(f"Manual yöntem süresi: {manuel_zaman:.6f} saniye\n")

    print(f"NumPy özdeğerler:   {np_vals}")
    print(f"NumPy yöntem süresi: {numpy_zaman:.6f} saniye")
