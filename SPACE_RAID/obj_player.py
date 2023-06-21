from obj_ship import *
#CONSTRUCTOR PLAYER
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0
        self.level = 0
        self.lives = 3
        self.laser_vel = 4
        self.vel = 7
        self.shoot_sound = pygame.mixer.Sound(os.path.join(carpeta_audio_lasers,"LASER.mp3"))

    def move_lasers(self):
        self.cooldown()
        for laser in self.lasers:
            laser.move(-self.laser_vel)
            if laser.off_screen(ALTO):
                self.lasers.remove(laser)


    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
    
    def update(self):
        #MOVIMIENTO W,A,S,D ESPACIO(DISPARAR),
        keys = pygame.key.get_pressed()

        self.ship_img = YELLOW_SPACE_SHIP

        if keys[pygame.K_a] and self.x - self.vel > 0: #IZQUIERDA

            self.x -= self.vel
            self.ship_img = YELLOW_SPACE_SHIP_L
            
        if keys[pygame.K_d] and self.x + self.vel + self.get_width() < ANCHO: #DERECHA
            self.x += self.vel
            self.ship_img = YELLOW_SPACE_SHIP_R

        if keys[pygame.K_w] and self.y - self.vel > 0: #ARRIBA
            self.y -= self.vel

        if keys[pygame.K_s] and self.y + self.vel + self.get_height() + 15 < ALTO: #ABAJO
            self.y += self.vel
        
        if keys[pygame.K_SPACE]:#DISPARAR
            #self.shoot_sound.play(1)
            self.shoot()
            
            
