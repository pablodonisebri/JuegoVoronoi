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
V=[]
Area1=0
Area2=0
Area=700*700
#Definimos i que sera para ver cuando el numero de puntos es menor que 4, se usa en la funcion juego
i=0



def Poner_marcador():
    global Area1,Area2
    pygame.draw.rect(ventana, (250,250,250),marcador)
    Area1=(Area1/Area)*100
    # print(Area1)
    # print(Area2)
    Area2=(Area2/Area)*100
    tArea1=font.render(str(Area1)+"%", True, (0, 0, 250))
    tArea2=font.render(str(Area2)+"%", True, (250, 0, 0))
    ventana.blit(tArea1, (15, 750))
    ventana.blit(tArea2, (350, 750))
    ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))
    pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)

    pygame.display.update()
    return



def juego():

    global p,V,i,l,Area1,Area2,Area
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

    if i<3:
        V=[]
        Area1=0
        Area2=0
        i=i+1

        if raton in p:
            p.append((raton[0]+l,raton[1]+l))
            l=l*(-1)

        else:
            p.append(raton)

        print(len(p))
        for k in range(len(p)):

                V.append(aux.voronoiRegion(p,k))
                if k%2:
                    pygame.draw.polygon(ventana,(0,0,250),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    Area1=aux.Area(V[k])+Area1
                else :
                    pygame.draw.polygon(ventana,(250,0,0),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    Area2=aux.Area(V[k])+Area2
        for po in p:
            pygame.draw.circle(ventana,(0,0,0),po,5)

        Poner_marcador()
        return

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

    for po in p:
        pygame.draw.circle(ventana,(0,0,0),po,5)

    Poner_marcador()
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
            


