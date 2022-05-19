"""Rutinas generales, formatos..."""

import math

from calculoastronomico.constant import *


def degree_to_radian(deg):
    """Convierte la cantidad de grados a radianes"""
    return deg / 180 * PI


def radian_to_degree(rad):
    """Convierte la cantidad de radianes a grados"""
    return rad / PI * 180


def degree_to_ddmmss(degree):
    """Convierte grados a formato grados, minutos, segundos"""
    sig = math.copysign(1.0, degree)
    ad = abs(degree)
    d = math.floor(ad)
    dm = (ad - d) * 60
    m = math.floor(dm)
    s = (dm - m) * 60
    return [sig, d, m, s]


def degree_to_ddmmss_compact(degree):
    """Convierte grados a formato compacto dd.mmss"""
    # some problems here with accuracy
    # performing the operation on [1.0, 40, 15, 59.99999999997101] results in 40.156, which is equivalent to 40.16 if the 6 is carried over.
    sig, d, m, s = degree_to_ddmmss(degree)
    return sig * (d + (m + s / 100) / 100)


def ddmmss_to_degree(sig, d, m, s):
    """Formato grados, minutos, segundos a grados"""
    return sig * (d + (m + s / 60) / 60)


def ddmmss_compact_to_degree(x):
    """Convierte grados, minutos y segundos en formato compacto a grados"""
    sig = math.copysign(1.0, x)
    da = abs(x)
    d = math.floor(da)
    dm = (da - d) * 100
    if dm > 90:
        dm -= 40
    m = math.floor(dm)
    s = (dm - m) * 100
    if s > 90:
        s -= 40
    return sig * (d + (m + s / 60.0) / 60.0)


def scale_angle(a):
    """Sitúa un ángulo en [0,2p)"""
    return a - 2 * PI * math.floor(a / (2 * PI))


#
# Rutinas opcionales
#


# -degree_to_ddmm: convierte grados a grados y minutos
# -degree_to_ddmm_compact: convierte grados a grados y minutos en formato compacto
# -ddmm_to_degree: convierte grados y minutos a grados
# -ddmm_compact_to_degree: misma que anterior pero en formato compacto

# hour_to_radian: convierte horas a radianes
def hour_to_radian(h):
    """convierte horas a radianes"""
    return h / 12 * PI


# radian_to_hour: convierte radianes a horas
def radian_to_hour(rad):
    """convierte radianes a horas"""
    return rad * 12 / PI


# degree_to_hour: convierte grados a horas
def degree_to_hour(deg):
    """convierte grados a horas"""
    return deg / 15


# hour_to_degree: convierte horas a grados
def hour_to_degree(h):
    """convierte horas a grados"""
    return h * 15


# hour_to_hhmmss: convierte horas a horas), minutos y segundos
def hour_to_hhmmss(h):
    """Convierte horas a horas, minutos y segundos"""
    return degree_to_ddmmss(h)


# -hour_to_hhmmss_compact: misma que anterior, pero en formato compacto

# hhmmss_to_hour: convierte horas, minutos y segundos a horas
def hhmmss_to_hour(sig, h, m, s):
    """Convierte horas, minutos y segundos a horas"""
    return ddmmss_to_degree(sig, h, m, s)


# Funciones adicionales
def hhmmss_to_ddmmss(sig, h, m, s):
    """Convierte horas,minutos y segundos a grados minutos y segundos"""
    hour = hhmmss_to_hour(sig, h, m, s)
    return degree_to_ddmmss(hour_to_degree(hour))


def ddmmss_to_hhmmss(sig, d, m, s):
    """Convierte horas,minutos y segundos a grados minutos y segundos"""
    deg = ddmmss_to_degree(sig, d, m, s)
    return hour_to_hhmmss(degree_to_hour(deg))


# -hhmmss_compact_to_hour: misma que anterior, pero en formato compacto
# -hour_to_hhmm: convierte horas a horas y minutos
# -hour_to_hhmm_compact: misma que anterior pero en formato compacto
# -hhmm_to_hour: convierte horas y minutos a horas
# -hhmm_compact_to_hour: misma que anterior pero en formato compacto


# scale_hour: sitúa una hora en formato decimal en el intervalo [0,24)
def scale_hour(h):
    """sitúa una hora en formato decimal en el intervalo [0,24)"""
    return h - 24 * math.floor(h / 24)


# scale_degree: sitúa un ángulo en grados en formato decimal en el intervalo [0,360)
def scale_degree(deg):
    """sitúa un ángulo en grados en formato decimal en el intervalo [0,360)"""
    return deg - 360 * math.floor(deg / 360)
