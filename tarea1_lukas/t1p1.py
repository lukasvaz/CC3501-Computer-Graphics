# coding=utf-8
import sys
import glfw
from OpenGL.GL import *
from gpu_shape import GPUShape
from easy_shaders import SimpleTransformShader
from basic_shapes import * 
import transformations as tr
from constants import *
import numpy as np



def main():
   

    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return -1

    #se crea la ventana a utilizar con glfw
    window = glfw.create_window(width, height, "Tarea 1: ghost", None, None)
    
    #se cierra glfw al cerrar la ventana
    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1
    glfw.make_context_current(window)
    #se inicializa el Shader y se le otorga a  opengl
    pipeline = SimpleTransformShader()
    glUseProgram(pipeline.shaderProgram)


    ##################### dibujamos la figura vertice por vertice#####################################################################


    #rectangulo fondo##
    c0 = createRectangle(x1_hitbox, y1_hitbox,-x1_hitbox,-y1_hitbox,r_back,g_back,b_back)
    gpuC0 = GPUShape().initBuffers()
    pipeline.setupVAO(gpuC0)
    gpuC0.fillBuffers(c0.vertexData, c0.indexData)

    #rectangulo cuerpo
    c1 = createRectangle(pos_rec[0], pos_rec[1],-pos_rec[0],-pos_rec[1],r_body,g_body,b_body)### se le otorgan colores solicitados en tarea
    gpuC1 = GPUShape().initBuffers()
    pipeline.setupVAO(gpuC1)
    gpuC1.fillBuffers(c1.vertexData, c1.indexData)

    ##casco
    c2 = createEllipse_alpha(pos_casco[0],pos_casco[1],15,180,ancho/2, alt_casco,r_body,g_body,b_body )
    gpuC2 = GPUShape().initBuffers()
    pipeline.setupVAO(gpuC2)
    gpuC2.fillBuffers(c2.vertexData, c2.indexData)
    
    ## falda
    c3 =falda(pos_rec[0],pos_rec[1],ancho , alt_falda, 4 ,r_body,g_body,b_body)
    gpuC3 = GPUShape().initBuffers()
    pipeline.setupVAO(gpuC3)
    gpuC3.fillBuffers(c3.vertexData, c3.indexData)
    
    ####ojos##
    ##izq
    c4 =createEllipse_alpha(posicion_ojos[0],posicion_ojos[1],15,360, radio_ojos,radio_ojos,r_back,g_back,b_back)
    gpuC4 = GPUShape().initBuffers()
    pipeline.setupVAO(gpuC4)
    gpuC4.fillBuffers(c4.vertexData, c4.indexData)
    
    ###der
    c5 =createEllipse_alpha(posicion_ojos[0]-delta_ojos,posicion_ojos[1],15,360, radio_ojos,radio_ojos,r_back,g_back,b_back)
    gpuC5 = GPUShape().initBuffers()
    pipeline.setupVAO(gpuC5)
    gpuC5.fillBuffers(c5.vertexData, c5.indexData)
    
    #pupilas
    c6 =rombo(posicion_ojos[0],posicion_ojos[1],par_pupilas[0],par_pupilas[1],r_body,g_body,b_body)
    gpuC6 = GPUShape().initBuffers()
    pipeline.setupVAO(gpuC6)
    gpuC6.fillBuffers(c6.vertexData, c6.indexData)

    c7 =rombo(posicion_ojos[0]-delta_ojos,posicion_ojos[1],par_pupilas[0],par_pupilas[1],r_body,g_body,b_body)
    gpuC7 = GPUShape().initBuffers()
    pipeline.setupVAO(gpuC7)
    gpuC7.fillBuffers(c7.vertexData, c7.indexData)

    #color fondo de la ventana##
    glClearColor(0,0,0, 1.0)


    ### determinamos velocidad####
    iniciales="lv"#las puse en minusculas pq en mayuscula era muy fome el mob¿vimiento
    alpha=ord(iniciales[0]) * ord(iniciales[1])
    delta_x=350*np.cos(alpha)
    delta_y=350*np.sin(alpha)
    # la velocidad es determinada en pixel/segundo####
    print("velocidad  en pix/seg:{} {}".format(delta_x,delta_y))
    
    #### debemos cambiarles las unidades de medida a la velocidad para adecuarlo a la pantalla, para esto debemos normalizar  los pixeles a las dimensiones de la pantalla 
    ### de esta manera moverse 20 px a la der=> corresponde a 20/ width "pixeles normalizados (norpx)" en la ventana.Ademas necesitamos saber el tiempo que demora cada frame
    ### ,para esto fijamos una velocidad de 60 fps (posteriormente se vera como), utilizando esto calculamos los norpx/frame que debra moverse la  figura en cada frame
    # (px/seg*(norpx/px)*(seg/frame)=>norpx/frame)
      
    
    delta_x=350*np.cos(alpha)/(fps*width)#norpx/frame
    delta_y=350*np.sin(alpha)/(fps*height)#norpx/frame
    
    print("velocidad  en norpix/frame:{} {}".format(delta_x,delta_y))
    ##parametros de movimiento
    vel_x,vel_y=0,0 # situamos las velocidades iniciales, las cuales serviran como vector posición del centro de la figura    
    hit_counter=0 # situamos  un contador de golpes, el cual servira para determinar la rotacion de la figura (90 grado*hit) 
                  #y ademas otorga informacion del sentido de la figura (si se encuentra vertical u horizontal)  
     
    
    scale=scale_factors[0]# seleccionamos la escala inicial, correspondiente a 1.0
   
   
    while not glfw.window_should_close(window): # mientras la ventana este abierta
        
       
        if  hit_counter%2==0:# si hit_counter es par la figura esta vertical
            scale=scale_factors[0] # escala=1.0
