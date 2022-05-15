"""Rutinas generales, formatos..."""

import math
from calculoastronomico.constant import *


def degree_to_radian(deg):
    """Convierte la cantidad de grados a radianes"""
    return deg/180*PI


def radian_to_degree(rad):
    """Convierte la cantidad de radianes a grados"""
    return rad/PI*180


def degree_to_ddmmss(degree):
    """Convierte grados a formato grados, minutos, segundos"""
    sig = math.copysign(1.0, degree)
    ad = abs(degree)
    d = math.floor(ad)
    dm = (ad-d)*60
    m = math.floor(dm)
    s = (dm-m)*60
    return [sig, d, m, s]


def degree_to_ddmmss_compact(degree):
    """Convierte grados a formato compacto dd.mmss"""
    # some problems here with accuracy
    # performing the operation on [1.0, 40, 15, 59.99999999997101] results in 40.156, which is equivalent to 40.16 if the 6 is carried over.
    sig, d, m, s = degree_to_ddmmss(degree)
    return sig*(d+m*1e-2+s*1e-4)


def ddmmss_to_degree(sig, d, m, s):
    """Formato grados, minutos, segundos a grados"""
    return sig*(d+(m+s/60)/60)


def ddmmss_compact_to_degree(x):
    """Convierte grados, minutos y segundos en formato compacto a grados"""
    sig = math.copysign(1.0, x)
    da = abs(x)
    d = math.floor(da)
    dm = (da-d)*100
    if dm > 90:
        dm -= 40
    m = math.floor(dm)
    s = (dm-m)*100
    if s > 90:
        s -= 40
    return sig*(d+(m+s/60.)/60.)


def scale_angle(a):
    """sitúa un ángulo en [0,2p)"""
    return a-2*PI*math.floor(a/(2*PI))
