from OpenGL.GL import *
import libs.scene_graph as sg
from libs.obj_reader import  readOBJ
import libs.easy_shaders as es
from libs.assets_path import getAssetPath
import numpy as np
import libs.basic_shapes as bs
import libs.transformations as tr
import libs.lighting_shaders as ls
import random


# creacion de escena de vecindario 

#funcion para crear nodo de una casa cubica sin techo
def create_cubic_house(gpuWalls,gpuDoor,gpuWindow,bool_door):
    
    #nodos pisos
    floor_1=sg.SceneGraphNode('floor_1')
    
    #nodo pared piso1
    wall=sg.SceneGraphNode('wall')
    wall.transform=tr.matmul([tr.translate(0,1,0),tr.scale(4,2,3.5)])
    wall.childs+=[gpuWalls] 
    floor_1.childs+=[wall]
    #nodo puerta
    if bool_door:
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
    return floor_1


#funcion para crear nodo de techo
def create_ceil_set(gpuWalls_2,gpuCeil,gpuWindow):      
   
    ceil_set=sg.SceneGraphNode('floor_2')
   
            #paredes sgdo piso
    
    wall_2=sg.SceneGraphNode('wall_2')
    wall_2.transform=tr.matmul([tr.translate(0,0.6,1.75),tr.scale(4.2,1.2,1),tr.rotationX(np.pi/2)])
    wall_2.childs+=[gpuWalls_2] 
    ceil_set.childs+=[wall_2]

    wall_3=sg.SceneGraphNode('wall_3')
    wall_3.transform=tr.matmul([tr.translate(0,0.6,-1.75),tr.scale(4.2,1.2,1),tr.rotationY(np.pi),tr.rotationX(np.pi/2)])
    wall_3.childs+=[gpuWalls_2] 
    ceil_set.childs+=[wall_3]
               #ventanas sgdo piso
    for i in range(2):
        translation=[tr.translate(-0.5,0.45,1.72),tr.translate(+0.5, 0.45 ,1.72)]
        window_2=sg.SceneGraphNode('window2{}'.format(i))
        window_2.transform=tr.matmul([translation[i],tr.scale(0.3,0.3,0.1)])
        window_2.childs+=[gpuWindow] 
        ceil_set.childs+=[window_2]
            
    #techo
    for i in range(2):
        ceil=sg.SceneGraphNode('ceil{}'.format(i))
        if i==0:
            ceil.transform=tr.matmul([tr.translate(-1.1,0.55,0),tr.rotationZ(-np.pi/2.9),tr.scale(0.2,2.6,3.7)])
        if i ==1:
            ceil.transform=tr.matmul([tr.translate(1.1,0.55,0),tr.rotationZ(np.pi/2.9),tr.scale(0.2,2.6,3.7)])
        ceil.childs+=[gpuCeil] 
        ceil_set.childs+=[ceil]
    return ceil_set
    
