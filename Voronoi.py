import pygame
import random
import scipy.spatial as sp
from scipy.spatial import Delaunay
import sys
import numpy
import auxiliar as aux
from auxiliar import Voronoi


#############################################COMINENZO PROGRAMA####################################################


p=[]
l=1

def juego():
    global i,l
    if i<3:
        i=i+1
        raton = pygame.mouse.get_pos()
        if raton in p:
            p.append((raton[0]+l,raton[1]-l))
            l=l*(-1)
        else:
            p.append(raton)
        for po in p:
            pygame.draw.circle(ventana,(0,0,0),po,5)
        return

    raton = pygame.mouse.get_pos()
    if raton in p:
            p.append((raton[0]+l,raton[1]-l))
            l=l*(-1)
    else:
        p.append(raton)

    D=Delaunay(p)
    #D=Delaunay(p,qhull_options="Qc")
    V=Voronoi(D)
    Area1=0
    Area2=0

    for v in range (len(p)):
        if v%2:
            pygame.draw.polygon(ventana,(0,0,250),V[v])
            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
            Area1=aux.Area(V[v])+Area1

        else:
            pygame.draw.polygon(ventana,(250,0,0),V[v])
            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
            Area2=aux.Area(V[v])+Area2
    # print(p)
    # print(Area1)
    # print(Area2)

    for po in p:
        print(po)
        pygame.draw.circle(ventana,(0,0,0) ,po , int(5))


    return




# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,700))
#podemos ponerle titulo a nuestra ventana, entre otras cosas,
#icono, que sea redimensionable...
pygame.display.set_caption("TFG")
ventana.fill((255,255,255))


V=[]
Area1=0
Area2=0
#Definimos i que sera para ver cuando el numero de puntos es menor que 4, se usa en la funcion juego
i=0
#Pedimos los primeros puntos



#Bucle de "Juego"
while True:



    for event in pygame.event.get():    #Cuando ocurre un evento...
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton que va hasta el punto (700,700)
            juego()
            pygame.display.flip()
            

        else:

            print("")


   # pygame.display.flip()               #Genera la ventana





#
