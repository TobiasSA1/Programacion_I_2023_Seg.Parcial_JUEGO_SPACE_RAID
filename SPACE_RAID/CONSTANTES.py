import pygame
import os
import random
import time
import sqlite3
import re
import os

#CARPETA DEL JUEGO
carpeta_juego = os.path.dirname(__file__)
carpeta_miscelaneos = os.path.join(carpeta_juego,"MISCELANEOS")

#CARPETA DE IMAGENES
carpeta_imagenes = os.path.join(carpeta_miscelaneos,"IMAGENES")
#SUB-CARPETAS
carpeta_imagenes_explosiones = os.path.join(carpeta_imagenes,"EXPLOSIONES")
carpeta_imagenes_lasers = os.path.join(carpeta_imagenes,"LASERS")
carpeta_imagenes_menu = os.path.join(carpeta_imagenes,"MENU")
carpeta_imagenes_otros = os.path.join(carpeta_imagenes,"OTROS")
carpeta_imagenes_spaceships = os.path.join(carpeta_imagenes,"SPACESHIPS")


#CARPETA DE AUDIO
carpeta_audio = os.path.join(carpeta_miscelaneos,"AUDIO")
##SUB-CARPETAS
carpeta_audio_boton = os.path.join(carpeta_audio,"BOTON")
carpeta_audio_explosiones = os.path.join(carpeta_audio,"EXPLOSIONES")
carpeta_audio_lasers = os.path.join(carpeta_audio,"LASERS")
carpeta_audio_menu = os.path.join(carpeta_audio,"MENU")
carpeta_audio_musica = os.path.join(carpeta_audio,"MUSICA")
carpeta_audio_powerup = os.path.join(carpeta_audio,"POWERUP")

#CARPETA DE FUENTES
carpeta_fuentes = os.path.join(carpeta_miscelaneos,"FUENTES")

BLANCO = (255,255,255)
ROSA = (255,0,139)
ROJO = (255,106,158)
ROSA_AGUA = (255, 162, 247)
CELESTE = (162,255,209)
AMARILLO = (255,255,162)
VERDE = (0,255,0)
ROJO_ERROR = (255,0,0)


"""PYGAME RELOJ"""
clock = pygame.time.Clock()

"""PYGAME PANTALLA"""
ANCHO, ALTO = 800,600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
#NOMBRE DEL JUEGO
pygame.display.set_caption("SPACE RAID")
#ICONO DEL JUEGO
icono = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_JUGADOR1_CENTRO.png"))
pygame.display.set_icon(icono)
#os.path.join(,)
"""PYGAME FUENTE"""
pygame.font.init()
#DIFERENTES FUENTES PARA EL HUD, Y REPRINTEO
main_font = pygame.font.Font(os.path.join(carpeta_fuentes,"ka1.ttf"),30)
timer_font = pygame.font.Font(os.path.join(carpeta_fuentes,"ka1.ttf"), 15)
title_font = pygame.font.Font(os.path.join(carpeta_fuentes,"ka1.ttf"), 25)
game_font = pygame.font.Font(os.path.join(carpeta_fuentes,"ka1.ttf"), 75)

#FONDO BACKGROUND
BG = pygame.image.load(os.path.join(carpeta_imagenes_menu,"PLANETA.png"))

#FONDO DEL MENU PRINCIPAL
BG_MENU = pygame.image.load(os.path.join(carpeta_imagenes_menu,"PLANETA.png"))
#FONDO DE LA PANTALLA "LEVEL -"
BG_LEVEL = pygame.image.load(os.path.join(carpeta_imagenes_menu,"BACKGROUND_LEVEL.png"))
#FONDO DE INSTRUCCIONES
BG_INSTRUCCIONES =  pygame.image.load(os.path.join(carpeta_imagenes_menu,"BACKGROUND_INSTRUCCIONES.png"))
#FONDO GAME OVER
BG_GAME_OVER = pygame.image.load(os.path.join(carpeta_imagenes_menu,"BACKGROUND_LEVEL.png"))
#FONDO DE INGRESAR HIGHSCORE
BG_INGRESAR_HIGHSCORE = pygame.image.load(os.path.join(carpeta_imagenes_menu,"BACKGROUND.png"))
#FONDO DE HIGHSCORE EN EL MENU
BG_HIGHSCORE = pygame.image.load(os.path.join(carpeta_imagenes_menu,"BACKGROUND.png"))

#IMAGEN VACIA PARA SPRITES
VACIO = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"VACIO.png"))

"""NAVE JUGADOR ESTATICA"""
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_JUGADOR1_CENTRO.png"))
"""NAVE JUGADOR IZQUIERDA"""
YELLOW_SPACE_SHIP_L = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_JUGADOR1_IZQUIERDA.png"))
"""NAVE JUGADOR DERECHA"""
YELLOW_SPACE_SHIP_R = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_JUGADOR1_DERECHA.png"))
"""LASER JUGADOR IMAGENES"""
YELLOW_LASER = pygame.image.load(os.path.join(carpeta_imagenes_lasers,"LASER_AMARILLO.png"))

YELLOW_LASER = pygame.transform.scale(YELLOW_LASER, (int(YELLOW_LASER.get_width() * 0.50) , int(YELLOW_LASER.get_height() * 0.50)))


"""NAVES ENEMIGAS 1 IMAGENES"""
RED_SPACE_SHIP = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_ROJA.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_VERDE.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_AZUL.png"))

