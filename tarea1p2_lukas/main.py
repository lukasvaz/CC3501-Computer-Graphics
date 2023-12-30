# coding=utf-8

# importamos librerias y varaiables a utilizar
import glfw
from OpenGL.GL import *
from gpu_shape import GPUShape
from easy_shaders import SimpleModelViewProjectionShaderProgram
from basic_shapes import *
import numpy as np
import transformations as tr
import constants

width = constants.SCREEN_WIDTH
height = constants.SCREEN_HEIGHT
scal=constants.SCALE

# creamos una clase controlador, la cual se encargará de detectar las colisiones entre dos objetos moviendose (bola1 y bola 2) mediante el metodo
# moving_bounce()  además se encargara de controlar la perspectiva de la camara mediante los metodos rot_right() y rot _left()


class Controller():
    def __init__(self):
        self.angle=0 # angulo inicial  de perspectiva
        self.dist=constants.LOOK_AT[0] # distancia desde la camara al origen
        self.look_at=constants.LOOK_AT # posiscion de la camara
        self.dt=0
        self.gravity=constants.GRAVITY # gravedad 
        
    
    def rot_right(self): # metodo que cambia el valor de la posicion de la camara  rotar 2pi/15 grados hacia la derecha  
        self.angle+=2*np.pi/15
        x=self.dist*np.cos(self.angle)
        z=self.dist*np.sin(self.angle)
        self.look_at=np.array([x,self.look_at[1],z]) # nueva posicion de la camara


    def rot_left(self):#  metodo que cambia el valor de la posicion de la camara  rotar 2pi/15 grados hacia la izquierda
        self.angle-=2*np.pi/15
        x=self.dist*np.cos(self.angle)
        z=self.dist*np.sin(self.angle)
        self.look_at=np.array([x,self.look_at[1],z])# nueva posicion de la camara

    def view(self):
        return self.look_at # retorna la nueva posicion de la camra
    

    ### metodos para determinar la colision entre objetos moviles

    def distance(self,vec1,vec2): # determina  distancia entre dos  vectores
        return np.linalg.norm(vec2-vec1)
    
    def moving_bounce(self,obj1,obj2): 
        # si dos objetos estan a una distancia menor a  2*scal(= 2 * radios de las bolas) estos  cambian sus velocidades en el plano 
        #horizontal manteniendo la magnitud de la velocidades  pero en una direccion opuesta al vector de  distancia entre los dos objetos

        if self.distance(obj1.current_pos,obj2.current_pos)<2*scal:
            
            vec2=np.array([obj2.current_pos[0],obj2.current_pos[2]])
            vec1=np.array([obj1.current_pos[0],obj1.current_pos[2]])
            const1=np.linalg.norm(np.array([obj1.delta[0],obj1.delta[2]]))
            const2=np.linalg.norm(np.array([obj2.delta[0],obj2.delta[2]]))
            vec=vec2-vec1
            norm_vec=vec/np.linalg.norm(vec)
         
            f_vec1=-const1*norm_vec
            f_vec2=const2*norm_vec
           
            obj1.delta[0]=f_vec1[0]
            obj1.delta[2]=f_vec1[1]
            obj2.delta[0]=f_vec2[0]
            obj2.delta[2]=f_vec2[1]
        
    
       
controller=Controller() # instanciamos controlador para posterior uso


##  detectamos teclas ##
def on_key(window, key, scancode, action, mods):

    if key == glfw.KEY_RIGHT and action==glfw.PRESS:# flecha derecha  rota hacia derecha
       controller.rot_right()
       
    if key == glfw.KEY_LEFT and action==glfw.PRESS:# flecha izq rota hacia  izq
        controller.rot_left()



##### clase que permite describir  el cubo ###

