import numpy as np
### determinamos las constantes a utilizar a lo largo del programa####

##ventana
width = 600 #ancho de la ventana
height = 600 # alto de la ventana

## posicion hitbox (rectangulo que encierra la figura)
######es necesario normalizar los valores  con  las medidas en px de la ventana utilizada ventana utilizada #####
###### tomar en cuenta que la proporcion se realiza desde el 0.0, por lo que si queremos  120 px de ancho, seria medir 60 px  hacia la derecha
###### partido en el ancho de la pantalla medido desde el 0.0 --> 60/(width/2)
#(esquina inferior izquierda)
x1_hitbox=-60/(width/2) 
y1_hitbox=-80/(height/2)
#(esquina sup derecha)
x2_hitbox=60/(width/2)
y2_hitbox=80/(height/2)

##################### colores###########
 ##colores correspondientes al hitbox

r_back,g_back,b_back=10/255,10/255,10/255 # colores normalizados 

#colores correspondientes al cuerpo de la figura (body)
tuNombre="Lukas"
l=len(tuNombre)
r_body=(ord(tuNombre[0%l]) * ord(tuNombre[1%l])%255)/255
g_body=(ord(tuNombre[2%l]) * ord(tuNombre[3%l])%255)/255
b_body=(ord(tuNombre[4%l]) * ord(tuNombre[5%l])%255)/255



###### A continuacion se situan los parametros asociados a cada vertice de la figura#######

##rectangulo cuerpo escala 1:1
pos_rec=[x1_hitbox+0.005,y1_hitbox*0.5] #inf/izq
ancho=2*(-pos_rec[0])

##ojos
radio_ojos=-x1_hitbox/4.5
par_pupilas=[radio_ojos*2/3,radio_ojos*3/4]#ancho,alto
posicion_ojos=[-x1_hitbox-0.05,-y1_hitbox/3]
delta_ojos=-x1_hitbox/1.4

## posicion casco
pos_casco=[0,-pos_rec[1]]
alt_casco=-y1_hitbox*0.5

#largo  de la falda 
alt_falda=y1_hitbox*0.5


## factores de escala a ocupar##
scale_rut=((19732655/20000000)**-3) ### como mi rut es menor a 20 millones lo inverti para agrandarlo, 
scale_factors=[1,scale_rut]## probar con otros valores para notar cambio de tamaño max(2)
print("escala rut:",scale_rut)
 
# la velocidad  determinada en frames/segundo####
fps=60 




