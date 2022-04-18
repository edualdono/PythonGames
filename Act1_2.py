
import pygame
import sys
from os import path

class Game:

    fps = 60
    time_per_frame = 1000.0 / fps
    #mensaje = ' HOLA AMIGO!!! '

    def __init__(self):
        pygame.init()

        self.mensaje = 'galgo corredor'
        self.__window = pygame.display.set_mode((640, 480), 0, 32)
        self.__running = False
        self.contador_fuente = 0
        self.event_vector= [False,False,False]
        self.mensaje = ' '+self.mensaje+' '
        self.time = 0
        self.__letrasesc = Letras(self.__window.get_size(), self.mensaje, self.contador_fuente)
    
    def run(self):
        #en este modulo el sistema esta corriendo 
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
                    self.event_vector [1] = False
                    #print(self.event_vector)
                elif event.key == pygame.K_LEFT:
                    #se presiona flecha izquierda
                    self.event_vector [0] = False
                    self.event_vector [1] = True
                elif event.key == pygame.K_SPACE:
                    #se presiona espacio
                    self.event_vector [2] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    #se suelta el espacio
                    self.event_vector [2] = False 

    def __update(self, delta_time):

        if self.event_vector[2] and self.time < 0:
            #caso en dodne se presiono el espacio
            self.time = 500
            if self.contador_fuente < 2 :
                #cambiamos la fuente
                self.contador_fuente += 1
            else:
                self.contador_fuente = 0
            self.__letrasesc = Letras(self.__window.get_size(), self.mensaje,self.contador_fuente)
        else:
            #se da tiempo para que se pueda cambiar de forma comoda la fuente
            self.time -= delta_time 

        self.__letrasesc.update(delta_time,self.event_vector)

    def __render(self):
        #se dibujan los elementos en la pantalla
        self.__window.fill((0, 0, 0))
        self.__letrasesc.render(self.__window)
        pygame.display.update()
    
    def __quit(self):
        pygame.quit()

    def __calc_delta_time(self, last):
        current = pygame.time.get_ticks()
        delta = current - last
        return delta, current


class LetterType:

    def __init__(self, location, total, letrasxlinea, tamanio):
        self.__cuadro = pygame.image.load(path.join(*location)).convert_alpha()
        self.__cuadro.set_colorkey((0,0,0))
        self.tamanio = tamanio
        self.__letras = []
        #inicializamso el mensaje a escribir
        for n in range(total):
            left = (n % letrasxlinea ) * self.tamanio[0]
            top = int(n / letrasxlinea) * self.tamanio[1]
            width=self.tamanio[0]
            height=self.tamanio[1]
            self.__letras.append(pygame.Rect(left,top,width,height))

    def render(self, dest, letras, position):
        #se dibujan las letras
        index = self.mapeo(letras)
        #print(position)
        dest.blit(self.__cuadro, position, self.__letras[index])

    def mapeo(self, letras):
        #se mapean el alfabeto a las letras disponibles
        ascii = ord(letras)
        if ascii >= 65 and ascii <= 90:  #letras a -z
            index = ascii - 32
        elif ascii >= 97 and ascii <= 122: #letras A - Z 
            index = ascii - 64
        elif ascii >= 48 and ascii <= 57: # 0 - 9 
            index = ascii - 32
        elif ascii >= 44 and ascii <= 47: # , - . /
            index = ascii - 32
        elif ascii == 145 or ascii == 146: # ' '
            index = 7
        elif ascii == 147 or ascii == 148: # " "
            index = 2
        elif ascii >= 40 and ascii <=41: # ( )
            index = ascii - 32
        elif ascii == 33: # !
            index = 1
        elif ascii == 63: # ?
            index = 31
        else:
            index = 0

        return index

class Letras:
    #seleccionamos las fuentes disponibles
    locations = []
    locations.append(["./BitmapFonts-main/bennyfnt.png"])
    locations.append(["./BitmapFonts-main/auto_f02r.png"])
    locations.append( ["./BitmapFonts-main/crikey_f.png"])

    #damso las acaracteristicas de la fuente
    total = 59
    letrasxlinea = 10
    tamanio = (32,32)

    def __init__(self, window_size, text, num_fuente):
        #print(num_fuente)
        #se inicializa la fuente
        self.__letras = LetterType(Letras.locations[num_fuente], Letras.total, Letras.letrasxlinea, Letras.tamanio)
        self.texto = list(text)
        self.index_act = 0
        self.velocidad = 1/10
        self.position = pygame.math.Vector2(-window_size[0] * len(text),window_size[1]/2)
        self.window_size = window_size

    def update(self, delta_time, event_vector):
        if(event_vector[0]):
            #caso donde va a la derecha
            self.position.x += (self.velocidad * delta_time)
            #print('cambio der')
            
        elif(event_vector[1]):
            #caso donde va a la izquierda
            self.position.x -= (self.velocidad * delta_time)
            #print('cambio izq')

        else:
            #caso inicial
            self.position.x -= (self.velocidad * delta_time)

        
    def render(self, destino):
        #se dibujan las letras y se genera el movimiento
        letras_esc = int((self.window_size[0] - self.position.x) / self.__letras.tamanio[0]) +1
        #print(letras_esc)
        for n in range (letras_esc):
            index = (self.index_act + n) % len(self.texto)
            #print(self.texto)
            self.__letras.render(destino, self.texto[index],((self.position.x) + (self.__letras.tamanio[0] * n), self.position.y))


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    app = Game()
    app.run()

if __name__ == '__main__':
    sys.exit(main())



        