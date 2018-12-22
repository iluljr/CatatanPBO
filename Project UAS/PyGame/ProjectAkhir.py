import math
import pygame
from os import path

## assets folder
sound_folder = path.join(path.dirname(__file__), 'suara')
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
KUNINGAN = (240, 230, 140)
RED=(255, 0, 0)
R= (255, 23, 100)
SKYBLUE = (43,191,254)
LSG = (60, 179, 113)
BROWN = (150, 75, 0)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
###############################
font_name = pygame.font.match_font('Comic Sans MS')
font = pygame.font.SysFont('Comic Sans MS',20)
font2 = pygame.font.SysFont('Comic Sans MS', 70)
font3 = pygame.font.SysFont('Comic Sans MS', 70)

def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render("Level: "+text, True, R) ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect) 
class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
        self.life=3
        self.mn=0
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('poke.png')
        self.image = pygame.transform.scale(self.image, (40, 60))
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
    def lifetext(self):
        lext = font.render("Life : ", True, R)
        lextpos = lext.get_rect(centerx=(SCREEN_WIDTH/2)-5)
        lextpos.top = 40
        screen.blit(lext, lextpos)

        lifeimg=pygame.image.load("Hati2.png")
        s=SCREEN_WIDTH/2
        for i in range(self.life):
            screen.blit(lifeimg,[s+20,47])
            s+=20
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

    def update_life(self):
        if self.rect.bottom >= 600:
            if self.life == 0:
                pygame.mixer.music.stop()
                game_over_sound.play()
                die_sound.stop()
                return True
            else:
                self.life-=1
                img = font.render(" ", True, WHITE)
                se=120
                screen.blit(img,[se,45])
                se-=20
                self.y=470
                self.x=100
        else:
            return False
    def update_menang(self):
        if self.rect.top <= 0:
            if self.mn == 0:
                win_sound.play()
                pygame.mixer.music.stop()
                return True
        else:
            return False
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -9
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -5
        self.image = pygame.image.load('poke2.png')
        self.image = pygame.transform.scale(self.image, (40, 60))
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 5
        self.image = pygame.image.load('poke.png')
        self.image = pygame.transform.scale(self.image, (40, 60))
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height,color):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()

##        self.image = pygame.image.load('brick1.png')
##        self.image = pygame.transform.scale(self.image, ([width, height]))
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()

