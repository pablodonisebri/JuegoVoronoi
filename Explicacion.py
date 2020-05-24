import pygame
import sys






# #Inicializamos pygame
pygame.init()

#Establecemos el tamaño de la ventana.
ventana = pygame.display.set_mode((700,700))
pygame.display.set_caption("Juego de Voronoi")
ventana.fill((255,255,255))
font = pygame.font.Font('freesansbold.ttf', 14)




#Aqui ponemos el recuadro del boton de return
return_cadena=font.render('return', True, (0, 0, 0))
return_rect=pygame.Rect(580,640,100,50)
pygame.draw.rect(ventana,(255, 255, 255),return_rect)
pygame.draw.rect(ventana,(0, 0, 0),return_rect,2)
ventana.blit(return_cadena, (return_rect.centerx-30, return_rect.centery-10))






#Aquí se escribe el texto de la explicacion

linea1=font.render('Bienvenido al Juego de Voronoi', True, (0, 0, 0))
#linea2=font.render('Jugarán dos jugadores que  por turnos colocarán sus puntos clickando en el lugar deseado.', True, (0, 0, 0))
linea3=font.render('Encontramos tres variantes del Juego de Voronoi en esta aplicación. Una versión clásica y dos', True, (0, 0, 0))
linea4=font.render('dinámicas.', True, (0, 0, 0))
linea5=font.render('', True, (0, 0, 0))
linea6=font.render('JUEGO CLÁSICO: competirán dos jugadores que por turnos haciendo click en el tablero colocarán', True, (0, 0, 0))
linea7=font.render('puntos con el objetivo de controlar la mayor proporción del área posible. Al inicio de la partida se', True, (0, 0, 0))
linea8=font.render('les da la opción a los jugadores de escoger el número de puntos que deseen jugar esa partida.', True, (0, 0, 0))
linea9=font.render('', True, (0, 0, 0))
linea10=font.render('JUEGO DINÁMICO: competirán dos jugadores que por turnos colocarán puntos en el tablero de la ', True, (0, 0, 0))
linea11=font.render('misma forma que en el juego clásico, pero con el añadido que podrán dotar de movimiento a los  ', True, (0, 0, 0))
linea12=font.render('puntos durante la partida. Cuando es el turno del jugador, este hace click con el ratón donde', True, (0, 0, 0))
linea13=font.render('quiere posicionar su punto y entonces con las flechas del teclado mueve el punto por el tablero', True, (0, 0, 0))
linea14=font.render('hasta que encuentra una trayectoria que le gusta para que el punto siga durante el resto de la ', True, (0, 0, 0))
linea15=font.render('partida. Durante el desarrollo de esta, los puntos rebotan entre sí cuando se acercan demadiado.', True, (0, 0, 0))
linea16=font.render('En la partida se jugarán 10 puntos por jugador, cuando se coloca el punto número 20, el jugador', True, (0, 0, 0))
linea17=font.render('que lo ha colocado dispone de 10 segundos para mover el punto antes de que acabe la partida,', True, (0, 0, 0))
linea18=font.render('o bien si desea detener el juego antes, puede pulsar la barra espaciadora con el mismo fin.', True, (0, 0, 0))
linea19=font.render('', True, (0, 0, 0))
linea20=font.render('JUEGO DINÁMICO 2: competirá un solo jugador contra 10 puntos que aparecerán en el tablero.', True, (0, 0, 0))
linea21=font.render('Cuando comience la partida, estos puntos estarán estáticos hasta que el jugador posicione', True, (0, 0, 0))
linea22=font.render('un punto en la posición del tablero que desee, en ese momento los puntos del plano empezarán ', True, (0, 0, 0))
linea23=font.render('a moverse y el jugador dispondrá de 30 segundos para haber maximizado en la medida de lo', True, (0, 0, 0))
linea24=font.render('posible la región asociada a su punto, pasado el tiempo la partida terminará. En caso de obtener  ', True, (0, 0, 0))
linea25=font.render('una región que el jugador considere que es la mayor que va a poder conseguir durante la partida ', True, (0, 0, 0))
linea26=font.render('podrá detener el temporizador pulsando la barra espaciadora, terminando asi la partida. ', True, (0, 0, 0))

ventana.blit(linea1, (10, 10))
#ventana.blit(linea2, (10, 40))
ventana.blit(linea3, (10, 60))
ventana.blit(linea4, (10, 80))
ventana.blit(linea5, (10, 100))
ventana.blit(linea6, (10, 120))
ventana.blit(linea7, (10, 140))
ventana.blit(linea8, (10, 160))
ventana.blit(linea9, (10, 180))
ventana.blit(linea10, (10,200))
ventana.blit(linea11, (10, 220))
ventana.blit(linea12, (10, 240))
ventana.blit(linea13, (10, 260))
ventana.blit(linea14, (10, 280))
ventana.blit(linea15, (10, 300))
ventana.blit(linea16, (10, 320))
ventana.blit(linea17, (10, 340))
ventana.blit(linea18, (10, 360))
ventana.blit(linea19, (10, 380))
ventana.blit(linea20, (10, 400))
ventana.blit(linea21, (10, 420))
ventana.blit(linea22, (10, 440))
ventana.blit(linea23, (10, 460))
ventana.blit(linea24, (10, 480))
ventana.blit(linea25, (10, 500))
ventana.blit(linea26, (10, 520))







pygame.display.flip()

Hola=pygame.USEREVENT




while True:

    for event in pygame.event.get():
        if event.type==Hola:
            print('Hola')
        if event.type == pygame.QUIT:   #Si el evento es cerrar la ventana
            pygame.quit()               #Se cierra pygame
            sys.exit()                  #Se cierra el programa
        elif event.type == pygame.MOUSEBUTTONDOWN:
            raton=pygame.mouse.get_pos()
            if return_rect.collidepoint(raton):
                 exec(open('Juego.py').read())
