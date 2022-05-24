"""Rutinas de transformaciones."""
import math
from typing import List

import numpy as np


def rectangular_to_spherical(v):
    """
    Transforma coordenadas rectangulares a esféricas.

    Args:
        v: Vector [x, y, z]

    Returns:
        Vector [theta, phi, r]
    """
    x, y, z = v
    theta = math.atan(z / math.sqrt(x**2 + y**2))
    phi = math.atan2(y, x)
    r = math.sqrt(x**2 + y**2 + z**2)
    return [theta, phi, r]


def spherical_to_rectangular(v):
    """
    Transforma coordenadas esféricas a rectangulares.

    Args:
        v: Vector [theta, phi, r]

    Returns:
        Vector [x, y, z]
    """
    theta, phi, r = v
    x = r * math.cos(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.cos(theta)
    z = r * math.sin(theta)
    return [x, y, z]


def translation(x, R):
    """efectúa una traslación"""
    if isinstance(x, np.ndarray) and isinstance(R, np.ndarray):
        x1 = x - R
    else:
        x1 = [xi - ri for xi, ri in zip(x, R)]
    return x1


def rotation(n, theta, x):
    """efectúa una rotación elemental alrededor de un eje cartesiano"""
    # mats=np.array(
    #     [[],[],[]],
    #     [[],[],[]],
    #     [[],[],[]]
    # )

    pass


def rotation_Euler():
    """efectúa una rotación de Euler"""
    pass


if __name__ == "__main__":
    rec = [1, 0, -1]
    print("Rectangular coordinates: ", rec)
    sph = rectangular_to_spherical(rec)
    print("Spherical coordinates: ", sph)
    rec2 = spherical_to_rectangular(sph)
    print("Back to rectangular: ", rec2)
