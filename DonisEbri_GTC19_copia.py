########################LIBRERIA  GTC 2019-2020 PABLO DONIS EBRI #####################

######################################PRACTICA 0 #############################################
def dist(A,B):
     
     return sqrt((A[0]-B[0])^2 + (A[1]-B[1])^2)


def dist2(A,B):
    
    return  ((A[0]-B[0])^2 + (A[1]-B[1])^2)


def sarea(A,B,C):
    
    return (1/2 * ( ((B[0]-A[0])*(C[1]-A[1])) - ( (C[0]- A[0] )*(B[1]-A[1]) )) )


def orientation(A,B,C):
    
    return sign(sarea(A,B,C))


def midPoint(A,B):
    
    return [(A[0]+B[0])/2,(A[1]+B[1])/2]


def inSegment(P,s):
        if sarea(s[0],s[1],P)>0.001 or sarea(s[0],s[1],P)<-0.001 : 
            
            return false
        if min(s[0][0],s[1][0])<= P[0] and  P[0]<= max(s[0][0],s[1][0]) and min(s[0][1],s[1][1]) <= P[1] and P[1]<= max(s[0][1],s[1][1]):
            return true
        
        return false


def segmentIntersectionTest(a,b):
   a11=sarea(a[0],a[1],b[0]) 
   a12=sarea(a[0],a[1],b[1]) 
   b11=sarea(b[0],b[1],a[0])
   b12=sarea(b[0],b[1],a[1])
   
   
   if a11*a12 <0 and b11*b12 <0 :
       return true 
   #Vamos a contemplar ahora los casos degenerados en los que el area signada es igual a cero porque los segmentos están alienados algunos de 
   #los extremos 
   
   #Para ello vemos si los extremos de alguno de los dos segmentos estan en el otro segmento
   if inSegment(a[0],b) or inSegment(a[1],b): return true
   elif inSegment(b[1],a) or inSegment(b[0],a): return true
   else :return false



def inTriangle(P,t):
    #Para ver que esta dentro del triangulo hay que ver que las tres orientaciones coinciden con la orientacion del triangulo original 
    #siendo to la orientacion del triangulo original 
    to=orientation(t[0],t[1],t[2])
    if orientation(t[0],t[1],P) == orientation(t[2],t[0],P) == orientation(t[1],t[2],P) == to :
        return true    
    else : return false
    #ver los casos degenerados del problema
    





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
        x= Matrix([[c1,1],[c2,1]]).det()/Matrix([[-m1,1],[-m2,1]]).det()
        y= Matrix([[-m1,c1],[-m2,c2]]).det()/Matrix([[-m1,1],[-m2,1]]).det()
        
        
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

def mediatriz(r):
  
   u=vector([r[1][0]-r[0][0],r[1][1]-r[0][1]])#vector que representa el segmento
   v=vector([-u[1],u[0]])#vector perpendicular al segmento
   
   m=vector(midPoint(r[0],r[1]))#punto medio del segmento 
   c=list(m+v)# punto de la recta 
   return [m,c] # la recta se devuelve como dos puntos de esta

def circumcenter(a,b,c):
    a=[a[0]+random()*0.000001,a[1]+random()*0.000001]
    b=[b[0]+random()*0.000001,b[1]+random()*0.000001]
    med1=mediatriz([a,b])
    med2=mediatriz([b,c])
    med3=mediatriz([a,c])
    
    
    corte1=lineIntersection(med1,med2)
 
    corte2=lineIntersection(med1,med3)
    corte3=lineIntersection(med3,med2)
    
    circum=[(corte1[0]+corte2[0]+corte3[0])/3,(corte1[1]+corte2[1]+corte3[1])/3]
   
    return circum

#def circumcenter(a,b,c):
#    sa=sarea(a,b,c)
#    if (sa==0):
#        print ("alineados")
#        return
#    cx=matrix([[1,1,1],[a[1],b[1],c[1]],[a[0]**2+a[1]**2,b[0]**2+b[1]**2,c[0]**2+c[1]**2]]).det()/(-4*sa)
#    cy=matrix([[1,1,1],[a[0],b[0],c[0]],[a[0]**2+a[1]**2,b[0]**2+b[1]**2,c[0]**2+c[1]**2]]).det()/(4*sa)
#    return [cx,cy]



#incircle test. Entrada cuatro puntos a,b,c,d y salida 1, -1 o 0 dependiendo de que el punto d sea interior, exterior o este en la frontera #del circulo que determinan a,b y c.

