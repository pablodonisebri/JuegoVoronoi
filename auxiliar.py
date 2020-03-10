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
    [Ap,Bp]=[[-B[0],-B[1]],A] # Vector perpendicular a la recta
    vp=[Bp[0]-Ap[0],Bp[1]-Ap[1]]#Vector perpendicular a la recta
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
       print ("alineados")
       return

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
    j=(i+1)%len(p)
    [A,B]=mediatriz([p[i],p[j]])
    v=[B[0]-A[0],B[1]-A[1]]
    #Creamos un cuadrilatero infinito alrededor
    A0=[A[0]-10000*v[0],A[1]-10000*v[1]]
    A1=[A[0]+10000*v[0],A[1]+10000*v[1]]
    A2=[A1[0]-10000*v[1],A1[0]+10000*v[0]]
    A3=[A0[0]-10000*v[1],A0[0]+10000*v[0]]

    R=[A0,A1,A2,A3]

    for k in range (len(p)):
        if k!=i and k!=j:
            #Hacemos clipping con las mediatrices de los segmentos que le unen a los otros puntos
            R=clipping(R,mediatriz([p[i],p[k]]))
    R=clipping(R,[[0,0],[700,0]])
    R=clipping(R,[[0,700],[0,0]])
    R=clipping(R,[[700,700],[0,700]])
    R=clipping(R,[[700,0],[700,700]])
    return R

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




