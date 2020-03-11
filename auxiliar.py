#import pygame
import random
import scipy.spatial as sp
from scipy.spatial import Delaunay
import sys
from numpy.linalg import det

import numpy

#def sarea(A,B,C):
    #return (1/2 * ( ((B[0]-A[0])*(C[1]-A[1])) - ( (C[0]- A[0] )*(B[1]-A[1]) )) )
def sarea(A,B,C):
    return (1/2 * ( ((B[0]-A[0])*(C[1]-A[1])) - ( (C[0]- A[0] )*(B[1]-A[1]) )) )

    

def midPoint(A,B):

    return [(A[0]+B[0])/2,(A[1]+B[1])/2]


def mediatriz(r):
    [A,B]=r #Vector de la recta

    vp=[-(B[1]-A[1]),B[0]-A[0]]#Vector perpendicular a la recta
    m=midPoint(A,B)
    c=[m[0]+vp[0],m[1]+vp[1]]

    return [m,c] #Igual que en los demás métodos, la recta perpendicular se devuelve como dos puntos de esta


def lineIntersection(r,s):
    #Ver el determinante con la regla de Kramer
    #Las rectas vienen dadas como dos puntos de esta
    if (r[1][0]-r[0][0])!=0 and (s[1][0]-s[0][0])!=0:
        m1=(r[1][1]-r[0][1])/(r[1][0]-r[0][0])#pendientes
        m2=(s[1][1]-s[0][1])/(s[1][0]-s[0][0])

        c1=r[0][1]-m1*r[0][0]
        c2=s[0][1]-m2*s[0][0]

        if m1==m2 and c1==c2 :
            return r
        if m1==m2  :
            #print "Son rectas paralelas"
            return []

        #Resolución por Cramer
        x= det(numpy.matrix([[c1,1],[c2,1]]))/det(numpy.matrix([[-m1,1],[-m2,1]]))
        y= det(numpy.matrix([[-m1,c1],[-m2,c2]]))/det(numpy.matrix([[-m1,1],[-m2,1]]))

        return [x,y]
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


def clipping(P,r):
   C=[]
   for i in range(len(P)):
       if sarea(P[i],r[0],r[1])>=0:
           C.append(P[i])
           if sarea(P[(i+1)%len(P)],r[0],r[1])<0 :
                  C.append(lineIntersection(r,[P[i],P[(i+1)%len(P)]]))
       elif sarea(P[(i+1)%len(P)],r[0],r[1])>=0:
                  C.append(lineIntersection(r,[P[i],P[(i+1)%len(P)]]))

   return C

#TODO: Preguntar a Manuel por como calcular circuncentro

def circumcenter(a,b,c):
   sa=sarea(a,b,c)
   if (sa==0):

       return [(a[0]+b[0]+c[0])/3,(a[1]+b[1]+c[1])/3]

   cx=det(numpy.matrix([[1,1,1],[a[1],b[1],c[1]],[a[0]**2+a[1]**2,b[0]**2+b[1]**2,c[0]**2+c[1]**2]]))/(-4*sa)
   cy=det(numpy.matrix([[1,1,1],[a[0],b[0],c[0]],[a[0]**2+a[1]**2,b[0]**2+b[1]**2,c[0]**2+c[1]**2]]))/(4*sa)
   return [cx,cy]


def dist2(A,B):
    
    return  ((A[0]-B[0])**2 + (A[1]-B[1])**2)

def angularSort(p,c):
    #Listas left, right y alineados del punto 
    L,R,A = [],[],[]
    for i in p:
        if i[0]<c[0]:
            L.append(i)
        elif i[0]>c[0]:
            R.append(i)
        
        else:
            A.append(i)
    return sorted(R,key=lambda x : [((x[1]-c[1])/(x[0]-c[0])),dist2(x,c)])+ sorted(A,key=lambda x :[1, dist2(x,c)])+sorted(L,key=lambda x : [((x[1]-c[1])/(x[0]-c[0])),dist2(x,c)])


#Region de Voronoi para un punto dentro un conjunto de puntos

def voronoiRegion(p,i):

    if len(p)==1 and i==0:
        return [[0,0],[700,0],[700,700],[0,700]]

    else:
        Region=[[0,0],[700,0],[700,700],[0,700]]
        for k in range (len(p)):
            if k!=i :
                Region=clipping(Region,mediatriz([p[i],p[k]]))
        return Region




#https://plot.ly/python/v3/polygon-area/
def Area(corners):
    n = len(corners)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area




def infinityPoint(e,S,D):
        A=D.points[e[0]]#Coordenada del primer punto de la arista
        B=D.points[e[1]]#Coordenada del segundo punto de la arista

        U=numpy.array(B)-numpy.array(A)

        V=numpy.array([-U[1],U[0]])

        cir=circumcenter(D.points[S[0]],D.points[S[1]],D.points[S[2]])
        m=numpy.array(cir)
        return (m+5000*V).tolist()

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
        c=circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
        Region.append(c)
        #Viajamos a las regiones
        while True:
           ultimos=s
           c=circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
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
                   c=circumcenter(D.points[D.simplices[s][0]],D.points[D.simplices[s][1]],D.points[D.simplices[s][2]])
                   Region.insert(0,c)
                   #Region.append(c)
               n=list(D.simplices[s]).index(v)
               s=D.neighbors[s][(n+1)%3]
               if  s==-1:
                   break
           inf2=infinityPoint([v,D.simplices[ultimos][((n+2)%3)]],D.simplices[ultimos],D)
           Region.insert(0,inf2)
           Region=clipping(Region,[[0,0],[700,0]])
           Region=clipping(Region,[[0,700],[0,0]])
           Region=clipping(Region,[[700,700],[0,700]])
           Region=clipping(Region,[[700,0],[700,700]])
           V.append(Region)

    return V