def svolume(a,b,c,d):
    M=[a,b,c,d]
    for i in M:
        i.insert(0,1)
    m=matrix(M).transpose()
    return m.det()/6

#def inCircle(a,b,c,d):
#   center=circumcenter(a,b,c)
#   if len(center)==0:
#       #print "Caso de fallo, los tres puntos estan alineados"
#       return
#   distance=dist(center,d)
#   distance2=dist(a,center)
#   if distance==distance2: return 0 #es un punto del circulo
#   elif distance2> distance: return 1 # es un punto interior del circulo
#   else : return -1 # es un punto exterior al circulo

def inCircle(a,b,c,d):
    if sarea(a,b,c)==0: 
        print ("Los puntos estan alineados")
        return
    A,B,C,D=copy(a),copy(b),copy(c),copy(d)
    A.append(a[0]**2+a[1]**2),B.append(b[0]**2+b[1]**2),C.append(c[0]**2+c[1]**2),D.append(d[0]**2+d[1]**2)
    return -sign(sarea(a,b,c)*svolume(A,B,C,D))


#######################################################PRACTICA 1 ###################################################################################
def maxmin (P):
    Mx=mx=My=my=P[0]
    
    for i in range(1,len(P)):
        #Guardar en las variables los valores de los maximos y los minimos
        # El formato a devolver sera [Max,minx,Maxy,miny]
        if P[i][0]<mx[0]: 
            mx=P[i]
        if P[i][0]>Mx[0]: 
            Mx=P[i]
        if P[i][1]<my[1]: 
            my=P[i]
        if P[i][1]>My[1]: 
            My=P[i]
        
    return [Mx,mx,My,my]


def xmin (P):
    return maxmin(P)[1]


def xmax (P):
    return maxmin(P)[0]



def ymax (P):
    return maxmin(P)[2]


def ymin (P):
    return maxmin(P)[3]


def boundingBox(p):
    if len(p)==0:
        print( "No hay puntos")
    [Mx,mx,My,my]= maxmin(p)
   
    return [[mx[0],my[1]],[Mx[0],my[1]],[Mx[0],My[1]],[mx[0],My[1]]]


def abscisasSort(p):
     return sorted(p,key=lambda x : x[0])

def ordenadasSort(p):
     return sorted(p,key=lambda x : x[1])



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





#################################################################PRACTICA 2######################################################
# poligonizacion X-monotona

def polygonization(p):
    if not p: return []
    x1=xmax(p)
    x2=xmin(p)
    
    arriba=[]
    debajo=[]
    
    for i in range (len(p)):
        if sarea(x1,p[i],x2)>=0 : debajo.append(p[i])
        else: arriba.append(p[i])
        
    arriba=sorted(arriba)
    debajo=sorted(debajo)
    debajo.reverse()
    
    return arriba+debajo
    
# poligonizacion estrellada

def starPolygonization(p):
   if not p: return []
   c= [(p[0][0]+p[1][0]+p[2][0])/3,(p[0][1]+p[1][1]+p[2][1])/3 ]
   P=angularSort(p,c)
   return P



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


def kernel(p):
    C=copy(p)
    for i in range(len(p)):
        C=clipping(C,[p[i-1],p[i]])

    return 

def pointInPolygon(Q,p):
    n=0
    for i in range (len(Q)):
        #Los dos vertices de la arista a la izqda de mi punto
        if p[0]>Q[i][0] and p[0]>Q[(i+1)%len(Q)][0]: 
           
            continue
        #Punto de interseccion de las dos rectas
        r= lineIntersection( [ p,[p[0]+1,p[1]]],[Q[i],Q[(i+1)%len(Q)]] )
        
        #Si es vacio es que no intersecan
        if len(r)==0: 
            continue
        #Si el punto de interseccion esta a la izqda de mi punto 
        if r[0]<p[0]: 
            continue
        #Si las dos rectas han intersecado pero fuera de la arista
        if inSegment(r,[Q[i],Q[(i+1)%len(Q)]]):
            n=n+1
          
    return (n%2!=0)

    ### funcion auxiliar que detecta si un vertice es oreja en tiempo O(n)    

def earTest(P,i):
   n = len(P)
   if  sarea( P[i-1],P[i],P[(i+1)%n] )>0:
       for j in range(len(P)):
           if j != (i-1)%n and j !=i and j !=(i+1)%n and inTriangle(P[j],[P[(i-1) % n],P[i],P[(i+1)%n]]): 
               return false
       return true 
   else :
        return false
       
    

# devolver el índice del vertice oreja

def ear(P):
    for i in range(len(P)):
        #print earTest(P,i)
        if earTest(P,i):
              return i



