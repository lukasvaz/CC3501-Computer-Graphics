
# coding=utf-8
"""Vertices and indices for a variety of simple shapes"""

from libs.assets_path import getAssetPath
import math
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

__author__ = "Daniel Calderon"
__license__ = "MIT"

# A simple class container to store vertices and indices that define a shape


class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

    def __str__(self):
        return "vertices: " + str(self.vertices) + "\n"\
            "indices: " + str(self.indices)


def merge(destinationShape, strideSize, sourceShape):

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset/strideSize) +
                                 index for index in sourceShape.indices]


def applyOffset(shape, stride, offset):

    numberOfVertices = len(shape.vertices)//stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index] += offset[0]
        shape.vertices[index + 1] += offset[1]
        shape.vertices[index + 2] += offset[2]


def scaleVertices(shape, stride, scaleFactor):

    numberOfVertices = len(shape.vertices) // stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index] *= scaleFactor[0]
        shape.vertices[index + 1] *= scaleFactor[1]
        shape.vertices[index + 2] *= scaleFactor[2]


def createAxis(length=1.0):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -length,  0.0,  0.0, 0.0, 0.0, 0.0,
        length,  0.0,  0.0, 1.0, 0.0, 0.0,

        0.0, -length,  0.0, 0.0, 0.0, 0.0,
        0.0,  length,  0.0, 0.0, 1.0, 0.0,

        0.0,  0.0, -length, 0.0, 0.0, 0.0,
        0.0,  0.0,  length, 0.0, 0.0, 1.0]

    # This shape is meant to be drawn with GL_LINES,
    # i.e. every 2 indices, we have 1 line.
    indices = [
        0, 1,
        2, 3,
        4, 5]

    return Shape(vertices, indices)


def createRainbowTriangle():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
        0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
        0.0,  0.5, 0.0,  0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)

def createPrisma():
    
    vertices = [ #cara 1
                -0.5,0,0.5,    0,0,                       
                0.5,0,0.5,    1,0, 
                 0,0.4,0.5,   0.5,1, 
                 0.5,0,-0.5,    0,0,
                 0,0.4,-0.5,    0.5,1,
                 -0.5,0,-0.5,    1,0    ]
    
    indices = [ 0,1,2,
                2,1,3,
                3,2,4,
                3,4,5,
                5,2,4,
                0,5,2   ]
    return Shape(vertices,indices)
       
           
           

def createRainbowQuad():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
        0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
        0.5,  0.5, 0.0,  0.0, 0.0, 1.0,
        -0.5,  0.5, 0.0,  1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createColorQuad(r, g, b):

    # Defining locations and colors for each vertex of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0,  r, g, b,
        0.5, -0.5, 0.0,  r, g, b,
        0.5,  0.5, 0.0,  r, g, b,
        -0.5,  0.5, 0.0,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createTextureNormalQuad(nx, ny):

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions        texture     #normal
        -0.5, 0, -0.5,        0, ny,           0,1,0,
        0.5, 0, -0.5,        nx, ny,           0,1,0,
        0.5,  0, 0.5,        nx, 0,            0,1,0,
        -0.5,  0, 0.5,        0, 0,           0,1,0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)
def createTextureNormalTriangle():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions        texture     #normal
        0.0,  0.0,-0.5,         0.5,1,           0,1,0,
        0.5,  0.0, 0.5,        1, 0,            0,1,0,
        -0.5,  0.0, 0.5,        0, 0,           0,1,0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2
        ]

    return Shape(vertices, indices)


def createColorCircle(N, r, g, b):

    # First vertex at the center
    colorOffsetAtCenter = 0.3
    vertices = [0, 0, 0,
                r + colorOffsetAtCenter,
                g + colorOffsetAtCenter,
                b + colorOffsetAtCenter]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,
            # color
            r, g, b]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return Shape(vertices, indices)


def createRainbowCircle(N):

    # First vertex at the center, white color
    vertices = [0, 0, 0, 1.0, 1.0, 1.0]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,

            # color generates varying between 0 and 1
            math.sin(theta),       math.cos(theta), 0]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i+1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return Shape(vertices, indices)


