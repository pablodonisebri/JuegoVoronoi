import pygame
from pygame.locals import *
from auxiliar import *
import math
import itertools
#from itertools import combinations



# #Inicializamos pygame
pygame.init()




#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,800))
#Rectangulo que representara el marcador
marcador=pygame.Rect(0,700,700,100)
#Titulo de la ventana
pygame.display.set_caption("Juego de Voronoi")
#Se pinta el fondo de la ventana  de blanco
ventana.fill((255,255,255))

#Se pone el marcador en la ventana
pygame.draw.rect(ventana, (250,250,250),marcador)

#Fuente de los textos que se van a mostrar
font = pygame.font.Font('freesansbold.ttf', 18)

#Boton de return
return_cadena=font.render('return', True, (0, 0, 0))
return_rect=pygame.Rect(580,740,100,50)
pygame.draw.rect(ventana,(255, 255, 255),return_rect)
pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))

#Se actualiza lo que se muestra por pantalla
pygame.display.flip()

#Vector de puntos que los jugaodres pondran por turnos en el tablero
p=[]
#Vectores de velocidad de los puntos, estos vectores deben estar normalizados para que todos vayan igual de rapidos
vec=[]
#Area del primer jugador
Area1=0
#Area del segundo jugador
Area2=0
#Area total del tablero que se necesita para calcular los porcentajes, se calcula como la suma de Area1 mas Area2
area=0
#Parametro para que no haya problema de superposicion de puntos, el que determinara el pequeño desplazamiento
l=1

#Modulo de la velocidad de los puntos, determina si es lento, medio o rapido
velocidad=0

#booelano que muestra el estado del movimiento de los puntos en la partida (algo asi como el interruptor general)
PAUSA=False

#Contador de segundos
segundos=0

#Botones de seleccion de la velocidad de los puntos
lento_rect=pygame.Rect(200,100,300,100)
rapido_rect=pygame.Rect(200,500,300,100)
medio_rect= pygame.Rect(200,300,300,100)

#Se muestran los botones en la pantalla
pygame.draw.rect(ventana, (72, 209, 204),lento_rect)
pygame.draw.rect(ventana, (72, 209, 204),medio_rect)
pygame.draw.rect(ventana, (72, 209, 204),rapido_rect)

font2 = pygame.font.Font('freesansbold.ttf', 20)

#Texto de los botones de seleccion
puntos_cadena=font.render('Escoge la velocidad del movimiento de los puntos', True, (0, 0, 0))
lento_cadena=font2.render('Lenta ', True, (0, 0, 0))
medio_cadena=font2.render('Media', True, (0, 0, 0))
rapido_cadena=font2.render('Rápida', True, (0, 0, 0))

#Se añade el texto a los botones
ventana.blit(rapido_cadena, (rapido_rect.centerx-80, rapido_rect.centery-10))
ventana.blit(medio_cadena, (medio_rect.centerx-80, medio_rect.centery-10))
ventana.blit(lento_cadena, (lento_rect.centerx-80, lento_rect.centery-10))
ventana.blit(puntos_cadena, (lento_rect.centerx-200, lento_rect.centery-100))

#Se actualiza lo que se muestra por pantalla
pygame.display.flip()



#Distancia euclidea de dos puntos en el plano
def dist(A,B):
     return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)

