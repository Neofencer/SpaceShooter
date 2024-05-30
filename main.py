import pygame as py
import random
from os.path import join





class Player(py.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image=py.image.load(join('images','player.png')).convert_alpha()
        self.rect=self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction=py.Vector2()
        self.speed=300

        #cool down and fire logic
        self.can_shoot=True
        self.laser_shoot_time=0
        self.cooldown_duration=400


        

        #mask
        self.mask=py.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time=py.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot=True

    def update(self,dt):
        keys=py.key.get_pressed()
        self.direction.x=int(keys[py.K_RIGHT]) - int(keys[py.K_LEFT])
        self.direction.y=int(keys[py.K_DOWN]) - int(keys[py.K_UP])
        self.direction=self.direction.normalize() if self.direction else self.direction
        self.rect.center +=self.direction*self.speed*dt

        recent_keys=py.key.get_just_pressed()
        if recent_keys[py.K_SPACE]and self.can_shoot:
            Laser(lazer_surf,self.rect.midtop,(all_sprites,laser_sprites))
            self.can_shoot=False
            self.laser_shoot_time=py.time.get_ticks()
            laser_sound.play()

         
        self.laser_timer()

#Create 20 Star sprites and display them on the screen in random positions

class Star(py.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH),random.randint(0, WINDOW_HEIGHT)))


class Meteor(py.sprite.Sprite):
    def __init__(self,surf,groups):
        super().__init__(groups)
        self.original_surf=surf
        self.image=self.original_surf
        self.rect=self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH),random.randint(-200,-100)))
        self.start_time=py.time.get_ticks()
        self.lifetime=3000
        self.direction=py.Vector2(random.uniform(-0.5,0.5),1)
        self.speed=random.randint(400,500)
        self.rotation=0


    def update(self,dt):
        self.rotation +=random.randint(20,50)*dt
        self.rect.center +=self.direction*self.speed *dt
        self.image=py.transform.rotozoom(self.original_surf, self.rotation,1)
        #to avoid weird behavior as the image is updating but not the rectangle we need to update the rectangle as well with the new image position
        self.rect=self.image.get_frect(center=self.rect.center)
        if py.time.get_ticks()-self.start_time>=self.lifetime:
            self.kill()

        



class Laser(py.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(midbottom=pos)
        
#to move things you update the position of the rectangle
    def update(self,dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom <0:
            self.kill()


class AnimatedExplosion(py.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frames=frames
        self.index=0
        self.image=self.frames[self.index]
        self.rect=self.image.get_frect(center=pos)
        
        

    def update(self,dt):
        self.index +=20 *dt
        if self.index<len(self.frames):
            
            self.image=self.frames[int(self.index)]
            
        else:
            self.kill()



def collision():
    global running
    global score
    global game_state
    collision_sprites=py.sprite.spritecollide(player,meteor_sprites,True,py.sprite.collide_mask)
    if collision_sprites:
        game_state = "game_over"

    #check if in the group of laser it collide with meteor
    for laser in laser_sprites:
        collided_sprites=py.sprite.spritecollide(laser,meteor_sprites,True)
        if collided_sprites:
            laser.kill()
            score+=1
            AnimatedExplosion(explosion_frames,laser.rect.midtop,all_sprites)
            explosion_sound.play()


def display_score():
    #if I want the score in time or no
    #current_time=py.time.get_ticks()
    text_surf=font.render(str(score),True,(240,240,240))
    text_rect=text_surf.get_frect(midbottom=(WINDOW_WIDTH/2,WINDOW_HEIGHT-50))
    display_surface.blit(text_surf,text_rect)
    py.draw.rect(display_surface,(240,240,240),text_rect.inflate(20,10).move(0,-8),5,10)




#pygame setup
py.init()
py.display.set_caption("Space shooter")
WINDOW_WIDTH, WINDOW_HEIGHT=1280,720
display_surface=py.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock=py.time.Clock()
running =True
score=0


#creating surface
surf=py.Surface((100,200))
surf.fill('orange')
x=100


all_sprites=py.sprite.Group()
meteor_sprites= py.sprite.Group()
laser_sprites=py.sprite.Group()

#to prevent importanting the star 20 time
star_surf=py.image.load('images\star.png').convert_alpha()
for i in range(20):
    Star(all_sprites,star_surf)

player=Player(all_sprites)

#importing an image
# player_surf= py.image.load('images\player.png').convert_alpha()
# player_rect = player_surf.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
# player_direction=py.math.Vector2(0,0)
# player_speed=200

#stars
# star_surf=py.image.load('images\star.png').convert_alpha()
# stars = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(20)]


#Meteors
meteor_surf=py.image.load('images\meteor.png').convert_alpha()
#meteor_rect=meteor_surf.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

#lazers
lazer_surf=py.image.load('images\laser.png').convert_alpha()
#lazer_rect=lazer_surf.get_frect(bottomleft=(20,WINDOW_HEIGHT-20))

font=py.font.Font('images\Oxanium-Bold.ttf',40)
# text_surf=font.render('text',True,(240,240,240))

explosion_frames=[py.image.load(join('images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]
print(explosion_frames)


laser_sound=py.mixer.Sound(join('audio','laser.wav'))
laser_sound.set_volume(0.2)


explosion_sound=py.mixer.Sound(join('audio','explosion.wav'))
explosion_sound.set_volume(0.3)

#custom events -> meteor event
meteor_event=py.event.custom_type()
#event happen every 0.5
py.time.set_timer(meteor_event,500)

game_state = "start_menu"

def draw_start_menu():
   display_surface.fill((0, 0, 0))
   font = py.font.SysFont('arial', 40)
   title = font.render('My Game', True, (255, 255, 255))
   start_button = font.render('Start', True, (255, 255, 255))
   display_surface.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2, WINDOW_HEIGHT/4 - title.get_height()/2))
   display_surface.blit(start_button, (WINDOW_WIDTH/2 - start_button.get_width()/2, WINDOW_HEIGHT/2))
   py.display.update()


def game_over():
   display_surface.fill((0, 0, 0))
   font = py.font.SysFont('arial', 40)
   title = font.render('Game_Over', True, (255, 255, 255))
   restart_button = font.render('R - Restart', True, (255, 255, 255))
   quit_button = font.render('Q - Quit', True, (255, 255, 255))
   display_surface.blit(title, (WINDOW_WIDTH/2 - title.get_width()/2, WINDOW_HEIGHT/4 - title.get_height()/2))
   display_surface.blit(restart_button, (WINDOW_WIDTH/2 - restart_button.get_width()/2, WINDOW_HEIGHT/2))
   display_surface.blit(quit_button, (WINDOW_WIDTH/2 - quit_button.get_width()/2, WINDOW_HEIGHT/2.5 + quit_button.get_height()/2))
   py.display.update()

while running:
    dt = clock.tick() / 1000

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
         
        if event.type == meteor_event:
            Meteor(meteor_surf, (all_sprites, meteor_sprites))

    if game_state == "start_menu":
        draw_start_menu()
        keys = py.key.get_pressed()
        if keys[py.K_SPACE]:
            game_state = "game"
    elif game_state == "game":
        all_sprites.update(dt)
        collision()
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE]:
            py.quit()
            quit()

        display_surface.fill('#3a2e3f')
        display_score()
        all_sprites.draw(display_surface)
    
    elif game_state == "game_over":
       game_over()
       score=0
       keys = py.key.get_pressed()
       if keys[py.K_r]:
           game_state = "start_menu"
       if keys[py.K_q]:
           py.quit()
           quit()



    py.display.update()

py.quit()