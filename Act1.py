
import pygame
from pygame.locals import *
import sys
from os import path

class Game:
    fps = 60
    time_per_frame = 1000 / fps
    #event_vector = [0,0,0]

    def __init__(self):
        #se inicializa el juego 
        pygame.init()
        #se especifica el tamanio de la pantalla
        self.__window = pygame.display.set_mode((640, 480), 0 ,32)
        #creamos un vector de booleanos para detectar cambios en el teclado
        self.event_vector= [False,False,False]
        self.__running = False
        self.__hero = Hero(self.__window.get_size())
        #se

    def run(self):
        #en esta funcion corre el juego 
        self.__running = True

        last_time = pygame.time.get_ticks()
        time_since_last_update = 0
        while self.__running:
            delta_time, last_time = self.__calc_delta_time(last_time)
            time_since_last_update += delta_time
            while time_since_last_update > Game.time_per_frame:
                time_since_last_update -= Game.time_per_frame
                self.__process_events()
                self.__update(Game.time_per_frame)

            self.__render()

        self.__quit()

    def __process_events(self):
        #detectamos los posibles eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #cerramos aplicacion si se cierra el programa
                self.__running = False
            if event.type == pygame.KEYDOWN:
                #esta en epera de presionar una tecla
                if event.key == pygame.K_RIGHT:
                    #se presiona flecha derecha
                    self.event_vector [0] = True
                    self.event_vector [1] = True 
                    #print(self.event_vector)
                elif event.key == pygame.K_LEFT:
                    #se presiona flecha izquierda
                    self.event_vector [0] = True
                    self.event_vector [2] = True 
                    #print(self.event_vector)
            if event.type == pygame.KEYUP:
                #si se presiona una tecla se revisa si esta dejo de ser presionada
                if event.key == pygame.K_RIGHT:
                    #se dejo de presionar flexha derecha
                    self.event_vector [0] = False
                    self.event_vector [1] = False 
                    #print(self.event_vector)
                elif event.key == pygame.K_LEFT:
                    #se dej ode presionar flecha izquierda
                    self.event_vector [0] = False
                    self.event_vector [2] = False 
                    #print(self.event_vector)

    def __update(self, delta_time):
        #se actualiza el personaje , envian los posibles eventos 
        self.__hero.update(delta_time,self.event_vector)

    def __render(self):
        #se dibujan los elementos en la pantalla
        self.__window.fill((0,0,0))
        self.__hero.render(self.__window)
        pygame.display.update()

    def __quit(self):
        pygame.quit()

    def __calc_delta_time(self, last):
        #se calcula el timepo en el cual va ser actualizado el sistema
        current = pygame.time.get_ticks()
        delta = current - last
        return delta, current

class Images:

    def __init__(self, location, pasos , secuencias, vel):
        #clase de las imagenes que se usaran del personaje
        self.__cuadro = pygame.image.load(path.join(*location)).convert_alpha()
        self.__numpasos = pasos
        self.tamaniocuadro = pygame.math.Vector2(self.__cuadro.get_width() / pasos, self.__cuadro.get_height() / secuencias)
        self.__velocidad = vel
        self.__inicio = 0

        self.__animacion = []
        #se crean los cuadros que se utilizaran para las animaciones
        for n in range(secuencias):
            self.__animacion.append([])
            for j in range(pasos):
                self.__animacion[n].append(pygame.Rect(self.tamaniocuadro.x*j,self.tamaniocuadro.y*n,self.tamaniocuadro.x,self.tamaniocuadro.y))
                #print(self.__animacion[n])


    def update(self, delta_time):
        self.__inicio = (self.__inicio + self.__velocidad) % self.__numpasos
        

    def render(self, dest, secuencia, position, stop):
        #en caso de que no se reciba ninguna senal se debe quedar parado el personaje
        if stop:
            dest.blit(self.__cuadro, position, self.__animacion[0][0])
        else:
            dest.blit(self.__cuadro, position, self.__animacion[secuencia][int(self.__inicio)])

class Hero:

    location = ['walking_animation.png']
    pasos = 10
    num_secuencias = 2
    velocidad = 1 / 5

    def __init__(self, window_size):
        #se inicializa el personaje
        self.__heromove = Images(Hero.location, Hero.pasos, Hero.num_secuencias, Hero.velocidad)
        self.__derecha = True
        #print(self.__heromove.tamaniocuadro.y)
        self.__position = pygame.math.Vector2(0.0, window_size[1] - self.__heromove.tamaniocuadro.y)
        self.__speed = self.velocidad
        self.__window_size = window_size
        self.time = 0
        self.stop = False

    def update(self, delta_time, event_vector):
        
        if event_vector[0]:
            #caso donde se presiona tecla 
            self.stop = False
            if event_vector[1]:
                #caso dodne se presiona derecha
                self.__derecha = True
                if self.__position.x >= self.__window_size[0] - self.__heromove.tamaniocuadro.x:
                    #evitamos quese slaga de la pantalla el eprsonaje
                    self.__position.x = self.__position.x
                else:
                    self.__position.x += self.__speed * delta_time

                #print('presionado derecha')
                #print(self.__position)
            elif event_vector[2]:
                #caso dodne se presiona la izquierda
                self.__derecha = False
                if self.__position.x <= 0:
                    #evitamso que se salga de la pantalla el personaje
                    self.__position.x = 0
                else:
                    self.__position.x -= self.__speed * delta_time
                #print('presionado izquierda')
                #print(self.__position)      
            self.time = 5000
        else:
            #caso automatico
            if self.time > 0:
                self.time -= delta_time
                self.stop = True
            else:
                if self.__derecha:
                    self.__position.x += self.__speed * delta_time
                    if self.__position.x >= self.__window_size[0] - self.__heromove.tamaniocuadro.x:
                        self.__derecha = False
                else:
                    self.__position.x -= self.__speed * delta_time
                    if self.__position.x <= 0:
                        self.__derecha = True
                self.stop = False

        self.__heromove.update(delta_time)

    def render(self, dest):
        #dibujamso el personaje
        self.__heromove.render(dest, 0 if self.__derecha else 1, self.__position, self.stop)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    app = Game()
    app.run()

if __name__ == '__main__':
    sys.exit(main())