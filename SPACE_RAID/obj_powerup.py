from CONSTANTES import *

class PowerUp:

    COLOR_MAP = {
                "red": (RED_POWERUP),
                "green": (GREEN_POWERUP),
                "blue": (BLUE_POWERUP),
                "green_2": (GREEN_2_POWERUP)
                }
    
    #BANDERA PARA CUANDO PICKEE EL POWERUP AZUL SOLO SE PUEDA USAR UNA VEZ.
    bandera_powerup_azul = 1

    #CONSTRUCTOR NAVES
    def __init__(self, x, y,color):
        self.x = x
        self.y = y
        self.img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 1
        #CRONOMETRO PARA POWERUP DE VELOCIDAD
        self.timer_iniciado = False
        self.duracion_powerup = 10000  
        self.tiempo_colision = None
        self.explosion_index = 0
        self.explosion_images = []
        #NUMERO DE IMAGENES
        num_imagenes = 37
        #CARGAR LAS IMAGENES
        for i in range(1, num_imagenes + 1):
            #CONSTRUIR LA RUTA DEL ARCHIVO DE IMAGEN
            ruta_imagen = os.path.join(carpeta_imagenes_explosiones, f"{i}.png")
            #CARGAR LA IMAGEN Y AGREGARLA A LA LISTA
            imagen = pygame.image.load(ruta_imagen)
            self.explosion_images.append(imagen)
        self.is_exploding = False
        self.explosion_sound = pygame.mixer.Sound(os.path.join(carpeta_audio_explosiones,"EXPLOSION.mp3"))
        self.collect_sound = pygame.mixer.Sound(os.path.join(carpeta_audio_powerup,"POWERUP.mp3"))
        self.bandera_powerup_azul = 1

    def draw(self, ventana):
        ventana.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.vel

    def collision(self, obj):
        return collide(self, obj)
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def move_powerup(self, vel, obj):

        for powerup in self.powerups:
            powerup.move(vel)
            if powerup.off_screen(ALTO):
                self.powerup.remove(powerup)
            elif powerup.collision(obj):
            
                self.powerup.remove(powerup)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def update(self,power_ups,player,VENTANA):
        
        bandera = 1

        if self.is_exploding:

            self.img = VACIO
            self.explosion = self.explosion_images[self.explosion_index]
            rect_imagen = self.explosion.get_rect()

            x = self.x + 25 - rect_imagen.width // 2
            y = self.y + 25 - rect_imagen.height // 2

            VENTANA.blit(self.explosion, (x, y))

            self.explosion_index += 1

            if self.explosion_index >= len(self.explosion_images):

                power_ups.remove(self)
                self.is_exploding = False
                self.explosion_index = 0

                bandera = 1
                

        else:

            self.move()

            if collide(self, player):
                #DAÑO DE COLISION AL JUGADOR DE ENEMIGO
                if self.img == RED_POWERUP:
                    if bandera == 1:
                        player.score = player.score - 200
                        player.health -= 50

                        if player.score < 0:
                            player.score = 0
                            
                        bandera = 0

                        self.is_exploding = True
                        self.explosion_sound.play(0)
                    

                if self.img == GREEN_POWERUP:
                    self.collect_sound.play(0)
                    if player.health < 100:
                        player.health += 30
                        if player.health > 100:
                            player.health = 100
                    player.score = player.score + 750
                    power_ups.remove(self)


                if self.img == BLUE_POWERUP:

                    

                    if PowerUp.bandera_powerup_azul == 1:

                        self.collect_sound.play(0)
                        player.score = player.score + 500
                        PowerUp.bandera_powerup_azul = 0

                        player.vel = 7
                        player.laser_vel = 10
                        player.COOLDOWN = 10
                        
                        if not self.timer_iniciado:

                            self.tiempo_colision = pygame.time.get_ticks()
                            self.timer_iniciado = True
                            self.vel = 0
                            self.img = VACIO
                    else:
                        self.collect_sound.play(0)
                        player.score = player.score + 500
                        power_ups.remove(self)

                if self.img == GREEN_2_POWERUP:
                    self.collect_sound.play(0)
                    player.lives = player.lives + 1
                    if player.lives >= 7:
                        player.lives = 6
                    player.score = player.score + 1000
                    power_ups.remove(self)


            elif self.y + self.get_height() > ALTO:

                power_ups.remove(self)
