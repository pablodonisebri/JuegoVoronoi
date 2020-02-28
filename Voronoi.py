import pygame
import random
import scipy.spatial as sp
from scipy.spatial import Delaunay
import sys
from numpy.linalg import det
import numpy
import numpy.matrixlib as np
import auxiliar

#############################################COMINENZO PROGRAMA####################################################

p=[[random.random(), random.random()] for i in range(10)]#La llamada a random da números entre 0 y 1
V=[]
D=Delaunay(p,incremental=True)

for T in D.simplices:#T es cada triangulo, que esta dado como tres indices de D.points() de los vertices que lo forman
    break


print(D.simplices)
print(D.neighbors)
print(D.convex_hull)




p2=[[random.random(),random.random()]for i in range(6)]
#D.add_points(p2)



#print(D.neighbors)
#print(D.simplices)


#Recibe la triangulación ya hecha, me interesa mas que sea asi ya que la triangulacion tiene la opcion incremental
def Voronoi(D):
    def infinityPoint(e,D):
        A=D.points[e[0]]#Coordenada del primer punto de la arista
        B=D.points[e[1]]
        U=numpy.array(B)-numpy.array(A)
        V=numpy.array([-U[1],U[0]])
        F=[0,0]###TODO: ENCONTRAR PUNTO F DE MANERA OPTIMA
        cir=auxiliar.circumcenter(e[0],e[1],F)
        m=numpy.array(cir)
        return list(m+1000000*V)
    V=[]
    N=len(D.points)#Numero de puntos
    #Para cada punto saber su region
    for v in range(N) :
        L=[A for A in D.simplices if v in A]#Todos los simplices en los que esta el vertice
        I=[E for E in D.convex_hull if v in E]#Aristas a las que pertenece el punto y que estan en el cierre convexo

        #Region del punto dada por los vertices que forman la region
        R=[auxiliar.circumcenter(D.points(L[0]),D.points(L[1]),D.points(L[2]))]+[infinityPoint(e,D)for e in I]
        V.append(R)
    return V

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




# #Inicializamos pygame
# pygame.init()
#
#
#
# #Establecemos el tamaño de la ventana.
# ventana = pygame.display.set_mode((700,700))
# #podemos ponerle titulo a nuestra ventana, entre otras cosas,
# #icono, que sea redimensionable...
# pygame.display.set_caption("TFG")
# for v in V:
#     pygame.draw.polygon(v,(random.random()*255,random.random()*255,random.random()*255))
#
# #Bucle de "Juego"
# while True:
#     for event in pygame.event.get():    #Cuando ocurre un evento...
#         if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
#             pygame.quit()               #Se cierra pygame
#             sys.exit()                  #Se cierra el programa
#         else:
#
#             print("")
#
#
#     pygame.display.flip()               #Genera la ventana






