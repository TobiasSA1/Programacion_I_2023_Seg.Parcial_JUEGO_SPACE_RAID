from CONSTANTES import *
from obj_laser import Laser

#CLASE PARA NAVES
class Ship:
    #COOLDOWN DE DISPARO
    COOLDOWN = 30

    #CONSTRUCTOR NAVES
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, ventana):
        ventana.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(ventana)

    #COLISION DE LASERES CON OBJETOS
    def move_lasers(self, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(self.laser_vel)
            if laser.off_screen(ALTO):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                #DAÑO POR LASER DE LOS ENEMIGOS

                if self.ship_img == RED_2_SPACE_SHIP or self.ship_img == GREEN_2_SPACE_SHIP or self.ship_img == BLUE_2_SPACE_SHIP:
                    obj.health -= 50
                    self.lasers.remove(laser)
                else:
                    obj.health -=20
                    self.lasers.remove(laser)
                

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            self.shoot_sound.play()
            #POSICION DEL LASER DEL PLAYER
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
    