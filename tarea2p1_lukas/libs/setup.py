import  libs.transformations as tr
from OpenGL.GL import glUseProgram, glUniformMatrix4fv, glGetUniformLocation,\
    GL_TRUE, glUniform3f, glUniform1ui, glUniform1f
import numpy as np
import libs.basic_shapes as bs


def setPlot(pipeline, mvpPipeline, width, height):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(
        pipeline.shaderProgram, "lightPosition"), 5, 5, 5)

    glUniform1ui(glGetUniformLocation(
        pipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(
        pipeline.shaderProgram, "constantAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(
        pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(
        pipeline.shaderProgram, "quadraticAttenuation"), 0.01)


def setView(pipeline, mvpPipeline, controller):
    if controller.camera_state==0:
   
        view = tr.lookAt(
        controller.pos,
        controller.look_at,
        np.array([0, 1, 0])
        )
    if controller.camera_state==1:
        
        view=tr.matmul([
            
            
            tr.ortho(-10, 10, -5, 5, 70, 150),
            tr.translate(-50,-12,200),
            tr.rotationX(-np.pi/2)
        ])
    if controller.camera_state==2:
        position=controller.pos-5*controller.direction
        position[1]=1.0
        look_at=controller.look_at
        look_at[1]=1.0
        view = tr.lookAt(
        position,
        look_at,
        np.array([0, 1, 0])
        )
    

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.pos[0], controller.pos[1], controller.pos[2])




    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+: block top
        0.5,  0.5,  0.5, 1/4, 2/3,
        0.5, -0.5,  0.5, 0, 2/3,
        -0.5, -0.5,  0.5, 0, 1/3,
        -0.5,  0.5,  0.5, 1/4, 1/3,

        # Z-: block bottom
        -0.5, -0.5, -0.5, 3/4, 1/3,
        0.5, -0.5, -0.5, 3/4, 2/3,
        0.5,  0.5, -0.5, 2/4, 2/3,
        -0.5,  0.5, -0.5, 2/4, 1/3,

        # X+: block left
        0.5, -0.5, -0.5, 2/4, 1,
        0.5,  0.5, -0.5, 2/4, 2/3,
        0.5,  0.5,  0.5, 1/4, 2/3,
        0.5, -0.5,  0.5, 1/4, 1,

        # X-: block right
        -0.5, -0.5, -0.5, 3/4, 2/3,
        -0.5,  0.5, -0.5, 2/4, 2/3,
        -0.5,  0.5,  0.5, 2/4, 1/3,
        -0.5, -0.5,  0.5, 3/4, 1/3,

        # Y+: white face
        -0.5,  0.5, -0.5, 2/4, 1/3,
        0.5,  0.5, -0.5, 2/4, 2/3,
        0.5,  0.5,  0.5, 1/4, 2/3,
        -0.5,  0.5,  0.5, 1/4, 1/3,

        # Y-: yellow face
        -0.5, -0.5, -0.5, 1, 1/3,
        0.5, -0.5, -0.5, 1, 2/3,
        0.5, -0.5,  0.5, 3/4, 2/3,
        -0.5, -0.5,  0.5, 3/4, 1/3
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return bs.Shape(vertices, indices)
