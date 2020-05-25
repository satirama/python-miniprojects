# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(sprite_set, canvas):
    for s in list(sprite_set):
        s.draw(canvas)
        if s.update():
            sprite_set.remove(s)

def group_collide(group, other_object):
    for g in list(group):
        if g.collide(other_object):
            pos = g.get_pos()
            group.remove(g)
            explosion = Sprite(pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            return True

def group_group_collide(group1, group2):
    num_collisions = 0
    for g in list(group1):
        if group_collide(group2, g):
            num_collisions += 1
            group1.discard(g)
    return num_collisions
    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
            
    def update(self):
        # position update
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # friction update 
        friction = 0.05
        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction)
    
        # velocity update (small scalar to increase velocity in an adequate amount)
        if self.thrust:
            forward = angle_to_vector(self.angle)
            scalar = 1.2
            self.vel[0] += forward[0] * scalar
            self.vel[1] += forward[1] * scalar
       
    def set_thrust(self,on):
        if on:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def turn(self, direction):
    # angle_vel fixed value according to the direction   
        if direction == 'right':
            self.angle_vel = 0.08
        elif direction == 'left':
            self.angle_vel = -0.08
        else:
            self.angle_vel = 0
     
    def shoot(self):
        forward = angle_to_vector(self.angle)
        scalar = 1.2
        ship_point_pos = [self.pos[0] + forward[0] * self.radius, self.pos[1] + forward[1] * self.radius]
        missile_vel = [self.vel[0] + forward[0] * scalar * 2, self.vel[1] + forward[1] * scalar * 2] 
        missile_group.add(Sprite([ship_point_pos[0], ship_point_pos[1]], [missile_vel[0], missile_vel[1]], 0, 0, missile_image, missile_info, missile_sound))
        missile_sound.play()
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
              
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.animated:
                tick_index = (self.age % self.lifespan) // 1
                current_center = self.image_center[0] + tick_index * self.image_size[0]
                canvas.draw_image(self.image, [current_center, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
                
       
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age <= self.lifespan:
            return False
        else:
            return True

    def collide(self, other_object):
        return dist(self.get_pos(), other_object.get_pos()) <= self.get_radius() + other_object.get_radius()
        
#Key handlers
def key_down(key):
    #global 
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        my_ship.set_thrust(True)
    elif  key == simplegui.KEY_MAP['left']:
        my_ship.turn('left')
    elif  key == simplegui.KEY_MAP['right']:
        my_ship.turn('right')
    elif  key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def key_up(key):
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False 
        my_ship.set_thrust(False)        
    elif  key == simplegui.KEY_MAP['left']:
        my_ship.turn('stop')
    elif  key == simplegui.KEY_MAP['right']:
        my_ship.turn('stop')

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started, my_ship
    ship_pos = my_ship.get_pos()
    r_pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
    sign = [-1,1]
    scalar = score // 50 + 1.8
    r_vel = [random.random() * scalar * random.choice(sign), random.random() * scalar * random.choice(sign)]
    r_ang_vel= random.random() * .1 * random.choice(sign)
    if started and len(rock_group) < 12:
        rock = Sprite([r_pos[0], r_pos[1]], [r_vel[0], r_vel[1]], 0, r_ang_vel, asteroid_image, asteroid_info)
        # checks position, if it does not overlap the ship then rock is drawn
        r = rock.get_pos()
        h_overlap = ship_pos[0] + 1.7 * my_ship.get_radius() > r[0] > ship_pos[0] - 1.7 * my_ship.get_radius()
        v_overlap = ship_pos[1] + 1.7 * my_ship.get_radius() > r[1] > ship_pos[1] - 1.7 * my_ship.get_radius()
        if not h_overlap and not v_overlap:
            rock_group.add(rock)
            
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, soundtrack
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()

def draw(canvas):
    global time, lives, score, started, rock_group, my_ship, soundtrack
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(missile_group,canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    my_ship.update()
    
    # draw text
    canvas.draw_text("Lives: " + str(lives), [20, 30], 20, 'White')
    canvas.draw_text("Score: " + str(score), [WIDTH - 90, 30], 20, 'White')

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())    
        
    # restart if game over
    if started and group_collide(rock_group, my_ship):
        lives -= 1
        if lives == 0:
            started = False
            rock_group = set([])
            lives = 3
            score = 0
            my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
            soundtrack.rewind()
    
    # update score if missile hits a rock
    score += 10 * group_group_collide(rock_group, missile_group)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and three sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_mouseclick_handler(click)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

# get things rolling
timer.start()
frame.start()