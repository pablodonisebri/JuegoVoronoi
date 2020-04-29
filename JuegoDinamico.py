import pygame,sys,random,math
import scipy.spatial
from scipy.spatial import Delaunay
from auxiliar import Voronoi
from itertools import combinations
#from random import random
from auxiliar import Area
import threading

pygame.init()


puntos=[[int(random.random()*700),int(random.random()*700)]for i in range(20)]
velocidad=[[random.uniform(-1,1),random.uniform(-1,1)]for i in range(20)]
#normalizamos la velocidad
velocidad=[[2*(velocidad[v][0]/(math.sqrt((velocidad[v][0])**2+(velocidad[v][1])**2))),2*(velocidad[v][1]/(math.sqrt((velocidad[v][0])**2+(velocidad[v][1])**2)))]for v in range(len(velocidad))]
usuario=False
PAUSA=True
areaTotal=700*700
Area1=0


# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,800))
marcador=pygame.Rect(0,700,700,100)
#podemos ponerle titulo a nuestra ventana, entre otras cosas,
#icono, que sea redimensionable...
pygame.display.set_caption("Juego de Voronoi")
ventana.fill((255,255,255))
pygame.draw.rect(ventana, (250,250,250),marcador)
font = pygame.font.Font('freesansbold.ttf', 18)
return_cadena=font.render('return', True, (0, 0, 0))
return_rect=pygame.Rect(580,740,100,50)
pygame.draw.rect(ventana,(255, 255, 255),return_rect)
pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))


pygame.display.flip()


def temporizador():
    global PAUSA
    PAUSA=True
def dist(A,B):
     return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)

def movimiento():
    global velocidad,puntos,PAUSA
    if not PAUSA:

        for p in range (len(puntos)):

            #Si el punto llega al borde debe rebotar
             if puntos[p][0]>700:
                velocidad[p]=[-velocidad[p][0],velocidad[p][1]]
             elif puntos[p][0]<0:
                velocidad[p]=[-velocidad[p][0],velocidad[p][1]]

             elif puntos[p][1]<0:
               velocidad[p]=[velocidad[p][0],-velocidad[p][1]]
             elif puntos[p][1]>700:
                velocidad[p]=[velocidad[p][0],-velocidad[p][1]]
             #Se mueve el punto sumandole el vector
             puntos[p]=[puntos[p][0]+velocidad[p][0],puntos[p][1]+velocidad[p][1]]

    #Segundo ,tratamos colisiones
        colision=[]

        comb=combinations([i for i in range(len(puntos))],2)
        for c in comb:
            if dist(puntos[c[1]],puntos[c[0]])<15:
                colision.append([c[1],c[0]])
            continue
        for [v1,v2] in colision:
            #Tratar las colisiones
            #EL rebote se hace intercambiando los vectores velocidad de cada uno
            aux=velocidad[v1]
            velocidad[v1]=velocidad[v2]
            velocidad[v2]=aux
    pintar()
    return

def pintar():
    global puntos,Area1
    D=Delaunay(puntos)
    V=Voronoi(D)
    if not usuario:
        for p in range(len(puntos)):
            pygame.draw.polygon(ventana,(100,100,100),V[p])
            pygame.draw.polygon(ventana,(0,0,0),V[p],2)
            pygame.draw.circle(ventana,(180,180,180),[int(puntos[p][0]),int(puntos[p][1])],9)
            pygame.draw.circle(ventana,(0,0,0),[int(puntos[p][0]),int(puntos[p][1])],4)
    else:
        for p in range(len(puntos)-1):
            pygame.draw.polygon(ventana,(100,100,100),V[p])
            pygame.draw.polygon(ventana,(0,0,0),V[p],2)
            pygame.draw.circle(ventana,(180,180,180),[int(puntos[p][0]),int(puntos[p][1])],9)
            pygame.draw.circle(ventana,(0,0,0),[int(puntos[p][0]),int(puntos[p][1])],4)
        pygame.draw.polygon(ventana,(180,0,0),V[len(puntos)-1])
        pygame.draw.polygon(ventana,(0,0,0),V[len(puntos)-1],2)
        pygame.draw.circle(ventana,(180,180,180),[int(puntos[len(puntos)-1][0]),int(puntos[len(puntos)-1][1])],9)
        pygame.draw.circle(ventana,(0,0,0),[int(puntos[len(puntos)-1][0]),int(puntos[len(puntos)-1][1])],4)
        Area1=Area(V[len(puntos)-1])
    poner_marcador()
    pygame.display.update()

    return


