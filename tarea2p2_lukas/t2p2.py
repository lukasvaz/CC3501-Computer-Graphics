# coding=utf-8
"""Textures and transformations in 3D"""

import glfw
from OpenGL.GL import *
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libs.setup import setView, setPlot, setLights
import libs.transformations as tr
import libs.basic_shapes as bs
import libs.easy_shaders as es
import libs.scene_graph as sg
import libs.performance_monitor as pm
import libs.lighting_shaders as ls
from libs.obj_reader import  readOBJ 
import libs.bezier as off
from libs.assets_path import getAssetPath
import libs.lamps_scene as lamps
import libs.neighbourhood_scene as nb

import random


class Controller:
    def __init__(self):
        self.camera_state=0# estado de la camra (ortogonal  rera persona o primera persona)
        self.cameraThetaAngle =0 # angulo de la camra plano x-z
        self.deltaAngle=0#velocidad rotacion de la camara en eje x-z, se modificara en main() con deltatime()
        self.pos=np.array([0,1.0,0]) # posicion de la camra
        self.constant_vel=5
        self.vel=0 #velocidad de traslacion de la camra,se modificara en main() con deltatime()
        self.look_at=np.array([0.5,0.0,0.0])# a dd mira la camara
        self.direction=np.array([np.sin(self.cameraThetaAngle),0.0,np.cos(self.cameraThetaAngle)])#direccion de traslacion de la camara
        self.vision_range=5
        
        
    
    #validate-position y validadte position_s determinan si es valido   mover la camara (la mantienen dentro del mapa)
    #para traslacion hacia adelante
    def validate_position(self):
        position=[]
        if self.pos[0]<-2.5 and self.direction[0]<0:
            position.append(0)
        if self.pos[0]>102.5 and self.direction[0]>0:
            position.append(0)
        if self.pos[2]<-2.5 and self.direction[2]<0:
            position.append(0)
        if self.pos[2]>27 and self.direction[2]>0:
            position.append(0)
        
        return all(position)
    #para traslacion hacia atras
    def validate_position_s(self):
        position=[]
        if self.pos[0]<-2.5 and self.direction[0]>0:
            position.append(0)
        if self.pos[0]>102.5 and self.direction[0]<0:
            position.append(0)
        if self.pos[2]<-2.5 and self.direction[2]>0:
            position.append(0)
        if self.pos[2]>27 and self.direction[2]<0:
            position.append(0)
        return all(position)
# global controller as communication with the callback function
controller = Controller()

