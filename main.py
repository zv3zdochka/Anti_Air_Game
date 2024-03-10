import time
import os
import pygame
from math import *
from random import *
import sys

from pygame import K_LEFT, K_RIGHT, K_f, K_a, K_d, K_SPACE


class Base(object):
    def __init__(self):
        self.l = 3
        self.moving_rocket = []

    def count(self):
        R.create_rocket()
        rls_rocket = self.rls_update(R.rockets)
        self.rockets_move(R.rockets, H.house)
        self.border_check(R.rockets)
        self.fire(G.gun, rls_rocket)
        self.bullet_move(Bu.bullet, G.gun)
        self.bordere_check(Bu.bullet)
        # self.static(self.rockets_move(R.rockets, H.house), self.gun_move(rls_rocket))  # error
        self.hit(R.rockets, H.house, Bu.bullet)

    def fire(self, gun_co, rockets):
        global reload, mode, fire_wait, fire_time, time_f_f, rc, fire, shot, bum
        if mode:
            if fire_wait >= 1:

                if reload > 200:
                    reload = 0
                    fire_wait = -1
                    Bu.bullet_create(gun_co)
        else:
            global gun_pos
            self.gun_move(rockets, G.gun)
            if gun_pos:
                if reload > 200:
                    if fire_time:
                        fire_time = False
                        reload = 0
                        time_f_f = time.time()
                        Bu.bullet_create(gun_co)
            else:
                self.gun_move(rockets, G.gun)

    @staticmethod
    def rls_update(rockets):
        return RL.scan(rockets)

    def rockets_move(self, rockets, house):
        for stop_r in rockets:
            if stop_r.get('xy')[1] != -100:
                if (0 < stop_r.get('xy')[0] < 1000) and (-200 < stop_r.get('xy')[1] < 850):
                    self.moving_rocket.append(stop_r)
        if len(self.moving_rocket) == 0:
            rockets[0].get('xy')[1] = -99
        for i in self.moving_rocket:
            x0 = i.get('xy')[0]
            y0 = i.get('xy')[1]
            if not ((0 < x0 < 1000) and (-200 < y0 < 850)):
                self.moving_rocket.remove(i)
                continue
            if len(i) == 3:
                rc.play()
                s_x = (house[0].get('xy')[0] - x0) + 10
                ux = s_x / 1200
                uy = 870 / 1200
                x = x0 + ux * dt
                y = y0 + uy * dt
                i['xy'] = [x, y]
                i['ux'] = ux
                i['uy'] = uy
                return [ux, uy]
            else:
                rc.play()
                ux = i.get('ux')
                uy = i.get('uy')
                x = x0 + ux * dt
                y = y0 + uy * dt
                i['xy'] = [x, y]
                return [ux, uy]

    @staticmethod
    def border_check(list_of_objects):
        for j in list_of_objects:
            x = j.get('xy')[0]
            y = j.get('xy')[1]
            if not (0 <= x <= 1000 and -150 <= y < 800):
                list_of_objects = list_of_objects.remove(j)
        return list_of_objects

    @staticmethod
    def bordere_check(list_of_objects):
        for j in list_of_objects:
            x = j.get('xy')[0]
            y = j.get('xy')[1]
            if not (0 <= x <= 1100 and -150 <= y < 900):
                Bu.bullet.remove(j)

        return list_of_objects

    @staticmethod
    def bullet_move(bul, gun_co):
        for i in bul:
            a0 = gun_co[0].get('a')
            if a0 < 0:
                a = radians(90 - abs(gun_co[0].get('a')))
            elif a0 > 0:
                a = radians(90 + abs(gun_co[0].get('a')))
            else:
                a = radians(90)
            rc.stop()
            shot.play()
            rc.play()
            x = i.get('xy')[0]
            y = i.get('xy')[1]
            v = i.get('v')
            if i.get('u_x') is None:
                u_x = v * cos(a)
                u_y = -(v * sin(a))
                i['u_x'] = u_x
                i['u_y'] = u_y
            v_x = i.get('u_x')
            v_y = i.get('u_y')
            a_y = 9.81 * i.get('m')
            a_x = -0.47 * 1.200 * pi * (i.get('r') ** 2) * (v_x ** 2)
            v_y = v_y + a_y * dt
            v_x = v_x + a_x * dt
            x += v_x * dt + (a_x * dt ** 2) / 2
            y += v_y * dt + (a_y * dt ** 2) / 2
            i['u_x'] = v_x
            i['u_y'] = v_y
            i['xy'] = [x, y]

    @staticmethod
    def hit(roc, hou, bul):
        h_x, h_y = hou[0].get('xy')[0], hou[0].get('xy')[1]
        for i in roc:
            x_r, y_r = i.get('xy')[0], i.get('xy')[1]
            # r_c_x, r_c_y = (i.get('xy')[0] + 30) // 2, (i.get('xy')[1] + 100) // 2
            if h_x <= x_r <= h_x + 40 and h_y - 80 <= y_r <= h_y + 40:
                rc.stop()
                shot.stop()
                bum.play()
                shot.play()
                roc.remove(i)
                nein.play()
                time.sleep(4)
                exit('Rocket destroy the house')
            for f in bul:
                b_x, b_y, r = f.get('xy')[0], f.get('xy')[1], 8
                if h_x - 10 <= b_x <= h_x + 110 and h_y - 10 <= b_y <= h_y + 280:
                    rc.stop()
                    shot.stop()
                    bum.play()
                    bul.remove(f)
                    nein.play()
                    time.sleep(4)
                    exit('You destroy the house')
                if x_r - 10 <= b_x <= x_r + 34 and y_r - 30 <= b_y <= y_r + 110:
                    rc.stop()
                    shot.stop()
                    bum.play()
                    shot.play()
                    bul.remove(f)
                    roc.remove(i)
                    print("We intercepted enemy missile")
                    continue

    def gun_move(self, rls_get, gun):
        global gun_pos, fire_time, time_f_f
        if gun[0].get('a') > -81:
            gun[0]['a'] = gun[0].get('a') - 0.5
        elif gun[0].get('a') < -81:
            gun[0]['a'] = gun[0].get('a') + 0.5
        else:
            gun_pos = True
        f_c = sorted(rls_get, key=lambda key: key[2])[0]
        dis, a0 = f_c[2], f_c[1]
        if a0 < 0:
            a = radians(90 - a0)
        elif a0 > 0:
            a = radians(90 + a0)
        else:
            a = radians(90)
        x = dis * cos(90 - a) - defi / 2
        y = dis * sin((90 - a)) + defi * 0.7
        if -100 <= x <= 120 and - 100 <= y <= 120:
            if time_f_f == 0:
                time_f_f = time.time()
                fire_time = True
            elif time_f_f - time.time() < 5:
                pass
            else:
                time_f_f = time.time()
                fire_time = True


