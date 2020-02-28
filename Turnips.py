# -*- coding: utf-8 -*-
import sympy as sy
import pygame as pg
import random
from pygame.locals import *
from PIL import Image
from typing import Any

"""1. Recuperar las funciones"""
def mex(lista):
    indice = 0
    encontrado=0 
    while encontrado==0:
        if(indice in lista):
            indice = indice + 1
        else :
            encontrado = 1
      
    return indice
    
def gmt(n):
    nb= decabin(2*n)
    if sum(nb) % 2: return 2*n 
    else: return 2*n +1 
    
def sumnim(a,b): return a^b

def sumdig(lista):
    indice = 1
    suma = lista[0]
    while indice<len(lista):
        suma = sumnim(suma,lista[indice])
        indice=indice+1
    return suma
    
def decabin(dec):
    bina = []
    while dec:
        bina.insert(0, dec & 1)
        dec >>= 1
    return bina



"""Recibe: pila desde donde se debe buscar posicion P  y posicion actual 
devuelve: indice de la pila que debe modificarse y el valor de dicha pila"""


def apnim(posN, i = 0):
    #Calculamos la suma nim de los valores sg de las posiciones con cara
    suma = sumdig(posN)
    #Pasamos el valor a binario
    bin = decabin(suma)
     #Teniendo en cuenta que decabin devuelve el numero en binario y siempre empieza por 1
    #h sera la posicion del uno mas a la izquierda
    h = len(bin)-1

    #Habra que recorrer los valores sg de las caras para ver en cuales hay un 1 en la posicion h
    indice = i
    encontrado = 0
    while encontrado == 0:
        elem = decabin(posN[indice])
        if (len(elem)-1-h) < 0:
            indice += 1
            continue
        if elem[len(elem)-1-h] == 1: encontrado = 1
        else: indice += 1
    
    #Calculo del valor que deberia tomar posN[indice]
    #Ese valor sera la sumdig de posN menos el valor sg de la posicion que queremos cambiar
    ind = 0
    suma = 0
    while ind < len(posN):
        if ind == indice:
            ind = ind+1
            continue
        suma = sumnim(suma, posN[ind])
        ind = ind+1

    #Suma es el valor que debe tomar el adyacente  a la posicion que queremos cambiar
    return (indice, suma)
    


#Funcion SG para posiciones con una sola cara, es decir, posiciones irreducibles
def sgtur(n): #La n hace referencia a la posicion donde esta la cara de las posiciones irreducibles empezando en 0
    g = [0, 0] #Inicialmente sabemos los valores SG de dos posiciones: C X X ... y X C X X ... siendo C cara y X cruz
    for m in range(2, n+1):
        #En S se van a guardar los valores SG de las posiciones adyacentes de la posicion
        S = [sumdig([g[m1], g[2*m1-m]]) for m1 in range(1, m) if 2*m1 >= m]
        g.append(mex(S))
    return g[-1] #El ultimo valor añadido a g, el ultimo elemento de la lista

def clastur(L):
    Lc = L[:] #Se extraen todos los elementos de L
    #1 = cara; 0 = cruz
    posicioncaras = [i for i in range(len(L)) if L[i]]
    valorSGcaras = list(map(sgtur,posicioncaras)) #Se obtiene el valor SG de las posiciones con caras

    #Ahora hay que ver si la posicion de las monedas es P o N
    #Para ello calculamos la suma digital de valoresSGcaras,
    #ya que la posicion actual es composicion de esos valores irreducibles
    if(sumdig(valorSGcaras)):
        #Como el valor es distinto de 0, se trata de una posición N
        i, valfin = apnim(valorSGcaras) #Siendo i el indice de la pila a modificar, y valfin el valor que debe tomar

        moneda2 = posicioncaras[i] #Moneda que cambia de cara a cruz
        moneda1 = posicioncaras[i]-1 #Moneda situada justo a la izquierda de la que se quiere cambiar
        moneda0 = 2*moneda1-moneda2

        valini = sumnim(sgtur(moneda0),sgtur(moneda1))
        while valini != valfin:
            if moneda1:
                moneda1 = moneda1-1
                valini = sumnim(sgtur(2*moneda1-moneda2),sgtur(moneda1))
            else:
                i, valfin = apnim(valorSGcaras, i+1)
                moneda1 = posicioncaras[i]-1
                moneda2 = posicioncaras[i]


        monedas=[2*moneda1-moneda2,moneda1,moneda2] #Ya se sabe que monedas girar
        if len(monedas)<=3:
            print("El valor de L es ",L)
            print("Los valores SG de las caras son ",valorSGcaras)
            print("Moneda de la izquierda: ", 2*moneda1-moneda2)
            print("Moneda del medio: ", moneda1)
            print("Moneda de la derecha: ", moneda2)
        for moneda in monedas:
            L[moneda] = 1 - L[moneda] #Se giran las monedas

        return  "N", L

    else: return "P", Lc