class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1 
 
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
 
        # How far this world has been scrolled left/right
        self.world_shift = 0
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
  
    def shift_world(self, shift_y):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_y
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.y += shift_y
 
        for enemy in self.enemy_list:
            enemy.rect.y += shift_y
 
 
 #Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[800, 50, 0, 550, BROWN],
                 [50, 35, 50, 400, KUNINGAN],
                 [700, 10, 50, 430, KUNINGAN],
                 [50, 50, 750, 200, KUNINGAN],
                 [70, 20, 510, 150, KUNINGAN],
                 [60, 20, 300, 150, KUNINGAN],
                 [20, 20, 280, 130, KUNINGAN],
                 [20, 20, 260, 110, KUNINGAN],
                 [20, 20, 240, 90, KUNINGAN],
                 [680, 15, 120, 0,GREEN],
                 [50, 15, 0, 0,GREEN]
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            
            block = Platform(platform[0], platform[1],platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        block = MovingPlatform(70, 40, R)
        block.rect.x = 400
        block.rect.y = 280
        block.boundary_left = 200
        block.boundary_right = 575
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(20, 20, R)
        block.rect.x = 400
        block.rect.y = 410
        block.boundary_left = 300
        block.boundary_right = 500
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(50, 20, WHITE)
        block.rect.x = 190
        block.rect.y = 90
        block.boundary_left = 50
        block.boundary_right = 190
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

class Level_02(Level):
    """ Definition for level 1. """
##    pygame.mixer.music.stop()
##    #Play the gameplay music
##    pygame.mixer.music.load(path.join(sound_folder, 'enak.mp3'))
##    pygame.mixer.music.play(-1) 
## 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 
        # Array with width, height, x, and y of platform
        level = [[70, 20, 50, 580,KUNINGAN],
                 [40, 20, 0, 470,KUNINGAN],
                 [150, 15, 170, 430,KUNINGAN],
                 [15, 100, 320, 430,KUNINGAN],
                 [70, 20, 100, 300,GREEN],
                 [110, 20, 600, 270,KUNINGAN],
                 [700, 15, 0, 0,GREEN],
                 [50, 15, 750, 0,GREEN]
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1],platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        block = MovingPlatform(50, 50, WHITE)
        block.rect.x = 50
        block.rect.y = 300
        block.boundary_top = 300
        block.boundary_bottom = 490
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(50, 20, R)
        block.rect.x = 360
        block.rect.y = 470
        block.boundary_left = 360
        block.boundary_right = 420
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(60, 20, R)
        block.rect.x = 430
        block.rect.y = 450
        block.boundary_left = 430
        block.boundary_right = 640
        block.change_x = 2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(50, 30, R)
        block.rect.x = 750
        block.rect.y = 300
        block.boundary_top = 300
        block.boundary_bottom = 450
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(30, 30, WHITE)
        block.rect.x = 710
        block.rect.y = 70
        block.boundary_top = 70
        block.boundary_bottom = 300
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

class Level_03(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
##        self.background = pygame.image.load("backgr.jpg").convert()
##        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.level_limit = -1000
 
        # Array with width, height, x, and y of platform
        level = [[50, 20, 700, 580,BROWN],
                 [60, 20, 550, 500,KUNINGAN],
                 [60, 20, 400, 420,KUNINGAN],
                 [100, 15, 220, 420,KUNINGAN],
                 [15, 100, 320, 420,KUNINGAN],
                 [20, 20, 45, 260, KUNINGAN],
                 [20, 20, 65, 280, KUNINGAN],
                 [20, 20, 85, 300, KUNINGAN],
                 [650, 15, 100, 100,KUNINGAN],
                 [750, 15, 0, 0,GREEN],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        block = MovingPlatform(30, 30, WHITE)
        block.rect.x = 0
        block.rect.y = 100
        block.boundary_top = 100
        block.boundary_bottom = 530
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(60, 20, R)
        block.rect.x = 0
        block.rect.y = 580
        block.boundary_left = 0
        block.boundary_right = 340
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(40, 30, WHITE)
        block.rect.x = 760
        block.rect.y = 0
        block.boundary_top = 0
        block.boundary_bottom = 250
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

      
# Create platforms for the level
stage1_sound=pygame.mixer.music.load(path.join(sound_folder, 'backsound1.mp3'))
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)
jump_sound = pygame.mixer.Sound(path.join(sound_folder, 'jump.wav'))
##pygame.mixer.sound.set_volume(0)
die_sound = pygame.mixer.Sound(path.join(sound_folder, 'die.wav'))
game_over_sound = pygame.mixer.Sound(path.join(sound_folder, 'game_over.wav'))
win_sound = pygame.mixer.Sound(path.join(sound_folder, 'win.wav'))
background = pygame.image.load('backgr.jpg').convert()
background_rect = background.get_rect()
 
def main():
    """ Main Program """
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("LOMPAT-LOMPAT'")
 
    # Create the player
    player = Player()
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - 70
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    score=1
 
    # Is the game over?
    game_over = False
    menang= False
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                    jump_sound.play()
 

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

##        if player.rect.top <= 150:
##            diff = 150 - player.rect.top
##            player.rect.top = 150
##            current_level.shift_world(diff)
##
##        if player.rect.bottom >= 570:
##            diff = 570 - player.rect.bottom
##            player.rect.bottom = 570
##            current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        
        if player.rect.y < 0:
            player.rect.y = 480
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                score+=1
                player.level = current_level
         
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        # as the game is not over.
        if not game_over:
            # Update the player and ball positions
            if player.rect.bottom == 600:
                #player.update_life()
                game_over = player.update_life()
                if current_level_no == 1:
                    current_level = level_list[current_level_no]
                    player.level = current_level
##                    if self.life >= 1:
##                        die_sound.play()
                    player.rect.bottom = 560
                    player.rect.x = 70
                if current_level_no == 2:
                    current_level = level_list[current_level_no]
                    player.level = current_level
##                    if self.life >= 1:
##                        die_sound.play()
                    player.rect.bottom = 560
                    player.rect.x = 700
     
        # If we are done, print game over
        if game_over:
            screen.fill(R)
            text = font2.render("Game Over", True, BLACK)
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 250
            screen.blit(text, textpos)
        if not menang:
            # Update the player and ball positions
            if player.rect.top == 0:
                menang = player.update_menang()
                if current_level_no == 3:
                    current_level = level_list[current_level_no]
                    player.level = current_level
                    player.rect.top = 50
        if menang:
            screen.fill(SKYBLUE)
            text = font3.render("WINNER", True, BLACK)
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 250
            screen.blit(text, textpos)        
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        screen.fill(SKYBLUE)
        screen.blit(background, background_rect)
    # Draw Everything
        draw_text(screen, str(score), 20, SCREEN_WIDTH/2,15)
        player.lifetext()
    
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()
