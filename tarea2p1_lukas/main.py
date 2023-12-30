# coding=utf-8
"""Textures and transformations in 3D"""

import glfw
from OpenGL.GL import *
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libs.setup import setView, setPlot
import libs.transformations as tr
import libs.basic_shapes as bs
import libs.easy_shaders as es
import libs.scene_graph as sg
import libs.performance_monitor as pm
from libs.assets_path import getAssetPath
import random


class Controller:
    def __init__(self):
        self.camera_state=0# estado de la camra (ortogonal  rera persona o primera persona)
        self.cameraThetaAngle =0 # angulo de la camra plano x-z
        self.deltaAngle=0#velocidad rotacion de la camara en eje x-z, se modificara en main() con deltatime()
        self.pos=np.array([0,0.6,0]) # posicion de la camra
        self.constant_vel=5
        self.vel=0 #velocidad de traslacion de la camra,se modificara en main() con deltatime()
        self.look_at=np.array([0.5,0.0,0.0])# a dd mira la camara
        self.direction=np.array([np.sin(self.cameraThetaAngle),0.0,np.cos(self.cameraThetaAngle)])#direccion de traslacion de la camara
        self.vision_range=5
        self.ball_rotation=0
    
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
            controller.ball_rotation+=np.pi/10
    #rotacion hacia la izq (relativo)
    if key == glfw.KEY_A and controller.camera_state!=1:
        controller.cameraThetaAngle+=controller.deltaAngle
        vec=np.array([np.sin(controller.cameraThetaAngle),0,np.cos(controller.cameraThetaAngle)])
        controller.direction=vec/np.linalg.norm(vec)
        controller.look_at=controller.pos+controller.vision_range*controller.direction
    
    #traslacion hacia atras si se esta dentro del mapa
    if key == glfw.KEY_S and controller.camera_state!=1:
        if controller.validate_position_s():
            controller.pos-=controller.vel*(controller.direction/np.linalg.norm(controller.direction))
        controller.look_at=controller.pos+controller.vision_range*controller.direction
        controller.ball_rotation+=-np.pi/10
    
    #rotacion hacia la derecha (relativo)
    if key == glfw.KEY_D and controller.camera_state!=1:
        controller.cameraThetaAngle-=controller.deltaAngle
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
        if controller.pos[1]>=0.5:
            controller.pos+=np.array([0.0,-controller.vel,0.0])
        controller.look_at=controller.pos+controller.vision_range*controller.direction
        
    # cambio a proyeccion otrogonal
    if key == glfw.KEY_SPACE:
        controller.camera_state=(controller.camera_state+1)%3
       
        
        
    
    #cierra ventana
    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

#detecta las teclas presionadas una vez dentro del loop
# internamente idem a on_key

def check_key_inputs(window):
    if  controller.camera_state==0 or  controller.camera_state==2:
        
    # Controles de la camara
        
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            if controller.validate_position(): 
                controller.pos+=controller.vel*(controller.direction/np.linalg.norm(controller.direction))
            
            controller.look_at=controller.pos+controller.vision_range*controller.direction
            controller.ball_rotation+=np.pi/10
        
        
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            controller.cameraThetaAngle+=controller.deltaAngle
            vec=np.array([np.sin(controller.cameraThetaAngle),0,np.cos(controller.cameraThetaAngle)])
            controller.direction=vec/np.linalg.norm(vec)
            controller.look_at=controller.pos+controller.vision_range*controller.direction
       
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:

            controller.cameraThetaAngle-=controller.deltaAngle
            vec=np.array([np.sin(controller.cameraThetaAngle),0,np.cos(controller.cameraThetaAngle)])
            controller.direction=vec/np.linalg.norm(vec)
            controller.look_at=controller.pos+controller.vision_range*controller.direction

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS :
            if controller.validate_position_s():
                controller.pos-=controller.vel*(controller.direction/np.linalg.norm(controller.direction))
            controller.look_at=controller.pos+controller.vision_range*controller.direction
            controller.ball_rotation-=np.pi/10
   
        if  glfw.get_key(window, glfw.KEY_UP) and controller.camera_state==0:

            if controller.pos[1]<30:
                controller.pos+=np.array([0.0,controller.vel,0.0])
            controller.look_at=controller.pos+controller.vision_range*controller.direction

        if glfw.get_key(window, glfw.KEY_DOWN) and controller.camera_state==0 :
            if controller.pos[1]>=0.5:
                controller.pos+=np.array([0.0,-controller.vel,0.0])
            controller.look_at=controller.pos+controller.vision_range*controller.direction
        
