from matplotlib.colors import rgb2hex
import numpy as np
from OpenGL.GL import *

SIZE_IN_BYTES = 4

class Shape:
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData


def createRectangle(x1,y1,x2,y2,r,g,b):
##funcion que crea rectangulo,se necesita vertice inferior izquerdo(x1,y1) y superior derecho(x2,y2)
 #verifica que las coordenadas se entreguen correctamente
    if x1>0 or y1>0 or x2<0 or y2<0:
        raise Exception("invalid coordinates in rectangle")
    vertexData = np.array([
    #   positions        colors
        x1, y1, 0.0,  r, g, b,
         x2, y1, 0.0,  r, g, b,
         x2,  y2, 0.0,  r, g, b,
        x1, y2, 0.0,  r, g, b
        ], dtype = np.float32)
    indexData = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    return Shape(vertexData, indexData)



def createEllipse_alpha(x,y,N,alpha,Rx,Ry, r, g, b):
#dibuja elipse  barriendo cierto angulo alpha(sexagesimal)en sentido antihorario 
# a partir del eje x apuntando a la derecha (inspiracion en createEllipse aux3 )
#x,y indica vector de dezplazamiento izquerdo a partir del origen

    vertexData = [
        # posicion     # color
        x, y, 0.0, r, g, b
    ]

    indexData = []

    dtheta = (2 * np.pi*alpha) /(360*N)



    for i in range(N+1):
        theta = i * dtheta

        xv = x+Rx * np.cos(theta)
        yv = y+Ry * np.sin(theta)
        z = 0

        vertexData += [
            # pos    # color
            xv, yv, z, r, g, b
        ]

        indexData += [0, i, i+1]

    

    return Shape(vertexData, indexData)

def falda(x1,y1,len,h,num,r,g,b):
    ##funcion que crea triangulos equiespaciados en fila apuntando hacia abajoo arriba,
    ##a partir de un (x1,y1) correspondiente al punto sup izq, un len que determina el largo horizontal a
    # partir de x1 , un num que determina el numero de triangulos y un h que representa la altura de cada triangulo 
        vertexData = []
        indexData=[]
        for i in range(num):
            v1_x=x1+len*i/num
            v3_x=x1+len*(i+1)/num
            v2_x=(v1_x+v3_x)/2
            v1_y=v3_y=y1
            v2_y=y1+h

            vertexData +=[
             # positions    colors
                 v1_x, v1_y, 0.0, r, g, b,
                 v2_x, v2_y, 0.0,  r, g, b,
                     
                 ]
        vertexData+=[x1+len,y1,0.0,r,g,b]
        for i in range(0,num*2,2):
            indexData +=[i,i+1,i+2]
        return Shape(vertexData, indexData)
def rombo(x,y,ancho,alto,r,g,b) :
 # funcion que forma un rombo a prtir de su  posicion central(x,y),
 #  una altura(diferencia vertice sup-inf) y un ancho (diferencia vertice izq-der)
    vertexData=[x-ancho/2,y,  0,r,g,b,
                x, y-alto/2,  0,r,g,b,
                x+ancho/2,y,0,r,g,b,
                x,y+alto/2,0,r,g,b  ]
    indexData=[0,1,2,
              2,3,0]
    
    return Shape(vertexData, indexData)
