import  libs.transformations as tr
from OpenGL.GL import *
import numpy as np
import libs.scene_graph as sg

class Spotlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,0,0])
        self.cutOff = 0
        self.outerCutOff = 0    
spotlightsPool = dict()
class Pointlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])

pointlightsPool = dict()
#se crea  diccionario con spotligths y pointlights
def setLights(daystage,ball,car,postes):
    length=car.length/2
    angle1=car.angle+np.pi/20
    angle2=car.angle-np.pi/20
    dir=np.array([np.sin(car.angle),-0.2,np.cos(car.angle)])
    
    #auto1
    spot1 = Spotlight()
    spot1.ambient = np.array([0.1, 0.1, 0.1])
    spot1.diffuse = np.array([1.0, 1.0,0.5])
    spot1.specular = np.array([1.0, 1.0, 1.0])
    spot1.constant = car.cte
    spot1.linear = car.cte
    spot1.quadratic = car.cte
    spot1.position = np.array([car.position[0]+length*np.sin(angle1),0.3,car.position[2]+length*np.cos(angle1)])#TAREA4: esta ubicada en esta posición
    spot1.direction = dir #TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    spot1.cutOff = np.cos(np.radians(12.5)) #TAREA4: corte del ángulo para la luz
    spot1.outerCutOff = np.cos(np.radians(15)) #TAREA4: la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto
    
    spotlightsPool['spot1'] = spot1 

    #auto2
    spot2 = Spotlight()
    spot2.ambient = np.array([0.1, 0.1, 0.1])
    spot2.diffuse = np.array([1.0, 1.0,0.5])
    spot2.specular = np.array([1.0, 1.0, 1.0])
    spot2.constant = car.cte
    spot2.linear = car.cte
    spot2.quadratic = car.cte
    spot2.position = np.array([car.position[0]+length*np.sin(angle2),0.3,car.position[2]+length*np.cos(angle2)]) #TAREA4: esta ubicada en esta posición
    spot2.direction = dir#TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    spot2.cutOff = np.cos(np.radians(12.5)) #TAREA4: corte del ángulo para la luz
    spot2.outerCutOff = np.cos(np.radians(15)) #TAREA4: la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto
    
    spotlightsPool['spot2'] = spot2 
    for i in range(0,5):
        spot = Spotlight()
        spot.ambient = np.array([0.01, 0.01, 0.01])
        spot.diffuse = np.array([1.0, 1.0,0.5])
        spot.specular = np.array([1.0, 1.0, 1.0])
        spot.constant = daystage.cte_posts
        spot.linear = daystage.cte_posts
        spot.quadratic = daystage.cte_posts
        position=sg.findPosition(postes,"lamp{}".format(i)).reshape(4)
        spot.position = np.array([position[0],3,position[2]-1]) #TAREA4: esta ubicada en esta posición
        spot.direction = np.array([0,-1,0])#TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
        spot.cutOff = np.cos(np.radians(30)) #TAREA4: corte del ángulo para la luz
        spot.outerCutOff = np.cos(np.radians(30))
        spotlightsPool['spotlamp{}'.format(i)]=spot

    for i in range(5,10):
        spot = Spotlight()
        spot.ambient = np.array([0.01, 0.01, 0.01])
        spot.diffuse = np.array([1.0, 1.0,0.5])
        spot.specular = np.array([1.0, 1.0, 1.0])
        spot.constant = daystage.cte_posts
        spot.linear = daystage.cte_posts
        spot.quadratic = daystage.cte_posts
        position=sg.findPosition(postes,"lamp{}".format(i)).reshape(4)
        spot.position = np.array([position[0],3,position[2]+1]) #TAREA4: esta ubicada en esta posición
        spot.direction = np.array([0,-1,0])#TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
        spot.cutOff = np.cos(np.radians(30)) #TAREA4: corte del ángulo para la luz
        spot.outerCutOff = np.cos(np.radians(30))
        spotlightsPool['spotlamp{}'.format(i)]=spot
    
    #sol
    point1 = Pointlight()
    point1.ambient = np.array([0.1, 0.1, 0.1])
    point1.diffuse = np.array([1.0, 1.0,1.0])
    point1.specular = np.array([0.1, 0.1, 0.1])
    point1.constant =daystage.cte_sun
    point1.linear = daystage.cte_sun
    point1.quadratic = daystage.cte_sun
    point1.position = np.array([50, daystage.radius*np.cos(daystage.light_rotation), 12.5+daystage.radius*np.sin(daystage.light_rotation)]) #TAREA4: esta ubicada en esta posición
    
    pointlightsPool['point1'] = point1 
    #luna
    point2 = Pointlight()
    point2.ambient = np.array([0.1, 0.1, 0.1])
    point2.diffuse = np.array([1.0, 1.0,1.0])
    point2.specular = np.array([0.1, 0.1, 0.1])
    point2.constant =daystage.cte_moon
    point2.linear = daystage.cte_moon
    point2.quadratic = daystage.cte_moon
    point2.position = np.array([50.0,-daystage.radius*np.cos(daystage.light_rotation), 12.5-daystage.radius*np.sin(daystage.light_rotation)]) #TAREA4: esta ubicada en esta posición
  
    
    pointlightsPool['point2'] = point2 
    #bola
    point3 = Pointlight()
    point3.ambient = np.array([0, 0, 0])
    point3.diffuse = np.array([1.0, 0.2,0.2])
    point3.specular = np.array([0, 0, 0])
    point3.constant =ball.cte
    point3.linear = ball.cte
    point3.quadratic = ball.cte
    point3.position = ball.pos
  
    
    pointlightsPool['point3'] = point3 #TAREA4: almacenamos la luz en el diccionario, con una clave única'''

    

