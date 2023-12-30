from OpenGL.GL import *
import libs.scene_graph as sg
from libs.obj_reader import  readOBJ
import libs.easy_shaders as es
from libs.assets_path import getAssetPath
import numpy as np
import libs.transformations as tr
#se crea escena de los postes ocupando scenegraph
def create_lamps_scene(colorShaderProgram):
    #creamos shape de los postes
    shapePost=readOBJ(getAssetPath("lamppost.obj"),np.array([0,0,0]))
    gpuPost=es.GPUShape().initBuffers()
    colorShaderProgram.setupVAO(gpuPost)
    gpuPost.fillBuffers(shapePost.vertices, shapePost.indices, GL_STATIC_DRAW)
    #               lamp set
    #upperleft   | upper right | lowerleft | lower right
    lamps_set = sg.SceneGraphNode('scene')
    lamps_upper_left=sg.SceneGraphNode('lamps_upper_left')
    
    for i in range(0,2):  
        lamp=sg.SceneGraphNode('lamp{}'.format(i))
        lamp.transform=tr.matmul([tr.translate(35+10*i,0,2.5),tr.rotationY(-np.pi/2)])
        lamp.childs+=[gpuPost]
        lamps_upper_left.childs+=[lamp]
        lamps_set.childs+=[lamps_upper_left]

    lamps_upper_right=sg.SceneGraphNode('lamps_upper_right')
    for i in range(0,3):  
        lamp=sg.SceneGraphNode('lamp{}'.format(i+2))
        lamp.transform=tr.matmul([tr.translate(55+20*i,0,2.5),tr.rotationY(-np.pi/2)])
        lamp.childs+=[gpuPost]
        lamps_upper_right.childs+=[lamp]

    lamps_set.childs+=[lamps_upper_right]

    lamps_lower_right=sg.SceneGraphNode('lamps_lower_right')
    for i in range(0,3):  
        lamp=sg.SceneGraphNode('lamp{}'.format(i+5))
        lamp.transform=tr.matmul([tr.translate(55+20*i,0,20+2.5),tr.rotationY(np.pi/2)])
        lamp.childs+=[gpuPost]
        lamps_lower_right.childs+=[lamp]

    lamps_set.childs+=[lamps_lower_right]

    lamps_lower_left=sg.SceneGraphNode('lamps_lower_left')
    for i in range(0,2):  
        lamp=sg.SceneGraphNode('lamp{}'.format(i+8))
        lamp.transform=tr.matmul([tr.translate(25+20*i,0,20+2.5),tr.rotationY(np.pi/2)])
        lamp.childs+=[gpuPost]
        lamps_lower_left.childs+=[lamp]

    lamps_set.childs+=[lamps_lower_left]

    return lamps_set