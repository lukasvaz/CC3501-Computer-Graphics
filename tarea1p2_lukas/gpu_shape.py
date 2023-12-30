from OpenGL.GL import *
import numpy as np
import constants

SIZE_IN_BYTES = constants.SIZE_IN_BYTES
# clase que caracteriza cada shape, otorga un VAO VBO y EBO a  cada una
class GPUShape:
    def __init__(self):
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.size = None

    def initBuffers(self):# creamos  buffers para entregarlos a la gpu 
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        return self

    def __str__(self):
        return "vao=" + str(self.vao) +\
            "  vbo=" + str(self.vbo) +\
            "  ebo=" + str(self.ebo)

    def fillBuffers(self, vertexData, indexData): # entregamos data (vertices e indices a cada buffer)

        vertexData = np.array(vertexData, dtype=np.float32)
        indexData = np.array(indexData, dtype=np.uint32)

        self.size = len(indexData)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertexData) * SIZE_IN_BYTES, vertexData, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indexData) * SIZE_IN_BYTES, indexData, GL_STATIC_DRAW)

    def clear(self): # eliminamos buffers luego de su uso

        if self.ebo != None:
            glDeleteBuffers(1, [self.ebo])

        if self.vbo != None:
            glDeleteBuffers(1, [self.vbo])

        if self.vao != None:
            glDeleteVertexArrays(1, [self.vao])