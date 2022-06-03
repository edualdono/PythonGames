import pygame
from settings import *
from support import *
from tile import Tile
from player import Player
from armas import Armas
from UI import UI
from enemgo import Enemigo
from particulas import AnimationPlayer, Particulas
from magia import MagicPlayer
from upgrade import Upgrade

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.kind_pause = 'Normal'
        self.boss_alert = False

        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.atacar_enemigo = pygame.sprite.Group()
        self.atacables_sprites = pygame.sprite.Group()

        self.create_map()
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        self.armas = None
        

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)


    def create_map(self):
        layouts = {
         
            'boundary' : import_csv_layout('./Map/Map2_piso.csv'),
            'entidades' : import_csv_layout('./Map/map_Entities.csv')
        }

        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'entidades':
                            if col == '397':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.crear_ataque,
                                    self.destroy_arma,
                                    self.crear_magia)
                            else:
                                if col == '163': monster_name = 'spirit'
                                elif col == '181': monster_name = 'raccoon'
                                elif col == '406': monster_name = 'bamboo'
                                elif col =='365': 
                                    monster_name = 'spirit'
                                    self.boss = Enemigo(
                                        'boss',
                                        (x, y),
                                        [self.visible_sprites,
                                            self.atacables_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_xp)

                                else: monster_name = 'squid'
                                Enemigo(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites, self.atacables_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_xp)
                                #print('enemigo founded')
        #        if col == 'X':
        #            Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
        #        if col == 'p':
        #            self.player = Player((x,y),[self.visible_sprites], self.obstacle_sprites)
        

    def crear_ataque(self):
        self.armas = Armas(self.player,[self.visible_sprites, self.atacar_enemigo])
    
    def crear_magia(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites, self.atacar_enemigo])

    def destroy_arma(self):
        if self.armas:
            self.armas.kill()
        self.arma = None

    def logica_de_ataque(self):
        if self.atacar_enemigo:
            for atacar_enemigo in self.atacar_enemigo:
                collision_sprites = pygame.sprite.spritecollide(atacar_enemigo,self.atacables_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player,atacar_enemigo.sprite_type) 

    def damage_player(self,amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount 
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def add_xp(self,amount):
        self.player.exp += amount

    def toggle_menu(self,kind_pause):
        self.game_paused = not self.game_paused
        self.kind_pause = kind_pause

    def check_deaths(self):
        #pause = False
        if self.player.health <= 0:
            self.game_paused = True
            self.kind_pause = 'PLAYER'
        else:
            self.kind_pause = self.kind_pause
        
        if self.boss.health <= 0:
            self.game_paused = True
            self.kind_pause = 'BOSS'
        else:
            self.kind_pause = self.kind_pause

    def boss_moment(self):
        enemy_vec = pygame.math.Vector2(self.boss.rect.center)
        player_vec = pygame.math.Vector2(self.player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance < 400:
            self.boss_alert = True        

    def run(self):
        self.visible_sprites.custom_draw(self.player, self.armas)
        self.ui.display(self.player,self.boss,self.boss_alert)
        self.check_deaths()
        #print(self.kind_pause)

        if self.game_paused:
            if self.kind_pause == 'EXP':
                self.upgrade.display()
            elif self.kind_pause == 'PLAYER':
                image_aux = pygame.image.load(
                    './graphics/menu/DEATH_IMAGE.png').convert_alpha()
                image_aux_rect = image_aux.get_rect(topleft=(0, 0))
                self.display_surface.blit(image_aux, image_aux_rect)
            elif self.kind_pause == 'BOSS':
                image_aux = pygame.image.load(
                    './graphics/menu/WIN_IMAGE.png').convert_alpha()
                image_aux_rect = image_aux.get_rect(topleft=(0, 0))
                self.display_surface.blit(image_aux, image_aux_rect)
            else:
                #self.display_surface.fill('black')
                image_aux = pygame.image.load(
                    './graphics/menu/MENU_IMAGE.png').convert_alpha()
                image_aux_rect = image_aux.get_rect(topleft=(0, 0))
                self.display_surface.blit(image_aux,image_aux_rect)
        else:
            self.boss_moment()
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.logica_de_ataque()
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.mitad_ancho = self.display_surface.get_size()[0] // 2
        self.mitad_altura = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.piso_area = pygame.image.load('./graphics/tilemap/Map2.png').convert()
        self.piso_rect = self.piso_area.get_rect(topleft = (0,0))

    def custom_draw(self,player,armas):
        self.offset.x = player.rect.centerx - self.mitad_ancho
        self.offset.y = player.rect.centery - self.mitad_altura

        floor_offset_pos = self.piso_rect.topleft - self.offset
        self.display_surface.blit(self.piso_area,floor_offset_pos)
        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            #print(str(type(sprite)))
                #print('enemigo founded')
            offset_pos = sprite.rect.topleft - self.offset
            if not sprite.rect.center == player.rect.center:
                if 'ataque' in player.status:
                    if 'arma' in str(type(sprite)):
                        #pass
                        self.display_surface.blit(sprite.image, offset_pos)
                #print(sprite.rect)
                    #self.display_surface.blit(armas.image, offset_pos)
            else:
                self.display_surface.blit(
                    player.image, offset_pos, player.rect_animation)

            #print(sprite)  
            if 'nemigo' in str(type(sprite)):
                #pass
                self.display_surface.blit(sprite.image, offset_pos)
            elif 'articula' in str(type(sprite)):
                self.display_surface.blit(sprite.image, offset_pos)
            #self.display_surface.blit(Enemigo.image,offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(
		    sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
