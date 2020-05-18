import pygame
import sys
import pygame,sys,random,math
import scipy.spatial
from scipy.spatial import Delaunay
from auxiliar import Voronoi
import itertools
#from itertools import combinations
from auxiliar import Area





#Inicializamos pygame
pygame.init()


#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,700))
#Cabecera de la ventana
pygame.display.set_caption("Juego de Voronoi")
#se pinta de blanco el fondo
ventana.fill((255,255,255))
#Fuente de la letra que se muestra por pantalla
font = pygame.font.Font('freesansbold.ttf', 24)
#Letretos de los botones que se muestran como opciones
dinamico_cadena=font.render('Juego Dinámico', True, (0, 0, 0))
dinamico2_cadena=font.render('Juego Dinámico 2', True, (0, 0, 0))
normal_cadena=font.render('Juego Clásico', True, (0, 0, 0))
explicacion_cadena=font.render('Explicación', True, (0, 0, 0))

#Rectangulos que representan los botones
explicacion=pygame.Rect(100,80,500,80)
dinamico=pygame.Rect(100,400,500,80)
normal= pygame.Rect(100,240,500,80)
dinamico2= pygame.Rect(100,560,500,80)

#Se pintan los botones
pygame.draw.rect(ventana, (72, 209, 204),dinamico)
pygame.draw.rect(ventana, (72, 209, 204),normal)
pygame.draw.rect(ventana, (72, 209, 204),explicacion)
pygame.draw.rect(ventana, (72, 209, 204),dinamico2)


#Se les pone el texto a los botones
ventana.blit(dinamico_cadena, (dinamico.centerx-85, dinamico.centery-10))
ventana.blit(normal_cadena, (normal.centerx-85, normal.centery-10))
ventana.blit(explicacion_cadena, (explicacion.centerx-85, explicacion.centery-10))
ventana.blit(dinamico2_cadena, (dinamico2.centerx-85, dinamico2.centery-10))

#Se despliega la ventana
pygame.display.flip()


#Bucle de "Juego"
while True:
    #Se obtiene la interaccion del usuario
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa

        #Si el usaurio hace click con el boton
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Se obtiene
            raton = pygame.mouse.get_pos()
            if normal.collidepoint(raton):
                #import Voronoi.py
                exec(open('Voronoi.py').read())
            elif dinamico.collidepoint(raton):
                import Pruebas
                exec(open('Pruebas.py').read())

            elif explicacion.collidepoint(raton):

                 import Explicacion
                 exec(open('Explicacion.py').read())

            if dinamico2.collidepoint(raton):
                 import JuegoDinamico
                 exec(open('JuegoDinamico.py').read())


