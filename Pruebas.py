import pygame
from auxiliar import *
#from Voronoi import *














# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,700))
#Titulo de la Ventana
pygame.display.set_caption("Prueba")
#Pintamos de blanco la ventana
ventana.fill((255,255,255))
pygame.display.flip()




p=[[int(random.random()*700),int(random.random()*700)] for i in range (9)]
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
                p2=p+[raton]
                D=Delaunay(p2)
                V=Voronoi(D)
                for v in range (len(p2)):
                    if v%2:
                        pygame.draw.polygon(ventana,(0,0,250),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(0,0,0),p2[v],5)


                    else:
                        pygame.draw.polygon(ventana,(250,0,0),V[v])
                        pygame.draw.polygon(ventana,(0,0,0),V[v],2)
                        pygame.draw.circle(ventana,(0,0,0),p2[v],5)


                pygame.display.update()


        else:

            continue








#
