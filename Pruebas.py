import pygame
from pygame.locals import *
from auxiliar import *
#from Voronoi import *
import math
from itertools import combinations




def dist(A,B):
     return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)

def movimiento():
    global p,vec
    #Primero movemos puntos
    for j in range(len(p)):
        #Si el punto llega al borde debe rebotar
         if p[j][0]>700:
            vec[j]=[-vec[j][0],vec[j][1]]
         elif p[j][0]<0:
            vec[j]=[-vec[j][0],vec[j][1]]
         elif p[j][1]<0:
            vec[j]=[vec[j][0],-vec[j][1]]
         elif p[j][1]>700:
            vec[j]=[vec[j][0],-vec[j][1]]
         #Se mueve el punto sumandole el vector
         p[j]=[p[j][0]+vec[j][0],p[j][1]+vec[j][1]]
    #Segundo ,tratamos colisiones
    colision=[]

    comb=combinations([i for i in range(len(p))],2)
    for c in comb:
        if dist(p[c[1]],p[c[0]])<18:
            colision.append([c[1],c[0]])
        continue
    for [v1,v2] in colision:
        #Tratar las colisiones
        #EL rebote se hace intercambiando los vectores velocidad de cada uno
        aux=vec[v1]
        vec[v1]=vec[v2]
        vec[v2]=aux

    return

#Funcion para pintar en pantalla los diagramas despues de cada interaccion con el usuario
def pintar():
    #En primer lugar se encarga de calcular la triangulacion y la division del plano en las regiones
    global p,Area2,Area1
    if len(p)<3:
        Area1=0
        Area2=0
        V=[]
        for k in range(len(p)):

                V.append(voronoiRegion(p,k))
                if k%2:
                    pygame.draw.polygon(ventana,(0,0,250),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    pygame.draw.circle(ventana,(143,143,143),[int(p[k][0]),int(p[k][1])],9)
                    pygame.draw.circle(ventana,(0,0,0),[int(p[k][0]),int(p[k][1])],4)
                    Area1=Area(V[k])+Area1
                else :
                    pygame.draw.polygon(ventana,(250,0,0),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    pygame.draw.circle(ventana,(143,143,143),[int(p[k][0]),int(p[k][1])],9)
                    pygame.draw.circle(ventana,(0,0,0),[int(p[k][0]),int(p[k][1])],4)
                    Area2=Area(V[k])+Area2
        Poner_marcador()
        pygame.display.update()
        return

    else :
        D=Delaunay(p)
        V=Voronoi(D)
        Area1=0
        Area2=0

    for v in range (len(V)-1):
                    if v%2:
                        if len(V[v])>2:
                            pygame.draw.polygon(ventana,(0,0,250),V[v])
                            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(143,143,143),[int(p[v][0]),int(p[v][1])],9)
                        pygame.draw.circle(ventana,(0,0,0),[int(p[v][0]),int(p[v][1])],4)
                        Area1=Area(V[v])+Area1


                    else:
                        if len(V[v])>2:
                            pygame.draw.polygon(ventana,(250,0,0),V[v])
                            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(143,143,143),[int(p[v][0]),int(p[v][1])],9)
                        pygame.draw.circle(ventana,(0,0,0),[int(p[v][0]),int(p[v][1])],4)
                        Area2=Area(V[v])+Area2


                    if len(V[len(p)-1])>2:
                        if (len(p)-1)%2:
                            pygame.draw.polygon(ventana,(210, 210, 250),V[len(p)-1])

                        else :
                            pygame.draw.polygon(ventana,(255, 160, 122),V[len(p)-1])



                        pygame.draw.polygon(ventana,(0,0,0),V[len(p)-1],2)
                    pygame.draw.circle(ventana,(143,143,143),[int(p[len(p)-1][0]),int(p[len(p)-1][1])],9)
                    pygame.draw.circle(ventana,(0,0,0),[int(p[len(p)-1][0]),int(p[len(p)-1][1])],4)
                    #Se le debe sumar al rojo
    if (len(p)-1)%2:
         Area1=Area(V[len(p)-1])+Area1
    else:
        Area2=Area(V[len(p)-1])+Area2




    Poner_marcador()
    pygame.display.update()
    return



