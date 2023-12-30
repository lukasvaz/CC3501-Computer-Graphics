import numpy as np

SCREEN_WIDTH = int(1600/1.5)
SCREEN_HEIGHT = int(900/1.5)
SCALE=0.1 # escala a ocupar en bolas
SIZE_IN_BYTES = 4
GRAVITY=9.8 
LARGO_CUBO=1 
V=LARGO_CUBO*0.4 # velocidad en bolas  en plano horizontal 
LOOK_AT=np.array([4,0.5,0]) # posicion de la camara
FOVY=35 # apertura de la camara 

C_r,C_g,C_b=250/256,200/256,100/256 # color del cubo