#creacion de grafo de escena:
#               scene
#      ground     neighbourhood    forest
#                   |casax30 |arboles 
#                   |floor1 floor2| hojasx5,trunc 
def createScene(pipeline): 
    #se crean los vertices de cada figura (a partir de basic shapes), espacio en la gpu para cada figura(initbuffers),
    # se llena con vertices e indices(fillbuffers),se sube la textura (simpesetup)
    
    
    
    #calle
    shapeStreet=bs.createTextureQuad(1,1)
    gpuStreet=es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuStreet)
    gpuStreet.fillBuffers(shapeStreet.vertices, shapeStreet.indices, GL_STATIC_DRAW)
    gpuStreet.texture = es.textureSimpleSetup(
    getAssetPath("street.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    

    #creamos cemento
    shapePavement=bs.createTextureQuad(1,1)
    gpuPavement=es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPavement)
    gpuPavement.fillBuffers(shapePavement.vertices, shapePavement.indices, GL_STATIC_DRAW)
    gpuPavement.texture = es.textureSimpleSetup(
    getAssetPath("pavement.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    #creamos pasto
    shapeGrass=bs.createTextureQuad(1,1)
    gpuGrass=es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGrass)
    gpuGrass.fillBuffers(shapeGrass.vertices, shapeGrass.indices, GL_STATIC_DRAW)
    gpuGrass.texture = es.textureSimpleSetup(
    getAssetPath("grass.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #tronco de arboles
    shapeTrunc = bs.createTextureCube()
    gpuTrunc = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTrunc)
    gpuTrunc.fillBuffers(shapeTrunc.vertices,
                             shapeTrunc.indices, GL_STATIC_DRAW)
    gpuTrunc.texture = es.textureSimpleSetup(
        getAssetPath("trunc.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    #hojas
    #verde
    shapeFoliage_1 = bs.createTextureCube()
    gpuFoliage_1 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFoliage_1)
    gpuFoliage_1.fillBuffers(shapeFoliage_1.vertices,
                             shapeFoliage_1.indices, GL_STATIC_DRAW)
    gpuFoliage_1.texture = es.textureSimpleSetup(
        getAssetPath("foliaje.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    #cafe
    shapeFoliage_2 = bs.createTextureCube()
    gpuFoliage_2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFoliage_2)
    gpuFoliage_2.fillBuffers(shapeFoliage_2.vertices,
                             shapeFoliage_2.indices, GL_STATIC_DRAW)
    gpuFoliage_2.texture = es.textureSimpleSetup(
        getAssetPath("foliaje_cafe.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    
    
    #muros 
    shapeWalls = bs.createTextureCube()
    gpuWalls = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls)
    gpuWalls.fillBuffers(shapeWalls.vertices,
                             shapeWalls.indices, GL_STATIC_DRAW)
    gpuWalls.texture = es.textureSimpleSetup(
        getAssetPath("wall2.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    #murosegundopiso
    shapeWalls_2 =  bs.createPrisma()
    gpuWalls_2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_2)
    gpuWalls_2.fillBuffers(shapeWalls_2.vertices,
                             shapeWalls_2.indices, GL_STATIC_DRAW)
    gpuWalls_2.texture = es.textureSimpleSetup(
        getAssetPath("wall2.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    
    #puerta
    shapeDoor = bs.createTextureCube()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(shapeDoor.vertices,
                             shapeDoor.indices, GL_STATIC_DRAW)
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath("door.jfif"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    
    #ventana
    shapeWindow = bs.createTextureCube()
    gpuWindow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(shapeWindow.vertices,
                             shapeWindow.indices, GL_STATIC_DRAW)
    gpuWindow.texture = es.textureSimpleSetup(
        getAssetPath("window.jfif"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    #techo
    shapeCeil = bs.createTextureCube()
    gpuCeil = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCeil)
    gpuCeil.fillBuffers(shapeCeil.vertices,
                             shapeCeil.indices, GL_STATIC_DRAW)
    gpuCeil.texture = es.textureSimpleSetup(
        getAssetPath("tejas.jfif"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    
   

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

    #######################
    # tercera rama:conjunto de casas de 2 pisos (prismo sobre cubo) dispuestas uniformemente
    #  pared,ventanax2,puerta|pared techox2 ventana x2-->,floor1,floor2-->casax27-->neighbouhood-->scene
    nbhood=sg.SceneGraphNode('neighbourhood')
    for y in range(2,5):#rango a pintar
        column=12-y
        for x in range(column,20):
            if x== 12 or (x,y) in(10,2):
                continue
            #nodo casa
            value=random.randint(0,1)
            house=sg.SceneGraphNode('house{x}{y}')
            if value:
                house.transform=tr.matmul([tr.translate(-22+6*x,0,-7.5+7*y),tr.scale(1.2,1,1.2)])
            else:
                house.transform=tr.matmul([tr.translate(-22+6*x,0,-7.5+7*y),tr.scale(1.2,1,1.2),tr.rotationY(np.pi)])


            nbhood.childs+=[house]
            #nodos pisos
            floor_1=sg.SceneGraphNode('floor_1')
            floor_2=sg.SceneGraphNode('floor_2')
            #nodo pared piso1
            wall=sg.SceneGraphNode('wall')
            wall.transform=tr.matmul([tr.translate(0,1,0),tr.scale(4,2,3.5)])
            wall.childs+=[gpuWalls] 
            floor_1.childs+=[wall]
            #nodo puerta
            door=sg.SceneGraphNode('door')
            door.transform=tr.matmul([tr.translate(0,0.5,1.75),tr.scale(0.5,1,0.2)])
            door.childs+=[gpuDoor] 
            floor_1.childs+=[door]
            #nodo ventanas primer piso
            for i in range(2):
                translation=[tr.translate(-1.1,1.5,1.72),tr.translate(+1.1,1.5,1.72)]
                window_1=sg.SceneGraphNode('window1{}'.format(i))
                window_1.transform=tr.matmul([translation[i],tr.scale(0.5,0.5,0.1)])
                window_1.childs+=[gpuWindow] 
                floor_1.childs+=[window_1]
            
            #paredes sgdo piso
    
            wall_2=sg.SceneGraphNode('wall_2')
            wall_2.transform=tr.scale(4,2.5,3.5)
            wall_2.childs+=[gpuWalls_2] 
            floor_2.childs+=[wall_2]
               #ventanas sgdo piso
            for i in range(2):
                translation=[tr.translate(-0.5,0.45,1.72),tr.translate(+0.5, 0.45 ,1.72)]
                window_2=sg.SceneGraphNode('window2{}'.format(i))
                window_2.transform=tr.matmul([translation[i],tr.scale(0.3,0.3,0.1)])
                window_2.childs+=[gpuWindow] 
                floor_2.childs+=[window_2]
            
            #techo
            for i in range(2):
                ceil=sg.SceneGraphNode('ceil{}'.format(i))
                if i==0:
                    ceil.transform=tr.matmul([tr.translate(-1.1,0.55,0),tr.rotationZ(-np.pi/2.9),tr.scale(0.2,2.6,3.5)])
                if i ==1:
                    ceil.transform=tr.matmul([tr.translate(1.1,0.55,0),tr.rotationZ(np.pi/2.9),tr.scale(0.2,2.6,3.5)])
                ceil.childs+=[gpuCeil] 
                floor_2.childs+=[ceil]
    
 
            #operaciones nodos internos
            floor_2.transform=tr.translate(0,2,0)
            house.childs+=[floor_1]
            house.childs+=[floor_2]

    
    scene.childs+=[nbhood]





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
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # color fondo de la ventana
    glClearColor(135/255, 206/256, 250/256, 1.0)

    # chehequeo de profundidad
    glEnable(GL_DEPTH_TEST)

    
    #creamos la escena
    dibujo = createScene(textureShaderProgram)
    

    
    setPlot(textureShaderProgram, colorShaderProgram, width, height)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    

    #creamos personaje de esfera, creamos su forma mediante la funcion de la tarea anterior
    shapeSphere=bs.createSphere(0.2,20,1,0,0)
    gpuSphere=es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuSphere)
    gpuSphere.fillBuffers(shapeSphere.vertices, shapeSphere.indices, GL_STATIC_DRAW)
    

    while not glfw.window_should_close(window):

        # Medicion de performance
        perfMonitor.update(glfw.get_time())
        controller.vel=5*perfMonitor.getDeltaTime() #aseguramos velocidad traslacional independiento del pc
        controller.deltaAngle=np.pi/2*perfMonitor.getDeltaTime() #aseguramos velocidad angular independiento del pc

        glfw.set_window_title(window, title + str(perfMonitor))

        # chequeo de inputs
        glfw.poll_events()

        check_key_inputs(window)

        # llenado de figuras
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    

        setView(textureShaderProgram, colorShaderProgram, controller)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Se entrega a open gl el shader a utilizar
        glUseProgram(textureShaderProgram.shaderProgram)
        sg.drawSceneGraphNode(dibujo, textureShaderProgram, "model")

        #shader para la esfera
        glUseProgram(colorShaderProgram.shaderProgram)

        #transformaciones de la esfera, se agrega rotacion para la animacion y traslacion segun la posicion de la camara 
        glUniformMatrix4fv(glGetUniformLocation(
        colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([tr.translate(controller.pos[0],0.2,controller.pos[2]),tr.rotationX(controller.ball_rotation),tr.rotationZ(controller.ball_rotation)]))
        colorShaderProgram.drawCall(gpuSphere)
        
        # intercambio de buffers 
        glfw.swap_buffers(window)

    # limpiamos la gpu

    dibujo.clear()
    gpuSphere.clear()
    #cerramos pantalla
    glfw.terminate()

    return 0


if __name__ == "__main__":
    main()