def earTriangulation(P):
    Q=copy(P)
    T=[]
    while len(Q)>3:
        e=ear(Q)
        T.append([Q[e-1],Q[e],Q[(e+1)%len(Q)]])
        del Q[e]
    T.append(Q)
    return T


def otectomyTriangulation(P):
    Q=copy(P)
    T=[]
    while len(Q)>3:
        e=ear(Q)
        T.append([Q[e-1],Q[e],Q[(e+1)%len(Q)]])
        del Q[e]
    T.append(Q)
    return T



def sareaPolygon(p):
    a=0
    for i in range(len(p)):
        a+= sarea(p[0],p[i-1],p[i])
    return a



#Buscar vertice mas a la dcha 
#Si es oreja sabemos la diagonal
#Si no es oreja, el vertice que forma la diagonal es el que forma la mayor area signada con i-1,i+1 
def diagonal(p):
        n=len(p)
        punto=xmax(p)
        ind= p.index(punto)
        if earTest(p,ind):
            return [ind-1,(ind+1)%n]
        else :
            dentro=[]
            for e in p:
                if inTriangle(e,[p[ind-1],p[ind],p[(ind+1)%n]]):
                    dentro.append(e)
            dentro=sorted(dentro,key=lambda x : sarea(p[ind-1],x,p[(ind+1)%n]))
            return [ind,p.index(dentro[-1])]



def polygonTriangulation(p):
      T=[]
      if len(p)<=3:
          
          T.append(p)
          return T
          
      [d0,d1]=diagonal(p)
      
      if d0>d1:
          d0,d1=d1,d0
      
      P1=[p[k] for k in range(d0)]+[p[d0]]+[p[k] for k in range(d1,len(p))]
      P2=[p[k] for k in range(d0,d1)]+[p[d1]]
      
      
      return polygonTriangulation(P2)+polygonTriangulation(P1)
      



###########################################################PRACTICA 3 ###################################################################

#Calculo del cierre convexo de una serie de puntos dados 
#Algoritmo de Graham 

def Graham(p):
    q=angularSort(p,xmax(p))
    i=1
    
    while q[(i%len(q))] !=q[-1]:
        while q[i]==q[i-1]:
              del q[i]
        if sarea(q[i-1],q[i],q[(i+1)%len(q)])>0:
            i=i+1
        else :
            del(q[i])
            i=i-1
    return q



def Jarvis(p):  
   m=xmax(p)
   CC=[m]
   n=len(p)
   
   for j in range(n):
       C=p[0]
       if C==m:
           C=p[1]
       for i in range (1, n):
           if sarea(CC[-1],C,p[i])<0:
               C=p[i]
       if C == CC[0]:
           return CC 
           break        
       else: CC.append(C)


def envolvente (p,A,B):
    if len(p)==0:
        return [A]
    m=0 
    n=len(p)
    
    for i in range (n):
        if sarea(A,p[i],B)>sarea(A,p[m],B):
            m=i
    M=p[m]
    R=[]
    L=[]
   
    for i in range (n):
        if sarea(M,A,p[i])>0:
            R.append(p[i])
        if sarea(B,M,p[i])>0:
            L.append(p[i])
    return envolvente(L,M,B)+envolvente(R,A,M)


def quickhull(p):
    A=xmax(p)
    B=xmin(p)
    return envolvente(p,A,B)+envolvente(p,B,A)



def verticeSeleccion(p):
    n=len(p)
    CC=copy(p)
    #todos los posibles triangulos
    p1=Combinations(p,3).list()
    for point in p:
        for triangle in p1:
            if inTriangle(point,triangle) and point!=triangle[0] and point != triangle[1] and point!=triangle[2]:
                CC.remove(point)
                break
    CC=starPolygonization(CC)
    return CC


def aristaSeleccion(p):
    n=len(p)
    #Hacemos las combinaciones de dos elementos 
    p1=Combinations(p,2).list()
    CC=[]
    for arista in p1:
        esta=true
        for i in range(n):
            if orientation(arista[0],arista[1],p[i])!=orientation(arista[0],arista[1],p[i-1]):
                if p[i]!=arista[0] and p[i]!=arista[1] and p[i-1]!=arista[0] and p[i-1]!=arista[1]:
                    esta=false
                    break
                else: continue
        #una vez acabado el bucle hay que ver si se ha llegado al final o ha sido interrumpido
        if esta==true:
            CC.append(arista[0])
            CC.append(arista[1])
            
    
    CC=starPolygonization(CC)
    
    return CC


