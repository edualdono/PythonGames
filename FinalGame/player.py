#from tkinter.messagebox import NO
import pygame 
from settings import *
from Entidad import Entidad

class Player(Entidad):
    def __init__(self,pos,groups, obstacle_sprites,crear_ataque,destroy_arma,crear_magia):

        super().__init__(groups)
        self.image = pygame.image.load('./graphics/test/test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.rect_animation = self.image.get_rect(topleft=pos)
        #print('se reinicio el rect')
        self.hitbox = self.rect.inflate(0, -26)

        self.import_player_assets()
        self.status = 'up'
        
        #print(type(self.direction))
        #self.speed = 5
        self.atacando = False
        self.atacar_cooldown = 400
        self.atacar_tiempo = None
        self.obstacles_sprites = obstacle_sprites

        #armas
        self.crear_ataque = crear_ataque
        self.destroy_arma = destroy_arma
        self.arma_indice = 0
        self.arma = list(arma_datos.keys())[self.arma_indice]
        self.can_switch_arma = True
        self.arma_switch_tiempo = None
        self.switch_duration_cooldown = 200

        #magia
        self.crear_magia = crear_magia
        self.magia_indice = 0
        self.magia = list(magia_datos.keys())[self.magia_indice]
        self.can_switch_magia = True
        self.magia_switch_tiempo = None

        #estadisticas
        self.stats = {'health': 100,  'energia':60, 'attack':10, 'magic':4, 'speed':5}
        self.max_stats = {'health': 300,  'energia': 140,
                          'attack': 20, 'magic': 10, 'speed': 12}
        self.update_cost = {'health': 100,  'energia': 100,
                            'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energia']
        self.exp = 500
        self.speed = self.stats['speed']

        #dano
        self.vulnerable = True
        self.hurt_time = None
        self.invunerability_duration = 500

        self.weapon_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.weapon_sound.set_volume(0.4)


    def import_player_assets(self):
        self.image = pygame.image.load('.\graphics\Characters\Pricipal\walk64.png').convert_alpha()
        self.num_cuadros = 12
        self.num_sec = 8
        self.tamaniocuadro = pygame.math.Vector2(self.image.get_width() / self.num_cuadros, self.image.get_height() / self.num_sec)
        #self.hitbox_cuadro = self.tamaniocuadro.inflate(0, -26)

        self.animaciones = {'down': [], 'left': [], 'right': [], 'up': [],
                            'down_parado': [], 'left_parado': [], 'right_parado': [], 'up_parado': [],
                            'down_ataque': [], 'left_ataque': [], 'right_ataque': [], 'up_ataque': []}

        n=0
        flag = False 
        for animation in self.animaciones.keys():
            if not flag:
                    for j in range(-1, 3):
                        self.animaciones[animation].append(pygame.Rect(
                            self.tamaniocuadro.x*abs(j)+7, self.tamaniocuadro.y*n, self.tamaniocuadro.x-8, self.tamaniocuadro.y))
                        #self.animaciones[animation][j+1].inflate(0, -26)
                    if n == 3:
                        flag = True
            else:
                if 'ataque' in animation:
                    if 't_' in animation:
                        self.animaciones[animation].append(pygame.Rect(
                            self.tamaniocuadro.x*4+7, self.tamaniocuadro.y*0, self.tamaniocuadro.x-10, self.tamaniocuadro.y))
                    else:
                        self.animaciones[animation].append(pygame.Rect(
                            self.tamaniocuadro.x*0+7, self.tamaniocuadro.y*n, self.tamaniocuadro.x-8, self.tamaniocuadro.y))
                else:
                    if 'right_parado' in animation:
                        self.animaciones[animation].append(pygame.Rect(
                            self.tamaniocuadro.x*8+7, self.tamaniocuadro.y*(n-1), self.tamaniocuadro.x-8, self.tamaniocuadro.y))
                    else:
                        self.animaciones[animation].append(pygame.Rect(
                            self.tamaniocuadro.x*1+7, self.tamaniocuadro.y*n, self.tamaniocuadro.x-8, self.tamaniocuadro.y))
                #self.animaciones[animation][0].inflate(0, -26)

            if n == 3:
                n = 0
            else:
                n += 1
        #print(self.animaciones)

    def input(self):
        keys = pygame.key.get_pressed()

        #MOVIMIENTO
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        #Atque
        if keys[pygame.K_q] and not self.atacando:
            self.atacando = True
            self.atacar_tiempo = pygame.time.get_ticks()
            self.crear_ataque()
            self.weapon_sound.play()
            #print('Atacando')
        
        #MAGIA
        if keys[pygame.K_e] and not self.atacando:
            self.atacando = True
            self.atacar_tiempo = pygame.time.get_ticks()
            style = list(magia_datos.keys())[self.magia_indice]
            strength = list(magia_datos.values())[self.magia_indice]['strength'] + self.stats['magic']
            cost = list(magia_datos.values())[self.magia_indice]['cost']
            self.crear_magia(style,strength,cost)
            #print('Magia')

        if keys[pygame.K_TAB] and self.can_switch_arma:
            self.can_switch_arma =False
            self.arma_switch_tiempo = pygame.time.get_ticks()
            if self.arma_indice < len(list(arma_datos.keys())) -1:
                self.arma_indice += 1
            else: 
                self.arma_indice = 0
            self.arma = list(arma_datos.keys())[self.arma_indice]
        
        if keys[pygame.K_LSHIFT] and self.can_switch_magia:
            self.can_switch_magia = False
            self.magia_switch_tiempo = pygame.time.get_ticks()
            if self.magia_indice < len(list(magia_datos.keys())) - 1:
                self.magia_indice += 1
            else:
                self.magia_indice = 0
            self.magia = list(magia_datos.keys())[self.magia_indice]

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
                if not 'parado' in self.status and not 'ataque' in self.status:
                    self.status = self.status + '_parado'

        if self.atacando:
            self.direction.x = 0
            self.direction.y = 0
            if not 'ataque' in self.status:
                if 'parado' in self.status:
                    self.status = self.status.replace('_parado', '_ataque')
                else:
                    self.status = self.status + '_ataque'
        else:
            if 'ataque' in self.status:
                self.status = self.status.replace('_ataque', '')

    def downtime(self):
        current_time = pygame.time.get_ticks()

        if self.atacando:
            if current_time - self.atacar_tiempo >= self.atacar_cooldown + arma_datos[self.arma]['cooldown']:
                self.atacando = False
                self.destroy_arma()
        
        if not self.can_switch_arma:
            if current_time - self.arma_switch_tiempo >= self.switch_duration_cooldown:
                self.can_switch_arma = True

        if not self.can_switch_magia:
            if current_time - self.magia_switch_tiempo >= self.switch_duration_cooldown:
                self.can_switch_magia = True
        
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invunerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animaciones[self.status]
        
        if 't_' in self.status:
            if 'right' in self.status:
                #print('Cambio imagen')
                self.image = pygame.image.load(
                    '.\graphics\Characters\Pricipal\others_2_rigth.png').convert_alpha()
            else:
                self.image = pygame.image.load(
                    '.\graphics\Characters\Pricipal\others_2.png').convert_alpha()
        else:
            self.image = pygame.image.load(
                '.\graphics\Characters\Pricipal\walk64.png').convert_alpha()
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
                self.frame_index = 0

            # set the image
            #self.image = animation[int(self.frame_index)]
            #self.rect = self.image.get_rect(center=self.hitbox.center)
        self.rect_animation = animation[int(self.frame_index)]
        
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = arma_datos[self.arma]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        magia_damage = magia_datos[self.magia]['strength']
        return base_damage + magia_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.update_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energia']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energia']

    def check_muerte(self):
        if self.health <= 0:
            """ self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play() """
            print('Jugador muerto')

    def update(self):
        self.input()
        self.downtime()
        self.get_status()
        #self.check_muerte()
        #print(self.rect.center)
        self.animate()
        self.move(self.speed)
        self.energy_recovery()