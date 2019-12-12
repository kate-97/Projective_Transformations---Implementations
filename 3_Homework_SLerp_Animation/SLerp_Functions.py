import math
import numpy as np

from Quaternions_Functions import *
from utilities import *

def slerp(q1,q2,tm,t):
    if t > tm:
        exit("Neispravno vreme")

    q1 = np.array(q1)
    q2 = np.array(q2)
    if not isUnit(q1):
        nq = norm(q1)
        q1 = q1 / nq
    if not isUnit(q2):
        nq = norm(q2)
        q2 = q2 / nq

    cos0 = scalarProduct(q1,q2)

    if cos0 > 0.95:
        return q1

    if cos0 < 0:
        q1 = (-1) * q1
        cos0 = -cos0

    fi0 = math.acos(cos0)

    return (math.sin(fi0 * (1 - t/tm)) / math.sin(fi0)) * q1 \
           + (math.sin(fi0 * (t/tm)) / math.sin(fi0)) * q2

def find_angles(e2b, e2e, t0, t):
    A = conversionFromEulersToMatrix (e2b)
    Aa = A2AngleAxis (A)

    q1 = AngleAxis2Q(vector = Aa[0], angle = Aa[1])

    A = conversionFromEulersToMatrix(e2e)
    Aa = A2AngleAxis(A)

    q2 = AngleAxis2Q(vector=Aa[0], angle=Aa[1])

    q = slerp(q1,q2,t,t0)

    Aa = Q2AngleAxis(q)
    A =  Rodriguez( vector = Aa[0], angle = Aa[1] )
    return conversionFromMatrixToEulers(A)