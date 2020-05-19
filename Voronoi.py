import pygame
import random
import scipy.spatial as sp
from scipy.spatial import Delaunay
import sys
import numpy
from auxiliar import *
from auxiliar import Voronoi


# #Inicializamos pygame
pygame.init()
#############################################COMINENZO PROGRAMA####################################################

#Lista de puntos que van a ir introduciendo los usuarios por turnod
p=[]
#Parametro utilizado para manejar el caso en el que se pinche varias veces sobre el mismo punto
#Asi poder mover de manera impercetible
l=1
#V=[]
#Area de las regiones asociadas al primer jugador
Area1=0
#Area de las regiones asociadas al segundo jugador
Area2=0
#Area total del tablero, es para poder calcular los porcentajes
area=700*700
#numero maximo de puntos que pone cada jugador
maximo=0

#Funcion encargada de mostrar en la pantalla los marcadores durante la partida
def Poner_marcador():
    global Area1,Area2
    #Se crea el rectangulo que servirá de marcador
    pygame.draw.rect(ventana, (250,250,250),marcador)
    #Se calcula el porcentaje que representa AREA1
    Area1=(Area1/area)*100
    #Se calcula el porcentaje que representa AREA2
    Area2=(Area2/area)*100
    tArea1=font.render(str(Area1)+"%", True, (0, 0, 250))
    tArea2=font.render(str(Area2)+"%", True, (250, 0, 0))
    n_puntos=font.render(str(len(p))+" puntos", True, (0, 0, 250))
    #Se muestra en el marcador el numero de puntos que hay en juego ahora mismo asi como los porcentajes de areas
    ventana.blit(n_puntos,(580,710))
    ventana.blit(tArea1, (15, 750))
    ventana.blit(tArea2, (350, 750))
    #Boton de return
    ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))
    pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
    #Se actualiza lo que se muestra por pantalla
    pygame.display.update()
    return


#Funciom encargada del desarrollo del juego durante la partida
def juego():
    global p,V,i,l,Area1,Area2,area,maximo
    #Se obtiene la posicion donde se ha hecho click
    raton = pygame.mouse.get_pos()
    #Si se selecciona el boton de return se debe volver al menu
    if return_rect.collidepoint(raton):
        exec(open('Juego.py').read())

    #Si el raton sale del tablero no debe ocurrir nada
    if raton[1]>700:
        return
    #Para cuando hay menos de 3 puntos no se puede obtener la triangulacion
    if len(p)<3:
        V=[]
        Area1=0
        Area2=0

        #Si se selecciona la posicion ya ocupada por otro punto se hace un pequeño desplazamiento inapreciable y se añade el punto
        if raton in p:
            p.append((raton[0]+l,raton[1]+l))
            l=l*(-1)
        #Se añade el punto
        else:
            p.append(raton)

        #Se calcula la region asociada al punto como interseccion de semiplanos
        for k in range(len(p)):
                #Se hace uso de la funcion VoronoiRegion
                V.append(voronoiRegion(p,k))
                #Los puntos con indice par son del primer jugador
                if k%2:
                    pygame.draw.polygon(ventana,(0,0,250),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    #Se pinta el punto
                    pygame.draw.circle(ventana,(0,0,0),p[k],5)
                    #Se calcula el area asociada al punto y se suma al area total de ese jugador
                    Area1=Area(V[k])+Area1
                #Los puntos con indice  impar son del primer jugador
                else :
                    pygame.draw.polygon(ventana,(250,0,0),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    #Se pinta el punto
                    pygame.draw.circle(ventana,(0,0,0),p[k],5)
                    #Se calcula el area
                    Area2=Area(V[k])+Area2
        #Se muestra el marcador
        Poner_marcador()
        return
    #Caso para cuando hay mas de 4 puntos en el tablero, ya se pueden obtener las regiones mediante la triangulacion
    #Limitado el numero de puntos maximo que puede poner cada jugador
    if len(p)<2*maximo:
        #Si se intenta hacer click sobre un punto ya existente se hace un ligero e inapreciable desplazamiento
        if raton in p:
                p.append((raton[0]+l,raton[1]-l))
                l=l*(-1)
        #Se añade el punto
        else:
            p.append(raton)
        #Se calcula la triangulacion del conjunto de puntos
        D=Delaunay(p)
        #Se obtiene el diagrama de Voronoi a partir de la triangulacion
        V=Voronoi(D)
        Area1=0
        Area2=0
        #Se pintan los puntos, las regiones y se calcula el area asociada a cada region
        for v in range (len(p)):
            #Regiones de indice par son las asociadas a los puntos del primer jugador
            if v%2:
                pygame.draw.polygon(ventana,(0,0,250),V[v])
                pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                #Se pintan los puntos
                pygame.draw.circle(ventana,(0,0,0),p[v],5)
                Area1=Area(V[v])+Area1
            #Regiones de indice impar son las asociadas a los puntos del segundo jugador
            else:
                pygame.draw.polygon(ventana,(250,0,0),V[v])
                pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                #Se pintan los puntos
                pygame.draw.circle(ventana,(0,0,0),p[v],5)
                Area2=Area(V[v])+Area2
        #Se muestra el marcador
        Poner_marcador()
    return



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




#Botones para el numero maximo de puntos en la partida
cinco_rect=pygame.Rect(200,100,300,100)
quince_rect=pygame.Rect(200,500,300,100)
diez_rect= pygame.Rect(200,300,300,100)


#Se muestran los botones en la pantalla
pygame.draw.rect(ventana, (72, 209, 204),cinco_rect)
pygame.draw.rect(ventana, (72, 209, 204),diez_rect)
pygame.draw.rect(ventana, (72, 209, 204),quince_rect)

font2 = pygame.font.Font('freesansbold.ttf', 20)

#Texto para los botones de la seleccion de los puntos
puntos_cadena=font.render('Escoge el número de puntos máximo por jugador', True, (0, 0, 0))
cinco_cadena=font2.render('5 puntos ', True, (0, 0, 0))
diez_cadena=font2.render('10 puntos', True, (0, 0, 0))
quince_cadena=font2.render('15 puntos', True, (0, 0, 0))


#Se muestran los botones en la pantalla
ventana.blit(quince_cadena, (quince_rect.centerx-80, quince_rect.centery-10))
ventana.blit(diez_cadena, (diez_rect.centerx-80, diez_rect.centery-10))
ventana.blit(cinco_cadena, (cinco_rect.centerx-80, cinco_rect.centery-10))
ventana.blit(puntos_cadena, (cinco_rect.centerx-200, cinco_rect.centery-100))


pygame.display.flip()

#Bucle de seleccion
while True:
    for event in pygame.event.get():    #Cuando ocurre un evento...
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton que va hasta el punto (700,700)
            raton=pygame.mouse.get_pos()
            if cinco_rect.collidepoint(raton):
                maximo=5
            elif diez_rect.collidepoint(raton):
                maximo=10
            elif quince_rect.collidepoint(raton):
                maximo=15

            elif return_rect.collidepoint(raton):
                exec(open('Juego.py').read())

            break
    #Cuando ya se ha seleccionado se pasa al juego
    if maximo!=0:
        break
#Una vez hecha la seleccion se muestra el tablero en blanco para que los jugadores
ventana.fill((255,255,255))
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
            