def preProcesado(p):
    #t0=time()
    [p1,p2,p3,p4]= maxmin(p)
    CC=[p1,p2,p3,p4]
    n=len(p)
   
    #seleccionamos los candidatos al cierre convexo
    for i in range(n):
        if inTriangle(p[i],[p1,p3,p4]) or inTriangle(p[i],[p2,p3,p4]):
            continue
        else: CC.append(p[i])
    #t1=time()
    #print "Han quedado para evaluar",len(CC)
    #print "Se ha tardado en preprocesar", t1-t0 
   
    #t0=time()
    CC=Graham(CC)
    #t1=time()
    #print "El algoritmo ha tardado:", t1-t0 

    return CC



def diametroFB(p):#fuerza bruta 
    max=0
    elementos=[]
    p1=Combinations(p,2).list()
    for pareja in p1:
        if dist(pareja[0],pareja[1])>max:
            max=dist(pareja[0],pareja[1])
            elementos=pareja
    return elementos


def diametroFR(p):#fuerza refinada 
    p=Graham(p)
    max=0
    elementos=[]
    p1=Combinations(p,2).list()
    for pareja in p1:
        if dist(pareja[0],pareja[1])>max:
            max=dist(pareja[0],pareja[1])
            elementos=pareja
    return elementos


def diameter(p):#rotating caliper
    n=len(p)
    #Sabemos que estas funciones usan el orden lexicografico
    m1,m2=min(p),max(p)
    i,j=p.index(m1),p.index(m2)
    jinicio=j
    diametro=dist(p[i],p[j])
    D=[i,j]
    #Vectores de las rectas
    vi=vector([0,-1])
    vj=-vi
    #El bucle solo debe dar media vuelta al cierre convexo
    while i!=jinicio:
        #vectores pipi+1 y pjpj+1
        ui=vector([p[(i+1)%n][0]-p[i][0],p[(i+1)%n][1]-p[i][1]])
        uj=vector([p[(j+1)%n][0]-p[j][0],p[(j+1)%n][1]-p[j][1]])
        #Angulos que forman ui con vi y uj con vj (realmente es el coseno del angulo)
        Oi=vi*ui/(vi.norm()*ui.norm())
        Oj=vj*uj/(vj.norm()*uj.norm())
        #Si el angulo i es menor (tiene mayor coseno) se actualiza i 
        if Oi>Oj: 
            #Se rota la recta un angulo Oi
            vi=vector([p[(i+1)%n][0]-p[i][0],p[(i+1)%n][1]-p[i][1]])
            vj=-vi
            i=(i+1)%n
        else :
            #Se rota la recta un angulo Oj
            vj=vector([p[(j+1)%n][0]-p[j][0],p[(j+1)%n][1]-p[j][1]])
            vi=-vj
            j=(j+1)%n
        #Si el diametro es mayor se actualiza 
        if dist(p[i],p[j])>diametro:
            diametro=dist(p[i],p[j])
            D=[i,j]
   
    return [p[D[0]],p[D[1]]]


#Algoritmo de Graham adaptado para obtener una triangulación 
def GrahamTriangulation(p):
    #triangulos del abanico
    n=len(p)
    T=[]
    m=max(p)
    p.remove(m)
    q=angularSort(p,m)
    q=q+[m]
    for i in range(n-2):
        T.append([q[-1],q[i],q[i+1]])
    
    i=1
    #scan de graham
    while q[(i%len(q))] !=q[-1]:
        if sarea(q[i-1],q[i],q[(i+1)%len(q)])>=0:
            i=i+1
        else :
            T.append([q[i],q[i-1],q[i+1]])
            del(q[i])
            i=i-1
    return T




######################################################PRACTICA 4 ####################################################################

# funcion que crea un DCEL, para un poligono
def dcel(P):
    n=len(P)
    V=[[P[i],i] for i in range(len(P))]
    e=[[i,n+i,(i-1)%n,(i+1)%n,1]for i in range(n)]+[[(i+1)%n,i,n+(i+1)%n,n+(i-1)%n,0]for i in range(n)]
    f=[n,0]
    return [V,e,f]

# funciones para referirse a los elementos asociados a un elemento del DCEL

# indice del origen de una arista e
def origin(e,D):
    return D[1][e][0]

# coordenadas del origen de la arista e
def originCoords(e,D):
    return D[0][origin(e,D)][0]

# arista gemela de la arista e    
def twin(e,D):
    return D[1][e][1]

# arista previa de la arista e    
def prev(e,D):
    return D[1][e][2]

# arista siguiente de la arista e    
def next(e,D):
    return D[1][e][3] 

