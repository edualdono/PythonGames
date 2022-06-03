WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

#Interface
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE =80
UI_FONT = './graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'yellow'
UI_BORDER_COLOR_ACTIVE ='gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

#armas
arma_datos = {
    'sword' : {'cooldown' : 100, 'damage': 15, 'graphic':'./graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': './graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': './graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': './graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': './graphics/weapons/sai/full.png'}}
#magia

magia_datos = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': './graphics/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': './graphics/particles/heal/heal.png'}
}

enemigos_datos = {
	'squid': {'health': 120, 'exp': 100, 'damage': 8, 'attack_type': 'slash', 'attack_sound': './audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw',  'attack_sound': './audio/attack/claw.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 150, 'exp': 110, 'damage': 20, 'attack_type': 'thunder', 'attack_sound': './audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 100, 'exp': 120, 'damage': 10, 'attack_type': 'leaf_attack', 'attack_sound': './audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300},
    'boss': {'health': 1000, 'exp': 550, 'damage': 50, 'attack_type': 'nova', 'attack_sound': './audio/attack/slash.wav', 'speed': 5, 'resistance': 4, 'attack_radius': 60, 'notice_radius': 300}
    }
