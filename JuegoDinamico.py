import pygame,sys,random,math
import scipy.spatial
from scipy.spatial import Delaunay
from auxiliar import Voronoi
import itertools
#from itertools import combinations
from auxiliar import Area



##Inicializamos pygame
pygame.init()
#Generamos aleatoriamente los puntos contra los que va a competir el usuario
puntos=[[int(random.random()*700),int(random.random()*700)]for i in range(20)]


#Generamos los vectores velocidad de los puntos aleatoriamente
velocidad=[[random.uniform(-1,1),random.uniform(-1,1)]for i in range(20)]
#normalizamos la velocidad de los puntos para que sea constante
velocidad=[[2*(velocidad[v][0]/(math.sqrt((velocidad[v][0])**2+(velocidad[v][1])**2))),2*(velocidad[v][1]/(math.sqrt((velocidad[v][0])**2+(velocidad[v][1])**2)))]for v in range(len(velocidad))]
#Parametro que indica si el usuario ha introducido ya su punto
usuario=False
#Parametro que indica el estado del juego
PAUSA=True

#Area total del tablero
areaTotal=700*700
Area1=0
start_ticks=0

###Incializacion de la pantalla del juego###


#Establecemos el tamaño de la ventana2.
ventana2 = pygame.display.set_mode((700,800))
#Establecemos el rectangulo que va  a representar el marcador2
marcador2=pygame.Rect(0,700,700,100)
#Titulo de la ventana2
pygame.display.set_caption("Juego de Voronoi")
#Se pinta el fondo de la pantalla de blanco
ventana2.fill((255,255,255))
#Se pinta el rectangulo del marcador2
pygame.draw.rect(ventana2, (250,250,250),marcador2)
#La fuente para renderizar el texto que aparecera por pantalla
font = pygame.font.Font('freesansbold.ttf', 18)
#Texto del boton de return
return_cadena=font.render('return', True, (0, 0, 0))
#Rectangulo del boton return
return_rect=pygame.Rect(580,740,100,50)
#Pintamos el boton de return
pygame.draw.rect(ventana2,(255, 255, 255),return_rect)
pygame.draw.rect(ventana2,(0, 0, 0),return_rect,2)
ventana2.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))

# se despliega la pantalla
pygame.display.flip()




#Funcion que controla el temporizador
def temporizador():
    global PAUSA,start_ticks,font

    #Calcula cuantos segundos han pasado desde que comenzo el temporizador
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds

    #Si el juego esta esta ya PAUSAdo no debe haber temporizador
    if PAUSA:return
    #Si han pasado mas de 30 segundos y el juego sigue en movimiento debe parar el juego
    if seconds>30 and not PAUSA:
        PAUSA=True
        return

    #Cuenta inversa del temporizador
    seconds=30-int(seconds)
    segundos=font.render('Segundos restantes: '+str(seconds), True, (0, 0, 0))
    #Se muestra en la pantalla el temporizador
    ventana2.blit(segundos, (marcador2.centerx-60, marcador2.centery-10))


#Funcion que calcula la distancia euclidea de dos puntos en el plano
def dist(A,B):
     return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2)


#Funcion que se encarga de mover los puntos en cada unidad temporal
def movimiento():
    global velocidad, puntos, PAUSA
    #Si el juego no esta PAUSAdo se deben mover los puntos
    if not PAUSA:
        #Hay que mover cada punto
        for p in range (len(puntos)):
            #Si el punto llega al borde debe rebotar, se le cambia de signo la coordenada del vector en funcion de
            #si rebota con borde superior o inferior (cambia coordenada y) o borde izqdo o dcho (cambia coordenada x)
             if puntos[p][0]>700:
                velocidad[p]=[-velocidad[p][0],velocidad[p][1]]
             elif puntos[p][0]<0:
                velocidad[p]=[-velocidad[p][0],velocidad[p][1]]
             elif puntos[p][1]<0:
               velocidad[p]=[velocidad[p][0],-velocidad[p][1]]
             elif puntos[p][1]>700:
                velocidad[p]=[velocidad[p][0],-velocidad[p][1]]
             #Se mueve el punto sumandole el vector velocidad que le corresponde
             puntos[p]=[puntos[p][0]+velocidad[p][0],puntos[p][1]+velocidad[p][1]]

    #Segundo ,tratamos colisiones
        #Se crea lista de colisiones pendientes para tratar en esta unidad temporal
        colision=[]
        #Toda la lista de combinaciones de indices que pueden colisionar, con combinaciones no revisamos todos los indices como
        # si lo hicieramos en un bucle doble, asi nos ahorramos repeticiones
        comb=itertools.combinations(list(range(len(puntos))),2)

        for c in comb:
            #Se comprueba si la distancia a los demas puntos es menor que la establecida como minima para una colision
            if dist(puntos[c[1]],puntos[c[0]])<11:
                aux=velocidad[c[0]]
                velocidad[c[0]]=velocidad[c[1]]
                velocidad[c[1]]=aux
                #colision.append([c[1],c[0]])
            continue
    #Tras los movimientos de los puntos se pintan
    pintar2()
    return