#Sacado del video : https://www.youtube.com/watch?v=i6xMBig-pP4
def teclas():
    global vec
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        #vec[len(p)-1]=[-6,0]
        vec[len(p)-1]=[vec[len(p)-1][0]-1,vec[len(p)-1][1]]
        #Despues de mover el punto normalizamos la velocidad
        norma=math.sqrt((vec[len(p)-1][0])**2+(vec[len(p)-1][1])**2)
        if norma==0:
            norma=1
        vec[len(p)-1]=[  ((vec[len(p)-1][0])/norma ) ,((vec[len(p)-1][1])/norma ) ]



    if keys[pygame.K_RIGHT]:
        #vec[len(p)-1]=[6,0]
        vec[len(p)-1]=[vec[len(p)-1][0]+1,vec[len(p)-1][1]]
        #Despues de mover el punto normalizamos la velocidad
        norma=math.sqrt((vec[len(p)-1][0])**2+(vec[len(p)-1][1])**2)
        if norma==0:
            norma=1
        vec[len(p)-1]=[  ((vec[len(p)-1][0])/norma ) , ((vec[len(p)-1][1])/norma ) ]

    if keys[pygame.K_UP]:
        #vec[len(p)-1]=[0,-6]
        vec[len(p)-1]=[vec[len(p)-1][0],vec[len(p)-1][1]-2]
        #Despues de mover el punto normalizamos la velocidad
        norma=math.sqrt((vec[len(p)-1][0])**2+(vec[len(p)-1][1])**2)
        if norma==0:
            norma=1


        vec[len(p)-1]=[  ((vec[len(p)-1][0])/norma ) , ((vec[len(p)-1][1])/norma ) ]

    if keys[pygame.K_DOWN]:
        #vec[len(p)-1]=[0,6]
        vec[len(p)-1]=[vec[len(p)-1][0],vec[len(p)-1][1]+1]
        #Despues de mover el punto normalizamos la velocidad
        norma=math.sqrt((vec[len(p)-1][0])**2+(vec[len(p)-1][1])**2)
        if norma==0:
            norma=1
        vec[len(p)-1]=[  ((vec[len(p)-1][0])/norma ) , ((vec[len(p)-1][1])/norma ) ]



    return


def Poner_marcador():
    global Area1,Area2
    pygame.draw.rect(ventana, (250,250,250),marcador)
    Area1=(Area1/area)*100
    #print(Area1)
    #print(Area2)
    Area2=(Area2/area)*100
    tArea1=font.render(str(int(Area1))+"%", True, (0, 0, 250))
    tArea2=font.render(str(int(Area2))+"%", True, (250, 0, 0))
    ventana.blit(tArea1, (15, 750))
    ventana.blit(tArea2, (350, 750))
    ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))
    pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
    #pygame.display.update()
    return

def juego():
    global p,vec,l
    #Los primeros cuatro puntos hay que pedirlos y calcular Voronoi haciendo clipping
    raton = pygame.mouse.get_pos()
    if return_rect.collidepoint(raton):
        #import Juego
        V=[]
        p=[]
        Area1=0
        Area2=0
        exec(open('Juego.py').read())
    if raton[1]>700:
        return

        # #LIMITA EL NUMERO DE PUNTOS QUE SE PUEDEN INSERTAR
    if len(p)<200:
        if raton in p:
            raton=(raton[0]+l,raton[1]+l)
            l=l*(-1)
        p.append(raton)
        vec.append([0,0])
        pintar()
    return



# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,800))

marcador=pygame.Rect(0,700,700,100)
#podemos ponerle titulo a nuestra ventana, entre otras cosas,
#icono, que sea redimensionable...
pygame.display.set_caption("TFG")
ventana.fill((255,255,255))


pygame.draw.rect(ventana, (250,250,250),marcador)


font = pygame.font.Font('freesansbold.ttf', 18)


return_cadena=font.render('return', True, (0, 0, 0))
return_rect=pygame.Rect(580,740,100,50)
pygame.draw.rect(ventana,(255, 255, 255),return_rect)
pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))

pygame.display.flip()

#Puntos ya generados en el plano que van a estar en movimiento
#p=[[int(random.random()*700),int(random.random()*700)] for i in range (9)]
p=[]
vec=[]
Area1=0
Area2=0
area=700*700
#Vectores de las direcciones en las que se van a mover los puntos
#vec=[[int(random.random()*10),int(random.random()*10)] for i in range (9)]

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
                juego()
    teclas()
    movimiento()
    pintar()


