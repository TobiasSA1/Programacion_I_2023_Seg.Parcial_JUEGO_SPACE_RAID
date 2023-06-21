from obj_ship import *
#CLASE PARA ENEMIGOS
class Enemy(Ship):

    #DEFINICION DE NAVES, AGREGAR 3 TIPOS DE NAVE MAS CON DIF CARACTERISTICAS
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                "red_2": (RED_2_SPACE_SHIP, RED_2_LASER),
                "green_2": (GREEN_2_SPACE_SHIP, GREEN_2_LASER),
                "blue_2": (BLUE_2_SPACE_SHIP, BLUE_2_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
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
        self.shoot_sound = pygame.mixer.Sound(os.path.join(carpeta_audio_lasers,"LASER_2.mp3"))
        self.enemy_vel = 0.9
        self.laser_vel = 4

    #FUNCION MOVIMIENTO DEL ENEMIGO
    def move(self, vel):
        self.y += vel

    #FUNCION DE DISPARO DEL ENEMIGO
    def shoot(self):
        if self.cool_down_counter == 0:
            self.shoot_sound.play()
            laser = Laser(self.x+2, self.y-5, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    #FUNCION PARA RE DIBUJAR EN PANTALLA
    def update(self,enemies,player,VENTANA):
        #SI EXPLOTA, CAMBIA LA IMAGEN DEL SHIP A VACIO, ARRANCA EL SPRITE DE EXPLOSION,ELIMINA EL ENEMIGO Y TERMINA LA EXPLOSION
        if self.is_exploding:

            self.lasers = []
            self.ship_img = VACIO
            self.explosion = self.explosion_images[self.explosion_index]
            rect_imagen = self.explosion.get_rect()

            x = self.x + 25 - rect_imagen.width // 2
            y = self.y + 25 - rect_imagen.height // 2

            VENTANA.blit(self.explosion, (x, y))

            self.explosion_index += 1

            if self.explosion_index >= len(self.explosion_images):

                enemies.remove(self)
                self.is_exploding = False
                self.explosion_index = 0

        else:
            #MUEVE LOS LASERES DEL ENEMIGO
            self.move_lasers(player)

            #SETEA DE MOVIMIENTO DE ENEMIGOS POR COLOR
            if self.ship_img == RED_SPACE_SHIP:
                    self.move(self.enemy_vel)
            if self.ship_img == GREEN_SPACE_SHIP:
                    self.move(self.enemy_vel+0.3)
            if self.ship_img == BLUE_SPACE_SHIP:
                    self.move(self.enemy_vel-0.1)
            #SETEA DE MOVIMIENTO DE ENEMIGOS POR COLOR 2
            if self.ship_img == RED_2_SPACE_SHIP:
                    self.move(self.enemy_vel)
            if self.ship_img == GREEN_2_SPACE_SHIP:
                    self.move(self.enemy_vel+0.2)
            if self.ship_img == BLUE_2_SPACE_SHIP:
                    self.move(self.enemy_vel-0.2)

            for laser in player.lasers[:]:

                if laser.collision(self):

                    #DAÑO DE LASERES JUGADOR A ENEMIGOS
                    if self.ship_img == RED_SPACE_SHIP:
                        self.health = self.health -100
                    if self.ship_img == GREEN_SPACE_SHIP:
                        self.health = self.health -100
                    if self.ship_img == BLUE_SPACE_SHIP:
                        self.health = self.health -100

                    #DAÑO DE LASERES JUGADOR A ENEMIGOS 2
                    if self.ship_img == RED_2_SPACE_SHIP:
                        self.health = self.health -50
                    if self.ship_img == GREEN_2_SPACE_SHIP:
                        self.health = self.health -50
                    if self.ship_img == BLUE_2_SPACE_SHIP:
                        self.health = self.health -50

                    #REMUEVE EL LASER DEL PLAYER SI COLISIONA CON EL ENEMIGO
                    player.lasers.remove(laser)
        
            if self.health <= 0:
                #EXPLOISION
                self.is_exploding = True
                #EXPLOISION SONIDO
                self.explosion_sound.play(0)

                #SCORES DE NAVES
                if self.ship_img == RED_SPACE_SHIP:
                    player.score = player.score + 150
                if self.ship_img == GREEN_SPACE_SHIP:
                    player.score = player.score + 200
                if self.ship_img == BLUE_SPACE_SHIP:
                    player.score = player.score + 250
                #SCORES DE NAVES 2
                if self.ship_img == RED_2_SPACE_SHIP:
                    player.score = player.score + 300
                if self.ship_img == GREEN_2_SPACE_SHIP:
                    player.score = player.score + 350
                if self.ship_img == BLUE_2_SPACE_SHIP:
                    player.score = player.score + 400

                
            if 0 <= self.x <= 800 and 0 <= self.y <= 600:
                if random.randrange(0, 2*60) == 1:
                    #DISPARO RANDOM DE LOS ENEMIGOS
                    #self.shoot_sound.play(0)
                    self.shoot()


            if collide(self, player):
                #DAÑO DE COLISION AL JUGADOR DE ENEMIGO
                player.health -= 30

                self.is_exploding = True
                self.explosion_sound.play(0)


            elif self.y + self.get_height() > ALTO:
                #ELIMINA LOS ENEMIGOS QUE SE PASAN DE LA PANTALLA
                player.lives = player.lives -1

                enemies.remove(self)
    #FUNCION PARA ACTUALIZAR SI ESTA EXPLOTANDO
    def explode(self):

        self.is_exploding = True
    
