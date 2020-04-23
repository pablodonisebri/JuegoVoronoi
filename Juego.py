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
normal_cadena=font.render('Juego Clásico', True, (0, 0, 0))
explicacion_cadena=font.render('Explicación', True, (0, 0, 0))



explicacion=pygame.Rect(100,100,500,100)
dinamico=pygame.Rect(100,500,500,100)
normal= pygame.Rect(100,300,500,100)



pygame.draw.rect(ventana, (72, 209, 204),dinamico)
pygame.draw.rect(ventana, (72, 209, 204),normal)
pygame.draw.rect(ventana, (72, 209, 204),explicacion)


ventana.blit(dinamico_cadena, (dinamico.centerx-100, dinamico.centery-10))
ventana.blit(normal_cadena, (normal.centerx-100, normal.centery-10))
ventana.blit(explicacion_cadena, (explicacion.centerx-90, explicacion.centery-10))

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




