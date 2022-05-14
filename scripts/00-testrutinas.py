import calculoastronomico.formats as cf
from calculoastronomico.constant import *

rad=cf.degree_to_radian(180)

print("degree_to_radian",rad)

print(cf.degree_to_ddmmss(-12.513))
print(cf.degree_to_ddmmss(9.9999999999999931))

print(cf.degree_to_ddmmss_compact(-12.513))

print(cf.ddmmss_to_degree(*cf.degree_to_ddmmss(-12.513)))