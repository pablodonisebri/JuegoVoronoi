import pygame
from auxiliar import *
#from Voronoi import *


#Funcion para determinar el movimiento de los puntos dandole un punto y un vector
def movimiento(p,v):
    if p[0]>700:
        v=[-v[0],v[1]]
    elif p[0]<0:
        v=[-v[0],v[1]]
    elif p[1]<0:
        v=[v[0],-v[1]]
    elif p[1]>700:
        v=[v[0],-v[1]]
    return ([p[0]+v[0],p[1]+v[1]],v)










# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,700))
#Titulo de la Ventana
pygame.display.set_caption("Prueba")
#Pintamos de blanco la ventana
ventana.fill((255,255,255))
pygame.display.flip()



#Puntos ya generados en el plano que van a estar en movimiento
p=[[int(random.random()*700),int(random.random()*700)] for i in range (9)]

#Vectores de las direcciones en las que se van a mover los puntos
vec=[[int(random.random()*10),int(random.random()*10)] for i in range (9)]
#Parametro para que no haya problema de superposicion de puntos
l=1








#Bucle del juego

while True:



    for event in pygame.event.get():    #Cuando ocurre un evento...
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Obtenemos la posicion del raton que va hasta el punto (700,700)

                raton = pygame.mouse.get_pos()

                if raton in p:
                    raton=(raton[0]+l,raton[1]+l)
                    l=l*(-1)
                p.append(raton)
                vec.append([0,0])

                D=Delaunay(p)
                V=Voronoi(D)
                for v in range (len(p)-1):
                    if v%2:
                        pygame.draw.polygon(ventana,(0,0,250),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(0,0,0),p[v],5)


                    else:
                        pygame.draw.polygon(ventana,(250,0,0),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(0,0,0),p[v],5)


                    pygame.draw.polygon(ventana,(0,250,0),V[len(p)-1])
                    pygame.draw.polygon(ventana,(0,0,0),V[len(p)-1],2)
                    pygame.draw.circle(ventana,(0,0,0),p[len(p)-1],5)


                pygame.display.update()


        elif event.type == pygame.KEYDOWN:
            # gets the key name
            key_name = pygame.key.name(event.key)
            # converts to uppercase the key name
            key_name = key_name.upper()

            if  key_name=="UP":
                vec[len(p)-1]=[0,-5]
            elif key_name=="DOWN":

                vec[len(p)-1]=[0,5]

            elif key_name=="RIGHT":
                vec[len(p)-1]=[5,0]

            elif key_name=="LEFT":
                vec[len(p)-1]=[-5,0]

            for k in range (len(p)):
                (p[k],vec[k])=movimiento(p[k],vec[k])

            D=Delaunay(p)
            V=Voronoi(D)
            for v in range (len(p)-1):
                    if v%2:
                        pygame.draw.polygon(ventana,(0,0,250),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(0,0,0),p[v],5)


                    else:
                        pygame.draw.polygon(ventana,(250,0,0),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(0,0,0),p[v],5)


                    pygame.draw.polygon(ventana,(0,250,0),V[len(p)-1])
                    pygame.draw.polygon(ventana,(0,0,0),V[len(p)-1],2)
                    pygame.draw.circle(ventana,(0,0,0),p[len(p)-1],5)


            pygame.display.update()


            continue








#