#Funcion que maneja el movimiento de los puntos por el plano
def movimiento():
    global p,vec,PAUSA
    #Primero movemos puntos

    if not PAUSA:
        for j in range(len(p)):
            #Si el punto llega al borde debe rebotar, se le cambia de signo la coordenada del vector en funcion de
            #si rebota con borde superior o inferior (cambia coordenada y) o borde izqdo o dcho (cambia coordenada x)
             if p[j][0]>700:
                vec[j]=[-vec[j][0],vec[j][1]]
             elif p[j][0]<0:
                vec[j]=[-vec[j][0],vec[j][1]]
             elif p[j][1]<0:
                vec[j]=[vec[j][0],-vec[j][1]]
             elif p[j][1]>700:
                vec[j]=[vec[j][0],-vec[j][1]]
             #Se mueve el punto sumandole el vector velocidad
             p[j]=[p[j][0]+vec[j][0],p[j][1]+vec[j][1]]

        #Segundo ,tratamos colisiones
        #Se crea lista de colisiones pendientes para tratar en esta unidad temporal
        colision=[]
        #Toda la lista de combinaciones de indices que pueden colisionar, con combinaciones no revisamos todos los indices como
        # si lo hicieramos en un bucle doble, asi nos ahorramos repeticiones
        comb=itertools.combinations(list(range(len(p))),2)

        for c in comb:
            #Se comprueba si la distancia a los demas puntos es menor que la establecida como minima para una colision
            if dist(p[c[1]],p[c[0]])<18:
                aux=vec[c[0]]
                vec[c[0]]=vec[c[1]]
                vec[c[1]]=aux

            continue
    pintar()
    return

#Funcion para pintar en pantalla los diagramas en cada unidad temporal
def pintar():
    global p,Area2,Area1,PAUSA,area

