import pygame
from pygame.locals import *
from auxiliar import *
#from Voronoi import *
import math


def dist(A,B):
     return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)


def colision(punto,vector,k):
    global p,vec

    for i in range(len(p)):
        if i!=k and dist(punto,p[i])<20:
            #Aqui se debe producir el rebote
            return [-vector[0],-vector[1]]

    return vector



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
    if [p[0]+v[0],p[1]+v[1]] in p:
        return ([p[0]+v[0]+2+int(random.random()*10),p[1]+v[1]-6],[v[0]+1,v[1]+1])
    if ([p[0]+v[0],p[1]+v[1]],v) in p: return ([p[0]+v[0]+1,p[1]+v[1]-1],v)
    return ([p[0]+v[0],p[1]+v[1]],v)







#Funcion para pintar en pantalla los diagramas despues de cada interaccion con el usuario
def pintar():
    #En primer lugar se encarga de calcular la triangulacion y la division del plano en las regiones
    global p
    D=Delaunay(p)
    V=Voronoi(D)

    for v in range (len(V)-1):
                    if v%2:
                        if len(V[v])>2:
                            pygame.draw.polygon(ventana,(0,0,250),V[v])
                            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(143,143,143),p[v],9)
                        pygame.draw.circle(ventana,(0,0,0),p[v],4)


                    else:
                        if len(V[v])>2:
                            pygame.draw.polygon(ventana,(250,0,0),V[v])
                            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(143,143,143),p[v],9)
                        pygame.draw.circle(ventana,(0,0,0),p[v],4)

                    if len(V[len(p)-1])>2:

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

#Los puntos y los vectores deben de ser numeros enteros para que no haya problema, ya que la pantalla es
#una matriz de numeros enteros

#Parametro para que no haya problema de superposicion de puntos
l=1




#Bucle del juego (Se encarga sobretodo de la interacción con el usuario)

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

                #LIMITA EL NUMERO DE PUNTOS QUE SE PUEDEN INSERTAR
                if len(p)<20:p.append(raton)
                vec.append([0,0])

                pintar()

    teclas()

    for k in range (len(p)):
        (p[k],vec[k])=movimiento(p[k],vec[k],k)

    pintar()