class Cube():
    
    def __init__(self,init=[0,0,0]):
        self.current_pos=np.array(init)# centro del cubo 
       
   
    def set(self,shape,pipeline): # inicializamos buffers , entregamos VAO e indices
        gpuC = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC)
        gpuC.fillBuffers(shape.vertexData, shape.indexData)
        return gpuC

    def set_trans(self,pipeline,transform=[tr.scale(1,1,1)]): # funcion que aplica transformaciones al cubo, le entrgamos las transformaciones en una lista(transform)

        #proyeccion 
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, tr.perspective(constants.FOVY, float(width)/float(height), 0.1, 100))

        #posicion y foco de la camara (parametros en controller)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, tr.lookAt(
            controller.view(),
            np.array([0,0,0]),
            np.array([0,1,0])
        ))
        #transformaciones al cubo
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul(transform +[  
            tr.translate(self.current_pos[0],self.current_pos[1],self.current_pos[2]),         
            tr.scale(1,1,1),
        ]))
        
        
    
##### clase que permite describir  las bolas ###

class Ball():

    def __init__(self,init=[0,0,0],delta=[0,0,0]):

        self.init=np.array(init) # posicion inicial de la bola
        self.vel=np.array([0,0,0],dtype=np.float64) # vector de traslacion desde init hasta su posicion actual
        self.trans=[] #transformaciones a aplicar en la bola
        self.first_floor=False #booleano que retorna TRUE  si la bola toca por primera vez el piso(se usará para determinar vel de rebote)
        self.terminal_vel=0 # velocidad al tocar el piso (0 inicialmente)
        self.delta=np.array(delta) # vector con velocidades instantaneas 
        self.current_pos=np.array(init,dtype=np.float64)# posicion actual (init+vel)
        
        self.rot_x=0 #parametro que determinara rotacione en eje x (se rotara un poco en x por cada rebote)

    def set(self,shape,pipeline): # inicializamos buffers , entregamos VAO e indices
        gpuC = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC)
        gpuC.fillBuffers(shape.vertexData, shape.indexData)
        return gpuC


    def set_trans(self,pipeline): # funcion que aplica transformaciones a la bola, le entrgamos las transformaciones en una lista (self.trans)
        #proyeccion 
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, tr.perspective(constants.FOVY, float(width)/float(height), 0.1, 100))

        #posicion y foco de la camara (parametros en controller)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, tr.lookAt(
            controller.view(),
            np.array([0,0,0]),
            np.array([0,1,0])
        ))
        
        #transformaciones a Bola
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul(self.trans+[  
            tr.translate(self.init[0],self.init[1],self.init[2]),         
            tr.scale(scal,scal, scal),
            tr.rotationX(self.rot_x)
            

        ]))
        
    
    def update(self): # metodo que va actualizando los valores de  la bola en cada iteracion
        # utilizamos factor dt para trabajar con respecto al tiempo en segundo  y no en frames 
        self.delta[1]-=controller.gravity*controller.dt# restamos velocidad vertical de acuerdo a la gravedad
        self.vel+=self.delta*controller.dt # se actualiza la velocidad 
        self.current_pos=self.init+self.vel # actualizamos posicion actual
        self.trans=[tr.translate(self.vel[0],self.vel[1],self.vel[2])] # actualizamos transformaciones 

    def  get_terminal_vel(self): # metodo que captura la velocidad con la que una bola llega al piso, 
        #se ocupa esta misma velocidad como velocidad inicial para el trayecto de vuelta
        if not self.first_floor and abs(-0.5-self.current_pos[1])<(scal*constants.LARGO_CUBO):
            self.terminal_vel=self.delta[1]
            self.first_floor=True
            

    def bounce(self): # metodo que cambia las velocidades instanteaneas de acuerdo si hay  colision con las paredes del cubo,
        # el rebote se determina si la distancia entre  bola y cubo es menor a 0.1 (radio bola), en cada colision se le da rotacion de np.pi/10 en x a la bola
   

         ### paredes verticales
        if abs(-0.5-self.current_pos[0])<(scal*constants.LARGO_CUBO):
            self.delta[0]=abs(self.delta[0])
            self.rot_x+=np.pi/10
            
        if abs(0.5-self.current_pos[0])<(scal*constants.LARGO_CUBO):
            self.delta[0]=-abs(self.delta[0])
            self.rot_x+=np.pi/10
            
    
        if abs(-0.5-self.current_pos[2])<(scal*constants.LARGO_CUBO):
            self.delta[2]=abs(self.delta[2])
            self.rot_x+=np.pi/10
         
        
        if abs(0.5-self.current_pos[2])<(scal*constants.LARGO_CUBO):
            self.delta[2]=-abs(self.delta[2])
            self.rot_x+=np.pi/10
            
        ### piso y techo
        if abs(-0.5-self.current_pos[1])<(scal*constants.LARGO_CUBO):
            
            self.delta[1]= abs(self.terminal_vel) # si toca el piso rebota con velocidad= velocidaad terminal 
            self.rot_x+=np.pi/10
           
        if abs(0.5-self.current_pos[1])<(scal*constants.LARGO_CUBO):# si toce el techo su vel instantanea es 0
            self.delta[1]= 0
            self.rot_x+=np.pi/10
           
  