def createRainbowCube():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions         colors
        -0.5, -0.5,  0.5,  1.0, 0.0, 0.0,
        0.5, -0.5,  0.5,  0.0, 1.0, 0.0,
        0.5,  0.5,  0.5,  0.0, 0.0, 1.0,
        -0.5,  0.5,  0.5,  1.0, 1.0, 1.0,

        -0.5, -0.5, -0.5,  1.0, 1.0, 0.0,
        0.5, -0.5, -0.5,  0.0, 1.0, 1.0,
        0.5,  0.5, -0.5,  1.0, 0.0, 1.0,
        -0.5,  0.5, -0.5,  1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def readOFF(filename, color):
    vertices = []
    normals = []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line == "OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]

        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        #print(f'Vertices shape: {vertices.shape}')

        normals = np.zeros((numVertices, 3), dtype=np.float32)
        #print(f'Normals shape: {normals.shape}')

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]

            vecA = [vertices[aux[2]][0] - vertices[aux[1]][0], vertices[aux[2]]
                    [1] - vertices[aux[1]][1], vertices[aux[2]][2] - vertices[aux[1]][2]]
            vecB = [vertices[aux[3]][0] - vertices[aux[2]][0], vertices[aux[3]]
                    [1] - vertices[aux[2]][1], vertices[aux[3]][2] - vertices[aux[2]][2]]

            res = np.cross(vecA, vecB)
            normals[aux[1]][0] += res[0]
            normals[aux[1]][1] += res[1]
            normals[aux[1]][2] += res[2]

            normals[aux[2]][0] += res[0]
            normals[aux[2]][1] += res[1]
            normals[aux[2]][2] += res[2]

            normals[aux[3]][0] += res[0]
            normals[aux[3]][1] += res[1]
            normals[aux[3]][2] += res[2]
        # print(faces)
        norms = np.linalg.norm(normals, axis=1)
        normals = normals/norms[:, None]

        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)
        vertexData = np.concatenate((vertexData, normals), axis=1)

        # print(vertexData.shape)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0], :]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1], :]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2], :]
            vertexDataF += vertex.tolist()

            indices += [index, index + 1, index + 2]
            index += 3

        return Shape(vertexDataF, indices)


def createColorCubeTarea2(r, g, b):

    return readOFF(getAssetPath('cube.off'), (r, g, b))


def createColorSphereTarea2(r, g, b):

    return readOFF(getAssetPath('sphere.off'), (r, g, b))


def createColorCylinderTarea2(r, g, b):

    return readOFF(getAssetPath('cylinder.off'), (r, g, b))


def createColorConeTarea2(r, g, b):

    return readOFF(getAssetPath('cone.off'), (r, g, b))


