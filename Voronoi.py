import pygame
import random
import scipy.spatial as sp
from scipy.spatial import Delaunay
import sys
import numpy
import auxiliar as aux


#############################################COMINENZO PROGRAMA####################################################

#p=[[random.random()*700, random.random()*700] for i in range(4)]#La llamada a random da números entre 0 y 1
p=[]
#D=Delaunay(p,incremental=True)
#V=Voronoi(p)

def infinityPoint(e,S,D):
        A=D.points[e[0]]#Coordenada del primer punto de la arista
        B=D.points[e[1]]#Coordenada del segundo punto de la arista

        U=numpy.array(B)-numpy.array(A)

        V=numpy.array([-U[1],U[0]])

        cir=aux.circumcenter(D.points[S[0]],D.points[S[1]],D.points[S[2]])
        m=numpy.array(cir)
        return (m+5*V).tolist()

#Recibe la triangulación ya hecha, me interesa mas que sea asi ya que la triangulacion tiene la opcion incremental
def Voronoi(D):
    V=[]
    N=len(D.points)#Numero de puntos
    #Para cada punto saber su region
    for v in range(N) :
        Region=[]
        #Ver en que simplice esta
        s=D.vertex_to_simplex[v]
        saux=s
        ultimos=saux
        #Construir la region metiendo primero el circuncentro del simplice al que sabemos que pertenece
        c=aux.circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
        Region.append(c)
        #Viajamos a las regiones
        while True:
           ultimos=s
           c=aux.circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
           Region.append(c)
           n=list(D.simplices[s]).index(v)
           s=D.neighbors[s][(n+2)%3]
           if s==saux or s==-1:

               break
        if s!=-1:
            V.append(Region)
            continue

        else:
           inf1=infinityPoint([D.simplices[ultimos][((n+1)%3)],v],D.simplices[ultimos],D)
           Region.append(inf1)
           s=saux

           while True:
               ultimos=s
               if s!=saux:
                   c=aux.circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
                   Region.insert(0,c)
                   #Region.append(c)
               n=list(D.simplices[s]).index(v)
               s=D.neighbors[s][(n+1)%3]
               if  s==-1:
                   break
           inf2=infinityPoint([v,D.simplices[ultimos][((n+2)%3)]],D.simplices[ultimos],D)
           Region.insert(0,inf2)
           Region=aux.clipping(Region,[[0,0],[700,0]])
           Region=aux.clipping(Region,[[0,700],[0,0]])
           Region=aux.clipping(Region,[[700,700],[0,700]])
           Region=aux.clipping(Region,[[700,0],[700,700]])
           V.append(Region)

    return V





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
i=0
#Pedimos los primeros puntos
while True:
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton que va hasta el punto (700,700)
                raton = pygame.mouse.get_pos()
                pygame.draw.circle(ventana,(100,100,100),raton,5)
                pygame.display.update()
                p.append(raton)
                i=i+1

                if i ==4:
                    break
    if i==4:
        break


D=Delaunay(p)
V=Voronoi(D)
for v in range (len(p)):
                    if v%2:
                        pygame.draw.polygon(ventana,(0,0,250),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        Area1=aux.Area(V[v])+Area1

                    else:
                        pygame.draw.polygon(ventana,(250,0,0),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        Area2=aux.Area(V[v])+Area2


pygame.display.update()

for po in p:
                 pygame.draw.circle(ventana,(0,0,0),po,5)



#Bucle de "Juego"
while True:

    for event in pygame.event.get():    #Cuando ocurre un evento...
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton que va hasta el punto (700,700)
            raton = pygame.mouse.get_pos()

            p.append(raton)
            D=Delaunay(p)
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
            print(p)
            print(Area1)
            print(Area2)
            pygame.display.update()

            for po in p:
                 pygame.draw.circle(ventana,(0,0,0),po,5)

            pygame.display.update()
            #print(raton)

        else:

            print("")


    pygame.display.flip()               #Genera la ventana





#
