import pygame
from pygame.locals import *
from auxiliar import *
import math
import itertools


#####Clase correspondiente a Juego Dinamico siendo este el juego dinamico para dos jugadores ##########


#Parametro del modulo de la velocidad de los puntos, en funcion de el se ve si es lento, medio o rapido
velocidad=0
#Parametro que indica el estado del movimiento del juego
PAUSA=False
#Valor para el tiempo incial del temporizador
start_ticks=0

#Lista de los puntos que se van a jugar en la partida
p=[]
#Lista de los vectores velocidad de los puntos
vec=[]
#Area de las regiones del primer jugador
Area1=0
#Area de las regiones del segundo jugadro
Area2=0
#Area total del tablero
area=700*700


#Parametro para que no haya problema de superposicion de puntos
l=1

#Distancia euclidea entre dos puntos
def dist(A,B):
     return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)


#Funciom que se encarga del movimiento de los puntos en cada unidad temporal
def movimiento():
    global p,vec
    #Si el juego esta pausado no se deben mover los puntos
    if PAUSA:return
    #Los puntos se mueven sumandoles su vector velocidad
    for j in range(len(p)):
        #Si el punto llega al borde debe rebotar, se le cambia de signo la coordenada del vector en funcion de
        #si rebota con borde superior o inferior (cambia coordenada y) o borde izqdo o dcho (cambia coordenada x
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
    #Se crea lista de colisiones pendientes para tratar en esta unidad temporal
    colision=[]
    #Toda la lista de combinaciones de indices que pueden colisionar, con combinaciones no revisamos todos los indices como
    # si lo hicieramos en un bucle doble, asi nos ahorramos repeticiones

    comb=itertools.combinations(list(range(len(p))),2)
    for c in comb:
            #Se comprueba si la distancia a los demas puntos es menor que la establecida como minima para una colision
            if dist(p[c[1]],p[c[0]])<11:
                aux=vec[c[0]]
                vec[c[0]]=vec[c[1]]
                vec[c[1]]=aux
            continue
    pintar()
    return

#Funcion para pintar en pantalla los diagramas despues de cada interaccion con el usuario
def pintar():
    global p,Area2,Area1,PAUSA
    #if PAUSA: return
    #En primer lugar se encarga de calcular la triangulacion y la division del plano en las regiones
    #Si hay menos de 4 puntos no se puede hacer triangulacion y se calcula  por interseccion de planos
    if len(p)<3:
        Area1=0
        Area2=0
        #Lista de las regiones de Voronoi
        V=[]
        for k in range(len(p)):
                #Se calcula la region de Voronoi asociada a cada punto introducido de manera individual
                V.append(voronoiRegion(p,k))
                #Las regiones pares son las del primer jugador
                if k%2:
                    #Se pintan las regiones y se calcula el area
                    pygame.draw.polygon(ventana,(0,0,250),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    pygame.draw.circle(ventana,(143,143,143),[int(p[k][0]),int(p[k][1])],9)
                    pygame.draw.circle(ventana,(0,0,0),[int(p[k][0]),int(p[k][1])],4)
                    Area1=Area(V[k])+Area1
                #Las regiones impares son las del segundo jugador
                else :
                     #Se pintan las regiones y se calcula el area
                    pygame.draw.polygon(ventana,(250,0,0),V[k])
                    pygame.draw.polygon(ventana,(0,0,0),V[k],2)
                    pygame.draw.circle(ventana,(143,143,143),[int(p[k][0]),int(p[k][1])],9)
                    pygame.draw.circle(ventana,(0,0,0),[int(p[k][0]),int(p[k][1])],4)
                    Area2=Area(V[k])+Area2
        #Se actualiza el marcador
        Poner_marcador()
        pygame.display.update()
        return
    #Si hay mas de tres puntos se puede calcular haciendo uso de la triangulacion
    else :
        #Se calcula la triangulacion
        D=Delaunay(p)
        #se calculan las regiones de Voronoi
        V=Voronoi(D)
        Area1=0
        Area2=0
    #Para cada punto se pinta su region y se calcula su area correspondiente
    for v in range (len(V)-1):
                    #Las regiones pares son las del primer jugador
                    if v%2:
                        #Se pintan las regiones y se calcula el area
                        if len(V[v])>2:
                            pygame.draw.polygon(ventana,(0,0,250),V[v])
                            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(143,143,143),[int(p[v][0]),int(p[v][1])],9)
                        pygame.draw.circle(ventana,(0,0,0),[int(p[v][0]),int(p[v][1])],4)
                        Area1=Area(V[v])+Area1

                    #Las regiones impares son las del segundo jugador
                    else:
                         #Se pintan las regiones y se calcula el area
                        if len(V[v])>2:
                            pygame.draw.polygon(ventana,(250,0,0),V[v])
                            pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(143,143,143),[int(p[v][0]),int(p[v][1])],9)
                        pygame.draw.circle(ventana,(0,0,0),[int(p[v][0]),int(p[v][1])],4)
                        Area2=Area(V[v])+Area2

                    #La ultima region es la que se puede controlar con las flechas y tiene un color mas claro
                    if len(V[len(p)-1])>2:
                        if (len(p)-1)%2:
                            pygame.draw.polygon(ventana,(210, 210, 250),V[len(p)-1])

                        else :
                            pygame.draw.polygon(ventana,(255, 160, 122),V[len(p)-1])



                        pygame.draw.polygon(ventana,(0,0,0),V[len(p)-1],2)
                    pygame.draw.circle(ventana,(143,143,143),[int(p[len(p)-1][0]),int(p[len(p)-1][1])],9)
                    pygame.draw.circle(ventana,(0,0,0),[int(p[len(p)-1][0]),int(p[len(p)-1][1])],4)
                    #Se le debe sumar al rojo
    #Se añade el area de la ultima region
    if (len(p)-1)%2:
         Area1=Area(V[len(p)-1])+Area1
    else:
        Area2=Area(V[len(p)-1])+Area2
    #Se pone el marcador
    Poner_marcador()
    #Si la longitud de la lista de puntos llega al maximo de puntos debe saltar el temporizador
    if len(p)==20:
        temporizador()
    #Se actualiza lo que se muestra por pantalla
    pygame.display.update()
    return