def createColorCube(r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -0.5, -0.5,  0.5, r, g, b,
        0.5, -0.5,  0.5, r, g, b,
        0.5,  0.5,  0.5, r, g, b,
        -0.5,  0.5,  0.5, r, g, b,

        -0.5, -0.5, -0.5, r, g, b,
        0.5, -0.5, -0.5, r, g, b,
        0.5,  0.5, -0.5, r, g, b,
        -0.5,  0.5, -0.5, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createFacetedCube():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
        0.5,  0.5,  0.5, 1.0, 0.0, 0.0,
        -0.5,  0.5,  0.5, 1.0, 0.0, 0.0,
        -0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
        0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
        0.5,  0.5,  0.5, 1.0, 0.0, 0.0,

        0.5, -0.5,  0.5, 0.0, 1.0, 0.0,
        0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
        0.5,  0.5,  0.5, 0.0, 1.0, 0.0,
        0.5, -0.5,  0.5, 0.0, 1.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
        0.5,  0.5, -0.5, 0.0, 1.0, 0.0,

        0.5,  0.5,  -0.5, 0.0, 0.0, 1.0,
        -0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
        0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
        0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
        -0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
        -0.5,  0.5,  0.5, 0.0, 0.0, 1.0,

        -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5,  0.5, -0.5, 1.0, 0.0, 0.0,
        -0.5,  0.5, -0.5, 1.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5,  0.5, -0.5, 1.0, 0.0, 0.0,

        -0.5, -0.5,  0.5, 0.0, 1.0, 0.0,
        -0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
        -0.5,  0.5,  0.5, 0.0, 1.0, 0.0,
        -0.5, -0.5,  0.5, 0.0, 1.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
        -0.5,  0.5, -0.5, 0.0, 1.0, 0.0,

        0.5, -0.5,  -0.5, 0.0, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0, 1.0,
        0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
        0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0, 1.0,
        -0.5, -0.5,  0.5, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = range(36)

    return Shape(vertices, indices)


def createTextureCube():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5,  0.5, 0, 1,
        0.5, -0.5,  0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        -0.5,  0.5,  0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5,  0.5, -0.5, 1, 0,
        -0.5,  0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 0, 1,
        0.5,  0.5, -0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        0.5, -0.5,  0.5, 0, 0,

        # X-
        -0.5, -0.5, -0.5, 0, 1,
        -0.5,  0.5, -0.5, 1, 1,
        -0.5,  0.5,  0.5, 1, 0,
        -0.5, -0.5,  0.5, 0, 0,

        # Y+
        -0.5,  0.5, -0.5, 0, 1,
        0.5,  0.5, -0.5, 1, 1,
        0.5,  0.5,  0.5, 1, 0,
        -0.5,  0.5,  0.5, 0, 0,

        # Y-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5,  0.5, 1, 0,
        -0.5, -0.5,  0.5, 0, 0
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

    return Shape(vertices, indices)


def createRainbowNormalsCube():

    sq3 = 0.57735027

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors          normals
        -0.5, -0.5,  0.5, 1.0, 0.0, 0.0, -sq3, -sq3, sq3,
        0.5, -0.5,  0.5, 0.0, 1.0, 0.0,  sq3, -sq3,  sq3,
        0.5,  0.5,  0.5, 0.0, 0.0, 1.0,  sq3,  sq3,  sq3,
        -0.5,  0.5,  0.5, 1.0, 1.0, 1.0, -sq3,  sq3,  sq3,

        -0.5, -0.5, -0.5, 1.0, 1.0, 0.0, -sq3, -sq3, -sq3,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0,  sq3, -sq3, -sq3,
        0.5,  0.5, -0.5, 1.0, 0.0, 1.0,  sq3,  sq3, -sq3,
        -0.5,  0.5, -0.5, 1.0, 1.0, 1.0, -sq3,  sq3, -sq3]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               4, 5, 1, 1, 0, 4,
               6, 7, 3, 3, 2, 6,
               5, 6, 2, 2, 1, 5,
               7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorNormalsCube(r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions         colors   normals
        # Z+
        -0.5, -0.5,  0.5, r, g, b, 0, 0, 1,
        0.5, -0.5,  0.5, r, g, b, 0, 0, 1,
        0.5,  0.5,  0.5, r, g, b, 0, 0, 1,
        -0.5,  0.5,  0.5, r, g, b, 0, 0, 1,

        # Z-
        -0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5,  0.5, -0.5, r, g, b, 0, 0, -1,
        -0.5,  0.5, -0.5, r, g, b, 0, 0, -1,

        # X+
        0.5, -0.5, -0.5, r, g, b, 1, 0, 0,
        0.5,  0.5, -0.5, r, g, b, 1, 0, 0,
        0.5,  0.5,  0.5, r, g, b, 1, 0, 0,
        0.5, -0.5,  0.5, r, g, b, 1, 0, 0,

        # X-
        -0.5, -0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5,  0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5,  0.5,  0.5, r, g, b, -1, 0, 0,
        -0.5, -0.5,  0.5, r, g, b, -1, 0, 0,

        # Y+
        -0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5,  0.5, r, g, b, 0, 1, 0,
        -0.5, 0.5,  0.5, r, g, b, 0, 1, 0,

        # Y-
        -0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5,  0.5, r, g, b, 0, -1, 0,
        -0.5, -0.5,  0.5, r, g, b, 0, -1, 0
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

    return Shape(vertices, indices)


def createTextureNormalsCube():

    # Defining locations,texture coordinates and normals for each vertex of the shape
    vertices = [
        #   positions            tex coords   normals
        # Z+
        -0.5, -0.5,  0.5,    0, 1,        0, 0, 1,
        0.5, -0.5,  0.5,    1, 1,        0, 0, 1,
        0.5,  0.5,  0.5,    1, 0,        0, 0, 1,
        -0.5,  0.5,  0.5,    0, 0,        0, 0, 1,
        # Z-
        -0.5, -0.5, -0.5,    0, 1,        0, 0, -1,
        0.5, -0.5, -0.5,    1, 1,        0, 0, -1,
        0.5,  0.5, -0.5,    1, 0,        0, 0, -1,
        -0.5,  0.5, -0.5,    0, 0,        0, 0, -1,

        # X+
        0.5, -0.5, -0.5,    0, 1,        1, 0, 0,
        0.5,  0.5, -0.5,    1, 1,        1, 0, 0,
        0.5,  0.5,  0.5,    1, 0,        1, 0, 0,
        0.5, -0.5,  0.5,    0, 0,        1, 0, 0,
        # X-
        -0.5, -0.5, -0.5,    0, 1,        -1, 0, 0,
        -0.5,  0.5, -0.5,    1, 1,        -1, 0, 0,
        -0.5,  0.5,  0.5,    1, 0,        -1, 0, 0,
        -0.5, -0.5,  0.5,    0, 0,        -1, 0, 0,
        # Y+
        -0.5,  0.5, -0.5,    0, 1,        0, 1, 0,
        0.5,  0.5, -0.5,    1, 1,        0, 1, 0,
        0.5,  0.5,  0.5,    1, 0,        0, 1, 0,
        -0.5,  0.5,  0.5,    0, 0,        0, 1, 0,
        # Y-
        -0.5, -0.5, -0.5,    0, 1,        0, -1, 0,
        0.5, -0.5, -0.5,    1, 1,        0, -1, 0,
        0.5, -0.5,  0.5,    1, 0,        0, -1, 0,
        -0.5, -0.5,  0.5,    0, 0,        0, -1, 0
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

    return Shape(vertices, indices)


# funcion reciclada de la tarea anterior,  crea una esfera  de cierto radio centrada en el origen , sus colores van alternando 
# en la medida que se barre cierto angulo(simula pelota de playa)
###################rescatada de la tarea anterior , se le agregan las  normales para funcionamiento de los shaders###############
def createSphere(radius,total,r,g,b):
    vertexData=[0,0,radius,r,g,b ,0,0,1]# polo norte
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
            normal=np.array([x,y,z])/np.linalg.norm([x,y,z]) ## se agregan normales
            if i%2==0: # alternamos colores
                vertexData+=[x,y,z,r,g,b , normal[0],normal[1],normal[2] ]
            else:
                vertexData+=[x,y,z,1,1,1,  normal[0],normal[1],normal[2]]
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