def main():
   
    
    if not glfw.init(): # si no esta imicializado glfw  se cierra ventana
        glfw.set_window_should_close(window, True)
        return -1

    window = glfw.create_window(width, height, "bolitas", None, None) #creamos la ventana a utilizar

    if not window:  
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window) # se entrega el valor de la ventana
    glfw.set_key_callback(window, on_key) # se capturan los valores de las teclas

    pipeline = SimpleModelViewProjectionShaderProgram() #se instancia el shader a ocupar
    glUseProgram(pipeline.shaderProgram) #se le entrega el shader  a open gl 

   
    ## creamos las bolas####
    ##############pos inicial , vel
   
    ball_1=Ball([0,0.3,0],[np.sqrt((0.4**2)/2),0.5,np.sqrt((0.4**2)/2)])
    ball_2=Ball([-0.2,0.3,-0.2],[2*np.sqrt((0.4**2)/5),0.7,np.sqrt((0.4**2)/5)])
    ball_3=Ball([0.2,0.3,0.2],[np.sqrt((0.4**2)/10),1,3*np.sqrt((0.4**2)/10)])

    #chequeamos correctitud de la magnitudes en la velocidad
    print("bola1 ","vx^2+vy^2={}".format(ball_1.delta[0]**2+ball_1.delta[2]**2),"V^2={}".format(constants.V**2))
    print("bola2 ","vx^2+vy^2={}".format(ball_2.delta[0]**2+ball_2.delta[2]**2),"V={}".format(constants.V**2))
    print("bola3 ","vx^2+vy^2={}".format(ball_3.delta[0]**2+ball_3.delta[2]**2),"V={}".format(constants.V**2))
    ball1_shape=createSphere(1,20,1,0,1)
    ball2_shape=createSphere(1,20,0,0,1)
    ball3_shape=createSphere(1,20,1,0,0)
    
    gpuC13=ball_1.set(ball1_shape,pipeline)
    gpuC14=ball_2.set(ball2_shape,pipeline)
    gpuC15=ball_3.set(ball3_shape,pipeline)



    # creamos cada arista del cubo, para esto se utiliza la funcion para crear un cubo y se escala y traslada de tal manera de generar 
    # una arista en su ubicacion y medidas correcta , esto para cada una  
    cube1=Cube()
    cube1_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC1=cube1.set(cube1_shape,pipeline)

    cube2=Cube()
    cube2_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC2=cube2.set(cube2_shape,pipeline)

    cube3=Cube()
    cube3_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC3=cube3.set(cube3_shape,pipeline)

    cube4=Cube()
    cube4_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC4=cube4.set(cube4_shape,pipeline)

    cube5=Cube()
    cube5_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC5=cube5.set(cube5_shape,pipeline)

    cube6=Cube()
    cube6_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC6=cube6.set(cube6_shape,pipeline)

    cube7=Cube()
    cube7_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC7=cube7.set(cube7_shape,pipeline)

    cube8=Cube()
    cube8_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC8=cube8.set(cube8_shape,pipeline)

    cube9=Cube()
    cube9_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC9=cube9.set(cube9_shape,pipeline)

    cube10=Cube()
    cube10_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC10=cube10.set(cube10_shape,pipeline)

    cube11=Cube()
    cube11_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC11=cube11.set(cube11_shape,pipeline)

    cube12=Cube()
    cube12_shape=createCube(constants.C_r,constants.C_g,constants.C_b)
    gpuC12=cube12.set(cube12_shape,pipeline)



    glClearColor(0.15, 0.15, 0.15, 1.0) # color de fondo de la ventana
    glEnable(GL_DEPTH_TEST)

    t0 = glfw.get_time() #inicializamos el contador de tiempo  este se reiniciará entre cada iteracion, obteniendo un dt entre cada iteracion

    while not glfw.window_should_close(window):

        glfw.poll_events()
        controller.moving_bounce(ball_1,ball_2) #permitimos colisiones entre bola 1 y 2
        controller.moving_bounce(ball_1,ball_3) # permitimos colisiones entre bola 1 y 3
        controller.moving_bounce(ball_3,ball_2) # permitimos colisiones entre bola 3y 2
       
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # pintamos las figuras

        #################   preparamos vertices y dibujamos  el cubo     ###################
        cube1.set_trans(pipeline,[tr.translate(0.5,0,0.5),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC1)

        cube2.set_trans(pipeline,[tr.translate(0.5,0,-0.5),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC2)

        cube3.set_trans(pipeline,[tr.translate(-0.5,0,0.5),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC3)

        cube4.set_trans(pipeline,[tr.translate(-0.5,0,-0.5),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC4)

        cube5.set_trans(pipeline,[tr.translate(0.5,0.5,0),tr.rotationX(np.pi/2),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC5)

        cube6.set_trans(pipeline,[tr.translate(-0.5,0.5,0),tr.rotationX(np.pi/2),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC6)

        cube7.set_trans(pipeline,[tr.translate(-0.5,-0.5,0),tr.rotationX(np.pi/2),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC7)

        cube8.set_trans(pipeline,[tr.translate(0.5,-0.5,0),tr.rotationX(np.pi/2),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC8)

        cube9.set_trans(pipeline,[tr.translate(0,-0.5,0.5),tr.rotationZ(np.pi/2),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC9)

        cube10.set_trans(pipeline,[tr.translate(0,-0.5,-0.5),tr.rotationZ(np.pi/2),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC10)

        cube11.set_trans(pipeline,[tr.translate(0,0.5,0.5),tr.rotationZ(np.pi/2),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC11)

        cube12.set_trans(pipeline,[tr.translate(0,0.5,-0.5),tr.rotationZ(np.pi/2),tr.scale(0.01,1,0.01)])
        pipeline.drawCall(gpuC12)

        
        #################   preparamos vertices y dibujamos  las bolas     ###################
        ball_1.get_terminal_vel()
        ball_1.bounce()
        ball_1.set_trans(pipeline)
        pipeline.drawCall(gpuC13)
        ball_1.update()
          
        ball_2.get_terminal_vel()
        ball_2.bounce()
        ball_2.set_trans(pipeline)
        pipeline.drawCall(gpuC14)
        ball_2.update()
        
        
        ball_3.get_terminal_vel()
        ball_3.bounce()
        ball_3.set_trans(pipeline)
        pipeline.drawCall(gpuC15)
        ball_3.update()
    
        glfw.swap_buffers(window) #
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        controller.dt=dt
        
   
    gpuC1.clear()
    gpuC2.clear()
    gpuC3.clear()
    gpuC4.clear()
    glfw.terminate()

    

    return 0

if __name__ == "__main__":
    main()