#Funcion que se encarga de mostrar por pantalla en cada unidad temporal
def pintar2():
    global puntos, Area1, PAUSA, ventana2,usuario
    #Si el juego esta en PAUSA no debe cambiar nada en la pantalla
    #if PAUSA and usuario:return

    #Se calcula la triangulacion de Delaunay y a partir de ella las regiones de Voronoi
    D=Delaunay(puntos)
    V=Voronoi(D)

    #Si el usuario aun no ha colocado su punto todas las regiones son grises
    if not usuario:
        for p in range(len(puntos)):
            pygame.draw.polygon(ventana2,(100,100,100),V[p])
            pygame.draw.polygon(ventana2,(0,0,0),V[p],2)
            pygame.draw.circle(ventana2,(180,180,180),[int(puntos[p][0]),int(puntos[p][1])],9)
            pygame.draw.circle(ventana2,(0,0,0),[int(puntos[p][0]),int(puntos[p][1])],4)
    #Si el usuario ya ha colocado, la ultima region es la region que ha colocado el usuario y debe ser roja, las demas grises
    else:
        for p in range(len(puntos)-1):
            pygame.draw.polygon(ventana2,(100,100,100),V[p])
            pygame.draw.polygon(ventana2,(0,0,0),V[p],2)
            pygame.draw.circle(ventana2,(180,180,180),[int(puntos[p][0]),int(puntos[p][1])],9)
            pygame.draw.circle(ventana2,(0,0,0),[int(puntos[p][0]),int(puntos[p][1])],4)
        #La region del usuario:
        pygame.draw.polygon(ventana2,(180,0,0),V[len(puntos)-1])
        pygame.draw.polygon(ventana2,(0,0,0),V[len(puntos)-1],2)
        pygame.draw.circle(ventana2,(180,180,180),[int(puntos[len(puntos)-1][0]),int(puntos[len(puntos)-1][1])],9)
        pygame.draw.circle(ventana2,(0,0,0),[int(puntos[len(puntos)-1][0]),int(puntos[len(puntos)-1][1])],4)
        #Se calcula la proporcion del Area que supone la region del usuario
        Area1=Area(V[len(puntos)-1])
    #Se llama a las funciones auxiliares de poner marcador2 y temporizador
    poner_marcador()
    temporizador()
    #Se actualiza lo que aparece por pantalla
    pygame.display.update()
    return


#Funcion auxiliar a pintar que se encarga de mostrar toda la parte de abajo de la pantalla con los marcador2es
def poner_marcador():
    global areaTotal,Area1,ventana2,return_cadena,return_rect
    #Se calcula el porcentaje del area
    Area1=(Area1/areaTotal)*100
    #Se pinta el rectangulo del marcador2
    pygame.draw.rect(ventana2, (250,250,250),marcador2)
    #Se muestra el area por pantalla
    tArea1=font.render(str(int(Area1))+"%", True, (0, 0, 0))
    ventana2.blit(tArea1, (15, 750))
    #Boton de return
    pygame.draw.rect(ventana2,(255, 255, 255),return_rect)
    pygame.draw.rect(ventana2,(0, 0, 0),return_rect,2)
    #Se muestra boton de return por pantalla
    ventana2.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))
    return


#Funcion que se encarga de la interaccion con las teclas que pulsa el jugador
def teclas():
    global puntos,velocidad,PAUSA

    #La tecla que ha pulsado el usuario
    keys=pygame.key.get_pressed()
    #Al pulsar barra de space se PAUSA el juego
    if keys[pygame.K_SPACE] and not PAUSA:
        PAUSA=True
        return
    #En caso de que se quiera PAUSAr de manera no definitiva
    # if keys[pygame.K_SPACE] and  PAUSA:
    #     PAUSA=False
    if PAUSA:
        return
    #Pulsar alguna de las flechas modifica el vector velocidad del punto que controla el usuario, debe volver a ser normalizado

    if keys[pygame.K_LEFT]:
        velocidad[len(puntos)-1]=[velocidad[len(puntos)-1][0]-2,velocidad[len(puntos)-1][1]]

    if keys[pygame.K_RIGHT]:
        velocidad[len(puntos)-1]=[velocidad[len(puntos)-1][0]+2,velocidad[len(puntos)-1][1]]

    if keys[pygame.K_UP]:
        velocidad[len(puntos)-1]=[velocidad[len(puntos)-1][0],velocidad[len(puntos)-1][1]-2]

    if keys[pygame.K_DOWN]:
        velocidad[len(puntos)-1]=[velocidad[len(puntos)-1][0],velocidad[len(puntos)-1][1]+2]

    #Despues de mover el punto normalizamos la velocidad
    norma=math.sqrt((velocidad[len(puntos)-1][0])**2+(velocidad[len(puntos)-1][1])**2)
    if norma==0:
        norma=1
    velocidad[len(puntos)-1]=[ 2*((velocidad[len(puntos)-1][0])/norma ) ,2*((velocidad[len(puntos)-1][1])/norma ) ]

    return


#Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana2
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa
        #Si el usuario ha hecho click con el raton
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Posicion del raton dada como x e y en el plano
            raton=pygame.mouse.get_pos()
            #Obtenemos la posicion del raton que va hasta el punto (700,700)
            #Si pulsa return se vuelve al menu del juego
            if  return_rect.collidepoint(raton):
                exec(open('Juego.py').read())

            #El usuario solo debe colocar un punto, inicialmente la partida comienza con 20 puntos
            if len(puntos)<21:
                #Variable que indica si el usuario ha colocado su punto para poder pintar las regiones
                usuario=True
                #Cuando usuario añade punto los puntos aleatorios se comienzan a mover
                PAUSA=False
                #Obtenemos el tiempo actual, momento en el que comienza el temporizador
                start_ticks=pygame.time.get_ticks()

                #Si pulsa justo encima de un punto que ya está en la pantalla no se podria calcular Delaunay,
                # para evitar eso lo movemos de manera inapreciable
                if raton in puntos:
                     puntos.append([raton[0]+1,raton[1]-1])

                else:puntos.append(raton)
                #El punto comienza sin movimiento
                velocidad.append([0,0])
            continue
    #Se captura el movimiento del punto en caso de que se haya puesto
    if usuario:teclas()
    #Cada iteracion de este bucle se considera como unidad temporal asi que se deben mover los puntos
    movimiento()