# indice de la cara de cuyo borde forma parte la arista e    
def face(e,D):
    return D[1][e][4]               

# indice de una de las aristas del borde de la cara c
def edge(c,D):
    return D[2][c]
        
# funcion para dibujar las aristas de un DCEL



#PlotDCel que marca los indices de los vertices y de las aristas 
def plotDCELNum2(D):
   return sum(line([originCoords(i,D),originCoords(twin(i,D),D)],aspect_ratio=1) for i in range(len(D[1])))+sum(text(i,[D[0][i][0][0]+0.03,D[0][i][0][1]+0.03])for i in range (len(D[0])))+sum(text(i,[(2/3)*(originCoords(i,D)[0])+(1/3)*(originCoords(twin(i,D),D)[0]),(2/3)*(originCoords(i,D)[1])+(1/3)*(originCoords(twin(i,D),D)[1])],color="red") for i in range(len(D[1]))) 

#Plot dcel que marca los indices de los vertices
def plotDCELNum(D):
	return sum(line([originCoords(i,D),originCoords(twin(i,D),D)],aspect_ratio=1) for i in range(len(D[1])))+sum(text(i,[D[0][i][0][0]+0.03,D[0][i][0][1]+0.03])for i in range (len(D[0])))


def plotDCEL(D):
 return sum(line([originCoords(i,D),originCoords(twin(i,D),D)],aspect_ratio=1)for i in range(len(D[1])))     
# funcion para colorear una cara de un DCEL

def plotFace(c,D,col):

    f=D[2][c]
    C=[f]
    f=next(f,D)
    while f != C[0]:
        C.append(f)
        f=next(f,D)
    
    P=[originCoords(j,D) for j in C]
    return polygon(P,color=col, alpha=.5)     

# funcion para colorear las caras de un DCEL
    
def colorDCEL(D):
    return sum(plotFace(i,D,(random(),random(),random())) for i in range(1,len(D[2])))


# funcion para dividir una cara del DCEL D por una diagonal
# e1 y e2 son las aristas cuyos orígenes son los extremos de la diagonal que divide la cara

def splitFace(e1,e2,D):
    
    # si no son aristas de la misma cara o si son adyacentes sus origenes no definen una diagonal
    if face(e1,D) != face(e2,D) or origin(e2,D) == origin(twin(e1,D),D) or origin(e1,D) == origin(twin(e2,D),D):
        print ("no diagonal")
        return
    
    nv, ne, nf = len(D[0]), len(D[1]), len(D[2])
    preve1 = prev(e1,D)
    preve2 = prev(e2,D)
    k=face(e1,D)
    
    # añadimos las aristas nuevas
    D[1].append([origin(e1,D),ne+1,preve1,e2,k])
    D[1].append([origin(e2,D),ne,preve2,e1,nf])
    
    # modificamos aristas afectadas
    D[1][preve1][3]=ne
    D[1][e1][2]=ne+1
    D[1][preve2][3]=ne+1
    D[1][e2][2]=ne
    i=e1
    while i!=ne+1:
        D[1][i][4]=nf
        i=next(i,D)
    
    #modificamos la cara afectada
    D[2][k]=ne
    
    # añadimos la nueva cara
    D[2].append(ne+1)

#obtenga la lista de los indices de las aristas del borde de la cara c del DCEL D (en el orden en que aparecen al recorrer el borde de c)
def faceEdges(c,D):
    #arista que esta en la lista de caras
    arista=D[2][c]
    edges=[arista]
    siguiente=next(arista,D)
    while siguiente!=arista:
        edges.append(siguiente)
        siguiente=next(siguiente,D)
    return edges

#obtenga la lista de los indices de los vertices del borde de la cara c del DCEL D (en el orden en que aparecen al recorrer el borde de c)
def faceVertices(c,D):
    edges=faceEdges(c,D)
    vertices=[]
    for e in edges:
        vertices.append(origin(e,D))
        
    return vertices

def faceVerticesCoords(c,D):
    edges=faceEdges(c,D)
    vertices=[]
    for e in edges:
        vertices.append(originCoords(e,D))
       
    return vertices


#obtenga la lista de los indices de las caras vecinas de la cara c del DCEL D (en el orden en que aparecen al recorrer el borde de c)
def faceNeighbors(c,D):
    edges=faceEdges(c,D)
    vecinas=[]
    for e in edges :
        cara=face(twin(e,D),D)
        vecinas.append(cara)
    return vecinas