"""LASERS ENEMIGOS 1 IMAGENES"""
RED_LASER = pygame.image.load(os.path.join(carpeta_imagenes_lasers,"LASER_ROJO.png"))
RED_LASER = pygame.transform.scale(RED_LASER, (int(RED_LASER.get_width() * 0.50) , int(RED_LASER.get_height() * 0.50)))

GREEN_LASER = pygame.image.load(os.path.join(carpeta_imagenes_lasers,"LASER_VERDE.png"))
GREEN_LASER = pygame.transform.scale(GREEN_LASER , (int(GREEN_LASER.get_width() * 0.50) , int(GREEN_LASER.get_height() * 0.50)))

BLUE_LASER = pygame.image.load(os.path.join(carpeta_imagenes_lasers,"LASER_AZUL.png"))
BLUE_LASER = pygame.transform.scale(BLUE_LASER, (int(BLUE_LASER.get_width() * 0.50) , int(BLUE_LASER.get_height() * 0.50)))

"""NAVES ENEMIGAS 2 IMAGENES"""
RED_2_SPACE_SHIP = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_GRANDE_ROJA.png"))
GREEN_2_SPACE_SHIP = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_GRANDE_VERDE.png"))
BLUE_2_SPACE_SHIP = pygame.image.load(os.path.join(carpeta_imagenes_spaceships,"NAVE_GRANDE_AZUL.png"))
"""LASERS ENEMIGOS 2 IMAGENES"""
RED_2_LASER = pygame.image.load(os.path.join(carpeta_imagenes_lasers,"LASER_ROJO.png"))
RED_2_LASER = pygame.transform.scale(RED_2_LASER, (int(RED_2_LASER.get_width() * 0.50) , int(RED_2_LASER.get_height() * 0.50)))
GREEN_2_LASER = pygame.image.load(os.path.join(carpeta_imagenes_lasers,"LASER_VERDE.png"))
GREEN_2_LASER = pygame.transform.scale(GREEN_2_LASER, (int(GREEN_2_LASER.get_width() * 0.50) , int(GREEN_2_LASER.get_height() * 0.50)))
BLUE_2_LASER = pygame.image.load(os.path.join(carpeta_imagenes_lasers,"LASER_AZUL.png"))
BLUE_2_LASER = pygame.transform.scale(BLUE_2_LASER, (int(BLUE_2_LASER.get_width() * 0.50) , int(BLUE_2_LASER.get_height() * 0.50)))

"""POWER-UPS IMGANES"""
RED_POWERUP = pygame.image.load(os.path.join(carpeta_imagenes_otros,"POWERUP_ROJO.png"))
GREEN_POWERUP = pygame.image.load(os.path.join(carpeta_imagenes_otros,"POWERUP_VERDE.png"))
GREEN_2_POWERUP = pygame.image.load(os.path.join(carpeta_imagenes_otros,"POWERUP_VERDE_2.png"))
BLUE_POWERUP = pygame.image.load(os.path.join(carpeta_imagenes_otros,"POWERUP_AZUL.png"))

#VARIABLES PARA POWER-UP TIMER. (Total seran trabajadas dentro de la funcion)
timer_iniciado = False
duracion_powerup = 10000  
tiempo_colision = None
#VARIABLE ERROR PARA MOSTRAR MENSAJE EN HIGHSCORE
error = 0
#FPS
FPS = 60

#DEFINICION COLISION
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
#FUNCION PARA OBTENER FUENTE KARMATIC ARCADE
def get_font(size):
    return pygame.font.Font(os.path.join(carpeta_fuentes,"ka1.ttf"), size)
#FUNCION PARA VALIDAR NOMBRE ANTES DE INGRESARLO A LA BASE DE DATOS
def validar_nombre(nombre):
    return bool(re.match("^[a-zA-Z0-9]+$", nombre))
#SETEAR MUSICA DE FONDO
def musica():

    pygame.mixer.music.load(os.path.join(carpeta_audio_musica,"FONDO.mp3"))
    pygame.mixer.music.play(-1)
#SETEAR MUSICA PARA EL JUEGO
def musica_juego():

    pygame.mixer.music.load(os.path.join(carpeta_audio_musica,"FONDO_JUEGO.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def boton_sonido():
    BOTON_MUSIC = pygame.mixer.Sound(os.path.join(carpeta_audio_boton,"BOTON.mp3"))
    BOTON_MUSIC.play(0)

def error_sonido():
    ERROR_MUSIC = pygame.mixer.Sound(os.path.join(carpeta_audio_menu,"ERROR.mp3"))
    ERROR_MUSIC.play(0)

def ingresar_highscore_sonido():

    INGRESAR_HIGHSCORE_MUSIC = pygame.mixer.Sound(os.path.join(carpeta_audio_menu,"FELICITACIONES.mp3"))
    INGRESAR_HIGHSCORE_MUSIC .play(0)

def game_over_sonido():
    GAME_OVER = pygame.mixer.Sound(os.path.join(carpeta_audio_menu,"GAME_OVER.mp3"))
    GAME_OVER.play(0)

#TECLAS PARA CONTROLAR LA MUSICA. N = MUTEAR, M = DESMUTEAR , 9 = BAJAR, 0 = SUBIR
def musica_controles():
    
    keys = pygame.key.get_pressed()    

    if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)  


    if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)


    elif keys[pygame.K_m]:

        pygame.mixer.music.set_volume(1.0)


    elif keys[pygame.K_n]:

        pygame.mixer.music.set_volume(0.0)         
        


