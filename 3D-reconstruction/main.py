import numpy as np

# vidljive tacke --------------------
x1 = np.array([958,38,1])
y1 = np.array([933,33,1])
x2 = np.array([1117,111,1])
y2 = np.array([1027,132,1])
x3 = np.array([874,285,1])
y3 = np.array([692,223,1])
x4 = np.array([707,218,1])
y4 = np.array([595,123,1])
x9 = np.array([292,569,1])
y9 = np.array([272,360,1])
x10 = np.array([770,569,1])
y10 = np.array([432,814,1])
x11 = np.array([770,1465,1])
y11 = np.array([414, 1284,1])
x12 = np.array([317,1057,1])
y12 = np.array([258,818,1])
x = [x1, x2 , x3, x4, x9, x10, x11, x12]
y = [y1, y2, y3, y4, y9, y10, y11, y12]
# -----------------------------------

def jed(a,b):
    return [a[0] * b[0], a[1] * b[0], a[2] * b[0],
            a[0] * b[1], a[1] * b[1], a[2] * b[1],
            a[0] * b[2], a[1] * b[2], a[2] * b[2]]


matrica = np.zeros(shape = (0,9), dtype = int)
for i in range(len(x)):
    matrica = np.append(matrica, [jed(x[i], y[i])], axis = 0)

print(matrica)

u, s, v  = np.linalg.svd(matrica, full_matrices = True)

print(v[-1,:])
FF = (v.T)[:,-1].reshape(3,3)
print("******")
print(FF)
print("******")
svd_FF = np.linalg.svd(FF, full_matrices = True)

e1 = svd_FF[2][-1]
print(e1)
e1 = (1 / e1[2]) * e1
print("e1 ",e1)

e2 = svd_FF[0][-1]
e2 = (1 / e2[2]) * e2

print("e2:  ",e2)

FF1 = np.dot(svd_FF[0], np.dot(np.dot(np.diag([1,1,0]), np.diag(svd_FF[1])), svd_FF[2]))

# preostale tacke koje se vide --------------------
x6 = np.array([1094, 536, 1])
y6 = np.array([980, 535, 1])

x7 = np.array([862, 729, 1])
y7 = np.array([652, 638, 1])

x8 = np.array([710, 648, 1])
y8 = np.array([567, 532, 1])

x14 = np.array([1487, 598, 1])
y14 = np.array([1303, 700, 1])

x15 = np.array([1462, 1079, 1])
y15 = np.array([1257, 1165, 1])

y13 = np.array([1077, 269, 1])
# -----------------------------------

# Rekonstrukcija skrivenih tacaka
# --------- Ovde su to tacke : x5, y5, x13, x16, y16 -----------

# x, y - niz u kome se nalaze 2 niza koji predstavljaju 2 ivice koje pripadaju dvema pravama
# koje se seku u beskonacno dalekoj tacki
# x_, y_ - tacke koje sa odgovarajucim beskonacno dalekim tackama formiraju prave koje se medjusobno seku u
#          skrivenoj tacki koju trazimo
def rekonstruisi_skrivenu_tacku(x, x_, y , y_):
    x_infinity = np.cross(np.cross(x[0][0], x[0][1]),
                        np.cross(x[1][0], x[1][1]))
    x_infinity = x_infinity * (1 / x_infinity[2])
    y_infinity = np.cross(np.cross(y[0][0], y[0][1]),
                        np.cross(y[1][0], y[1][1]))
    y_infinity = y_infinity * (1 / y_infinity[2])

    final_point = np.cross(np.cross(x_infinity, x_), np.cross(y_infinity, y_))
    return final_point * (1 / final_point[2])

# -----------------------------------
x5 = np.round(rekonstruisi_skrivenu_tacku([[x4,x8], [x6,x2]], x1, [[x1,x4],[x3,x2]], x8))
y5 = np.round(rekonstruisi_skrivenu_tacku([[y4,y8], [y6,y2]], y1, [[y1,y4],[y3,y2]], y8))
x13 = np.round(rekonstruisi_skrivenu_tacku([[x9, x10], [x11, x12]], x14, [[x11, x15], [x10, x14]], x9))
x16 = np.round(rekonstruisi_skrivenu_tacku([[x10, x14], [x11, x15]], x12, [[x9, x10], [x11, x12]], x15))
y16 = np.round(rekonstruisi_skrivenu_tacku([[y10, y14], [y11, y15]], y12, [[y9, y10], [y11, y12]], y15))

#print("TACKA X5:  ",np.round(x5))
#print("TACKA X16:  " , np.round(y16))
# -----------------------------------


# Triangulacija --------------------
T1 = np.eye(3)
T1 = np.transpose(np.vstack((T1, np.zeros(3))))

def matrica_vektorskog_mnozenja(p):
    return np.array([[0, -p[2], p[1]],
                     [p[2], 0, -p[0]],
                     [-p[1], p[0], 0]])

E2 = matrica_vektorskog_mnozenja(e2)
print(E2)

T2 = E2.dot(FF1)
T2 = np.hstack((T2, e2.reshape(3,1)))
print(T2)

def jne(x,y,T1,T2):
    return np.array([x[1] * T1[2] - x[2] * T1[1],
                     -x[0] * T1[2] + x[2] * T1[0],
                     y[1] * T2[2] - y[2] * T2[1],
                     -y[0] * T2[2] + y[2] * T2[0]])


rekonstruisane_koordinate = np.array([0,0,0])

s1 = np.array([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12, x13, x14, x15, x16])
s2 = np.array([y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12, y13, y14, y15, y16])

for i in range(len(s1)):
    t = jne(s1[i], s2[i], T1, T2)
    u, d, v = np.linalg.svd(t)

    xx = v[3]
    xx *= (1/ xx[3])
    xx = xx[:-1]

    rekonstruisane_koordinate = np.append(rekonstruisane_koordinate,xx, axis = 0)

print("********************")
print(rekonstruisane_koordinate)
print("********************")