# aqui se determina la condicion para determinar un hit,si la distancia entre el centro de la figura y la pared es menor que el ancho(verticalmente,dado por x1_hitbox) 
# se cambia el sentido de la velocidad en x,en cada hit con la pantalla se realizara un desplazamiento central para evitar comportamientos oscilantes entre las paredes  debido a que de un frame a otro este se mantenga
#  fuera de la pantalla.Es necesario desplazar la figura hacia el centro cuando esta choca por su lado mayor(en este caso horizontalmente), este desplazamiento esta dado por
#  abs(y1_hitbox-x1_hitbox)+0.05*scale_factors[1])*scale_factors[1]*delta_x/abs(delta_x)    (  abs(y1_hitbox-x1_hitbox) nos da la magnitud del dezplazamiento, 0.05*scale_factors[1] 
# corresponde a un epsilon que evita el caso borde (es decir que quede fuera o justo en la pantalla) y delta_x/abs(delta_x) nos da el sentido del dezplazamiento) 
            
            if 1-abs(vel_x)<(-x1_hitbox)*scale :
                hit_counter+=1 #aumentamos el contador de hits
                delta_x=-delta_x #cambia el sentido de la velocidad
                vel_x+=(abs(y1_hitbox-x1_hitbox)+0.05*(scale_factors[1])**2)*scale_factors[1]*delta_x/abs(delta_x) # desplazamiento para evitar casos borde
                
               
            
            if 1-abs(vel_y)<(-y1_hitbox)*scale : 
                hit_counter+=1 
                delta_y=-delta_y
                vel_y+=0.04*(scale_factors[1]**3)*delta_y/abs(delta_y)## desplazaminto para evitar casos borde
               
               

## esta condicion es analogo al caso anterior solo que la figura se encuentra orientada verticalmente##
        if  hit_counter%2!=0:
            scale=scale_factors[1] ## escala aumentada
            if 1-abs(vel_x)<(-y1_hitbox)*scale  :
                hit_counter+=1
                delta_x=-delta_x
                vel_x+=0.03*(scale_factors[0]**3)*delta_x/abs(delta_x)## desplazaminto para evitar casos borde
               
                
            
            if 1-abs(vel_y)<(-x1_hitbox)*scale  :
                hit_counter+=1
                delta_y=-delta_y
                vel_y+=(abs(y1_hitbox-x1_hitbox)+0.05*(scale_factors[0])**2)*scale_factors[0]*delta_y/abs(delta_y)# desplazamiento para evitar casos borde
                
                
       
        vel_x+=delta_x #determinamos posicion final
        vel_y+=delta_y #
       
       
        glfw.poll_events()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)## FILL llenar las figuras

        glClear(GL_COLOR_BUFFER_BIT)

##### realizamos las transformaciones necesarias para rotar , escalar y transladar la figura##########
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(vel_x,vel_y,0),
            tr.scale(scale,scale,0),
            tr.rotationZ(-np.pi/2*hit_counter)
            
            
            
        ]))
        ###comenzamos a dibujar cada figura##
        ##cuerpo
        pipeline.drawCall(gpuC0)
        pipeline.drawCall(gpuC1)
        pipeline.drawCall(gpuC2)
        pipeline.drawCall(gpuC3)
        pipeline.drawCall(gpuC4)
        pipeline.drawCall(gpuC5)
        pipeline.drawCall(gpuC6)
        pipeline.drawCall(gpuC7)
        glfw.swap_buffers(window)
        

        ## esta parte corresponde a determinar la velocidad de fps, para esto se situa un contador temporal en 0  (en cada iteracion) y se espera (mediante el while)
        ## que transcurran  1/fps segundos para  comenzar la siguiente iteracion. en cada iteracion se obtiene u  aporximado de 1/fps seg  el cual no es exacto 
        # por las opercaiones anteriores

        glfw.set_time(0)
        time=0
        while time<(1/fps):
            time=glfw.get_time()
        
        
    ## al salir del while se limpia la pantalla y se termina glfw
    gpuC0.clear()
    gpuC1.clear()
    gpuC2.clear()
    gpuC3.clear()
    gpuC4.clear()
    gpuC5.clear()
    gpuC6.clear()
    gpuC7.clear()

    glfw.terminate()

    return 0

if __name__ == "__main__":
    
    main()