class ImmovingObject(Base):
    def __init__(self):
        super().__init__()


class RLS(ImmovingObject):
    def __init__(self):
        self.rls = []
        self.max_distance = 500
        self.scanning = []
        super().__init__()

    def create_rls(self):
        self.rls.append({
            'xy': [randint(100, 300), 760],
        })
        return self.rls

    def scan(self, rocket):
        self.scanning.clear()
        for rockets in rocket:
            cen_rls = self.center(self.rls[0].get('xy')[0] + 40, self.rls[0].get('xy')[1] + 40,
                                  self.rls[0].get('xy')[0],
                                  self.rls[0].get('xy')[1])
            cen_rocket = self.center(rockets.get('xy')[0] + 10, rockets.get('xy')[1] + 40, rockets.get('xy')[0],
                                     rockets.get('xy')[1])
            distance = sqrt(((rockets.get('xy')[0] + cen_rocket[0]) - (self.rls[0].get('xy')[0] + cen_rls[1])) ** 2 + (
                    (rockets.get('xy')[1] + cen_rocket[1]) - (self.rls[0].get('xy')[1] + cen_rls[1])) ** 2)
            # if distance > self.max_distance:
            #     continue
            angle = atan(
                (rockets.get('xy')[0] - self.rls[0].get('xy')[0]) / (rockets.get('xy')[1] - self.rls[0].get('xy')[1]))
            self.scanning.append((rockets.get('id'), degrees(angle), distance))
            print('SCANNING: ' + str(self.scanning))
        return self.scanning

    @staticmethod
    def center(x1, y1, x, y):
        x_c = 0.5 * (x1 - x)
        y_c = 0.5 * (y1 - y)
        return [x_c, y_c]


