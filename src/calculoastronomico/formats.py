"""Rutinas generales, formatos..."""

import math
from calculoastronomico.constant import *

def degree_to_radian(deg):
    """Convierte la cantidad de grados a radianes"""
    return deg/180*PI

def radian_to_degree(rad):
    """Convierte la cantidad de radianes a grados"""
    return rad/PI*180
    
# degree_to_ddmmss 
def degree_to_ddmmss(degree):
    """Convierte grados a formato grados, minutos, segundos"""
    sig=math.copysign(1.0, degree)
    ad=abs(degree)
    d=math.floor(ad)
    dm=(ad-d)*60
    m=math.floor(dm)
    s=(dm-m)*60
    return [sig,d,m,s]

# degree_to_ddmmss_compact 
def degree_to_ddmmss_compact(degree):
    """Convierte grados a formato compacto dd.mmss"""
    sig,d,m,s=degree_to_ddmmss(degree)
    return sig*(d+m*1e-2+s*1e-4)


# ddmmss_to_degree 
def ddmmss_to_degree(sig,d,m,s):
    """Formato grados, minutos, segundos a grados"""
    return sig*(d+(m+s/60)/60)


# ddmmss_compact_to_degree 
# scale_angle