#En primer lugar se encarga de calcular la triangulacion y la division del plano en las regiones
    #Si hay menos de tres puntos no se puede hacer uso de la triangulacion y se debe hacer por interseccion de semiplanos
    if len(p)<3:
        Area1=0
        Area2=0
        V=[]
        #Para cada punto se calcula su region por interseccion de semiplanos
        for k in range(len(p)):
                #Llamada a la funcion que calcula la region del punto
                V.append(voronoiRegion(p,k))
                #Los puntos pares son los asociados al primer jugador, se pinta su region, el punto y se calcula el area
                if k%2:
                    #Pintar region
                    pygame.draw.polygon(ventana,(0,0,250),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    #Pintar punto
                    pygame.draw.circle(ventana,(143,143,143),[int(p[k][0]),int(p[k][1])],9)
                    pygame.draw.circle(ventana,(0,0,0),[int(p[k][0]),int(p[k][1])],4)
                    #Calcular area
                    Area1=Area(V[k])+Area1
                #Los puntos con indice impar son los asociados al segundo jugador, se pinta su region y se calcula el area
                else :
                    #Pintar region
                    pygame.draw.polygon(ventana,(250,0,0),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    #Pintar punto
                    pygame.draw.circle(ventana,(143,143,143),[int(p[k][0]),int(p[k][1])],9)
                    pygame.draw.circle(ventana,(0,0,0),[int(p[k][0]),int(p[k][1])],4)
                    #Calcular area
                    Area2=Area(V[k])+Area2
        #Se pone el marcador
        area=Area1+Area2
        Poner_marcador()
        #Se actualiza pantalla
        pygame.display.update()
        return
    #Para cuando hay cuatro puntos o mas ya se puede hacer uso de la triangulacion
    else :
        #Triangulacion de los puntos
        D=Delaunay(p)
        #Diagrama a partir de la triangulacion
        V=Voronoi(D)
        Area1=0
        Area2=0
    #Para cada punto se debe pintar su region y calcular el area
    for v in range (len(V)-1):
                    #Los puntos pares son los asociados al primer jugador, se pinta su region, el punto y se calcula el area
                    if v%2:
                        #Pintar region
                        if len(V[v])>2:
                            pygame.draw.polygon(ventana,(0,0,250),V[v])
                            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        #Pintar punto
                        pygame.draw.circle(ventana,(143,143,143),[int(p[v][0]),int(p[v][1])],9)
                        pygame.draw.circle(ventana,(0,0,0),[int(p[v][0]),int(p[v][1])],4)
                        #Calcular region
                        Area1=Area(V[v])+Area1

                    #Los puntos con indice impar son los asociados al segundo jugador, se pinta su region y se calcula el area
                    else:
                        #Pintar region
                        if len(V[v])>2:
                            pygame.draw.polygon(ventana,(250,0,0),V[v])
                            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        #Pintar punto
                        pygame.draw.circle(ventana,(143,143,143),[int(p[v][0]),int(p[v][1])],9)
                        pygame.draw.circle(ventana,(0,0,0),[int(p[v][0]),int(p[v][1])],4)
                        #Calcular area
                        Area2=Area(V[v])+Area2

     #El ultimo punto es el que puede controlar el jugador, tiene un color mas suave
    if len(V[len(p)-1])>2:
            if (len(p)-1)%2:
                    pygame.draw.polygon(ventana,(210, 160, 250),V[len(p)-1])
                    Area1=Area(V[len(p)-1])+Area1

            else :
                    pygame.draw.polygon(ventana,(255, 160, 122),V[len(p)-1])
                    Area2=Area(V[len(p)-1])+Area2
                    #Contorno de la region en negro
            pygame.draw.polygon(ventana,(0,0,0),V[len(p)-1],2)
            #Se pinta el circulo
            pygame.draw.circle(ventana,(143,143,143),[int(p[len(p)-1][0]),int(p[len(p)-1][1])],9)
            pygame.draw.circle(ventana,(0,0,0),[int(p[len(p)-1][0]),int(p[len(p)-1][1])],4)
    area=Area1+Area2
    #Se pone el marcador
    Poner_marcador()

    #Cuando se pone el ultimo punto debe salir el temporizador
    if len(p)==20:
        temporizador()
    # se actualiza lo que se muestra por pantalla
    pygame.display.update()
    return



#Funcion encargada del movimiento de los puntos a partir de las teclas
def teclas():
    global vec,velocidad,PAUSA
    keys=pygame.key.get_pressed()
    #n=3#Velocidad de los puntos
    if len(p)<1: return
    if PAUSA:return

    #El segundo jugador tiene la opcion de parar el juego antes de que se le acabe el temporizador
    if keys[pygame.K_SPACE] and len(p)==20:
        PAUSA=True
        return
    if keys[pygame.K_LEFT]:
        vec[len(p)-1]=[vec[len(p)-1][0]-1,vec[len(p)-1][1]]

    if keys[pygame.K_RIGHT]:
        vec[len(p)-1]=[vec[len(p)-1][0]+1,vec[len(p)-1][1]]

    if keys[pygame.K_UP]:
        vec[len(p)-1]=[vec[len(p)-1][0],vec[len(p)-1][1]-2]

    if keys[pygame.K_DOWN]:
        vec[len(p)-1]=[vec[len(p)-1][0],vec[len(p)-1][1]+1]

    #Despues de actualizar el vector de la velocidad en funcion de las teclas pulsadas por el jugador
    #Se normaliza el vector velocidad, este tiene el modulo en funcion de la eleccion incial
    norma=math.sqrt((vec[len(p)-1][0])**2+(vec[len(p)-1][1])**2)
    if norma==0:
        norma=1
    vec[len(p)-1]=[velocidad*((vec[len(p)-1][0])/norma ) , velocidad*((vec[len(p)-1][1])/norma ) ]
    return

#Funcion encargada de mostrar el marcador en la pantalla
def Poner_marcador():
    global Area1,Area2,area

    #Se pinta el rectangulo del marcador
    pygame.draw.rect(ventana, (250,250,250),marcador)
    #Se calculan los areas de los jugadores como porcentajes
    if len(p)>0:
        Area1=(Area1/area)*100
        Area2=(Area2/area)*100
        #Texto de las areas
        tArea1=font.render(str(int(Area1))+"%", True, (0, 0, 250))
        tArea2=font.render(str(int(Area2))+"%", True, (250, 0, 0))
        #Se muestran en la pantalla las areas
        ventana.blit(tArea1, (15, 750))
        ventana.blit(tArea2, (350, 750))
    #Boton return
    ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))
    #Numero de puntos que hay en juego ahora mismo en el tablero
    pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
    n_puntos=font.render(str(len(p))+" puntos", True, (0, 0, 250))
    ventana.blit(n_puntos,(580,710))

    return