#obtenga la lista de los indices de las aristas del DCEL D cuyo origen es v (en orden angular positivo)
def vertexEdges(v,D):
   
    aristas=[D[0][v][1]]
    aux=twin(prev(aristas[-1],D),D)
    while aux != aristas[0]:
        aristas.append(aux)
        aux=twin(prev(aristas[-1],D),D)
    
    return aristas


#que obtenga la lista de los indices de las caras del DCEL D que contienen al vértice v en su borde (en orden angular positivo)
def vertexFan(v,D) :
    aristas=vertexEdges(v,D)
    caras=[]
    for a in aristas:
        caras.append(face(a,D))
    return caras

#Define una función convexHullDCEL(D) que triangule el exterior del borde de la cara externa iterando la función splitFace
def convexHullDCEL(p):
    m=min(p)
    p.remove(m)
    P=[m]+angularSort(p,m)
    p.append(m)
    D=dcel(P)
    e0=len(D[1])-1
    e=next(e0,D)
    while e != e0:
        if sarea(originCoords(e,D),originCoords(next(e,D),D), originCoords(next(next(e,D),D),D))>0:
            aux = prev(e,D)
            splitFace(e,next(next(e,D),D),D)
            if aux !=e0:
                e=aux
            else:
                e=next(e0,D)
        else:
             e=next(e,D)      
    return D



#triangulation(p) que obtenga el DCEL de una triangulación de la lista de puntos p.
def triangulation(p):
    D=convexHullDCEL(p)
    for i in range ((len(p)-2),1,-1):
        splitFace(0,i,D)
    return D



###################################################################### PRACTICA 5 ####################################################################
#Delaunay para un conjunto P de puntos 
def delaunay(p):
    T=[]
    for i in Combinations(p,3):
        de=true 
        for j in p:
            if inCircle(i[0],i[1],i[2],j)==1 and j!=i[0] and j!=i[1] and j!=i[2]:
                de=false
                break
        if de:
            T.append(i)
    return T


#Función para hacer flip de una arista en un DCEL
def flip(a,D):
    oa=D[1][a][0]
    ga=D[1][a][1]
    ca=D[1][a][4]
    aa=D[1][a][2]
    pa=D[1][a][3]
    cb=D[1][ga][4]
    ab=D[1][ga][2]
    pb=D[1][ga][3]
    oga=D[1][ga][0]
    D[1][a]=[D[1][aa][0],ga,pa,ab,ca]
    D[1][ga]=[D[1][ab][0],a,pb,aa,cb]
    D[1][pa][2]=ab
    D[1][pa][3]=a
    D[1][aa][2]=ga
    D[1][aa][3]=pb
    D[1][aa][4]=cb
    D[1][pb][2]=aa
    D[1][pb][3]=ga
    D[1][ab][2]=a
    D[1][ab][3]=pa
    D[1][ab][4]=ca
    D[2][ca]=a
    D[2][cb]=ga
    D[0][oa][1]=pb
    D[0][oga][1]=pa

    return


#Función que decide si se puede hacer flip con una arista del DCEL
def flipable(a,D):
    if face(a,D)==0 or face(twin(a,D),D)==0:
        return false
    return segmentIntersectionTest([originCoords(a,D),originCoords(twin(a,D),D)],[originCoords((prev(a,D)),D),originCoords(prev(twin(a,D),D),D)])


#Define una función legal(a,D) que analice si la arista a del DCEL D es legal
def legal(a,D):
    if not flipable(a,D): return true
    # indice de la cara de cuyo borde forma parte la arista e 
    #vertices que van a formar el triangulo   
    c1=originCoords(a,D)
    c2=originCoords(twin(a,D),D)
    c3=originCoords(next(next(a,D),D),D)
    #c4 vertice que vemos si esta en el circulo
    c4=originCoords(prev(twin(a,D),D),D)
    
    return (inCircle(originCoords(a,D),originCoords(next(a,D),D),originCoords(next(next(a,D),D),D),originCoords(prev(twin(a,D),D),D))<0)and (inCircle(originCoords(a,D),originCoords(next(a,D),D),originCoords(prev(twin(a,D),D),D),originCoords(next(next(a,D),D),D))<0)


def legalize(T):
    #Funcion que dice si hay aristas ilegales y en que posicion estan
    def legales(T):
        for e in range(len(T[1])):
            if not legal(e,T):
                return e
        return -1#Se devuelve -1 si todas son legales 
    l=legales(T)
    while l!=-1:
        flip(l,T)
        l=legales(T)
    return