class House(ImmovingObject):
    def __init__(self):
        self.house = []
        super().__init__()

    def create_house(self):
        if not self.house:
            self.house.append({
                'xy': [randint(600, 750), 760]
            })
        else:
            pass
        return self.house


class MovingObject(Base):
    def __init__(self):
        super().__init__()


class Rocket(MovingObject):
    def __init__(self, house):
        self.rockets = []
        self.dis = []
        self.house = house
        super().__init__()

    def create_rocket(self):
        if self.l != len(self.rockets):
            for _ in range(self.l - len(self.rockets)):
                if not self.dis:
                    self.rockets.append({'xy': [x_r := randint(100, 900), -100],
                                         'id': id(randint(0, 1000)),
                                         'a': (degrees(atan((self.house[0].get('xy')[0] - x_r) / 850)))})
                else:
                    a = None
                    while a is None:
                        a = self.spawn_clear()
                    self.rockets.append({'xy': [x_r := a, -100],
                                         'id': id(randint(0, 1000)),
                                         'a': (degrees(atan((self.house[0].get('xy')[0] - x_r) / 850)))})
                for i in self.rockets:
                    self.dis.append(i.get('xy')[0])
        return self.rockets

    def spawn_clear(self):
        n_x_r = randint(100, 900)
        for i in self.dis:
            a = [i - 50, i + 50]
            b = [n_x_r - 50, n_x_r + 50]
            if self.inter(a, b):
                self.spawn_clear()
            else:
                return n_x_r

    @staticmethod
    def inter(a, b):
        intervals = [a, b]
        intervals.sort()
        for i, current_interval in enumerate(intervals):
            for follow_interval in intervals[i + 1:]:
                if current_interval[1] <= follow_interval[0]:
                    break
                return True
        return False


class Bullet(MovingObject):
    def __init__(self, coords):
        self.bullet = []
        self.gun_coord = coords
        super().__init__()

    def bullet_create(self, guns):
        x0, y0, a0 = guns[0].get('xy')[0], guns[0].get('xy')[1], guns[0].get('a')
        x = x0 + 100
        y = y0 - 110
        self.bullet.append({'xy': [x, y],
                            'v': (v := 12),
                            'r': 0.01,
                            'm': 0.0099,
                            'id': id(randint(0, 1000))})

        return self.bullet


class Gun(MovingObject):
    def __init__(self, rls):
        self.gun = []
        self.rls = rls
        super().__init__()

    def create_gun(self):
        self.gun.append({
            'xy': [(self.rls[0].get('xy')[0] + 16), 760],
            'a': -45,
            'v_f': 18

        })
        return self.gun


def do():
    B.count()


