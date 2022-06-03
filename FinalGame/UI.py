#from cmath import exp
import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        self.helth_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.helth_enemy_bar_rect = pygame.Rect(500, 100, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,35,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        self.arma_graphics = []
        for arma in arma_datos.values():
            path = arma['graphic']
            arma = pygame.image.load(path).convert_alpha()
            self.arma_graphics.append(arma)
        
        self.magia_graphics = []
        for magia in magia_datos.values():
            path_m = magia['graphic']
            magia = pygame.image.load(path_m).convert_alpha()
            self.magia_graphics.append(magia)


    def mostrar_barra(self,current,max_amount,bg_rect,color):
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

    def mostrar_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = 50
        text_rect = text_surf.get_rect(bottomright = (x,y))
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

    def mostrar_pausa(self):
        text_surf = self.font.render('PRESS ESC para instrucciones', False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def selection_box(self,left,top,cambio):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if cambio:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def arma_overlay(self,arma_indice,cambio):
        bg_rect = self.selection_box(10, 630,cambio)  # caja arma
        arma_surf = self.arma_graphics[arma_indice]
        arma_rect =arma_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(arma_surf,arma_rect)

    def magia_overlay(self, magia_indice, cambio):
        bg_rect = self.selection_box(80, 635, cambio)  # caja arma
        #print(magia_indice)
        #print(self.magia_graphics)
        magia_surf = self.magia_graphics[magia_indice]
        magia_rect = magia_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magia_surf, magia_rect)

    def display(self,player,boss,boss_alert):
        #pygame.draw.rect(self.display_surface,HEALTH_COLOR,self.helth_bar_rect)
        self.mostrar_barra(player.health, player.stats['health'],self.helth_bar_rect,HEALTH_COLOR)
        self.mostrar_barra(player.energy, player.stats['energia'],self.energy_bar_rect,ENERGY_COLOR)
        #if boss_alert:
        self.mostrar_barra(
                boss.health, 1000, self.helth_enemy_bar_rect, HEALTH_COLOR)
        self.mostrar_pausa()
        self.mostrar_exp(player.exp)
        self.arma_overlay(player.arma_indice,not player.can_switch_arma)
        self.magia_overlay(player.magia_indice, not player.can_switch_magia)
        #self.selection_box(80, 635)  # caja magia

