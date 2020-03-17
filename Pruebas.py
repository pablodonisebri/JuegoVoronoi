import pygame
from pygame.locals import *
from auxiliar import *
#from Voronoi import *
import math

#Funcion para determinar el movimiento de los puntos dandole un punto y un vector
def movimiento(p,v,k):
    v=colision(p,v,k)
    if p[0]>700:
        v=[-v[0],v[1]]
    elif p[0]<0:
        v=[-v[0],v[1]]
    elif p[1]<0:
        v=[v[0],-v[1]]
    elif p[1]>700:
        v=[v[0],-v[1]]
    return ([p[0]+v[0],p[1]+v[1]],v)


#Funcion que se va a encargar de mantener distancia de seguridad entre los puntos y va a hacer que reboten en caso de colision
def colision(point,vectorp,k):
    global p,vec
    #Ver si ese punto va a colisionar con algun otro punto
    def abs(n):
        if n >= 0:
            return n
        else:
            return -n

    def mod(v):
        return int(math.sqrt(v[0]**2 +v[1]**2))

    for j in range(len(p)):
        rx=p[j][0]-point[0]
        ry=p[j][1]-point[1]

        if  j!=k and abs(rx)<12 and abs(ry)<12 :
            vec[j]=[int(5*((vec[j][0]-vectorp[0])/(mod([vec[j][0]-vectorp[0],vec[j][1]-vectorp[1]])))),int(5*((vec[j][1]-vectorp[1])/(mod([vec[j][0]-vectorp[0],vec[j][1]-vectorp[1]]))))]

            return [int(5*((vectorp[0]-vec[j][0])/(mod([vec[j][0]-vectorp[0],vec[j][1]-vectorp[1]])))),int(5*((vectorp[1]-vec[j][1])/(mod([vec[j][0]-vectorp[0],vec[j][1]-vectorp[1]]))))]

    return [vectorp[0],vectorp[1]]







#Funcion para pintar en pantalla los diagramas despues de cada interaccion con el usuario
def pintar():
    global p

    D=Delaunay(p)
    V=Voronoi(D)
    for v in range (len(p)-1):
                    if v%2:
                        pygame.draw.polygon(ventana,(0,0,250),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(143,143,143),p[v],9)
                        pygame.draw.circle(ventana,(0,0,0),p[v],4)


                    else:
                        pygame.draw.polygon(ventana,(250,0,0),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(143,143,143),p[v],9)
                        pygame.draw.circle(ventana,(0,0,0),p[v],4)


                    pygame.draw.polygon(ventana,(0,250,0),V[len(p)-1])
                    pygame.draw.polygon(ventana,(0,0,0),V[len(p)-1],2)
                    pygame.draw.circle(ventana,(143,143,143),p[len(p)-1],9)
                    pygame.draw.circle(ventana,(0,0,0),p[len(p)-1],4)



    pygame.display.update()


#Sacado del video : https://www.youtube.com/watch?v=i6xMBig-pP4
def teclas():
    global vec
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        vec[len(p)-1]=[-6,0]


    if keys[pygame.K_RIGHT]:
        vec[len(p)-1]=[6,0]

    if keys[pygame.K_UP]:
        vec[len(p)-1]=[0,-6]


    if keys[pygame.K_DOWN]:
        vec[len(p)-1]=[0,6]

    return



# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,700))
#Titulo de la Ventana
pygame.display.set_caption("Prueba")
#Pintamos de blanco la ventana
ventana.fill((255,255,255))
pygame.display.flip()



#Puntos ya generados en el plano que van a estar en movimiento
p=[[int(random.random()*700),int(random.random()*700)] for i in range (9)]

#Vectores de las direcciones en las que se van a mover los puntos
vec=[[int(random.random()*10),int(random.random()*10)] for i in range (9)]
#Parametro para que no haya problema de superposicion de puntos
l=1





#Bucle del juego

while True:

    for event in pygame.event.get():    #Cuando ocurre un evento...
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton que va hasta el punto (700,700)

                raton = pygame.mouse.get_pos()

                if raton in p:
                    raton=(raton[0]+l,raton[1]+l)
                    l=l*(-1)
                p.append(raton)
                vec.append([0,0])

                pintar()


        #elif event.type == pygame.KEYDOWN:
            # # gets the key name
            # key_name = pygame.key.name(event.key)
            # # converts to uppercase the key name
            # key_name = key_name.upper()



                # if (event.key == K_LEFT):
                #     print("1")
                #     vec[len(p)-1]=[-5,0]
                # elif (event.key == K_RIGHT):
                #     vec[len(p)-1]=[5,0]
                # elif (event.key == K_UP):
                #      vec[len(p)-1]=[0,-5]
                # elif (event.key == K_DOWN):
                #      vec[len(p)-1]=[0,5]

    teclas()
    for k in range (len(p)):
        (p[k],vec[k])=movimiento(p[k],vec[k],k)
    pintar()

        #continue
            # if  key_name=="UP":
            #     vec[len(p)-1]=[0,-5]
            # elif key_name=="DOWN":
            #      vec[len(p)-1]=[0,5]
            # elif key_name=="RIGHT":
            #     vec[len(p)-1]=[5,0]
            # elif key_name=="LEFT":
            #     vec[len(p)-1]=[-5,0]
            # for k in range (len(p)):
            #     (p[k],vec[k])=movimiento(p[k],vec[k])
            # pintar()