#Funcion encargada del posicionamiento de los puntos en el tablero por parte de los jugadores
def juego():
    global p,vec,l,PAUSA,segundos
    #Se obtiene la posicion en la que ha pulsado el raton
    raton = pygame.mouse.get_pos()
    #Si pulsa return debe volver al menu
    if return_rect.collidepoint(raton):
        segundos=0

        exec(open('Juego.py').read())
    # Si el juego esta pausado no debe poder hacer nada mas que pulsar return
    if PAUSA:return
    #Si hace click fuera del tablero no debe ocurrir nada
    if raton[1]>700:
        return

    # Se lIMITA EL NUMERO DE PUNTOS QUE SE PUEDEN INSERTAR
    #Ahora le he puesto un máximo de 10 puntos por jugador
    if len(p)<20:
        #Pequeño desplazamiento inperceptible si se pulsa sobre un punto ya puesto
        if raton in p:
            raton=(raton[0]+l,raton[1]+l)
            l=l*(-1)
        #Se añade la posicion marcada a la lista de puntos
        p.append(raton)
        #Al colocar un punto en el tablero este no tiene velocidad
        vec.append([0,0])
        #Se pinta el tablero
        pintar()
        #Cuando se pone el ultimo punto se le dan al jugador 10 segundos para mover el punto
        if len(p)==20:
            pygame.time.set_timer(pygame.USEREVENT,1000)


    return

#Funcion que hace tick al reloj
def tick():
    global segundos
    segundos=segundos+1

#Funcion encargada del temporizador cuando se ha colocado el ultimo punto sobre el tablero
def temporizador():
    global PAUSA,segundos

    if PAUSA: return
    #Si vence  el temporizador debe pararse el juego
    if segundos>10 :
        pygame.time.set_timer(pygame.USEREVENT,0)
        PAUSA=True
        return
    font = pygame.font.Font('freesansbold.ttf', 18)
    #Texto del temporizador que se muestra por pantalla

    ventana.blit(font.render('Segundos restantes: '+str(10-segundos), True, (0, 0, 0)), (marcador.centerx-60, marcador.centery-30))
    return





#Bucle de seleccion de la velocidad de los puntos
while True:
    for event in pygame.event.get():
        #Si el evento es cerrar la ventana
        if event.type == pygame.QUIT:
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        #Si el evento es una pulsacion de raton
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton
            raton=pygame.mouse.get_pos()
            #Se pone la velocidad en funcion de la eleccion del usuario
            if lento_rect.collidepoint(raton):
                velocidad=1
            elif medio_rect.collidepoint(raton):
                velocidad=2
            elif rapido_rect.collidepoint(raton):
                velocidad=3
            #Si el usuario selecciona return se vuelve al menu de seleccion
            elif return_rect.collidepoint(raton):
                exec(open('Juego.py').read())
            break
    #Cuando ya ha seleccionado debe comenzar el juego
    if velocidad!=0:
        break

#Se pinta el tablero de blanco
ventana.fill((255,255,255))
pygame.display.flip()



#Bucle del juego (Se encarga sobretodo de la interacción con el usuario)
while True:
    for event in pygame.event.get():#Cuando ocurre un evento...
        #Cuando ha pasado un segundo se hace tick al reloj
        if event.type == pygame.USEREVENT:
            tick()

        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        elif event.type == pygame.MOUSEBUTTONDOWN:
           #llamamos a juego
            juego()
    #Control de los puntos mediante el teclado
    teclas()
    #Movimiento de los puntos porque una iteracion de este bucle es una unidad temporal
    movimiento()



