import pygame
import random
import scipy.spatial as sp
from scipy.spatial import Delaunay
from scipy.spatial import Voronoi
from scipy.spatial import ConvexHull
import sys
from numpy.linalg import det
import numpy
import numpy.matrixlib as np
import auxiliar

#############################################COMINENZO PROGRAMA####################################################

p=[[random.random()*700, random.random()*700] for i in range(4)]#La llamada a random da números entre 0 y 1

D=Delaunay(p,incremental=True)
#V=Voronoi(p)



#Recibe la triangulación ya hecha, me interesa mas que sea asi ya que la triangulacion tiene la opcion incremental
# def Voronoi(D):
#     def infinityPoint(e,D):
#         A=D.points[e[0]]#Coordenada del primer punto de la arista
#         B=D.points[e[1]]#Coordenada del segundo punto de la arista
#
#         U=numpy.array(B)-numpy.array(A)
#
#         V=numpy.array([-U[1],U[0]])
#         [S]=[s for s  in D.simplices if e[0] in s and e[1] in s]
#
#         cir=auxiliar.circumcenter(D.points[S[0]],D.points[S[1]],D.points[S[2]])
#         m=numpy.array(cir)
#         return (m+1000000*V).tolist()
#     V=[]
#     N=len(D.points)#Numero de puntos
#     #Para cada punto saber su region
#
#     for v in range(N) :
#         L=[A for A in D.simplices if v in A]#Todos los simplices en los que esta el vertice
#         I=[E for E in D.convex_hull if v in E]#Aristas a las que pertenece el punto y que estan en el cierre convexo
#         #Region del punto dada por los vertices que forman la region
#         #Formada por:
#         #  1.Circuncentros de los simplices en los que esta el punto
#         #  2.Puntos del infinito de las regiones no acotadas(si el punto pertenece al cierre convexo de la triangulacion)
#         R=[auxiliar.circumcenter(D.points[l[0]],D.points[l[1]],D.points[l[2]]) for l in L]+[infinityPoint(e,D)for e in I]
#         CHR=ConvexHull(R)
#         Region=[R[i] for i in CHR.vertices]
#         V.append(Region)
#     return V


###########TODO: Traducir esa funcion a codigo python
# def Voronoi(p):
#     D=Delaunay(p)
#     V=[]
#     def infinityPoint(e,D):
#         A=originCoords(e,D)
#         B=originCoords(twin(e,D),D)
#         u=vector(B)-vector(A)    #Vector de dirección de la arista de delaunay
#         v=vector([-u[1],u[0]])  #Vector perpendicular a la arista de delaunay
#         F=originCoords(prev(twin(e,D),D),D)
#         m=vector(circumcenter(A,B,F)) # Da el vertice de la region de Voronoi
#         return list(m+1000000*v) # Direccion de la arista hacia el infinito, vertice y direccion del vector perpendicular
#     #Para cada punto calcular su region de voronoi y añadirla a V
#     for i in range(len(D[0])):
#         E=vertexEdges(i,D)
#         R=[] #La region
#         for j in E:
#             if face(j,D)==0:#Si va a ser una de las regiones no acotadas hay que llamar a infinty point
#                 R.append(infinityPoint(j,D))
#                 R.append(infinityPoint(prev(j,D),D))
#             else:
#                 R.append(circumcenter(originCoords(j,D),originCoords(next(j,D),D),originCoords(prev(j,D),D)))
#
#         V.append(R)
#     return V



#
# # #Inicializamos pygame
# pygame.init()
#
#
#
# #Establecemos el tamaño de la ventana.
# ventana = pygame.display.set_mode((700,700))
# #podemos ponerle titulo a nuestra ventana, entre otras cosas,
# #icono, que sea redimensionable...
# pygame.display.set_caption("TFG")
# ventana.fill((255,255,255))
# V=Delaunay(p)
# 
# for v in V.simplices:
#     pygame.draw.polygon(ventana,(random.random()*255,random.random()*255,random.random()*255),[V.points[v[0]],V.points[v[1]],V.points[v[2]]])
#
#
#
# #Bucle de "Juego"
# while True:
#     for event in pygame.event.get():    #Cuando ocurre un evento...
#         if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
#             pygame.quit()               #Se cierra pygame
#             sys.exit()                  #Se cierra el programa
#
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             #Obtenemos la posicion del raton que va hasta el punto (700,700)
#             raton = pygame.mouse.get_pos()
#             pygame.draw.circle(ventana,(100,100,100),raton,5)
#             p.append(raton)
#             V=Delaunay(p)
#             print(V.vertices)
#
#             for v in V.simplices:
#                 pygame.draw.polygon(ventana,(random.random()*255,random.random()*255,random.random()*255),[V.points[v[0]],V.points[v[1]],V.points[v[2]]])
#
#             pygame.display.update()
#             #print(raton)
#
#         else:
#
#             print("")
#
#
#     pygame.display.flip()               #Genera la ventana
#
#