#Funcion que controla la interaccion del usuario con las teclas del raton
def teclas():
    global vec,velocidad,p
    #No se deben mover si el juego esta pausado
    if len(p)<1:return
    if PAUSA: return
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        vec[len(p)-1]=[vec[len(p)-1][0]-1,vec[len(p)-1][1]]

    if keys[pygame.K_RIGHT]:
        vec[len(p)-1]=[vec[len(p)-1][0]+1,vec[len(p)-1][1]]


    if keys[pygame.K_UP]:
        vec[len(p)-1]=[vec[len(p)-1][0],vec[len(p)-1][1]-2]

    if keys[pygame.K_DOWN]:
        vec[len(p)-1]=[vec[len(p)-1][0],vec[len(p)-1][1]+1]

    #Despues de mover el punto normalizamos la velocidad
    norma=math.sqrt((vec[len(p)-1][0])**2+(vec[len(p)-1][1])**2)
    if norma==0:
        norma=1
    #Se normaliza y multiplica por el modulo de la velocidad deseada en funcion de si es lento, medio o rapido
    vec[len(p)-1]=[velocidad*((vec[len(p)-1][0])/norma ) ,velocidad*((vec[len(p)-1][1])/norma ) ]

    return


#Funcion para desplegar el marcador durante la partida
def Poner_marcador():
    global Area1,Area2,PAUSA
    if PAUSA:return
    #Se muestra el cuadrado donde va el marcador
    pygame.draw.rect(ventana, (250,250,250),marcador)
    #Se calcula Area1 como porcentaje
    Area1=(Area1/area)*100
     #Se calcula Area2 como porcentaje
    Area2=(Area2/area)*100
    #Texto de Areas
    tArea1=font.render(str(int(Area1))+"%", True, (0, 0, 250))
    tArea2=font.render(str(int(Area2))+"%", True, (250, 0, 0))
    #Se añaden al marcador las areas
    ventana.blit(tArea1, (15, 750))
    ventana.blit(tArea2, (350, 750))
    #Boton de return
    ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))
    #Se muestra en el marcador el boton de return
    pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
    # se muestra el numero de puntos que hay
    n_puntos=font.render(str(len(p))+" puntos", True, (0, 0, 250))
    ventana.blit(n_puntos,(580,710))
    if len(p)==20:
        temporizador()
    return

#Funcion que controla el proceso del juego
def juego():
    global p,vec,l,PAUSA,start_ticks,V

    #Los primeros cuatro puntos hay que pedirlos y calcular Voronoi haciendo clipping
    raton = pygame.mouse.get_pos()
    #Si se pincha return se vuelve al menu
    if return_rect.collidepoint(raton):
        #start_ticks=0
        exec(open('Juego.py').read())
    #si esta pausado solo se debe poder pinchar en return
    if PAUSA:return
    #Si se pincha fuera del tablero y no se ha pinchado en return no debe ocurrir nada
    if raton[1]>700:
        return

    # #LIMITA EL NUMERO DE PUNTOS QUE SE PUEDEN INSERTAR
    #Ahora le he puesto un máximo de 10 puntos por jugador
    if len(p)<20:
        #Si se pincha sobre un punto que ya existe, se coloca un poco movido pero de manera inapreciable para que se
        # pueda calcular la triangulacion
        if raton in p:
            raton=(raton[0]+l,raton[1]+l)
            l=l*(-1)
        #Se añade la posicion seleccionada en la lista de puntos
        p.append(raton)
        #Se añade sin movimiento
        vec.append([0,0])
        pintar()
        #Cuando se pone el ultimo punto se le dan al jugador 10 segundos para mover el punto
        if len(p)==20:
            start_ticks=pygame.time.get_ticks()
            #se inicia temporizador
            temporizador()

    return