# se determina la proyeccion y se entregan las  luces del diccionario a los shaders de texturas y colores
def setPlot(texPipeline, colorPipeline, width, height,controller):
    ##proyection
    if controller.camera_state==1:
        
        projection=tr.matmul([tr.scale(1,-1,1),tr.ortho(-60, 60, -20, 20, 20, 150)])
             
    else:
        projection =tr.matmul([tr.scale(-1,1,1),tr.perspective(45, float(width)/float(height), 0.1, 100)])

   ### lights
    # Primero al shader de color
    glUseProgram(colorPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        colorPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    #Enviamos la información de la luz puntual y del material

    glUniform3f(glGetUniformLocation(colorPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(colorPipeline.shaderProgram, "material.diffuse"), 0.1, 0.1, 0.1)
    glUniform3f(glGetUniformLocation(colorPipeline.shaderProgram, "material.specular"), 1, 1, 1)
    glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, "material.shininess"), 100)

    # spotlight 
    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)
    
    #pointlights
    for i, (k,v) in enumerate(pointlightsPool.items()):
        baseString = "pointLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "quadratic"),  v.quadratic)
        glUniform3fv(glGetUniformLocation(colorPipeline.shaderProgram, baseString + "position"), 1, v.position)


    
    # Ahora repetimos todo el proceso para el shader de texturas con mútiples luces
    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(
        texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.ambient"), 0.1, 0.1, 0.1)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.specular"), 0.2, 0.2, 0.2)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "material.shininess"), 10)

    #spotlights
    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)
   #pointlights
    for i, (k,v) in enumerate(pointlightsPool.items()):
        baseString = "pointLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"),  v.quadratic)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
       
      
#posicion y direccion de la camara 
def setView(pipeline, mvpPipeline, controller):

    if controller.camera_state==0:#primera persona
   
        view = tr.lookAt(
        controller.pos,
        controller.look_at,
        np.array([0, 1, 0])
        )
    if controller.camera_state==1:#vista superior
        
        view=tr.matmul([tr.lookAt(
        np.array([0,80,0]),
       np.array([0.2,0,0]),
        np.array([0, 1, 0])
        ),tr.rotationY(-np.pi/2),tr.translate(-50,0,-12.5)])

    if controller.camera_state==2:#vista tercera persona
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
    
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.pos[0], controller.pos[1], controller.pos[2])