#variables globales
N=15    #La N indica el número de monedas, que pueden ser 7, 10 o 15 monedas
LMENU = 500
DISABOTONMENU = 150
DISBOTONMENU = 200

LTOTAL, LBOT, LTEXALTURA, LTEXLARGO1, LTEXLARGO2 = 0, 0, 0, 0, 0

blanco = (255,255,255)
gris = (165,165,165)
verde_lanquecino = (189,236,182)

P = [random.randint(0,1) for i in range(N)]
#Vamos a ver que la posicion generada automaticamente no es final del juego
def buscarP():
    i = 2
    encontrado = False
    while i<N and not encontrado:
        if P[i]:
            encontrado = True
        i = i+1
    return encontrado


def inicializar():
    global LTOTAL,LBOT,LTEXALTURA,LTEXLARGO1,LTEXLARGO2,R,rtexto,rtextoVolverMenu,rtextoTurno,cara,cruz,seleccionado,mnd,P,M,T,RT
    LTOTAL = 1250
    LBOT = int (LTOTAL/N)     #Tamano del cuadrado de las monedas
    LTEXALTURA = 40     #Altura del rectangulo del texto (barra inferior)
    LTEXLARGO1 = int(LTOTAL/2)  #Largo del rectangulo del texto1 (seleccione movimiento...)
    LTEXLARGO2 = int(LTEXLARGO1/2) #Largo del rectangulo de volver a menu

    P = [random.randint(0,1) for i in range(N)]
    while(buscarP()==False): P = [random.randint(0,1) for i in range(N)]
    #P = [0,1,0,1,1,1,1,1,1,1]
    #P = [0,0,1,1,1,1,0,1,0,1]
    #P = [0,1,0,1,1,1,1]
    R = []
    for i in range(N):
        R.append(0)

    for i in range(N):
        R[i] = pg.Rect(i*LBOT, 0, LBOT, LBOT)

    rtexto = pg.Rect(0,LBOT,LTEXLARGO1,LTEXALTURA)      #Texto casilla 1 (texto de movimiento)
    rtextoVolverMenu = pg.Rect(LTEXLARGO1,LBOT,LTEXLARGO2,LTEXALTURA)    #Texto casilla 2
    rtextoTurno = pg.Rect(LTEXLARGO1+LTEXLARGO2,LBOT,LTEXLARGO2,LTEXALTURA)

    #vamos a cargar las imagenes de las monedas
    cara = pg.image.load("cara"+str(N)+".jpg")
    cruz = pg.image.load("cruz"+str(N)+".jpg")
    seleccionado = pg.image.load("seleccionado"+str(N)+".jpg")
    mnd = {0:cruz , 1:cara, 2: seleccionado}

    M , T, RT = 0, 0, 0

rboton1menu = pg.Rect(DISABOTONMENU,25,DISBOTONMENU,50)
rboton2menu = pg.Rect(DISABOTONMENU,25+50+75,DISBOTONMENU,50)
rboton3menu = pg.Rect(DISABOTONMENU,25+50+75+50+75,DISBOTONMENU,50)
rboton4menu = pg.Rect(DISABOTONMENU,25+50+75+50+75+50+75,DISBOTONMENU,50)


Tr0 = ["Seleccione un movimiento","Movimiento valido", "Movimiento no valido", "¡HAS GANADO!", "¡HAS PERDIDO!", "Pulse Enter"]
Tr1 = ["Turno Jugador", "Turno Maquina", "FIN DEL JUEGO"]
Tr2 = ["","  Volver al Menu"]
TxBMenu = ["Reglas","7 monedas","10 monedas","15 monedas"]

