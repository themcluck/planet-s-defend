from pygame.math import Vector2
from pygame.transform import rotozoom
from settings import loader, wrap_pos, vel_rand
UP = Vector2(0, -1)

class GameObject:
    def __init__(self, pos, sprite, vel):
        self.pos = Vector2(pos)
        self.sprite = sprite
        self.radius = sprite.get_width()*0.5
        self.vel = Vector2(vel)

    def obj_move(self, surface):
        self.pos = wrap_pos(self.pos+self.vel, surface)

    def obj_draw(self, surface):
        blit_pos = self.pos - Vector2(self.radius)
        surface.blit(self.sprite, blit_pos)

    def obj_collide(self, other):
        dis = self.pos.distance_to(other.pos)
        return dis < self.radius + other.radius


class Player(GameObject):
    MANEUV = 3
    ACC = 0.35
    BULLET_SPEED = 4
    BULLET_KD = 2

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.dir = Vector2(UP)
        super().__init__(position, loader("player"), Vector2(0))

    def draw(self, surface):
        angle = self.dir.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_pos = self.pos - rotated_surface_size*0.5
        surface.blit(rotated_surface, blit_pos)

    def rotate(self, clockwise=True):
        if clockwise:
            sign = 1
        else:
            sign = -1
        angle = self.MANEUV*sign
        self.dir.rotate_ip(angle)

    def fow_accelerate(self):
        self.vel += self.dir*self.ACC

    def back_accelerate(self):
        self.vel -= self.dir*self.ACC

    def shoot(self):
        b_vel = self.dir*self.BULLET_SPEED+self.vel
        bullet = Bullet(self.pos, b_vel)
        self.create_bullet_callback(bullet)

class Bullet(GameObject):
    def __init__(self, pos, vel):
        super().__init__(pos, loader("bullet"), vel)

class Meteor(GameObject):
    def __init__(self, position, create_meteor_callback, size=3):
        self.create_meteor_callback = create_meteor_callback
        self.size = size

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25
        }
        scale = size_to_scale[size]
        sprite = rotozoom(loader("meteor"), 0, scale)
        super().__init__(position, loader("meteor"), vel_rand(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                self.meteor = Meteor(self.pos, self.create_meteor_callback, self.size - 1)
            self.create_meteor_callback(self.meteor)