#Define una función legalize(T) que legalice las aristas de la triangulación T mediante flips
def legalizeClase(T):
    pendientes=[0..len(T[1])-1] #indices de las aristas
    while pendientes:
        e = pendientes.pop()
        if not legal(e,T):
            flip(e,T)
            anadir=[]
            if prev(e,T) not in pendientes : anadir.append(prev(e,T))
            if next(e,T) not in pendientes : anadir.append(next(e,T))
            if prev(twin(e,T),T) not in pendientes : anadir.append(prev(twin(e,T),T))
            if next(twin(e,T),T) not in pendientes : anadir.append(next(twin(e,T),T))
            pendientes+=anadir
    return


def DelaunayClase(p):
    T=triangulation(p)
    legalizeClase(T)
    return T

#Define la función delone(p) que calcule la triangulación de Delaunay de una lista de puntos p
def Delaunay(p):
    T=triangulation(p)
    legalizeClase(T)
    return T

#################################################################PRACTICA 6 ###########################################################################################

#Region de Voronoi para un punto dentro un conjunto de puntos
def voronoiRegion(p,i):
    j=(i+1)%len(p)
    [A,B]=mediatriz([p[i],p[j]])
    v=vector(B)-vector(A)
    #Creamos un cuadrilatero infinito alrededor
    A0=list(vector(A)-1000000*v)
    A1=list(vector(A)+1000000*v)
    A2=list(vector(A1)+1000000*vector([-v[1],v[0]]))
    A3=list(vector(A0)+1000000*vector([-v[1],v[0]]))
    R=[A0,A1,A2,A3]
 
    for k in range (len(p)):
        if k!=i and k!=j:
            #Hacemos clipping con las mediatrices de los segmentos que le unen a los otros puntos
            R=clipping(R,mediatriz([p[i],p[k]]))
            
    return R



def voronoi(p,R):
     V=[]
     #Para cada punto del conjunto se calcula su region de voronoi
     #Se hace append de su region de voronoi que viene dada como un poligono
     for i in range(len(p)):
          C=VoronoiRegion(p,i)
          for i in range (4):
              C=clipping(C,[R[i],R[(i+1)%len(R)]])
         
          V.append(C)
     return V


def Voronoi(p):
    D=Delaunay(p)
    V=[]
    def infinityPoint(e,D):
        A=originCoords(e,D)
        B=originCoords(twin(e,D),D)
        u=vector(B)-vector(A)
        v=vector([-u[-1],u[0]])
        F=originCoords(prev(twin(e,D),D),D)
        m=vector(circumcenter(A,B,F))
        return list(m+1000000*v)
    #Para cada punto calcular su region de voronoi y añadirla a V 
    for i in range(len(D[0])):
        E=vertexEdges(i,D)
        R=[]
        for j in E:
            if face(j,D)==0:
                R.append(infinityPoint(j,D))
                R.append(infinityPoint(prev(j,D),D))
            else:
                R.append(circumcenter(originCoords(j,D),originCoords(next(j,D),D),originCoords(prev(j,D),D)))
            
        V.append(R)
    return V


#Funcion que calcula un diagrama de Voronoi haciendo clipping igual que la funcion voronoi pero ahora trabaja con DCEL
def VoronoiClipping(p):
    D=Delaunay(p)
    V=[]
    def VoronoiRegion(i):
        E=vertexEdges(i,D)
        
        [A,B]=mediatriz([originCoords(E[0],D),originCoords(twin(E[0],D),D)])
        v=vector(B)-vector(A)
        A0=list(vector(A)-1000000*v)
        A1=list(vector(A)+1000000*v)
        A2=list(vector(A1)+1000000*vector([-v[1],v[0]]))
        A3=list(vector(A0)+1000000*vector([-v[1],v[0]]))
        R=[A0,A1,A2,A3]
        
        for k in range(len(E)):
            if k!=0:
                R=clipping(R,mediatriz([originCoords(E[k],D),originCoords(twin(E[k],D),D)]))        
        return R 
        
    for i in range(len(D[0])):
        V.append(VoronoiRegion(i))
    return V


#Funcion que dada una triangulacion de Delaunay devuelve las que son menores que r dado
def shortEdges(D,r):
    E=[]
    for i in range (len(D[1])):
        if dist(originCoords(i,D),originCoords(twin(i,D),D))<=r:
            E.append(i)
    return E


#Los vertices de un diagrama de Voronoi para una triangulacion de Delaunay 
#Son los circuncentros de los triangulos de Delaunay
def VoronoiVertices(D):
    vertices=[]
    for i in range (1,len(D[1])):
        vertices.append(circumecenter(originCoords(i,D),originCoords(prev(i,D),D),originCoords(next(i,D),D)))
    return vertices


#################################################################PRACTICA 8 ###########################################################################################