#Ventana de las reglas
#ventana para el menu inicial
def iniciarReglas ():
    ventana = pg.display.set_mode((LMENU,LMENU))
    ventana.fill(blanco) #definimos el fondo de la ventana con el color dado

    pg.display.set_caption("Turnips - REGLAS")#le damos titulo a la ventana

    rmarcofoto1 = pg.Rect(0, 350, 175, 150)
    rmarcofoto2 = pg.Rect(175, 350, 150, 150)
    rmarcofoto3 = pg.Rect(175+150, 350, 175, 150)
    rfoto1 = pg.Rect(50, 350, 100, 100)
    rfoto2 = pg.Rect(200, 350, 100, 100)
    rfoto3 = pg.Rect(350, 350, 100, 100)
    rtextofoto1 = pg.Rect(0, 300, 175, 50)
    rtextofoto2 = pg.Rect(175, 300, 150, 50)
    rtextofoto3 = pg.Rect(175+150, 300, 175, 50)
    rvolver = pg.Rect(350, 465, 175, 50)
    pg.draw.rect(ventana, gris, rmarcofoto1)
    pg.draw.rect(ventana, gris, rmarcofoto2)
    pg.draw.rect(ventana, gris, rmarcofoto3)
    pg.draw.rect(ventana, gris, rfoto1)
    pg.draw.rect(ventana, gris, rfoto2)
    pg.draw.rect(ventana, gris, rfoto3)
    pg.draw.rect(ventana, gris, rtextofoto1)
    pg.draw.rect(ventana, gris, rtextofoto2)
    pg.draw.rect(ventana, gris, rtextofoto3)
    pg.draw.rect(ventana, verde_lanquecino, rvolver)

    #vamos a cargar las imagenes de las monedas
    cara=pg.image.load("caraReglas.jpg")
    cruz=pg.image.load("cruzReglas.jpg")
    seleccionado=pg.image.load("seleccionadoReglas.jpg")

    tamanoletraboton = 30
    ventana.blit(seleccionado, (rfoto1.x, rfoto1.y))
    ventana.blit(cruz, (rfoto2.x, rfoto2.y))
    ventana.blit(cara, (rfoto3.x, rfoto3.y))

    tamanoletraboton = 20
    fuente = pg.font.SysFont("arial", tamanoletraboton)
    t11 = fuente.render("MONEDA", True, (255, 255, 255))
    t12 = fuente.render("SELECCIONADA", True, (255, 255, 255))
    tamanoletraboton = 25
    fuente = pg.font.SysFont("arial", tamanoletraboton)
    t2 = fuente.render("CRUZ", True, (255, 255, 255))
    t3 = fuente.render("CARA", True, (255, 255, 255))
    tvolver = fuente.render("VOLVER", True, (0, 0, 0))
    fuente = pg.font.SysFont("arial", 20)
    ttexto = fuente.render("Se dispone de una hilera de n monedas.", True, (0, 0, 0))
    ttexto1 = fuente.render("El jugador que hace la última jugada válida gana.", True, (0, 0, 0))
    ttexto2 = fuente.render("Un movimiento consiste en girar 3 monedas tales que:", True, (0, 0, 0))
    ttexto5 = fuente.render("- El número de monedas entre la moneda 1 y 2", True, (0, 0, 0))
    ttexto6 = fuente.render("es el mismo que hay entre la 2 y la 3", True, (0, 0, 0))
    ttexto7 = fuente.render("- La moneda que esté más a la derecha de las 3", True, (0, 0, 0))
    ttexto8 = fuente.render("escogidas, cambia de cara a cruz", True, (0, 0, 0))
    ttextosalto = fuente.render("", True, (0, 0, 0))
    ttextoParaIm = fuente.render("Las monedas durante el juego se representarán como: ", True, (0, 0, 0))

    ventana.blit(t11, (rtextofoto1.x+55,rtextofoto1.y+1))
    ventana.blit(t12, (rtextofoto1.x+30,rtextofoto1.y+20))
    ventana.blit(t2, (rtextofoto2.x+40,rtextofoto2.y+8))
    ventana.blit(t3, (rtextofoto3.x+40,rtextofoto3.y+8))
    ventana.blit(tvolver, (rvolver.x+30, rvolver.y+5))
    ventana.blit(ttexto, (5, 5))
    ventana.blit(ttexto1, (5, 30))
    ventana.blit(ttextosalto, (5, 55))
    ventana.blit(ttexto2, (5, 80))
    ventana.blit(ttexto5, (12, 105))
    ventana.blit(ttexto6, (30, 130))
    ventana.blit(ttexto7, (12, 155))
    ventana.blit(ttexto8, (30, 180))
    ventana.blit(ttextoParaIm, (5, 260))

    pg.draw.line(ventana, (0, 0, 0), (350, 465), (350, 500))
    pg.draw.line(ventana,(0,0,0),(350,465),(500,465))

    pg.display.update()

    final = False
    while not final:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                final=True
            elif event.type == pg.MOUSEBUTTONDOWN:
                raton = pg.mouse.get_pos()
                if rvolver.collidepoint(raton):
                    return


