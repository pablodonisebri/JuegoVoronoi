import pygame
import sys






# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,700))
pygame.display.set_caption("Juego de Voronoi")
ventana.fill((255,255,255))
font = pygame.font.Font('freesansbold.ttf', 16)




#Aqui ponemos el recuadro del boton de return
return_cadena=font.render('return', True, (0, 0, 0))
return_rect=pygame.Rect(580,640,100,50)
pygame.draw.rect(ventana,(255, 255, 255),return_rect)
pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))






#Aquí se escribe el texto de la explicacion

linea1=font.render('Explicación de las reglas del juego y demás', True, (0, 0, 0))

ventana.blit(linea1, (10, 10))


pygame.display.flip()



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa
        elif event.type == pygame.MOUSEBUTTONDOWN:
            raton=pygame.mouse.get_pos()
            if return_rect.collidepoint(raton):
                 exec(open('Juego.py').read())
