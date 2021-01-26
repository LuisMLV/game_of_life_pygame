'''

En este script me dispongo a desorrollar en python el famoso juego de vida
de Conway mediante una animación generada con la librería pygame.

Se trata a grandes rasgos de la creación de una matriz donde diversas células progresan en su estado vital (vivas o muertas) en función del estado vital
de sus vecinas más cercanas.

'''

#Importo las librerías necesarias:

import pygame
import sys
from pygame.locals import *
import random




fps = 1 #Al ser una animación, es conveniente establecer los fps. Como deseo que vaya lento para
        #para que se aprecie bien lo que ocurre, establezco los frames por segundo en 1.
screen_width = 600 #Ancho de la ventana que mostrara la animación.
screen_height = 700 #Alto de la ventana que mostrará la animación.
grid_height = 600 #Altura de la cuadrícula donde se desarrollará la animación en sí. El propósito de esta variable
                  #se entenderá mejor más adelante.
cellsize = 10 #Tamaño que tendrá la célula en la cuadrícula donde se llevará a cabo la animación.

cellwidth = int(screen_width/cellsize) #Ancho de la célula.
cellheight = int(grid_height/cellsize) #Alto de la célula.

#Aquí los colores que se usarán para la animación en formato RGB:

white = (255, 255, 255)
black = (0,0,0)
grey = (128,128,128)
blue = (0,0, 255)


#En la animación estableceré una cuadrícula donde cada celda será una célula. Aquí la función que crea
#esta cuadrícula:

def grid():

# En la cuadrícula estableceré un sistema cartesiano para poder así asignar y localizar las células vivas y muertas
    for x in range(0, screen_width, cellsize):
        pygame.draw.line(screen, grey, (x,0), (x, grid_height))
    for y in range(0, grid_height, cellsize):
        pygame.draw.line(screen, grey, (0,y),(screen_width,y))

    pygame.draw.line(screen, white, (0,grid_height),(screen_width, grid_height), width=2) #Establezco  al final de la cuadrícula una línea que separá a esta de una
                                                                                          #zona que reservaré para incluir una determinada métrica.



#Posteriormente defino una función que generará en la cuadrícula una matriz con distribución aleatoria de células vivas y muertas:

def cells_in_grid():

    cells = {} #Los datos de esta matriz se guardarán en un diccionario de python.

    for x in range(cellwidth):
        for y in range(cellheight):

            cells[x,y] = random.randint(0,1) #Cada célula (posición x/y) tendrá o el estado de muerta (0) o el estado de viva (1)

    return cells #La función retorna el diccionario generado.


#El juego de vida de Conway necesita evaluar el vecindario de la célula (las 8 más cercanas) para determinar si las células siguen vivas, muertas, mueren
#o reviven a lo largo de las generaciones. La siguiente función sumará 1 por cada célula del vecindario que esté viva, esto se usará posteriormente para evaluar el
#estado de cada célula con respecto a sus vecinas:

def get_neighbours(item, vidadict):

    neighbours = 0 #La variable sumatorio.

    for x in range(-1,2): #Las células más próximas a cada célula estarán, en ambos ejes, en un rango de -1 a 1
        for y in range(-1,2):
            neigh_cell=(item[0]+x, item[1]+y)
            if neigh_cell[0] < cellwidth  and neigh_cell[0] >=0:
                if neigh_cell[1] < cellheight and neigh_cell[1]>= 0:
                    if vidadict[neigh_cell] == 1:
                        if x == 0 and y == 0:
                            neighbours += 0
                        else:
                            neighbours += 1

    return neighbours #Retorna el sumatorio, la variable más importante en esta función.



#Esta función determinará/decidira el estado de la cuadrícula en la siguiente generación de células o estado del sistema. Evalúa el número de vecinas vivas de cada
#célula, y en función de las reglas establecidas por Conway para su juego, determina el estado vital de cada célula de la cuadrícula en la siguiente generación:

def next_grid(vidadict):

    new_grid={}

    for i in vidadict:
        n_neighbours = get_neighbours(i, vidadict) #Aquí aplico la función anterior que cuenta el número de células vecinas vivas para cada célula.

        #Aquí escribo las reglas establecidas por Conway referente al estado vital de las células para su juego de vida:

        if vidadict[i] == 1:

            if n_neighbours < 2 or n_neighbours> 3:
                new_grid[i] = 0

            else:

                new_grid[i] = 1

        elif vidadict[i] == 0:

            if n_neighbours == 3:

                new_grid[i] = 1

            else:

                new_grid[i] = 0

    return new_grid


#Creo ahora una función que servirá para añadir un determinado código de color que indique visualmente qué célula está viva (1) y qué célula está muerta (0):

def colored(vidadict):

    for i in vidadict:
            x = i[0]
            y = i[1]
            x = x*cellsize
            y = y*cellsize
            if vidadict[i] == 0:
                pygame.draw.rect(screen, black, (x,y, cellsize, cellsize)) #Las células muertas se verán en negro.
            if vidadict[i] == 1:
                pygame.draw.rect(screen, blue, (x,y,cellsize, cellsize)) #Las células vivas se verán en azul.


#En el hueco dejado en la ventana bajo la cuadrícula (screen_height - grid_height) coloco una métrica que indicara la generación actual y el paso de las generaciones.
#Esto voy a aplicarlo con la siguiente función, que mostrará el progreso de las generaciones en pantalla:

def generation_metric(generation):
    font = pygame.font.SysFont("monospace", 18)

    gen_text = font.render(f'Generation : {generation}', True, white, black)

    screen.blit(gen_text, (20, 630))
    pygame.display.update()




#Creo la función main(), que ejecutará todo el código anterior más ciertos aspectos a configurar de pygame:

def main():

    pygame.init() #Inicio pygame.
    global screen #Esteblezco screen, la variable encargada en este script de dar formato a la ventana, como variable global
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height)) #Defino el tamaño de la ventana en la variable screen.
    pygame.display.set_caption('Juego de vida de Conway') #El título de la ventana.

    screen.fill(black) #El color de fondo de la ventana.

    vidadict= cells_in_grid()
    colored(vidadict)
    grid()

    generation = 0 #Variable contador de las generaciones que se vayan sucediendo
    #gen_text = font.render("Generation : {0}".format(generation), 1, False, (255,255,255))

    #screen.blit(gen_text, (20, 650))
    #pygame.display.update()
    #print(vidadict)

     #Este bucle hará progresar el sistema que forman las células en la cuadrícula:

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        vidadict= next_grid(vidadict)
        colored(vidadict)
        generation_metric(generation)
        grid()

        generation +=1


        pygame.display.flip()
        fpsclock.tick(fps)


#LLamo a la función main() para que se ejecute todo el script:

if __name__ == '__main__':

    main()
