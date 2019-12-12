import numpy as np
import math

def conversionFromEulersToMatrix(EulerAngles):
    cs_rolling = math.cos(EulerAngles[0])
    sn_rolling = math.sin(EulerAngles[0])

    cs_pitch = math.cos(EulerAngles[1])
    sn_pitch = math.sin(EulerAngles[1])

    cs_yaw = math.cos(EulerAngles[2])
    sn_yaw = math.sin(EulerAngles[2])

    RZ = np.array([[cs_yaw, -sn_yaw, 0],
                   [sn_yaw, cs_yaw, 0],
                   [0, 0, 1]])  # .reshape(3,3)

    RY = np.array([[cs_pitch, 0, sn_pitch],
                   [0, 1, 0],
                   [-sn_pitch, 0, cs_pitch]])  # .reshape(3,3)

    RX = np.array([[1, 0, 0],
                   [0, cs_rolling, -sn_rolling],
                   [0, sn_rolling, cs_rolling]])  # .reshape(3,3)

    return np.dot(np.dot(RZ, RY), RX)

def vector_product(v1,v2):
    return [ v1[1] * v2[2] - v1[2] * v2[1],
           -(v1[0] * v2[2] - v1[2] * v2[0]),
             v1[0] * v2[1] - v1[1] * v2[0]
           ]

def isZeroVector(v):
    if v[0] == 0 and v[1] == 0 and v[2] == 0:
        return True
    return False


def A2AngleAxis(transformation):
    E = np.eye(3)
    AE = transformation - E

    v1 = list(AE[0, :])
    v2 = list(AE[1, :])
    v3 = list(AE[2, :])

    p = vector_product(v1, v2)

    if isZeroVector(p):
        p = vector_product(v2, v3)

        if isZeroVector(p):
            p = vector_product(v1, v3)

    euc = math.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2)
    p = [(e / euc) for e in p]
    u = [-p[1], p[0], 0]
    euc = math.sqrt((u[0] ** 2 + u[1] ** 2 + u[2] ** 2))
    u = np.array([(e / euc) for e in u])
    u = u.reshape(3, 1)
    u_prim = np.dot(transformation, u)
    u_priml = list(u_prim)
    euc_uprim = math.sqrt((u_priml[0] ** 2 + u_priml[1] ** 2 + u_priml[2] ** 2))
    u_prim = np.array([e/euc_uprim for e in u_priml])

    u = u.reshape(1, 3)
    u = u[0]

    angle = np.arccos(np.dot(u, u_prim))

    a = np.array([u[0], u[1], u[2],
                  u_prim[0], u_prim[1], u_prim[2],
                  p[0], p[1], p[2]], dtype='float').reshape(3, 3)

    if np.linalg.det(a) < 0:
        p = [e * (-1) for e in p]

    return (p, angle)


def AngleAxis2Q(angle, vector):
    w = math.cos(angle / 2)
    p_intensity = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    p = np.array([vector[0], vector[1], vector[2]]) / p_intensity

    qijk = math.sin(angle / 2) * p

    return (qijk[0], qijk[1], qijk[2], w)


def Q2AngleAxis(q):
    i, j, k, w = q

    if w < 0:
        i *= -1
        j *= -1
        k *= -1
        w *= -1

    angle = 2 * np.arccos(w)

    if abs(w) == 1:
        p = (1, 0, 0)
    else:
        u = math.sqrt(i ** 2 + j ** 2 + k ** 2)
        p = (i / u, j / u, k / u)

    return (p, angle)


def Rodriguez(angle, vector):
    p1 = vector[0]
    p2 = vector[1]
    p3 = vector[2]

    q = math.sqrt(p1 ** 2 + p2 ** 2 + p3 ** 2)
    p1 /= q
    p2 /= q
    p3 /= q
    p = np.array([p1, p2, p3]).reshape(1, 3)
    pT = p.reshape(3, 1)

    E = np.eye(3)
    px = np.array([0, -p3, p2, p3, 0, -p1, -p2, p1, 0]).reshape(3, 3)

    A = math.sin(angle) * px
    A = A + E * math.cos(angle)
    A = A + (1 - math.cos(angle)) * pT.dot(p)

    return A

def conversionFromMatrixToEulers(transformation):
    if abs(transformation[2, 0]) != 1:
        # normal case
        yaw = math.atan2(transformation[1, 0], transformation[0, 0])
        pitch = np.arcsin(-transformation[2, 0])
        rolling = math.atan2(transformation[2, 1], transformation[2, 2])
    elif transformation[2, 0] == -1:
        # gimball lock
        yaw = math.atan2(-transformation[0, 1], transformation[1, 1])
        pitch = math.pi / 2
        rolling = 0
    elif transformation[2, 0] == 1:
        # gimball lock
        yaw = math.atan2(transformation[0, 1], -transformation[1, 1])
        pitch = -math.pi / 2
        rolling = 0

    return (rolling, pitch, yaw)