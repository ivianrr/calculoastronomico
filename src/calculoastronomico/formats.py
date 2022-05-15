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
    # print([sig,d,m,s])
    # print("prueba",sig*(d+(m+s/60)/60))
    return [sig,d,m,s]

# degree_to_ddmmss_compact 
# some problems here with accuracy
# performing the operation on [1.0, 40, 15, 59.99999999997101] results in 40.156, which is equivalent to 40.16 if the 6 is carried over.
def degree_to_ddmmss_compact(degree):
    """Convierte grados a formato compacto dd.mmss"""
    sig,d,m,s=degree_to_ddmmss(degree)
    return sig*(d+m*1e-2+s*1e-4)


# ddmmss_to_degree 
def ddmmss_to_degree(sig,d,m,s):
    """Formato grados, minutos, segundos a grados"""
    return sig*(d+(m+s/60)/60)


# ddmmss_compact_to_degree 
# TODO: check accuracy, floor. in degree_to_ddmmssit doesnt matter but in this case it does
def ddmmss_compact_to_degree(x):
    """Convierte grados, minutos y segundos en formato compacto a grados"""
    sig=math.copysign(1.0, x)
    da=abs(x)
    d=math.floor(da)
    dm=(da-d)*100
    if dm>90:   # it should be enough to check for this
        dm-=40
    m=math.floor(dm)
    s=(dm-m)*100
    if s>90:   # it should be enough to check for this
        s-=40
    print(sig,d,m,s)
    # print(sig*( d*3600+ m*60+ s)/3600)
    return sig*(d+(m+s/60.)/60.)

# scale_angle