#ventana para el menu inicial
def marcoMenu (ventana):
    pg.draw.rect(ventana, gris, rboton1menu)
    pg.draw.rect(ventana, gris, rboton2menu)
    pg.draw.rect(ventana, gris, rboton3menu)
    pg.draw.rect(ventana, gris, rboton4menu)

    tamanoletraboton = 30

    fuente = pg.font.SysFont("arial", tamanoletraboton)
    tb0 = fuente.render(TxBMenu[0], True, (0, 0, 0))
    tb1 = fuente.render(TxBMenu[1], True, (0, 0, 0))
    tb2 = fuente.render(TxBMenu[2], True, (0, 0, 0))
    tb3 = fuente.render(TxBMenu[3], True, (0, 0, 0))
    ventana.blit(tb0, (rboton1menu.x+50, rboton1menu.y+7))
    ventana.blit(tb1, (rboton2menu.x+26, rboton2menu.y+7))
    ventana.blit(tb2, (rboton3menu.x+18, rboton3menu.y+7))
    ventana.blit(tb3, (rboton4menu.x+18, rboton4menu.y+7))

    j = 25
    for i in range(4):
        pg.draw.line(ventana, (0, 0, 0), (DISABOTONMENU, j), (DISABOTONMENU+DISBOTONMENU, j))
        j += 125
    j = 75
    for i in range(4):
        pg.draw.line(ventana,(0,0,0),(DISABOTONMENU,j),(DISABOTONMENU+DISBOTONMENU,j))
        j += 125
    j = 25
    for i in range(4):
        pg.draw.line(ventana,(0,0,0),(DISABOTONMENU,j),(DISABOTONMENU,j+50))
        pg.draw.line(ventana,(0,0,0),(DISABOTONMENU+DISBOTONMENU,j),(DISABOTONMENU+DISBOTONMENU,j+50))
        j += 125

    pg.display.update()

#lista de posiciones clicadas
def marco (ventana,lista=[]):

    for i in range(N):
        pg.draw.rect(ventana, (0,0,0), R[i]) #dibuja los cuadrados de colores
    pg.draw.rect(ventana,blanco,rtexto)
    pg.draw.rect(ventana,blanco,rtextoTurno)
    pg.draw.rect(ventana,blanco,rtextoVolverMenu)

    for i in range(N):
        if i in lista: ventana.blit(seleccionado, (R[i].x, R[i].y))
        else:
            if(mnd[P[i]]==cara):
                ventana.blit(cara, (R[i].x, R[i].y))
            else : ventana.blit(cruz,(R[i].x,R[i].y))

    tamanoletra7 = 21
    tamanoletra10 = 15
    tamanoletra15 = 10

    if N==7:
        tamano=tamanoletra7
    elif N==10:
        tamano=tamanoletra10
    elif N==15:
        tamano=tamanoletra15
    tamano=30
    fuente = pg.font.SysFont("arial", tamano)
    tr0 = fuente.render(Tr0[M],True,(0,0,0))
    tr1 = fuente.render(Tr1[T],True,(0,0,0))
    tr2 = fuente.render(Tr2[RT],True,(255,0,0))
    ventana.blit(tr0, (rtexto.x, rtexto.y+5))
    ventana.blit(tr1, (rtextoTurno.x+50, rtextoTurno.y+5))
    ventana.blit(tr2, (rtextoVolverMenu.x+40, rtextoVolverMenu.y+5))


    pg.draw.line(ventana, (0,0,0), (0,LBOT), (LTOTAL,LBOT), 1)

    # dibuja la línea
    if(RT):#Volver al menu
        pg.draw.line(ventana, (0,0,0), (LTEXLARGO1,LBOT), (LTEXLARGO1,LBOT+LTEXALTURA), 1)
        #pg.draw.line(ventana, (0,0,0), (LTEXLARGO1+int(2*LBOT/3),LBOT+LTEXALTURA), (LTEXLARGO1+int(2*LBOT/3),LBOT), 1)
        pg.draw.line(ventana, (0,0,0), (LTEXLARGO1+LTEXLARGO2,LBOT), (LTEXLARGO1+LTEXLARGO2,LBOT+LTEXALTURA), 1)
    pg.display.update()