def poner_marcador():
    global areaTotal,Area1
    Area1=(Area1/areaTotal)*100
    pygame.draw.rect(ventana, (250,250,250),marcador)
    tArea1=font.render(str(int(Area1))+"%", True, (0, 0, 0))
    ventana.blit(tArea1, (15, 750))
    pygame.draw.rect(ventana,(255, 255, 255),return_rect)
    pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
    ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))


    return



def teclas():
    global puntos,velocidad,PAUSA

    keys=pygame.key.get_pressed()
    #Al pulsar barra de space se pausa el juego
    if keys[pygame.K_SPACE] and not PAUSA:
        PAUSA=True
        my_timer.cancel()
        return
    # if keys[pygame.K_SPACE] and  PAUSA:
    #     PAUSA=False
    if PAUSA:
        return
    if keys[pygame.K_LEFT]:
        velocidad[len(puntos)-1]=[velocidad[len(puntos)-1][0]-2,velocidad[len(puntos)-1][1]]
        #Despues de mover el punto normalizamos la velocidad
        norma=math.sqrt((velocidad[len(puntos)-1][0])**2+(velocidad[len(puntos)-1][1])**2)
        if norma==0:
            norma=1
        velocidad[len(puntos)-1]=[ 2*((velocidad[len(puntos)-1][0])/norma ) ,2*((velocidad[len(puntos)-1][1])/norma ) ]

    if keys[pygame.K_RIGHT]:
        velocidad[len(puntos)-1]=[velocidad[len(puntos)-1][0]+2,velocidad[len(puntos)-1][1]]
        #Despues de mover el punto normalizamos la velocidad
        norma=math.sqrt((velocidad[len(puntos)-1][0])**2+(velocidad[len(puntos)-1][1])**2)
        if norma==0:
            norma=1
        velocidad[len(puntos)-1]=[2*((velocidad[len(puntos)-1][0])/norma ) , 2*((velocidad[len(puntos)-1][1])/norma ) ]

    if keys[pygame.K_UP]:
        velocidad[len(puntos)-1]=[velocidad[len(puntos)-1][0],velocidad[len(puntos)-1][1]-2]
        #Despues de mover el punto normalizamos la velocidad
        norma=math.sqrt((velocidad[len(puntos)-1][0])**2+(velocidad[len(puntos)-1][1])**2)
        if norma==0:
            norma=1
        velocidad[len(puntos)-1]=[2* ((velocidad[len(puntos)-1][0])/norma ) ,2*((velocidad[len(puntos)-1][1])/norma ) ]

    if keys[pygame.K_DOWN]:
        velocidad[len(puntos)-1]=[velocidad[len(puntos)-1][0],velocidad[len(puntos)-1][1]+2]
        #Despues de mover el punto normalizamos la velocidad
        norma=math.sqrt((velocidad[len(puntos)-1][0])**2+(velocidad[len(puntos)-1][1])**2)
        if norma==0:
            norma=1
        velocidad[len(puntos)-1]=[2*((velocidad[len(puntos)-1][0])/norma ) , 2*((velocidad[len(puntos)-1][1])/norma ) ]

    return


my_timer=threading.Timer(30.0, temporizador)

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        elif event.type == pygame.MOUSEBUTTONDOWN:
            raton=pygame.mouse.get_pos()
            #Obtenemos la posicion del raton que va hasta el punto (700,700)
            if  return_rect.collidepoint(raton):

                exec(open('Juego.py').read())

            if len(puntos)<21:

                usuario=True
                #Cuando usuario añade punto los puntos aleatorios se comienzan a mover
                PAUSA=False
                my_timer.start()


                if raton in puntos:
                     puntos.append([raton[0]+1,raton[1]-1])

                else:puntos.append(raton)

                velocidad.append([0,0])
            continue



    teclas()
    movimiento()





