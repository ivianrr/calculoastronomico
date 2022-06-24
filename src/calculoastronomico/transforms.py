"""Rutinas de transformaciones."""
import math
from math import cos, sin, sqrt

import numpy as np

import calculoastronomico.constant as c
from calculoastronomico.formats import degree_to_radian


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


def equatorial_to_ecliptic(x, eps=None):
    """
    Transforma de coordenadas ecuatoriales a eclípticas.

    Args:
        x: Vector en coordenadas ecuatoriales.
        eps[opt]: Oblicuidad de la eclíptica media o verdadera (radianes).

    Returns:
        Vector en coordenadas eclipticas.
    """
    if eps is None:
        eps = degree_to_radian(23.5)
    x1 = rotation(1, eps, x)
    return x1


def ecliptic_to_equatorial(x, eps=None):
    """
    Transforma de coordenadas eclípticas a ecuatoriales.

    Args:
        x: Vector en coordenadas eclipticas.
        eps[opt]: Oblicuidad de la eclíptica media o verdadera (radianes).

    Returns:
        Vector en coordenadas ecuatoriales.
    """
    if eps is None:
        eps = degree_to_radian(23.5)
    x1 = rotation(1, -eps, x)
    return x1


def equatorial_to_galactic(x):
    """
    Transforma de coordenadas ecuatoriales a galacticas.

    Args:
        x: Vector en coordenadas ecuatoriales.

    Returns:
        Vector en coordenadas galacticas.
    """
    phi, xi, zeta = c.galactic_angles
    x1 = rotation_Euler(phi, xi, zeta, x)
    return x1


def galactic_to_equatorial(x):
    """
    Transforma de coordenadas galacticas a ecuatoriales.

    Args:
        x: Vector en coordenadas galacticas.

    Returns:
        Vector en coordenadas ecuatoriales.
    """
    phi, xi, zeta = c.galactic_angles
    x1 = rotation_Euler(-zeta, -xi, -phi, x)
    return x1


#  Algoritmo tomado de 'Astronomie Pratique et Informatique',
#  C. Dumoulin y J.-P. Parisot.
#  Con reforma gregoriana
def julian_date(a,m,d,h):
    """
    Calcula la fecha juliana de una fecha gregoriana. Definimos
    fecha juliana como dia juliano -0.5 + fracción de día desde las 0h UT1 (o UTC, TT...).

    Args:
        a: Año.
        m: Mes.
        d: Día.
        h: Hora, en formato decimal.

    Returns:
        Fecha juliana.
    """
    if (m < 3):
        a = a - 1
        m = m + 12

    jd = int(365.25*a)
    jd = jd + int(30.6001*(m+1)) + d
    qq = a + m/100.0 + d/1e4
    if (qq > 1582.10145):
        ib = int(a/100.0)
        jd = jd + 2 - ib + int(ib/4.0)

    return jd + 1720994.5 + h/24

def split_julian_date(jd):
    """
    Divide una fecha juliana en día juliano más fracción.

    Args:
        jd: Fecha juliana.

    Returns:
        jd0: Fecha juliana a 0h UT1.
        h: Hora UT1.
    """
    jd0=int(jd+0.5)-0.5
    h=24*(jd-jd0)
    return [jd0, h]

# Algorithm tomado de 'Astronomie Pratique et Informatique',
# C. Dumoulin y J.-P. Parisot.
# Con reforma gregoriana
def gregorian_date(jd):
    """
    Dada una fecha juliana calcula la fecha gregoriana.

    Args:
        jd: Fecha juliana.

    Returns:
        a: Año.
        m: Mes.
        d: Día.
        h: Hora, en formato decimal.
    """
    aj1 = jd + 0.5
    iz = int(aj1)
    f = aj1 - iz
    if (iz < 2299161):
       aa = iz
    else:
       ial = int((iz - 1867216.25)/36524.25)
       aa = iz + ial - int(ial/4.0) + 1

    b = aa + 1524.0
    c = int((b - 122.1)/365.25)
    d1 = int(365.25*c)
    e = int((b - d1)/30.60001)
    dm = b - d1 - int(30.60001*e) + f

    if (e < 13.5):
        am=e-1
    else:
        am=e-13

    if (am > 2.5):
        an=c-4716
    else:
        an=c-4715

    d = int(dm)
    m = am
    a = an
    h= 24*(dm - int(dm))
    return [a, m, d, h]

def days_between_dates(a,m,d,a1,m1,d1):
    """
    Calcula los dias entre dos fechas gregorianas.

    Args:
        a,m,d: Primera fecha.
        a1,m1,d1: Segunda fecha.

    Returns:
        Dias de diferencia (entero).
    """
    jd=julian_date(a,m,d,0.0)
    jd1=julian_date(a1,m1,d1,0.0)
    f=round(jd1-jd)
    return f

def day_of_week(a,m,d):
    """
    Calcula el día de la semana.

    Args:
        a,m,d: Fecha gregoriana.

    Returns:
        Dia de la semana, como un entero del 1 al 7.
    """
    return round(julian_date(a,m,d,0)+0.5)%7+1

def week_day_name(d):
    """
    Devuelve el ldia del nombre de la semana.

    Args:
        d: Día de la semana.

    Returns:
        El nombre del día.
    """
    dl=["Lunes","Martes","Miercoles","Jueves","Viernes","Sábado","Domingo"]
    return dl[d-1]



if __name__ == "__main__":
    rec = [1, 0, -1]
    print("Rectangular coordinates: ", rec)
    sph = rectangular_to_spherical(rec)
    print("Spherical coordinates: ", sph)
    rec2 = spherical_to_rectangular(sph)
    print("Back to rectangular: ", rec2)
