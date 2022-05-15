import calculoastronomico.formats as cf
from calculoastronomico.constant import *

rad = cf.degree_to_radian(180)

print("degree_to_radian", rad)

print(cf.degree_to_ddmmss(-12.513))
print(cf.degree_to_ddmmss(9.9999999999999931))

print(cf.degree_to_ddmmss_compact(-12.513))

print(cf.ddmmss_to_degree(*cf.degree_to_ddmmss(-12.513)))


x = -12.513
print("degrees", x)
print("ddmmss", cf.degree_to_ddmmss(x))
print("ddmmsscompact", cf.degree_to_ddmmss_compact(x))
print("back to degrees", cf.ddmmss_compact_to_degree(cf.degree_to_ddmmss_compact(x)))

x = 40.16
print("accuracy check: ddmmss_c=", x)
print("deg:", cf.ddmmss_compact_to_degree(x))
print("back to compact:", cf.degree_to_ddmmss_compact(cf.ddmmss_compact_to_degree(x)))

print("back to degree one last time:", cf.ddmmss_compact_to_degree(
    cf.degree_to_ddmmss_compact(cf.ddmmss_compact_to_degree(x))))
print("back to compact one last time:", cf.degree_to_ddmmss_compact(
    cf.ddmmss_compact_to_degree(cf.degree_to_ddmmss_compact(cf.ddmmss_compact_to_degree(x)))))

print("scale 1", cf.scale_angle(3*PI/2))
print("scale 2", cf.scale_angle(-PI/2))
print("scale 3", cf.scale_angle(7*PI/2))
