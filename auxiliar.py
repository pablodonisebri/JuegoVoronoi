#import pygame
import random
import scipy.spatial as sp
from scipy.spatial import Delaunay
import sys
from numpy.linalg import det

import numpy

#Area signada de un triangulo dado por tres puntos en el plano
def sarea(A,B,C):
    return (1/2 * ( ((B[0]-A[0])*(C[1]-A[1])) - ( (C[0]- A[0] )*(B[1]-A[1]) )) )

    
#Punto medio del segemento delimitado por los puntos A y B
def midPoint(A,B):
    return [(A[0]+B[0])/2,(A[1]+B[1])/2]

#Mediatriz de la recta r, definida por dos puntos de esta
def mediatriz(r):
    #Vector de la recta
    [A,B]=r
    #Vector perpendicular a la recta
    vp=[-(B[1]-A[1]),B[0]-A[0]]

    #Punto medio de la recta
    m=midPoint(A,B)

    #El otro punto de la mediatriz es el punto medio del segmento al que se le suma el vector perpendicular
    c=[m[0]+vp[0],m[1]+vp[1]]

    return [m,c] #Igual que en los demás métodos, la recta perpendicular se devuelve como dos puntos de esta


#Obtencion del punto de interseccion de las rectas r y s
def lineIntersection(r,s):
    #Las rectas vienen dadas como dos puntos de esta
    #Se van a estudiar las rectas en la forma y=mx+c

    #Casos no degenerados
    if (r[1][0]-r[0][0])!=0 and (s[1][0]-s[0][0])!=0:
        #Pendientes de las rectas
        m1=(r[1][1]-r[0][1])/(r[1][0]-r[0][0])
        m2=(s[1][1]-s[0][1])/(s[1][0]-s[0][0])
        #Terminos independientes
        c1=r[0][1]-m1*r[0][0]
        c2=s[0][1]-m2*s[0][0]
        #Son la misma recta
        if m1==m2 and c1==c2 :
            return r
        #Son paralelas pues tienen misma pendiente
        if m1==m2  :
            #print "Son rectas paralelas"
            return []

        #Resolución por Cramer
        x= det(numpy.matrix([[c1,1],[c2,1]]))/det(numpy.matrix([[-m1,1],[-m2,1]]))
        y= det(numpy.matrix([[-m1,c1],[-m2,c2]]))/det(numpy.matrix([[-m1,1],[-m2,1]]))

        return [x,y]
    #Las dos rectas son paralelas al eje Y
    elif  (r[1][0]-r[0][0])==0 and (s[1][0]-s[0][0])==0 :
        print ("Las dos rectas son paralelas al eje y ")
        return []
    #Caso en el que la recta s es paralela al eje y
    elif (s[1][0]-s[0][0])==0 :
         m1=(r[1][1]-r[0][1])/(r[1][0]-r[0][0])
         c1=r[0][1]-m1*r[0][0]

         return [s[0][0],(m1*s[0][0])+c1]
    #Caso en el que la recta r es paralela al eje y
    else  :
         m1=(s[1][1]-s[0][1])/(s[1][0]-s[0][0])
         c1=s[0][1]-m1*s[0][0]

         return [r[0][0],(m1*r[0][0])+c1]

#Funcion para hacer clipping de un poligono con una recta dada
def clipping(P,r):
   #Se va a construir la region resultante en la lista C
   C=[]
   #Para cada punto del poligono
   for i in range(len(P)):
       #Si el punto se encuentra a la izquierda de la recta orientada entonces se añade a C
       if sarea(P[i],r[0],r[1])>=0:
           C.append(P[i])
           #Si este punto es el limite de una arista que corta con la recta se añade el punto de interseccion
           # de la arista con la recta
           if sarea(P[(i+1)%len(P)],r[0],r[1])<0 :
                  C.append(lineIntersection(r,[P[i],P[(i+1)%len(P)]]))
        #Si el punto no esta a la izquierda de la recta pero es el limite de una arista que interseca con la recta
       # se añade el punto de interseccion de la arista con la recta
       elif sarea(P[(i+1)%len(P)],r[0],r[1])>=0:
                  C.append(lineIntersection(r,[P[i],P[(i+1)%len(P)]]))
    #Se devuelve el poligono que se ha contruido
   return C

#Función prestada de la asignatura de GTC
#Calculo del circuncentro del Triangulo definifo por los puntos a,b,c
def circumcenter(a,b,c):
   #Se calcula el area signada del triangulo
   sa=sarea(a,b,c)
   #Si el area signada es cero, se tiene que los tres puntos estan alineados
   if (sa==0):
       return [(a[0]+b[0]+c[0])/3,(a[1]+b[1]+c[1])/3]
    #Se calcula el circuncentro con la elevacion de los puntos a un paraboloide
   cx=det(numpy.matrix([[1,1,1],[a[1],b[1],c[1]],[a[0]**2+a[1]**2,b[0]**2+b[1]**2,c[0]**2+c[1]**2]]))/(-4*sa)
   cy=det(numpy.matrix([[1,1,1],[a[0],b[0],c[0]],[a[0]**2+a[1]**2,b[0]**2+b[1]**2,c[0]**2+c[1]**2]]))/(4*sa)
   return [cx,cy]



