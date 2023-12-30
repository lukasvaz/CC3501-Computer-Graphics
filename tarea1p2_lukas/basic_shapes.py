import numpy as np
from OpenGL.GL import *
import constants

SIZE_IN_BYTES = constants.SIZE_IN_BYTES

class Shape:
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData

    
# funcion que crea un cubo centrado en el origen  se le entrea un color

def createCube(r,g,b):
    
    vertexData = np.array([
        # positions        # colors
        -0.5, -0.5,  0.5,  r, g, b,
         0.5, -0.5,  0.5,  r, g, b,
         0.5,  0.5,  0.5, r, g, b,
        -0.5,  0.5,  0.5,  r, g,b,
 
        -0.5, -0.5, -0.5, r, g, b,
         0.5, -0.5, -0.5,  r, g, b,
         0.5,  0.5, -0.5,  r, g, b,
        -0.5,  0.5, -0.5,  r, g, b,
    ], dtype=np.float32)

    indexData = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7
    ])

    return Shape(vertexData, indexData)


# funcion que crea una esfera  de cierto radio centrada en el origen , sus colores van alternando 
# en la medida que se barre cierto angulo(simula pelota de playa) 
def createSphere(radius,total,r,g,b):
    vertexData=[0,0,radius,r,g,b]# polo norte
    indexData=[]
    long_alpha=2*np.pi/total # delta angulo longitudinal 
    lat_alpha=np.pi/total # delta angulo latitudinal
    

    for lat in range(1,total): # creamos los vertices 
        # para esto se avanza  un delta longitudinalmente y se barre una vuelta completa latitudinalmente
        i=0
        for long in range(0,total):
            ang_long=long*long_alpha
            ang_lat=np.pi/2-lat*lat_alpha
            x=radius*np.cos(ang_lat)*np.cos(ang_long)
            y=radius*np.cos(ang_lat)*np.sin(ang_long)
            z=radius*np.sin(ang_lat)
            if i%2==0: # alternamos colores
                vertexData+=[x,y,z,r,g,b]
            else:
                vertexData+=[x,y,z,1,1,1]
            i+=1
    vertexData+=[0,0,-radius,r,g,b] # polo sur

    mat=np.zeros([total+1,total+1],dtype=int)# creamos una matriz para que sea mas facil unir los vertices 
    aux=np.arange(1,total*(total-1)+1,dtype=int)
    aux.resize(total-1,total)
    mat[1:-1,:-1]=aux
    mat[total]=total*(total-1)+1
    mat[::,total]=mat[::,0]
    indexData=[]
    
    for c in range(len(mat[0])-1): # se une polo norte a  latitud  inicial 
        indexData+=[mat[0,c],mat[1,c],mat[1,c+1]]

    for f in range(1,total-1): # se unen los vertices del medio 
        for c in range(total):
            indexData+=[mat[f,c],mat[f+1,c],mat[f+1,c+1],mat[f,c],mat[f,c+1],mat[f+1,c+1]]

    for c in range(len(mat[total])-1): # se une latitud final  con  polo sur 
        indexData+=[mat[total,c],mat[total-1,c],mat[total-1,c+1]]


    return Shape(np.array(vertexData),np.array(indexData))