def render():
    global reload, fire_wait
    reload += 1

    def blitRotateCenter(surf, image, topleft, angle):

        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

        surf.blit(rotated_image, new_rect)

    # pygame.draw.circle(screen, 'red', (H.house[0].get('xy')[0], H.house[0].get('xy')[1]), 10)

    screen.blit(back, (0, 0))
    do()
    # bullets
    for j in Bu.bullet:
        screen.blit(bul_im, (j.get('xy')[0], j.get('xy')[1]))

    # rockets
    for roce in R.rockets:
        blitRotateCenter(screen, rocket_im, (roce.get('xy')[0], roce.get('xy')[1]), roce.get('a'))

    # house
    screen.blit(house_im, (H.house[0].get('xy')[0] - 100, H.house[0].get('xy')[1] - 127))

    # RLS
    screen.blit(rls_im, (RL.rls[0].get('xy')[0], RL.rls[0].get('xy')[1] - 100))
    if reload >= 200:
        pygame.draw.circle(screen, 'green', (RL.rls[0].get('xy')[0] + 105, RL.rls[0].get('xy')[1] + 30), 8)
    else:
        pygame.draw.circle(screen, 'red', (RL.rls[0].get('xy')[0] + 105, RL.rls[0].get('xy')[1] + 30), 8)

    # GUN
    blitRotateCenter(screen, gun_im, (G.gun[0].get('xy')[0], G.gun[0].get('xy')[1] - 200), G.gun[0].get('a') + 90)
    pygame.display.update()
    fps.tick(60)


bul_im = pygame.image.load('files/images/cannonBall.png')

gun_im1 = pygame.image.load('files/images/cannon_up.png')
gun_im = pygame.transform.scale(gun_im1, (250, 200))

house_im1 = pygame.image.load('files/images/house_ima.png')
house_im = pygame.transform.scale(house_im1, (300, 300))

rls_im1 = pygame.image.load('files/images/cannon_down.png')
rls_im = pygame.transform.scale(rls_im1, (250, 200))

rocket_im1 = pygame.image.load('files/images/rocket_im.png')
rocket_im = pygame.transform.scale(rocket_im1, (30, 100))

back0 = pygame.image.load('files/images_background/' + str(choice(os.listdir('files/images_background'))))
back = pygame.transform.scale(back0, (1000, 800))


pygame.mixer.pre_init(44100, -16, 8, 512)
pygame.mixer.init()
pygame.mixer.music.load('files/sounds/backgr.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

bum = pygame.mixer.Sound('files/sounds/bum.ogg')
rc = pygame.mixer.Sound('files/sounds/pr.ogg')
shot = pygame.mixer.Sound('files/sounds/shot.ogg')
nein = pygame.mixer.Sound('files/sounds/nein.ogg')
fire = pygame.mixer.Sound('files/sounds/fire.ogg')
fire.set_volume(20)
rc.set_volume(0.2)
reload = 0
dt = 2

gun_ready = 0
mode = True
fire_wait = 0
gun_pos = False
fire_time = False
time_f_f = 0

B = Base()
H = House()
RL = RLS()

H.create_house()
rls_co = RL.create_rls()
defi = (-rls_co[0].get('xy')[0] + H.house[0].get('xy')[0])
R = Rocket(H.house)
roc = R.create_rocket()
G = Gun(rls_co)
Bu = Bullet(G.create_gun())
pygame.init()
pygame.display.set_caption('Ballistic Game')
screen = pygame.display.set_mode((1000, 800))
fps = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not mode:
                mode = True
    keystate = pygame.key.get_pressed()
    if mode:
        a = G.gun[0].get('a')
        if keystate[K_LEFT]:
            a += 2
            if a >= 120:
                a = 120
            G.gun[0]['a'] = a
            time.sleep(0.01)
        if keystate[K_a]:
            a += 2
            if a >= 120:
                a = 120
            G.gun[0]['a'] = a
            time.sleep(0.01)
        if keystate[K_RIGHT]:
            a -= 2
            if a <= -120:
                a = -120
            G.gun[0]['a'] = a
            time.sleep(0.01)
        if keystate[K_d]:
            a -= 2
            if a <= -120:
                a = -120
            G.gun[0]['a'] = a
            time.sleep(0.01)
        if keystate[K_f]:
            mode = not mode
            time_f_f = 0
            time.sleep(0.06)
        if reload >= 200:
            if keystate[K_SPACE]:
                fire_wait = 1
                bum.stop()
                rc.stop()
                shot.stop()
                fire.play()
                time.sleep(0.01)
        render()
    else:
        if keystate[K_f]:
            mode = not mode
            time_f_f = 0
            time.sleep(0.06)
        render()
