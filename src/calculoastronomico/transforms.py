"""Rutinas de transformaciones."""
import math
from math import cos, sin, sqrt

import numpy as np

import calculoastronomico.constant as c


def rectangular_to_spherical(v):
    """
    Transforma coordenadas rectangulares a esféricas.

    Args:
        v: Vector [x, y, z]

    Returns:
        Vector [theta, phi, r]
        In most cases, [delta, alpha, 1]
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
           In most cases, [delta, alpha, 1]

    Returns:
        Vector [x, y, z]
    """
    theta, phi, r = v
    x = r * math.cos(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.cos(theta)
    z = r * math.sin(theta)
    return [x, y, z]


def translation(x, R):
    """
    Efectúa una traslación en el espacio

    Args:
        x: Vector original en O
        R: Posicion de O' respecto a O

    Returns:
        Vector respecto a O'
    """
    if isinstance(x, np.ndarray) and isinstance(R, np.ndarray):
        x1 = x - R
    else:
        x1 = [xi - ri for xi, ri in zip(x, R)]
    return x1


def rotation(n, theta, x):
    """
    Efectúa una rotación elemental pasiva alrededor de un eje cartesiano

    Args:
        n: Eje  cartesiano para la rotación
        theta: Ángulo de la rotación
        X: Vector original

    Returns:
        Vector en el sistema de referencia rotado
    """
    x1 = x.copy()
    if n == 1:
        x1[0] = x[0]
        x1[1] = x[1] * cos(theta) + x[2] * sin(theta)
        x1[2] = -x[1] * sin(theta) + x[2] * cos(theta)
    elif n == 2:
        x1[0] = x[0] * cos(theta) - x[2] * sin(theta)
        x1[1] = x[1]
        x1[2] = x[0] * sin(theta) + x[2] * cos(theta)
    elif n == 3:
        x1[0] = x[0] * cos(theta) + x[1] * sin(theta)
        x1[1] = -x[0] * sin(theta) + x[1] * cos(theta)
        x1[2] = x[2]
    else:
        raise ValueError(f"Cant perform a rotation around axis {n}!")

    return x1


def rotation_Euler(phi, xi, zeta, x):
    """
    Efectúa una rotación de Euler

    Args:
        phi: Primer ángulo de Euler
        xi: Segundo ángulo de Euler
        zeta: Tercer ángulo de Euler
        x: Coponentes del vector originales

    Returns:
        Componentes del vector en el sistema de referencia rotado
    """
    a = rotation(3, phi, x)
    b = rotation(1, xi, a)
    x1 = rotation(3, zeta, b)
    return x1


def terrestrial_coordinates(lon, lat, h, dimensionless=False, fulloutput=False):
    """
    Calcula las coordenadas de un observador en el ITRS.

    Args:
        lon: Longitud geodesica (radianes).
        lat: Latitud geodesica (radianes).
        h: Altura sobre el elipsoide WGS84 (m).
        dimensionless: Si es True, el output se da en unidades del radio ecuatorial de la Tierra.
        fulloutput: Opcional, solicitar los valores de C y S

    Returns:
        Coordenadas terrestres [X, Y, Z]
        Si fulloutput=True, devuelve [X,Y,Z,C,S]

    """

    C = (c.r_e / sqrt(1 - c.e_t**2 * sin(lat) ** 2) + h) * cos(lat)
    S = (c.r_e * (1 - c.e_t**2) / sqrt(1 - c.e_t**2 * sin(lat) ** 2) + h) * sin(lat)

    R = [C * cos(lon), C * sin(lon), S]

    if dimensionless:
        R = [i / c.r_e for i in R]
        C /= c.r_e
        S /= c.r_e
    if fulloutput:
        return R + [C, S]
    else:
        return R


if __name__ == "__main__":
    rec = [1, 0, -1]
    print("Rectangular coordinates: ", rec)
    sph = rectangular_to_spherical(rec)
    print("Spherical coordinates: ", sph)
    rec2 = spherical_to_rectangular(sph)
    print("Back to rectangular: ", rec2)