#clase para determinar el estado del dia (dia/noche) en funcion del angulo
class Daystage():
    def __init__(self):
        self.light_rotation=0
        self.background_color_r=0
        self.background_color_g=0
        self.background_color_b=0
        self.diffuse=np.array([1.0, 1.0,0.0])
        self.cte_sun=0#cte de luz para el sol
        self.cte_moon=0 # cte de luz para la luna
        self.cte_posts=0
        self.radius=0 # radio de rotacion 
        self.hour=12 # hora inicial
        self.is_hour=True
        self.timer=0

    def update(self,delta,deltams,ball,car): # mueve la  luna y sol , ilumina las figuras si es de noche,imprime la hora
        self.light_rotation+=np.pi/30*delta
        self.timer+=deltams
       
        #noche
        if 90<np.degrees(self.light_rotation)%360<270:
            self.cte_sun=np.inf  
            self.cte_moon=0.002#se ilumina
            self.cte_posts=0.1#se ilumina
            ball.cte= ball.turn_off()#luces de la  bola se iluminan segun el input( apretar la G)
            car.cte=0.1#se ilumina
            self.background_color_r=25/256#fondo de noche
            self.background_color_g= 25/256
            self.background_color_b= 60/256
            self.radius=40
        #dia   
        else:
            self.radius=70+15*abs(np.sin(daystage.light_rotation))
            self.cte_sun=0.0002#se ilumina
            self.cte_moon=np.inf# se apaga
            self.cte_posts=np.inf# se apaga
            ball.cte=ball.mode[1]# se apaga
            car.cte=np.inf# se apaga
            self.background_color_r=135/256# fondo para el dia 
            self.background_color_g= 206/256
            self.background_color_b= 250/256
        
        actual=int(12+self.light_rotation//(np.pi/12))%24 # se imprime la hora
        if self.hour != actual:
            print("hora: {}:00  tiempo:{} seg ".format(actual,(self.timer/1000)%60))
            self.hour=actual
daystage=Daystage()


#clase para el personaje de la bola
class Ball:
    def __init__(self):
        self.ball_rotation=0 #rotacion para la animacion
        self.radius=0.4
        self.size=20#resolucion
        self.v_ini=5 #velocidad incial de salto
        self.velocity=5#velocidad actual
        self.gravity=9.8#gravedad para el salto
        self.pos=np.array([controller.pos[0],self.radius,controller.pos[2]])#posicion
        self.direction=controller.direction
        self.mode=[0.05,np.inf] #estado de la iluminacion(en día  se apaga en noche puede alternar)
        self.switch=0
        self.cte=self.mode[0]
    def update(self,delta):#se actualiza posicion y direcion de la bola
        
        self.pos=np.array([controller.pos[0],self.pos[1],controller.pos[2]])
        self.direction=controller.direction

    def animation(self,direction,colorShader):
        if direction:#transformaciones de la esfera, se agrega rotacion para la animacion y traslacion segun la posicion de la camara
            self.ball_rotation+=np.pi/15 
           
        else: #transformaciones de la esfera, se agrega rotacion para la animacion y traslacion segun la posicion de la camara 
            self.ball_rotation-=np.pi/15
            
    def bounce(self,delta): # permite saltar a la bola  al apretar enter

        if self.pos[1]<self.radius: # si esta en el suelo salta, delta: factor de tiempo en segundos 
            self.velocity=self.v_ini
        self.velocity-=self.gravity*delta
        self.pos[1]+=self.velocity*delta

    def on_air(self,delta): # si esta en aire  aplica gravedad
        if self.pos[1]>self.radius:
            self.velocity-=self.gravity*delta
            self.pos[1]+=self.velocity*delta
        elif self.pos[1]<self.radius: # si se queda clipeada al piso retorna a su posicion normal
            self.pos[1]=self.radius
           
    def turn_off(self):
         return ball.mode[ball.switch]
ball=Ball()

#clase para el auto
class Car:
    def __init__(self) :
        self.position=np.array([0,0,0]) #posicion 
        self.angle=0 #angulo de rotacion
        self.color_r=1
        self.color_g=0
        self.color_b=1
        self.length=6
        self.cte=0.1#cte para la iluminacion
    def update(self,step,C): #actualizamos posicion segun curva de bezier
       
        self.position=np.array([C[step,0],C[step,1],C[step,2]])
      
    def update_angle(self,step,C): #actualizamos angulo segun la tgte de la curva de bezier
        angle2=np.arctan2(C[step+1,0]-C[step,0], C[step+1,2]-C[step,2])
        if abs(abs(angle2)-abs(self.angle))>1: #evitamos discontinuidades
            angle2=self.angle
        self.angle=angle2
car=Car()

#detecta las teclas presionadas
def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    global controller

    # Movimiento de la camara
     # trasacion hacia adelante si se esta dentro del mapa
    if controller.camera_state!=1:
        if key == glfw.KEY_W: 
            if controller.validate_position():
                controller.pos+=controller.vel*(controller.direction/np.linalg.norm(controller.direction))
            controller.look_at=controller.pos+controller.vision_range*controller.direction
           
    #rotacion hacia la izq (relativo)
    if key == glfw.KEY_A and controller.camera_state!=1:
        controller.cameraThetaAngle-=controller.deltaAngle
        vec=np.array([np.sin(controller.cameraThetaAngle),0,np.cos(controller.cameraThetaAngle)])
        controller.direction=vec/np.linalg.norm(vec)
        controller.look_at=controller.pos+controller.vision_range*controller.direction
    
    #traslacion hacia atras si se esta dentro del mapa
    if key == glfw.KEY_S and controller.camera_state!=1:
        if controller.validate_position_s():
            controller.pos-=controller.vel*(controller.direction/np.linalg.norm(controller.direction))
        controller.look_at=controller.pos+controller.vision_range*controller.direction
    
    
    #rotacion hacia la derecha (relativo)
    if key == glfw.KEY_D and controller.camera_state!=1:
        controller.cameraThetaAngle+=controller.deltaAngle
        vec=np.array([np.sin(controller.cameraThetaAngle),0,np.cos(controller.cameraThetaAngle)])
        
        controller.direction=vec/np.linalg.norm(vec)
        controller.look_at=controller.pos+controller.vision_range*controller.direction
    #traslacion hacia arriba
    if key == glfw.KEY_UP and controller.camera_state==0:
        if controller.pos[1]<30:
            controller.pos+=np.array([0.0,controller.vel,0.0])
        controller.look_at=controller.pos+controller.vision_range*controller.direction
    #traslacion hacia abajo
    if key == glfw.KEY_DOWN and controller.camera_state==0:
        if controller.pos[1]>=2*ball.radius+0.2:
            controller.pos+=np.array([0.0,-controller.vel,0.0])
        controller.look_at=controller.pos+controller.vision_range*controller.direction
        
    # cambio a proyeccion otrogonal
    if key == glfw.KEY_SPACE:
        controller.camera_state=(controller.camera_state+1)%3

    # se prende y se apaga la luz de la bola (solo si es de noche)
    if key == glfw.KEY_G and controller.camera_state!=1:
        ball.switch=(ball.switch+1)%2
       
    #cierra ventana
    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

#detecta las teclas presionadas una vez dentro del loop
# internamente idem a on_key

def check_key_inputs(window,colorShader,delta):
    if  controller.camera_state==0 or  controller.camera_state==2:
        
    # Controles de la camara
        
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            if controller.validate_position(): 
                controller.pos+=controller.vel*(controller.direction/np.linalg.norm(controller.direction))
            
            controller.look_at=controller.pos+controller.vision_range*controller.direction
            ball.animation(True,colorShader)
            
        
        
        
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            controller.cameraThetaAngle-=controller.deltaAngle
            vec=np.array([np.sin(controller.cameraThetaAngle),0,np.cos(controller.cameraThetaAngle)])
            controller.direction=vec/np.linalg.norm(vec)
            controller.look_at=controller.pos+controller.vision_range*controller.direction
       
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:

            controller.cameraThetaAngle+=controller.deltaAngle
            vec=np.array([np.sin(controller.cameraThetaAngle),0,np.cos(controller.cameraThetaAngle)])
            controller.direction=vec/np.linalg.norm(vec)
            controller.look_at=controller.pos+controller.vision_range*controller.direction

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS :
            if controller.validate_position_s():
                controller.pos-=controller.vel*(controller.direction/np.linalg.norm(controller.direction))
            controller.look_at=controller.pos+controller.vision_range*controller.direction
            ball.animation(False,colorShader)
        if  glfw.get_key(window, glfw.KEY_UP) and controller.camera_state==0:

            if controller.pos[1]<30:
                controller.pos+=np.array([0.0,controller.vel,0.0])
            controller.look_at=controller.pos+controller.vision_range*controller.direction

        if glfw.get_key(window, glfw.KEY_DOWN) and controller.camera_state==0 :
            if controller.pos[1]>=2*ball.radius+0.2:
                controller.pos+=np.array([0.0,-controller.vel,0.0])
            controller.look_at=controller.pos+controller.vision_range*controller.direction

        #rebota la bola si  se presiona enter
        if glfw.get_key(window, glfw.KEY_ENTER)  and controller.camera_state==2:
            ball.bounce(delta)
        else:
            ball.on_air(delta)
        
            
        
#creacion  de escena piso y arboles
#               scene
#      ground         forest 
def createScene(pipeline): 
    #se crean los vertices de cada figura (a partir de basic shapes), espacio en la gpu para cada figura(initbuffers),
    # se llena con vertices e indices(fillbuffers),se sube la textura (simpesetup)
    


    #calle
    shapeStreet=bs.createTextureNormalQuad(1,1)
    gpuStreet=es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuStreet)
    gpuStreet.fillBuffers(shapeStreet.vertices, shapeStreet.indices, GL_STATIC_DRAW)
    gpuStreet.texture = es.textureSimpleSetup(
    getAssetPath("street.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    

    #creamos cemento
    shapePavement=bs.createTextureNormalQuad(1,1)
    gpuPavement=es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPavement)
    gpuPavement.fillBuffers(shapePavement.vertices, shapePavement.indices, GL_STATIC_DRAW)
    gpuPavement.texture = es.textureSimpleSetup(
    getAssetPath("pavement.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    #creamos pasto
    shapeGrass=bs.createTextureNormalQuad(1,1)
    gpuGrass=es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGrass)
    gpuGrass.fillBuffers(shapeGrass.vertices, shapeGrass.indices, GL_STATIC_DRAW)
    gpuGrass.texture = es.textureSimpleSetup(
    getAssetPath("grass.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #tronco de arboles
    shapeTrunc = bs.createTextureNormalsCube()
    gpuTrunc = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTrunc)
    gpuTrunc.fillBuffers(shapeTrunc.vertices,
                             shapeTrunc.indices, GL_STATIC_DRAW)
    gpuTrunc.texture = es.textureSimpleSetup(
        getAssetPath("trunc.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    #hojas
    #verde
    shapeFoliage_1 = bs.createTextureNormalsCube()
    gpuFoliage_1 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFoliage_1)
    gpuFoliage_1.fillBuffers(shapeFoliage_1.vertices,
                             shapeFoliage_1.indices, GL_STATIC_DRAW)
    gpuFoliage_1.texture = es.textureSimpleSetup(
        getAssetPath("foliaje.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    #cafe
    shapeFoliage_2 = bs.createTextureNormalsCube()
    gpuFoliage_2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFoliage_2)
    gpuFoliage_2.fillBuffers(shapeFoliage_2.vertices,
                             shapeFoliage_2.indices, GL_STATIC_DRAW)
    gpuFoliage_2.texture = es.textureSimpleSetup(
        getAssetPath("foliaje_cafe.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #Creamos nodos  de  escena
    #nodo raiz
    scene = sg.SceneGraphNode('system')
   
    #######primera rama
    ##############ground(cemento,pasto,calle)-->scene
    
    #ground
    ground=sg.SceneGraphNode('ground')
    i=7
    for y in range(0,6):  
        for x in range(0,21):
            if x in range(0,i) or (10<x<20 and 1<=y<=4):gpu=gpuGrass#pintamos como pasto
            elif x==i or y==0 or y==5 or x==20  or x==10:gpu=gpuStreet # pintamos como calle
            else:gpu=gpuPavement #pintamos como pavimento
            pavement= sg.SceneGraphNode('pavement({},{})'.format(x,y))
            pavement.transform=tr.matmul([tr.translate(5*x,0,5*+y),tr.scale(5,1,5)])
            pavement.childs+=[gpu]
            ground.childs+=[pavement]
        i-=1
    

    scene.childs+=[ground]
    
    #######segunda rama 
    ############bosque de arboles dispuestos semi-aleatorioamente 
    # (variacion delta-epsilon a partir de la cuadricula inicial:x+delta,y+epsilon) con delta:entre 0-5  epsilon:0-3
    
    # tronco,hojasx4-->arbol-->forest-->scene 
    forest=sg.SceneGraphNode('forest')
    for y in range(6):
        x=0
        deltax=0
        deltay=0
        while x< 30-5*y:
            if y==3 and x>4:
                x+=100
                continue
            #nodo arbol
            tree=sg.SceneGraphNode('tree{}{}'.format(x,y))
            tree.transform=tr.translate(x+deltax,0,5*y+deltay)
            #tronco
            trunc=sg.SceneGraphNode('trunc{}{}'.format(x,y))
            trunc.transform=tr.matmul([tr.translate(0,1.2,0),tr.scale(0.2,2.4,0.2)])
            trunc.childs=[gpuTrunc]
            tree.childs+=[trunc]
            #hojas  
            if random.randint(1,2)==1:
                gpu=gpuFoliage_1
            else:
                gpu=gpuFoliage_2
            for i in range(5):
                trans=[tr.translate(0,2.2,0),tr.translate(-0.8,1.5,0),tr.translate(0.8,1.5,0),tr.translate(0,1.5,0.8),tr.translate(0,1.5,-0.8)]
                if i==0:
                    scale=tr.scale(2,1.2,2)
                else:
                    scale=tr.scale(1.7,0.8,1.7)
                foliage=sg.SceneGraphNode('foliaje{}{}'.format(i,y))
                foliage.transform=tr.matmul([trans[i],scale])
                foliage.childs=[gpu]
                tree.childs+=[foliage]
            forest.childs+=[tree]
            deltax=random.randrange(1,5)
            deltay=random.randrange(1,3)
            x+=deltax

    scene.childs+=[forest]

   

    return scene


def main():

    # incializamos glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1000 #ancho
    height = 600 #alto
    title = "My city"

    window = glfw.create_window(width, height, title, None, None)#creamos ventana

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # detectamos teclas
    glfw.set_key_callback(window, on_key)

    # creamos shaders de textura y color
    textureShaderProgram = ls.MultipleLightTexturePhongShaderProgram()
    colorShaderProgram = ls.MultipleLightPhongShaderProgram()

    
    # chehequeo de profundidad
    glEnable(GL_DEPTH_TEST)

    
    #creamos la escena
    dibujo = createScene(textureShaderProgram)
    casas=nb.create_houses_scene(textureShaderProgram)
    postes=lamps.create_lamps_scene(colorShaderProgram)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    
    #creamos personaje de esfera, creamos su forma mediante la funcion de la tarea anterior
    shapeSphere=bs.createSphere(ball.radius,ball.size,1,0,0)
    gpuSphere=es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuSphere)
    gpuSphere.fillBuffers(shapeSphere.vertices, shapeSphere.indices, GL_STATIC_DRAW)

    #creamos shape auto
    shapeCar=readOBJ(getAssetPath("NormalCar1.obj"),np.array([1,0,1]))
    gpuCar=es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuCar)
    gpuCar.fillBuffers(shapeCar.vertices, shapeCar.indices, GL_STATIC_DRAW)

    

    #bezier
    N=50 
    step=0
    C=off.generateCurveT5(N)
    car.angle=np.arctan2(C[step+1,0]-C[step,0], C[step+1,2]-C[step,2])


    while not glfw.window_should_close(window):
        # color fondo de la ventana
        glClearColor(daystage.background_color_r, daystage.background_color_g, daystage.background_color_b, 1.0)
        # Medicion de performance
        perfMonitor.update(glfw.get_time())
        time=perfMonitor.getDeltaTime()
        controller.vel=5*time #aseguramos velocidad traslacional cte
        controller.deltaAngle=np.pi/2*time #aseguramos velocidad angular cte
        daystage.update(time,perfMonitor.getMS(),ball,car) # velocidad dia noche
    
        glfw.set_window_title(window, title)

        # chequeo de inputs
        glfw.poll_events()

        check_key_inputs(window,colorShaderProgram,time)

        # llenado de figuras
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # seteo de luces  proyeccion  y camara 
        setPlot(textureShaderProgram, colorShaderProgram, width, height,controller)
        setLights(daystage,ball,car,postes)
        setView(textureShaderProgram, colorShaderProgram, controller)
        

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Se entrega a open gl el shader a utilizar para las texturas
        glUseProgram(textureShaderProgram.shaderProgram)
        sg.drawSceneGraphNode(dibujo, textureShaderProgram, "model")
        sg.drawSceneGraphNode(casas, textureShaderProgram, "model")

        #  # Se entrega a open gl el shader a utilizar para la esfera y auto y postes
        glUseProgram(colorShaderProgram.shaderProgram)
        
        
        #animacion de la esfera
        ball.update(time)
        glUniformMatrix4fv(glGetUniformLocation(
            colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([tr.translate(ball.pos[0],ball.pos[1],ball.pos[2]),tr.rotationA(-ball.ball_rotation,np.cross(ball.direction,[0,1,0]))]))
        colorShaderProgram.drawCall(gpuSphere)
       
        #animacion para el auto
        car.update(step,C)
        glUniformMatrix4fv(glGetUniformLocation(
            colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([tr.translate(car.position[0],car.position[1],car.position[2]),tr.rotationY(car.angle)]))

        colorShaderProgram.drawCall(gpuCar)
        car.update_angle(step,C)
    
       ##postes
        sg.drawSceneGraphNode(postes,colorShaderProgram,"model")

        # intercambio de buffers 
        glfw.swap_buffers(window)
        step=(step+1)%(C.shape[0]-1)

    # limpiamos la gpu

    dibujo.clear()
    gpuSphere.clear()
    gpuCar.clear()
    postes.clear()
    casas.clear()
    #cerramos pantalla
    glfw.terminate()

    return 0


if __name__ == "__main__":
    main()