def chainComplex(D):
  #Lista de las aristas definidas por los indices de sus extremos, no estan las gemelas, se dan como [menor,mayor]
  edges=[]
  for i in range(len(D[1])):
      if [min(origin(twin(i,D),D),origin(i,D)),max(origin(twin(i,D),D),origin(i,D))] not in edges:
         edges.append([min(origin(twin(i,D),D),origin(i,D)),max(origin(twin(i,D),D),origin(i,D))])
 
  #Ordenar la lista por longitud de sus aristas
  edges=sorted(edges,key=lambda x: dist(originCoords(x[0],D),originCoords(x[1],D)))
  
  #Las caras del DCEL menos la 0, definidas por los indices de los extremos
  faces=[[origin(edge(i,D),D),origin(prev(edge(i,D),D),D),origin(prev(prev(edge(i,D),D),D),D)] for i in range(1,len(D[2]))] 
  return [[D[0][i][0] for i in range (len(D[0]))],edges,faces]



  def borderOperator(i,C):
    #C es una cadena como la que hemos calculado en chainComplex
    if i == 1:
        #Creamos la matriz de ceros
        M = [[0 for columnas in range(len(C[1]))] for filas in range(len(C[0]))]
        #Para cada elemento de la base C1 hay que ver su imagen
        for j  in range(len(M[1])):
           M[C[1][j][0]][j]=1
           M[C[1][j][1]][j]=1
        
        return matrix(GF(2),M) 
    elif i ==2:
         #Creamos la matriz de ceros
        M = [[0 for columnas in range(len(C[2]))] for filas in range(len(C[1]))]
        
        #Para cada cara
        for j in range (len(C[2])):
            aristas=[[min(C[2][j][0],C[2][j][1]),max(C[2][j][0],C[2][j][1])],[min(C[2][j][0],C[2][j][2]),max(C[2][j][0],C[2][j][2])],[min(C[2][j][1],C[2][j][2]),max(C[2][j][1],C[2][j][2])]]   
            M[C[1].index(aristas[0])][j]=1
            M[C[1].index(aristas[1])][j]=1
            M[C[1].index(aristas[2])][j]=1
        return matrix(GF(2),M) 
    elif i ==0:
        return matrix(GF(2),1,len(C[0]))
    else: 
        return matrix(GF(2),4,1)

def BettiNumbersAlphaComplex(p,a):
    D = Delaunay(p)
    
    C = chainComplex(D) 
    
    A = alphaComplex2(a,C)
    
    
    B0=(borderOperator(0,A).right_kernel().dimension())-(borderOperator(1,A).rank())
    B1=(borderOperator(1,A).right_kernel().dimension())-(borderOperator(2,A).rank())
    B2=(borderOperator(2,A).right_kernel().dimension())-(borderOperator(3,A).rank())
    
    print('Los números de Betti son '+str([B0,B1,B2]))
    print('El complejo tiene '+str(B0) + ' componentes conexas'+' y '+ str(B1) +' agujeros')
   
    return 

def alphaComplex(a,C):
    #C es el complejo de cadenas que se da como lista [vertices,aristas,caras]
    #Toda arista de longitud menor que 2*a
    
    edges=[i for i in range(len(C[1])) if dist(C[0][C[1][i][0]],C[0][C[1][i][1]])<2*a]
    faces=[i for i in range (len(C[2])) if dist(circumcenter(C[0][C[2][i][0]],C[0][C[2][i][1]],C[0][C[2][i][2]]),C[0][C[2][i][0]])<a]
    return [C[0],edges,faces] 

def alphaComplex2(a,C):
    #C es el complejo de cadenas que se da como lista [vertices,aristas,caras]
    #Toda arista de longitud menor que 2*a
    
    edges=[C[1][i] for i in range(len(C[1])) if dist(C[0][C[1][i][0]],C[0][C[1][i][1]])<2*a]
    faces=[C[2][i] for i in range (len(C[2])) if dist(circumcenter(C[0][C[2][i][0]],C[0][C[2][i][1]],C[0][C[2][i][2]]),C[0][C[2][i][0]])<a]
    return [C[0],edges,faces] 


#devuelve la matriz del operador borde i-esimo del alpha-complejo A del complejo de cadenas C compuesto por los puntos de p
def borderOperatorAlpha(i,C,A) :
    edges=[C[1][j] for j in range(len(C[1])) if j in A[1] ]
    faces=[C[2][j] for j in range(len(C[2])) if j in A[2] ]
    Co=[C[0],edges,faces]
    return borderOperator(i,Co) 

