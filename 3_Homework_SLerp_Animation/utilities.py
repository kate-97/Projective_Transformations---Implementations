import math

def norm(q):
    return math.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)

def isUnit(q):
    return norm(q) == 1.0

def scalarProduct(q1,q2):
    return q1[0] * q2[0] + q1[1] * q2[1] + q1[2] * q2[2] + q1[3] * q2[3]