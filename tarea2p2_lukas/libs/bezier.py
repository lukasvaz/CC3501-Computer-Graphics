import numpy as np


def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


def bezierMatrix(P0, P1, P2, P3):
    
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Bezier base matrix is a constant
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])
    
    return np.matmul(G, Mb)

# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve

# Función para generar la curva del recorrido del auto
def generateCurveT5(N):
    
    #Primera tramo
    R0 = np.array([[35, 0, 0]]).T
    R1 = np.array([[38, 0, 0]]).T
    R2 = np.array([[42, 0, 0]]).T
    R3 = np.array([[45, 0, 0]]).T
    
    M1 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve1 = evalCurve(M1, N)
    l1=0
    l2=2.5
    #Segundo tramo
    R0 = np.array([[45, 0, 0]]).T
    R1 = np.array([[45+l2,0,0-l1]]).T
    R2 = np.array([[50+l1,0,5-l2]]).T
    R3 = np.array([[50, 0, 5]]).T
    
    M2 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve2 = evalCurve(M2, N)

    #tercer tramo
    R0 = np.array([[50, 0, 5]]).T
    R1 = np.array([[50, 0, 10]]).T
    R2 = np.array([[50, 0, 15]]).T
    R3 = np.array([[50, 0, 20]]).T
    
    M3 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve3 = evalCurve(M3, N*2)

    #4to tramo
    R0 = np.array([[50, 0, 20]]).T
    R1 = np.array([[50-l1, 0, 20+l2]]).T
    R2 = np.array([[55-l2,0,25+l1]]).T
    R3 = np.array([[55, 0, 25]]).T
    
    M4 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve4 = evalCurve(M4, N)

    #5to tramo
    R0 = np.array([[55, 0, 25]]).T
    R1 = np.array([[68, 0, 25]]).T
    R2 = np.array([[81,0,25]]).T
    R3 = np.array([[95, 0, 25]]).T
    
    M5 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve5 = evalCurve(M5, N*2)
    #6to tramo
    R0 = np.array([[95, 0, 25]]).T
    R1 = np.array([[95+l2, 0, 25+l1]]).T
    R2 = np.array([[100+l1,0,20+l2]]).T
    R3 = np.array([[100, 0, 20]]).T
    
    M6 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve6 = evalCurve(M6, N)

    #7to tramo
    R0 = np.array([[100, 0, 20]]).T
    R1 = np.array([[100, 0, 15]]).T
    R2 = np.array([[100, 0, 10]]).T
    R3 = np.array([[100, 0, 5]]).T
    
    M7 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve7 = evalCurve(M7, N*2)
    #8vo tramo
    R0 = np.array([[100, 0, 5]]).T
    R1 = np.array([[100+l1, 0,5-l2]]).T
    R2 = np.array([[95+l2, 0, 0-l1]]).T
    R3 = np.array([[95, 0, 0]]).T
    
    M8 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve8 = evalCurve(M8, N)
    #9no tramo
    R0 = np.array([[95, 0, 0]]).T
    R1 = np.array([[82, 0,0]]).T
    R2 = np.array([[69, 0, 0]]).T
    R3 = np.array([[56, 0, 0]]).T
    
    M9 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve9 = evalCurve(M9, N*2)
    #10mo tramo
    R0 = np.array([[55, 0, 0]]).T
    R1 = np.array([[55-l2, 0,0-l1]]).T
    R2 = np.array([[50-l1, 0, 5-l2]]).T
    R3 = np.array([[50, 0, 5]]).T
    
    M10 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve10 = evalCurve(M10, N)

     #11vo tramo
    R0 = np.array([[50, 0, 20]]).T
    R1 = np.array([[50+l1,0,20+l2]]).T
    R2 = np.array([[45+l2, 0, 25+l1]]).T
    R3 = np.array([[45, 0, 25]]).T
    
    M11 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve11 = evalCurve(M11, N)
    #12to tramo
    R0 = np.array([[45, 0, 25]]).T
    R1 = np.array([[36.5,0,25]]).T
    R2 = np.array([[28, 0, 25]]).T
    R3 = np.array([[20, 0, 25]]).T
    
    M12 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve12 = evalCurve(M12, N)

    R0 = np.array([[20, 0, 25]]).T
    R1 = np.array([[13,0,25]]).T
    R2 = np.array([[13, 0, 20]]).T
    R3 = np.array([[30, 0, 5]]).T
     #13vo tramo
    M13 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve13 = evalCurve(M13, N*3)

     #14vo tramo
    R0 = np.array([[30, 0, 5]]).T
    R1 = np.array([[30+l2,0,l2]]).T
    R2 = np.array([[35-l2+0.3, 0, 0]]).T
    R3 = np.array([[35, 0, 0]]).T
    
    M14 = bezierMatrix(R0, R1, R2, R3)
    bezierCurve14 = evalCurve(M14, N)
    # Concatenamos las curvas
    C = np.concatenate((bezierCurve1,bezierCurve2,bezierCurve3, bezierCurve4,  bezierCurve5,bezierCurve6,bezierCurve7
    ,bezierCurve8,bezierCurve9,bezierCurve10,bezierCurve3,bezierCurve11,bezierCurve12,bezierCurve13,bezierCurve14), axis=0)
   
    return C