def movimiento1(ventana):
    global M
    j=-1
    raton=pg.mouse.get_pos()
    for i in range(N):
         if R[i].collidepoint(raton) :
            j=i
            M=5

    return j


def movimiento2(ventana,lista):
    global M
    #Hay que coger los tres elementos y ordenarlos
    aux = []

    #El mayor elemento sera aux[2] y el menor aux[0]
    aux = sorted(lista)

    #Ahora miramos que se trata de un movimiento valido
    #Mirar que las monedas son equidistantes y que la moneda de mas a la dcha es cara
    if (aux[2]-aux[1]==aux[1]-aux[0] and P[aux[2]]==1):
        M = 1
        for i in range(len(aux)):
            P[aux[i]]=1-P[aux[i]]
    else :
        M = 2

# def movimiento3(ventana): #Volver al menu
#     global M, T, RT, P
#     raton = pg.mouse.get_pos()
#     if rtextoVolverMenu.collidepoint(raton):
#         return True


def movimientoMaquina(ventana):
    global M,T,P, RT
    auxP= P[:]
    if(buscarP()==False):
        M = 3
        T = 2
        RT = 1
        return
    pos, lista = clastur(P)
    if pos=="N" :
        aux=[]
        #Vamos a ver las monedas que han cambiado
        for i in range(len(lista)):
            if lista[i]!=auxP[i] :
                aux.append(i)

        pg.time.wait(2000)
        marco(ventana,aux)
        pg.time.wait(2000)
        M = 0

    else : #Es una posicion P
        i=2
        while i<len(lista):
            if P[i]==1:
                break
            i=i+1
        if(i==len(lista)): #FINAL DEL JUEGO, gana el jugador
            M = 3
            T = 2
            RT = 1
        else:
            P[i]=1-P[i]
            P[i-1]=1-P[i-1]
            P[i-2]=1-P[i-2]
            pg.time.wait(2000)
            marco(ventana,[i-2,i-1,i])
            pg.time.wait(2000)
            M = 0

    T = 0


def juego ():

    global M, T, RT

    ventana = pg.display.set_mode((LTOTAL, LTEXALTURA+LBOT))
    ventana.fill(blanco) #definimos el fondo de la ventana con el color blanco
    marco(ventana)
    pg.display.set_caption("Turnips")#le damos titulo a la ventana

    pg.display.update()
    final = False

    pg.display.update()
    lista = []
    while not final:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                final = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if(RT): #activamos boton de volver a menu
                    lista = []
                    raton = pg.mouse.get_pos()
                    if rtextoVolverMenu.collidepoint(raton):
                        final = True
                        return

                else:
                    j = movimiento1(ventana)
                    if j in lista:
                        #deselecciono
                        lista.remove(j)
                    else:
                        lista.append(j)

                marco(ventana,lista)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if(len(lista)!=3):
                        M = 2
                        lista = []
                    else:
                        movimiento2(ventana,lista)
                        lista=[]
                        if(M==1):
                            T=1
                            marco(ventana)
                            movimientoMaquina(ventana)
                            if(buscarP()==False and M!=3):
                                M = 4
                                T = 2
                                RT = 1
                    marco(ventana)
            pg.display.update()


def iniciarMenu():
    ventana = pg.display.set_mode((LMENU,LMENU))
    ventana.fill(blanco) #definimos el fondo de la ventana con el color blanco

    marcoMenu(ventana)
    pg.display.set_caption("Turnips")#le damos titulo a la ventana

    pg.display.update()

def main():
    global N, LBOT
    iniciarMenu()
    final = False

    pg.display.update()

    while not final:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                final = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                raton = pg.mouse.get_pos()

                if rboton1menu.collidepoint(raton): #reglas
                    iniciarReglas()
                    iniciarMenu()

                elif rboton2menu.collidepoint(raton): #7 monedas
                    N = 7
                    inicializar()
                    juego()
                    iniciarMenu()
                elif rboton3menu.collidepoint(raton) : #10 monedas
                    N=10
                    inicializar()
                    juego()
                    iniciarMenu()
                elif rboton4menu.collidepoint(raton) : #15 monedas
                    N=15
                    inicializar()
                    juego()
                    iniciarMenu()
            pg.display.update()

    pg.quit()

if __name__== '__main__':
    pg.init()
    main()