#Region de Voronoi para un punto dentro un conjunto de puntos
def voronoiRegion(p,i):
    #Si solo hay un punto en el plano, su region es toda la region del plano
    if len(p)==1 and i==0:
        #medidas que delimitan la pantalla
        return [[0,0],[700,0],[700,700],[0,700]]
    #Si hay mas puntos
    else:
        #Se comienza con la region de la pantalla
        Region=[[0,0],[700,0],[700,700],[0,700]]
        #Se va a hacer clipping con las mediatrices de los demas puntos del conjunto
        for k in range (len(p)):
            if k!=i :
                Region=clipping(Region,mediatriz([p[i],p[k]]))

        return Region




# Obtenida de: https://plot.ly/python/v3/polygon-area/
#Funcion para calcular el area de un poligono que es pasado como parametro a la funcion en forma de lista de vertices
def Area(corners):
    n = len(corners)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area



#Funcion auxiliar que sera empleada para la obtencion de los puntos del infinito de las regiones no acotadas
def infinityPoint(e,S,D):
        A=D.points[e[0]]#Coordenada del primer punto de la arista 'e'
        B=D.points[e[1]]#Coordenada del segundo punto de la arista 'e'
        #Vector AB
        U=numpy.array(B)-numpy.array(A)
        #Vector perpendicular a AB
        V=numpy.array([-U[1],U[0]])
        #Circuncentro del triangulo dado por el simplice 'S'
        cir=circumcenter(D.points[S[0]],D.points[S[1]],D.points[S[2]])
        #se pasa a numpy.array para poder ser sumado a otro punto
        m=numpy.array(cir)
        #Se calcula el punto como el circuncentro del simolice  mas el vector perpendicular a la arista de la frontera
        # dada por 's'
        return (m+5000*V).tolist()

#Recibe la triangulación ya hecha
def Voronoi(D):
    #Se v a construir el diagrama añadiendo las regiones ya construidas en la lista V
    V=[]
    #Numero de puntos
    N=len(D.points)
    #Para cada punto saber su region
    for v in range(N) :
        Region=[]
        #Ver en que simplice esta, uno arbitrario
        s=D.vertex_to_simplex[v]
        #Necesitamos guardar en una variable auxiliar este vertice para cuando lleguemos a la frontera saber volver
        saux=s
        ultimos=saux

        #Construir la region metiendo primero el circuncentro del simplice al que sabemos que pertenece
        #c=circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
        #Region.append(c)
        #Viajamos a las regiones
        while True:
           ultimos=s
           #Se añade el circuncentro de la region a la que hemos viajado
           c=circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
           Region.append(c)
           #Viajamos al siguiente vecino
           n=list(D.simplices[s]).index(v)
           s=D.neighbors[s][(n+2)%3]
           #Si llegamos a la frontera o hemos dado una vuelta entera por no ser region acotada
           if s==saux or s==-1:

               break
        #Si hemos dado una vuelta completa
        if s!=-1:
             #Hacemos clipping con la pantalla por si
             #Region=clipping(Region,[[0,0],[700,0]])
             #Region=clipping(Region,[[0,700],[0,0]])
             #Region=clipping(Region,[[700,700],[0,700]])
             #Region=clipping(Region,[[700,0],[700,700]])
            #Añadimos la region al Diagrama
             V.append(Region)
             continue
        #Si hemos llegado a la frontera, se trata de una region no acotada
        else:
           #Calculamos el primer punto del infinito
           inf1=infinityPoint([D.simplices[ultimos][((n+1)%3)],v],D.simplices[ultimos],D)
           #Se añade a la region
           Region.append(inf1)
           #Se debe volver al simplice que incialmente ha devuelto la llamada vertex_to_simplex
           s=saux
            #Se debe ahora viajar en sentido contrario por las regiones vecinas
           while True:
               ultimos=s
               if s!=saux:
                   c=circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
                   Region.insert(0,c)
                   #Region.append(c)
               n=list(D.simplices[s]).index(v)
               s=D.neighbors[s][(n+1)%3]
               #Cuando se llega a la frontera
               if  s==-1:
                   break
           #Se añade el segundo punto del infinito y ya se dispine de toda la region no acotada, pero debe ser intersecada
           # con el rectangulo que representa la pantalla
           inf2=infinityPoint([v,D.simplices[ultimos][((n+2)%3)]],D.simplices[ultimos],D)
           Region.insert(0,inf2)
           Region=clipping(Region,[[0,0],[700,0]])
           Region=clipping(Region,[[0,700],[0,0]])
           Region=clipping(Region,[[700,700],[0,700]])
           Region=clipping(Region,[[700,0],[700,700]])
           V.append(Region)
   #Se devuelve el diagrama ya construido, constituido por las regiones asociadas a los puntos
    return V




