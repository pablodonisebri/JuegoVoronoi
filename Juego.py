import pygame
import sys


# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,700))
pygame.display.set_caption("Juego de Voronoi")
ventana.fill((255,255,255))

font = pygame.font.Font('freesansbold.ttf', 24)

dinamico_cadena=font.render('Juego Dinámico', True, (0, 0, 0))
dinamico2_cadena=font.render('Juego Dinámico 2', True, (0, 0, 0))

normal_cadena=font.render('Juego Clásico', True, (0, 0, 0))
explicacion_cadena=font.render('Explicación', True, (0, 0, 0))



explicacion=pygame.Rect(100,80,500,80)
dinamico=pygame.Rect(100,400,500,80)
normal= pygame.Rect(100,240,500,80)
dinamico2= pygame.Rect(100,560,500,80)


pygame.draw.rect(ventana, (72, 209, 204),dinamico)
pygame.draw.rect(ventana, (72, 209, 204),normal)
pygame.draw.rect(ventana, (72, 209, 204),explicacion)
pygame.draw.rect(ventana, (72, 209, 204),dinamico2)



ventana.blit(dinamico_cadena, (dinamico.centerx-100, dinamico.centery-10))
ventana.blit(normal_cadena, (normal.centerx-100, normal.centery-10))
ventana.blit(explicacion_cadena, (explicacion.centerx-90, explicacion.centery-10))
ventana.blit(dinamico2_cadena, (dinamico2.centerx-100, dinamico2.centery-10))

pygame.display.flip()

#Bucle de "Juego"
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa
        elif event.type == pygame.MOUSEBUTTONDOWN:
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

            elif dinamico2.collidepoint(raton):
                 import JuegoDinamico
                 exec(open('JuegoDinamico.py').read())