#Funcion encargada de poner el temporizador y pausar el juego cuando termina el tiempo
def temporizador():
    global PAUSA,start_ticks

    if PAUSA: return
    #Se calcula el timepo
    seconds=(pygame.time.get_ticks()-start_ticks)/1000

   #Cuando acaba el tiempo se pausa el juego
    if seconds>10 and not PAUSA:
        PAUSA=True
        return
    #Se muestra por pantalla el temporizador
    font = pygame.font.Font('freesansbold.ttf', 18)
    seconds=10-int(seconds)
    segundos=font.render('Segundos restantes: '+str(seconds), True, (0, 0, 0))
    ventana.blit(segundos, (marcador.centerx-60, marcador.centery-30))




#################COMIENZA JUEGO#############

# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,800))
#Establecemos el cuadrado que será el marcador
marcador=pygame.Rect(0,700,700,100)
#Le ponemos titulo a la ventana
pygame.display.set_caption("Juego de Voronoi")
#la pintamos de blanco
ventana.fill((255,255,255))

#Se añade el marcador a la ventana
pygame.draw.rect(ventana, (250,250,250),marcador)

#La fuente para el texto
font = pygame.font.Font('freesansbold.ttf', 18)

#Se preparan todos los elementos de la pantalla para ser mostrada
return_cadena=font.render('return', True, (0, 0, 0))
#Boton return
return_rect=pygame.Rect(580,740,100,50)
pygame.draw.rect(ventana,(255, 255, 255),return_rect)
pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))
#Se muestra la ventana
pygame.display.flip()







#Bucle de seleccion de la velocidad de los puntos

#Se crean los Botones de seleccion de velocidad
lento_rect=pygame.Rect(200,100,300,100)
rapido_rect=pygame.Rect(200,500,300,100)
medio_rect= pygame.Rect(200,300,300,100)


#Se pintan los botones de seleccion de velocidad
pygame.draw.rect(ventana, (72, 209, 204),lento_rect)
pygame.draw.rect(ventana, (72, 209, 204),medio_rect)
pygame.draw.rect(ventana, (72, 209, 204),rapido_rect)


font2 = pygame.font.Font('freesansbold.ttf', 20)
#Texto de los botones
puntos_cadena=font.render('Escoge la velocidad del movimiento de los puntos', True, (0, 0, 0))
lento_cadena=font2.render('Lenta ', True, (0, 0, 0))
medio_cadena=font2.render('Media', True, (0, 0, 0))
rapido_cadena=font2.render('Rápida', True, (0, 0, 0))


#Se ponen los botones
ventana.blit(rapido_cadena, (rapido_rect.centerx-80, rapido_rect.centery-10))
ventana.blit(medio_cadena, (medio_rect.centerx-80, medio_rect.centery-10))
ventana.blit(lento_cadena, (lento_rect.centerx-80, lento_rect.centery-10))
ventana.blit(puntos_cadena, (lento_rect.centerx-200, lento_rect.centery-100))
#Se actualiza la pantalla
pygame.display.flip()


#Bucle de seleccion de la velocidad
while True:
    for event in pygame.event.get():    #Cuando ocurre un evento...
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton que va hasta el punto (700,700)
            raton=pygame.mouse.get_pos()
            #Se actualiza la velocidad en funcion de lo que pincha el usuario
            if lento_rect.collidepoint(raton):
                velocidad=1
            elif medio_rect.collidepoint(raton):
                velocidad=3
            elif rapido_rect.collidepoint(raton):
                velocidad=5
            #Si selecciona return se debe volver al menu
            elif return_rect.collidepoint(raton):
                exec(open('Juego.py').read())
    #Cuando ha seleccionado debe comenzar la pantalla del juego
            break
    if velocidad!=0:
        break
#Ventana blanca para mostrar el tablero
ventana.fill((255,255,255))
pygame.display.flip()



#Bucle del juego (Se encarga sobretodo de la interacción con el usuario)
while True:
    for event in pygame.event.get():#Cuando ocurre un evento...
        #Cuando comineza el juego se debe poder poner puntos y jugar
        if len(p)==0: PAUSA=False
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        #Si el usuario hace click se llama a la funcion que se encarga de eso
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton que va hasta el punto (700,700)
            juego()
    #Control del usuario del movimiento del punto
    teclas()
    #Se mueven los puntos porque una iteracion de este bucle se considera una unidad temporal
    movimiento()