def create_houses_scene(pipeline):
    ##shapes a utiliazar
     #################   #muros ####################################
    shapeWalls = bs.createTextureNormalsCube()
    gpuWalls = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls)
    gpuWalls.fillBuffers(shapeWalls.vertices,
                             shapeWalls.indices, GL_STATIC_DRAW)
    gpuWalls.texture = es.textureSimpleSetup(
        getAssetPath("wall2.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
       #muromosaic
    shapeWalls_mosaic = bs.createTextureNormalsCube()
    gpuWalls_mosaic = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_mosaic)
    gpuWalls_mosaic.fillBuffers(shapeWalls_mosaic.vertices,
                             shapeWalls_mosaic.indices, GL_STATIC_DRAW)
    gpuWalls_mosaic.texture = es.textureSimpleSetup(
        getAssetPath("mosaic.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
          #muro beige
    shapeWalls_beige = bs.createTextureNormalsCube()
    gpuWalls_beige = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_beige)
    gpuWalls_beige.fillBuffers(shapeWalls_beige.vertices,
                             shapeWalls_beige.indices, GL_STATIC_DRAW)
    gpuWalls_beige.texture = es.textureSimpleSetup(
        getAssetPath("wall_beige.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
         #muro beige
    shapeWalls_red = bs.createTextureNormalsCube()
    gpuWalls_red = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_red)
    gpuWalls_red.fillBuffers(shapeWalls_red.vertices,
                             shapeWalls_red.indices, GL_STATIC_DRAW)
    gpuWalls_red.texture = es.textureSimpleSetup(
        getAssetPath("red.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
      #muro beige
    shapeWalls_blue = bs.createTextureNormalsCube()
    gpuWalls_blue = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_blue)
    gpuWalls_blue.fillBuffers(shapeWalls_blue.vertices,
                             shapeWalls_blue.indices, GL_STATIC_DRAW)
    gpuWalls_blue.texture = es.textureSimpleSetup(
        getAssetPath("blue.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    
    
    
    
    ################################murosegundopiso#################################################
    shapeWalls_2 =  bs.createTextureNormalTriangle()
    gpuWalls_2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_2)
    gpuWalls_2.fillBuffers(shapeWalls_2.vertices,
                             shapeWalls_2.indices, GL_STATIC_DRAW)
    gpuWalls_2.texture = es.textureSimpleSetup(
        getAssetPath("wall2.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
     #murosegundopiso
    shapeWalls_2_beige =  bs.createTextureNormalTriangle()
    gpuWalls_2_beige = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_2_beige)
    gpuWalls_2_beige.fillBuffers(shapeWalls_2_beige.vertices,
                             shapeWalls_2_beige.indices, GL_STATIC_DRAW)
    gpuWalls_2_beige.texture = es.textureSimpleSetup(
        getAssetPath("wall_beige.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    #murosegundopiso
    shapeWalls_2_mosaic =  bs.createTextureNormalTriangle()
    gpuWalls_2_mosaic = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_2_mosaic)
    gpuWalls_2_mosaic.fillBuffers(shapeWalls_2_mosaic.vertices,
                             shapeWalls_2_mosaic.indices, GL_STATIC_DRAW)
    gpuWalls_2_mosaic.texture = es.textureSimpleSetup(
        getAssetPath("mosaic.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
     #murosegunred
    shapeWalls_2_red =  bs.createTextureNormalTriangle()
    gpuWalls_2_red = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_2_red)
    gpuWalls_2_red.fillBuffers(shapeWalls_2_red.vertices,
                             shapeWalls_2_red.indices, GL_STATIC_DRAW)
    gpuWalls_2_red.texture = es.textureSimpleSetup(
        getAssetPath("red.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
      #murosegundopiso
    shapeWalls_2_blue =  bs.createTextureNormalTriangle()
    gpuWalls_2_blue = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_2_blue)
    gpuWalls_2_blue.fillBuffers(shapeWalls_2_blue.vertices,
                             shapeWalls_2_blue.indices, GL_STATIC_DRAW)
    gpuWalls_2_blue.texture = es.textureSimpleSetup(
        getAssetPath("blue.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
       #murosegundopiso
    shapeWalls_2 =  bs.createTextureNormalTriangle()
    gpuWalls_2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWalls_2)
    gpuWalls_2.fillBuffers(shapeWalls_2.vertices,
                             shapeWalls_2.indices, GL_STATIC_DRAW)
    gpuWalls_2.texture = es.textureSimpleSetup(
        getAssetPath("wall2.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) 


    ##################################puerta###############################
    shapeDoor = bs.createTextureNormalsCube()
    gpuDoor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuDoor)
    gpuDoor.fillBuffers(shapeDoor.vertices,
                             shapeDoor.indices, GL_STATIC_DRAW)
    gpuDoor.texture = es.textureSimpleSetup(
        getAssetPath("door.jfif"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    ########################## ventana######################################
    shapeWindow = bs.createTextureNormalsCube()
    gpuWindow = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWindow)
    gpuWindow.fillBuffers(shapeWindow.vertices,
                             shapeWindow.indices, GL_STATIC_DRAW)
    gpuWindow.texture = es.textureSimpleSetup(
        getAssetPath("window.jfif"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
   
     #####################################techo#################################
    shapeCeil = bs.createTextureNormalsCube()
    gpuCeil = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCeil)
    gpuCeil.fillBuffers(shapeCeil.vertices,
                             shapeCeil.indices, GL_STATIC_DRAW)
    gpuCeil.texture = es.textureSimpleSetup(
        getAssetPath("tejas.jfif"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    
     #techo
    shapeCeil_green = bs.createTextureNormalsCube()
    gpuCeil_green = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCeil_green)
    gpuCeil_green.fillBuffers(shapeCeil_green.vertices,
                             shapeCeil_green.indices, GL_STATIC_DRAW)
    gpuCeil_green.texture = es.textureSimpleSetup(
        getAssetPath("tejas_green.jfif"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
     #techo
    shapeCeil_black = bs.createTextureNormalsCube()
    gpuCeil_black = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCeil_black)
    gpuCeil_black.fillBuffers(shapeCeil_black.vertices,
                             shapeCeil_black.indices, GL_STATIC_DRAW)
    gpuCeil_black.texture = es.textureSimpleSetup(
        getAssetPath("tejas_black.jfif"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
      #techo
    shapeCeil_blue = bs.createTextureNormalsCube()
    gpuCeil_blue = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCeil_blue)
    gpuCeil_blue.fillBuffers(shapeCeil_blue.vertices,
                             shapeCeil_blue.indices, GL_STATIC_DRAW)
    gpuCeil_blue.texture = es.textureSimpleSetup(
        getAssetPath("blue.jpg"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

 
    
    nbhood=sg.SceneGraphNode('neighbourhood')
   
    
    #casa 1
    house1=sg.SceneGraphNode('house1')
    house1.transform=tr.matmul([tr.translate(20,0,20),tr.uniformScale(0.8)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    cube3=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube3.transform=tr.matmul([tr.translate(-1,0,0),tr.scale(0.5,2,1)])
    
    cube2=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(2,1.8,1),tr.uniformScale(0.8)])
    
    #operaciones nodos internos
    house1.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house1]

    #casa 2
    house2=sg.SceneGraphNode('house2')
    house2.transform=tr.matmul([tr.translate(25,0,19),tr.scale(1,0.6,1.3)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_mosaic,gpuDoor,gpuWindow,True)
    cube2=create_cubic_house(gpuWalls_mosaic,gpuDoor,gpuWindow,False)
    cube2.transform=tr.translate(0,2,0)
    cube3=create_ceil_set(gpuWalls_2_mosaic,gpuCeil_green,gpuWindow)
    cube3.transform=tr.translate(0,4,0)
    
    #operaciones nodos internos
    house2.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house2]
     #casa 3
    house3=sg.SceneGraphNode('house3')
    house3.transform=tr.matmul([tr.translate(30,0,18.5),tr.scale(1.1,0.6,1.5)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    cube2=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1)])
    cube3=create_ceil_set(gpuWalls_2_beige,gpuCeil_green,gpuWindow)
    cube3.transform=tr.matmul([tr.translate(0,2,0),tr.scale(1,1,1.05),tr.rotationY(np.pi/2)])
    cube4=create_ceil_set(gpuWalls_2_beige,gpuCeil_green,gpuWindow)
    cube4.transform=tr.matmul([tr.translate(0,4,0),tr.scale(0.6,1,1),tr.rotationY(np.pi/2)])
    #operaciones nodos internos
    house3.childs+=[cube1,cube2,cube3,cube4]
    nbhood.childs+=[house3]  

    #casa 4   
    house4=sg.SceneGraphNode('house4')
    house4.transform=tr.matmul([tr.translate(35,0,18.5),tr.scale(0.8,0.6,1.6)])
   
    #nodos pisos
    floor_1=create_cubic_house(gpuWalls_red,gpuDoor,gpuWindow,True)
    ceil_set=create_ceil_set(gpuWalls_2_red,gpuCeil,gpuWindow)
   
    #operaciones nodos internos
    ceil_set.transform=tr.translate(0,2,0)
    house4.childs+=[floor_1]
    house4.childs+=[ceil_set]
    nbhood.childs+=[house4]    

    #casa 5  
    house5=sg.SceneGraphNode('house5')
    house5.transform=tr.matmul([tr.translate(41.5,0,17.5),tr.scale(1.8,1.5,2)])
   
    #nodos pisos
    floor_1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    floor_2=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    floor_2.transform=tr.translate(0,2,0)

    house5.childs+=[floor_1,floor_2]
    
    nbhood.childs+=[house5]    
    
    #casa 6  
    house6=sg.SceneGraphNode('house6')
    house6.transform=tr.matmul([tr.translate(27,0,13),tr.scale(1,1.3,0.5),tr.rotationY(np.pi/2.6+np.pi)])
    #nodos pisos
    cube61=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    cube62=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    cube62.transform=tr.translate(4,0,0)
    ceil6_set=create_ceil_set(gpuWalls_2,gpuCeil_black,gpuWindow)
    ceil6_set.transform=tr.translate(0,2,0)
    ceil6_set2=create_ceil_set(gpuWalls_2,gpuCeil_black,gpuWindow)
    ceil6_set2.transform=tr.translate(4,2,0)

    house6.childs+=[cube61,cube62,ceil6_set,ceil6_set2]
    
    nbhood.childs+=[house6]    
      #casa 7  
    house7=sg.SceneGraphNode('house6')
    house7.transform=tr.matmul([tr.translate(37,0,9),tr.scale(1.3,1,1.6),tr.rotationY(np.pi)])
    #nodos pisos
    cube71=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    
    cube72=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube71.transform=tr.matmul([tr.translate(4,0,0.35),tr.scale(0.7,1,1)])
    cube72.transform=tr.matmul([tr.translate(0.6,0,0),tr.scale(1,1,1.3)])
    ceil7_set=create_ceil_set(gpuWalls_2_beige,gpuCeil_green,gpuWindow)
   
    ceil7_set2=create_ceil_set(gpuWalls_2_beige,gpuCeil_green,gpuWindow)
    ceil7_set2.transform=tr.matmul([tr.translate(0.6,2,0),tr.scale(1,1,1.3)])
    ceil7_set.transform=tr.matmul([tr.translate(4,2,0.35),tr.scale(0.7,1,1)])

    house7.childs+=[cube71,cube72,ceil7_set,ceil7_set2]
    
    nbhood.childs+=[house7]  

    #casa8
    #casa 2
    house8=sg.SceneGraphNode('house8')
    house8.transform=tr.matmul([tr.translate(43,0,7),tr.rotationY(np.pi),tr.scale(1.6,0.8,2)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_blue,gpuDoor,gpuWindow,True)
    cube2=create_cubic_house(gpuWalls_blue,gpuDoor,gpuWindow,False)
    cube2.transform=tr.translate(0,2,0)
    cube3=create_ceil_set(gpuWalls_2_blue,gpuCeil_black,gpuWindow)
    cube3.transform=tr.translate(0,4,0)
    
    #operaciones nodos internos
    house8.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house8]  

      
    #casa 9  
    house9=sg.SceneGraphNode('house9')
    house9.transform=tr.matmul([tr.translate(60,0,6),tr.rotationY(np.pi)])
   
    #nodos pisos
    module1=sg.SceneGraphNode('module1')
    floor_1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    ceil_set=create_ceil_set(gpuWalls_2,gpuCeil_black,gpuWindow)
    ceil_set.transform=tr.matmul([tr.translate(0,2,0)])
    module1.childs+=[floor_1,ceil_set]
    module1.transform=tr.matmul([tr.translate(4,0,-1),tr.scale(1.5,1,1)])
   
    module2=sg.SceneGraphNode('module2')
    floor_1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    ceil_set=create_ceil_set(gpuWalls_2,gpuCeil_black,gpuWindow)
    ceil_set.transform=tr.translate(0,2,0)   
    module2.childs+=[floor_1,ceil_set]
    module2.transform=tr.matmul([tr.translate(3,2,-1),tr.scale(1.2,1,1),tr.uniformScale(0.8)])

    module3=sg.SceneGraphNode('module3')
    floor_1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    ceil_set=create_ceil_set(gpuWalls_2,gpuCeil_black,gpuWindow)
    ceil_set.transform=tr.translate(0,2,0)
    module3.childs+=[floor_1,ceil_set]
    module3.transform=tr.scale(1,1,1.5)
   
    module4=sg.SceneGraphNode('module4')
    floor_1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    ceil_set=create_ceil_set(gpuWalls_2,gpuCeil_black,gpuWindow)
    ceil_set.transform=tr.translate(0,2,0)
    module4.childs+=[floor_1,ceil_set]
    module4.transform=tr.matmul([tr.translate(0,2,0),tr.uniformScale(0.8)])
   
   
    #operaciones nodos internos
   
    
    house9.childs+=[module1,module2,module3,module4]
    
    nbhood.childs+=[house9]

     #casa10
    house10=sg.SceneGraphNode('house8')
    house10.transform=tr.matmul([tr.translate(57,0,13),tr.rotationY(-np.pi/2),tr.scale(1.4,0.8,1.8)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    cube2=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube2.transform=tr.translate(0,2,0)
    cube3=create_ceil_set(gpuWalls_2_beige,gpuCeil_black,gpuWindow)
    cube3.transform=tr.translate(0,4,0)
    
    #operaciones nodos internos
    house10.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house10]  

    #casa 11 
    house11=sg.SceneGraphNode('house9')
    house11.transform=tr.matmul([tr.translate(75,0,6),tr.rotationY(np.pi)])
   
    #nodos pisos
    module1=sg.SceneGraphNode('module1')
    floor_1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    ceil_set=create_ceil_set(gpuWalls_2_beige,gpuCeil_black,gpuWindow)
    ceil_set.transform=tr.matmul([tr.translate(0,2,0)])
    module1.childs+=[floor_1,ceil_set]
    module1.transform=tr.matmul([tr.translate(4,0,-1),tr.scale(1.5,1,1)])
   
    module2=sg.SceneGraphNode('module2')
    floor_1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    ceil_set=create_ceil_set(gpuWalls_2_beige,gpuCeil_black,gpuWindow)
    ceil_set.transform=tr.translate(0,2,0)   
    module2.childs+=[floor_1,ceil_set]
    module2.transform=tr.matmul([tr.translate(4,2,-1),tr.scale(1.5,1,1),tr.uniformScale(0.8)])

    module3=sg.SceneGraphNode('module3')
    floor_1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    ceil_set=create_ceil_set(gpuWalls_2_beige,gpuCeil_black,gpuWindow)
    ceil_set.transform=tr.translate(0,2,0)
    module3.childs+=[floor_1,ceil_set]
    module3.transform=tr.scale(1,1,1.5)
   
    module4=sg.SceneGraphNode('module4')
    floor_1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    ceil_set=create_ceil_set(gpuWalls_2_beige,gpuCeil_black,gpuWindow)
    ceil_set.transform=tr.translate(0,2,0)
    module4.childs+=[floor_1,ceil_set]
    module4.transform=tr.matmul([tr.translate(0,2,0),tr.uniformScale(0.8)])
   
   
    #operaciones nodos internos
   
    
    house11.childs+=[module1,module2,module3,module4]
    
    nbhood.childs+=[house11]

   #casa12
    house12=sg.SceneGraphNode('house8')
    house12.transform=tr.matmul([tr.translate(82,0,6),tr.rotationY(np.pi),tr.scale(1.4,0.8,1.4)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    cube2=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    cube2.transform=tr.translate(0,2,0)
    cube3=create_ceil_set(gpuWalls_2,gpuCeil_blue,gpuWindow)
    cube3.transform=tr.translate(0,4,0)
    
    #operaciones nodos internos
    house12.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house12] 

    #casa13
    house13=sg.SceneGraphNode('house8')
    house13.transform=tr.matmul([tr.translate(90,0,6),tr.rotationY(np.pi),tr.scale(1.2,0.8,1.4)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    cube2=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    cube2.transform=tr.translate(0,2,0)
    cube3=create_ceil_set(gpuWalls_2,gpuCeil_green,gpuWindow)
    cube3.transform=tr.translate(0,4,0)
    
    #operaciones nodos internos
    house13.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house13] 
    #casa14
    house14=sg.SceneGraphNode('house14')
    house14.transform=tr.matmul([tr.translate(92,0,16),tr.rotationY(np.pi/2),tr.scale(1.7,0.8,1.2)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    cube1.transform=tr.scale(0.6,1,1)
    
    cube2=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1)])
   
    cube3=create_ceil_set(gpuWalls_2_beige,gpuCeil_black,gpuWindow)
    cube3.transform=tr.matmul([tr.translate(0,4,0),tr.scale(0.6,1,1)])
    
    #operaciones nodos internos
    house14.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house14] 

     #casa15
    house15=sg.SceneGraphNode('house15')
    house15.transform=tr.matmul([tr.translate(92,0,11),tr.rotationY(np.pi/2),tr.scale(1.2,0.8,1.4)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    cube1.transform=tr.scale(0.6,1,1)
    cube2=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1)])
   
    cube3=create_ceil_set(gpuWalls_2,gpuCeil,gpuWindow)
    cube3.transform=tr.matmul([tr.translate(0,4,0),tr.scale(0.6,1,1)])
    
    #operaciones nodos internos
    house15.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house15] 

     #casa16
    house16=sg.SceneGraphNode('house16')
    house16.transform=tr.matmul([tr.translate(92,0,20),tr.rotationY(np.pi/2),tr.scale(0.8,0.8,1.2)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    cube1.transform=tr.scale(1,1,1.3)
    
    cube2=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(0,2,-0.2),tr.scale(1,1,1)])
   
    cube3=create_ceil_set(gpuWalls_2_beige,gpuCeil_green,gpuWindow)
    cube3.transform=tr.matmul([tr.translate(0,4,-0.2),tr.scale(1,1,1)])
    
    #operaciones nodos internos
    house16.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house16] 

      #casa 17
    house17=sg.SceneGraphNode('house17')
    house17.transform=tr.matmul([tr.translate(84,0,20),tr.scale(1.5,0.6,1.1)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    cube1.transform=tr.scale(0.6,1,1)
    cube2=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1)])
    cube3=create_ceil_set(gpuWalls_2_beige,gpuCeil_green,gpuWindow)
    cube3.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1.05),tr.rotationY(np.pi/2)])
    cube4=create_ceil_set(gpuWalls_2_beige,gpuCeil_green,gpuWindow)
    cube4.transform=tr.matmul([tr.translate(0,4,0),tr.scale(0.6,1,1),tr.rotationY(np.pi/2)])
    #operaciones nodos internos
    house17.childs+=[cube1,cube2,cube3,cube4]
    nbhood.childs+=[house17]  
    
       #casa 18
    house18=sg.SceneGraphNode('house18')
    house18.transform=tr.matmul([tr.translate(79,0,20),tr.scale(1.5,0.6,1.1)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,True)
    cube1.transform=tr.scale(0.6,1,1)
    cube2=create_cubic_house(gpuWalls_beige,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1)])
    cube3=create_ceil_set(gpuWalls_2_beige,gpuCeil,gpuWindow)
    cube3.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1.05),tr.rotationY(np.pi/2)])
    cube4=create_ceil_set(gpuWalls_2_beige,gpuCeil,gpuWindow)
    cube4.transform=tr.matmul([tr.translate(0,4,0),tr.scale(0.6,1,1),tr.rotationY(np.pi/2)])
    #operaciones nodos internos
    house18.childs+=[cube1,cube2,cube3,cube4]
    nbhood.childs+=[house18] 

    
     #casa19
    house19=sg.SceneGraphNode('house19')
    house19.transform=tr.matmul([tr.translate(62,0,19),tr.rotationY(0),tr.scale(1.5,0.8,1.4)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls_red,gpuDoor,gpuWindow,True)
    cube1.transform=tr.scale(0.6,1,1)
    cube2=create_cubic_house(gpuWalls_red,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1)])
   
    cube3=create_ceil_set(gpuWalls_2_red,gpuCeil_green,gpuWindow)
    cube3.transform=tr.matmul([tr.translate(0,4,0),tr.scale(0.6,1,1)])
    
    #operaciones nodos internos
    house19.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house19] 

    #casa20
    house20=sg.SceneGraphNode('house20')
    house20.transform=tr.matmul([tr.translate(70,0,18),tr.rotationY(0),tr.scale(1.5,0.8,1.4)])
    
    #nodos pisos
    cube1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    cube1.transform=tr.scale(0.6,1,1)
    cube2=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,False)
    cube2.transform=tr.matmul([tr.translate(0,2,0),tr.scale(0.6,1,1)])
   
    cube3=create_ceil_set(gpuWalls_2,gpuCeil_green,gpuWindow)
    cube3.transform=tr.matmul([tr.translate(0,4,0),tr.scale(0.6,1,1)])
    
    #operaciones nodos internos
    house20.childs+=[cube1,cube2,cube3]
    
    nbhood.childs+=[house20] 
    
    #casa 21   
    house21=sg.SceneGraphNode('house21')
    house21.transform=tr.matmul([tr.translate(12,0,15),tr.scale(1.2,1,1.2),tr.rotationY(4/3*np.pi+np.pi)])
   
    #nodos pisos
    floor_1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    ceil_set=create_ceil_set(gpuWalls_2,gpuCeil_green,gpuWindow)
   
    #operaciones nodos internos
    ceil_set.transform=tr.translate(0,2,0)
    house21.childs+=[floor_1]
    house21.childs+=[ceil_set]
    nbhood.childs+=[house21] 

        #casa 22   
    house22=sg.SceneGraphNode('house22')
    house22.transform=tr.matmul([tr.translate(72,0,12),tr.scale(1.2,1,1.2),tr.rotationY(np.pi)])
   
    #nodos pisos
    floor_1=create_cubic_house(gpuWalls,gpuDoor,gpuWindow,True)
    ceil_set=create_ceil_set(gpuWalls_2,gpuCeil_green,gpuWindow)
   
    #operaciones nodos internos
    ceil_set.transform=tr.translate(0,2,0)
    house22.childs+=[floor_1]
    house22.childs+=[ceil_set]
    nbhood.childs+=[house22] 


  
    nbhood.transform=tr.translate(1,0,0.3 )
    return nbhood