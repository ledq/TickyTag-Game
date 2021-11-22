import pygame,sys
import random,math

def get(filename):
    return pygame.image.load(filename)

class Media:
    def __init__(self):
        self.lobby= get("Starting_window_official.png")
        self.start = get("Click_start.png")
        self.howto = get("Click_howtoplay.png")
        self.guidline = get("Guildnew1.png")
        self.set_time = get("Click_settime.png")

        self.blue_win = get("Blue_win.png")
        self.pink_win = get("Pink_win.png")

        # self.opening_music = pygame.mixer.music.play()
        self.click_sound = pygame.mixer.Sound("interface1.wav")
        self.tag_sound = pygame.mixer.Sound("the tag.wav")
        self.hit_trap_sound = pygame.mixer.Sound("Oooo.wav")
        self.hit_trap_sound2= pygame.mixer.Sound("Oooo.wav")
        self.wave_sound = pygame.mixer.Sound("pulling.wav")
        self.gem_sound = pygame.mixer.Sound('bubble2.wav')
        self.boost_sound = pygame.mixer.Sound("Powerup13.wav")


class Ball:
    def __init__(self, screen, x, y, radius, color, role):
        self.screen = screen
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
        self.radius = radius
        self.role = role
        self.color = color
        self.original_color = color
        self.dust_color = color
        if self.original_color == (244, 119, 125):
            self.skill_color = (237, 28, 36)
        if self.original_color == (88, 196, 222):
            self.skill_color = (0, 110, 245)
        self.velocity = 2.25
        self.speed = 0

        self.become_chaser = False
        self.skill_time = -7
        # Motion Trail
        self.dust = []
        self.dust_activate = False
        # Waves
        self.stunt_time = pygame.time.get_ticks()
        self.wave = Wave(screen)
        self.waves = [self.wave]
        self.wave_activate = False
        self.wave_time = -10000
        self.push_speed = 2
        self.wave_cooldown_time = 6000
        self.sign = 1
        # Spike:
        self.stunt = False

    def draw(self):
        self.draw_wave()
        self.creat_dust()
        self.dust_move()

        pygame.draw.circle(self.screen, self.color, (self.x, self.y),
                           self.radius)

        self.get_tag()

    def distance(self, opponent):
        return math.sqrt((self.x - opponent.x) ** 2 + (self.y - opponent.y) ** 2)

    def turnback(self, border_x, border_y):
        if self.x <= border_x:
            self.x = self.screen.get_width() - border_x - 1
        if self.x >= self.screen.get_width() - border_x:
            self.x = border_x + 1

        if self.y <= border_y:
            self.y = self.screen.get_height() - 50 - 1
        if self.y >= self.screen.get_height() - 50:
            self.y = border_y + 1

    def make_hitbox(self):
        return pygame.draw.circle(self.screen, self.color, (self.x, self.y),
                                  self.radius)

    def get_tag(self):
        if self.become_chaser:
            pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y),
                               self.radius / 2.5, 3)

    def cool_down(self):
        if pygame.time.get_ticks() // 1000 - self.skill_time > 6:
            self.speed = 0
            if pygame.time.get_ticks() - self.stunt_time > 1500:
                self.dust_color = self.original_color
        if pygame.time.get_ticks() // 1000 - self.skill_time <= 6:
            if pygame.time.get_ticks() - self.stunt_time > 1500:
                self.dust_color = self.skill_color

    def creat_dust(self):
        if self.dust_activate == True:
            new_particle = Dust(self.screen, self.x + random.randint(-self.radius + 1, self.radius - 1),
                                self.y + random.randint(-self.radius + 1, self.radius - 1), self.dust_color)
            self.dust.append(new_particle)

    def dust_move(self):
        for particle in self.dust:
            if particle.radius <= 0:
                self.dust.remove(particle)
            particle.move()
            particle.draw()

    def draw_wave(self):
        if pygame.time.get_ticks() - self.wave_time < self.wave_cooldown_time:
            for wave in self.waves:
                if wave.radius == self.radius * 3:
                    self.waves.append(Wave(self.screen))
                if wave.radius >= self.radius * 12:
                    self.waves.remove(wave)
                wave.expand()
                wave.draw(self.x, self.y, self.color)

    def push(self, opponent):
        if pygame.time.get_ticks() - self.wave_time < self.wave_cooldown_time:
            if self.distance(opponent) <= self.radius * 12:
                opponent.x += (self.sign * (self.x - opponent.x) * (self.push_speed)) / self.distance(opponent)
                opponent.y += (self.sign * (self.y - opponent.y) * (self.push_speed)) / self.distance(opponent)


#####################################################################################################################

class Timer:
    def __init__(self, screen):
        self.screen = screen
        self.time_set_string = ''
        self.time_limit = 2
        self.time_run = 60
        self.minute = '0'
        self.second = '0'
        self.complement = 0
        self.waiting_time = 0
        self.string = "{} : {}".format(self.time_limit, self.time_run)
        self.timesup = False
        self.font = pygame.font.Font("FreeSansBold-Xgdd.ttf", 40)
        self.color = (255, 255, 255)
        # Lobby:
        self.input_appear = False
        self.set_font = pygame.font.Font("FreeSansBold-Xgdd.ttf", 30)
        self.box = pygame.Rect(640, 630, 100, 30)
        self.border_color = (255, 255, 255)
        self.dash = '_'
        self.input_box = "Set the time limit {}{} : 00".format(self.dash, self.time_set_string)
        self.input_image = self.set_font.render(self.input_box, True, self.border_color)

    def draw(self):
        if self.time_run < 10:
            self.second = '0'

            if self.time_limit == 0:
                self.color = (255, 0, 0)
        else:
            self.second = ''
            self.color = (255, 255, 255)
        if self.time_limit < 10:
            self.minute = '0'
        else:
            self.minute = ''
        self.string = "{}{} : {}{}".format(self.minute, self.time_limit, self.second, self.time_run)
        image = self.font.render(self.string, True, self.color)
        self.screen.blit(image, (self.screen.get_width() / 2 - image.get_width() / 2, 100 - image.get_height() - 25))

    def count_down(self):
        if self.time_run == -1:
            self.complement += 60
            self.time_limit += -1
        if self.time_limit == 0 and self.time_run == 0:
            self.time_limit = 0
            self.time_run = 0
            self.timesup = True
        else:
            self.time_run = self.waiting_time - pygame.time.get_ticks() // 1000 + self.complement

    def set_time(self):
        self.time_limit = 0
        pass

    def input(self):
        self.input_box = "Set the time limit {}{} : 00".format(self.dash, self.time_set_string)
        self.input_image = self.set_font.render(self.input_box, True, self.border_color)


#####################################################################################################################

class Skillbar:
    def __init__(self, screen, x, y, ball, m, n):
        self.screen = screen
        self.x = x
        self.y = y
        self.ball = ball
        self.color = (255, 255, 255)
        self.bonus = 0  # 50
        self.rect = pygame.Rect(self.x, self.y, 200, 20)
        # math logic
        self.m = m  # right: -1   #left:1
        self.n = n  # right:  1   #left: 0
        # Constructing the bar:
        self.starting_x = self.x + self.n * 200 - self.n
        self.starting_mana = self.starting_x + self.m * 200 - 1 + 2 * self.n
        # Mana amout:
        self.mana = self.starting_mana
        # Hit condition
        self.after_hit = True

    def draw(self):
        rect = pygame.Rect(self.x - 1, self.y - 1, 200 + 2, 20 + 2)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
        pygame.draw.line(self.screen, self.ball.original_color, (self.starting_x, self.y + rect.height / 2 - 2),
                         (self.mana
                          , self.y + rect.height / 2 - 2), 20)
        pygame.draw.line(self.screen, (255, 255, 255),
                         (self.starting_x + 120 * self.m, self.y - 1),
                         (self.starting_x + 120 * self.m, self.y - 1 + rect.height - 1))

    def gain(self):
        if self.mana * self.m < (self.starting_mana) * self.m - self.n:
            self.mana += self.m * 0.01
            if self.bonus == 50 and self.after_hit == True:
                if self.mana * self.m > (self.starting_mana) * self.m - self.n - self.bonus:
                    self.mana = self.starting_mana
                else:
                    self.mana += self.bonus * self.m
                self.bonus = 0


#####################################################################################################################

class Gem:
    def __init__(self, screen, timer):
        self.screen = screen
        self.x = -50
        self.y = -50
        self.timer = timer
        self.color = (181, 230, 29)
        self.min = 18
        self.total_time = self.timer.time_limit * 60
        self.timeget = pygame.time.get_ticks() // 1000
        self.number = random.randint(3, self.total_time // self.min)
        self.period = []
        for k in range(self.number):
            self.period += [self.min]
        for k in range(self.total_time - self.min * self.number):
            self.period[random.randint(0, len(self.period) - 1)] += 1
        self.k = 0

        self.get_hit = False

    def draw(self):
        if pygame.time.get_ticks() // 1000 - self.timeget <= self.period[self.k]:
            if pygame.time.get_ticks() // 1000 - self.timeget <= 5 and self.get_hit == False:
                pygame.draw.circle(self.screen, self.color, (self.x, self.y), 10)
                pygame.draw.circle(self.screen, (200, 200, 200), (self.x, self.y), 2)
            else:
                self.x = -50
                self.y = -50

        else:
            self.x = random.randint(32, self.screen.get_width() - 44)
            self.y = random.randint(150, self.screen.get_height() - 200)
            self.timeget = pygame.time.get_ticks() // 1000
            if self.k < len(self.period) - 1:
                self.k += 1
            self.get_hit = False


#####################################################################################################################

class Spike:
    def __init__(self, screen, x, y, horizontal, x_direction, y_direction):
        self.screen = screen
        self.x = x
        self.y = y
        self.x_o = x
        self.y_o = y
        self.size = 20
        self.velocity = 0.5
        self.spike_number = 5
        self.horizontal = horizontal
        self.x_direction = x_direction
        self.y_direction = y_direction
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.image = pygame.draw.circle(screen, (0, 0, 0), (-50, -50), 1)

    def draw(self):
        points = []
        t = -1
        if self.horizontal == True:
            for j in range(self.spike_number * 2 + 1):
                b = (self.x + self.size * j * self.x_direction,
                     self.y + (self.size / 2 + self.size / 2 * t) * self.y_direction)
                t = -t
                points += [b, ]
        else:
            self.spike_number = 4
            for j in range(self.spike_number * 2 + 1):
                b = (self.x + (self.size / 2 + self.size / 2 * t) * self.x_direction,
                     self.y + self.size * j * self.y_direction)
                t = -t
                points += [b, ]
        self.image = pygame.draw.polygon(self.screen, (100, 100, 100), points)

    def move(self):
        if self.horizontal == True:
            self.x += self.velocity * self.x_direction
            end = self.x + self.size * 2 * self.spike_number * self.x_direction
            start = self.x
            if self.x_direction * (end - self.screen.get_width() / 2) >= 0 or self.x_direction * (
                    start - self.x_o) <= -1:
                self.velocity = - self.velocity
        else:
            self.y += self.velocity * self.y_direction
            end = self.y + self.size * 2 * self.spike_number * self.y_direction
            start = self.y
            if self.y_direction * (end - self.screen.get_height() / 2) >= 0 or self.y_direction * (
                    start - self.y_o) <= -1:
                self.velocity = - self.velocity


#####################################################################################################################

class Dust:
    def __init__(self, screen, x, y, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.x_v = random.randint(-22, 22) * 0.01
        self.y_v = random.randint(-22, 22) * 0.01
        self.color = color
        self.radius = 3

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_v
        self.y += self.y_v
        self.radius += -0.02


#####################################################################################################################

class Wave:
    def __init__(self, screen):
        self.screen = screen
        self.radius = 0

    def draw(self, x, y, color):
        pygame.draw.circle(self.screen, color, (x, y), self.radius, 1)

    def expand(self):
        self.radius += 3

class Game:
    def __init__(self, screen: pygame.Surface,media):
        self.screen = screen
        self.border_x = 12
        self.border_y = 102
        # Assign the Role randomly
        a = [-1, 1]
        role1 = random.choice(a)
        a.remove(role1)
        role2 = random.choice(a)
        ##################
        self.ball = Ball(self.screen,700,560,20,(244,119,125),role1)
        self.ball2 = Ball(self.screen,300,240,20,(88,196,222),role2)
        self.tag = 1
        self.m = 1

        #Testing variables
        self.testing_value = 1
        self.test =''
        self.n = 0

        # Timer:
        self.timer = Timer(screen)
        #game start-replay-end:
        self.game_start = False
        self.game_replay = False
        self.game_end = False
        self.media = media
        self.lobby_image = self.media.lobby
        #Button:
        self.howtoplay_box = False
        self.start_box = False
        self.settime_box = False

        # Result
        self.winner_color = (0, 0, 0)
        self.winner = ''
        self.winner_font = pygame.font.Font("FreeSansBold-Xgdd.ttf",50)
        self.winner_state = self.winner_font.render(self.winner,True, self.winner_color)
        self.winner_image= self.media.blue_win
        self.loser_abuse = ''
        self.loser_font = pygame.font.Font("FreeSansBold-Xgdd.ttf",30)
        self.loser_state = self.loser_font.render(self.loser_abuse,True,(0,0,0))

        # Skil bar:
        self.skillbar= Skillbar(self.screen,775,50,self.ball,-1,1)
        self.skillbar2 = Skillbar(self.screen, 20, 50, self.ball2,1,0)
        # Gem:
        self.gem = Gem(self.screen,self.timer)
        # Trap (anticipated)
        x_left = self.border_x-1
        x_right = self.screen.get_width() - self.border_x
        y_top = self.border_y-1
        y_bottom = self.screen.get_height() - 53

        spike1 = Spike(self.screen,x_left ,y_top , True, 1,1)
        spike2 = Spike(self.screen,x_right , y_top, True, -1,1)
        spike3 = Spike(self.screen, x_left, y_bottom, True, 1,-1)
        spike4 = Spike(self.screen, x_right,y_bottom , True, -1,-1)
        spike5 = Spike(self.screen,x_left,y_top, False, 1,1)
        spike6 = Spike(self.screen, x_left, y_bottom, False, 1,-1)
        spike7 = Spike(self.screen, x_right , y_top, False, -1,1)
        spike8 = Spike(self.screen, x_right,y_bottom, False, -1,-1)

        self.spikes=[spike1,spike2,spike3,spike4,spike5,spike6,spike7,spike8]
        self.entraped = False
        self.entraped2=False




    def draw_game(self):
        self.ball.draw()
        self.ball2.draw()
        self.gem.draw()
        for spike in self.spikes:
            spike.draw()

        pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(0,0,self.screen.get_width(),98))

        border2 = pygame.Rect(0, 90, self.screen.get_width(), self.screen.get_height() - 50 - 100 + 20)
        pygame.draw.rect(self.screen, (0, 0, 0), border2, 30)
        border = pygame.Rect(self.border_x, self.border_y, self.screen.get_width() - 24,
                             self.screen.get_height() - 54 - 100)
        pygame.draw.rect(self.screen, (100, 100, 100), border, 7)


        self.timer.draw()
        self.skillbar.draw()
        self.skillbar2.draw()


    def run_one_cycle(self):
        # Make balls return:
        self.ball.turnback(self.border_x,self.border_y)
        self.ball2.turnback(self.border_x,self.border_y)

        # Skill Bar:
        self.skillbar.gain()
        self.skillbar2.gain()
        # Ball Skill cool down:
        self.ball.cool_down()
        self.ball2.cool_down()

        # Wave:
        self.ball.push(self.ball2)
        self.ball2.push(self.ball)


        # Tagging:
        chaser = ''
        if self.ball.make_hitbox().colliderect(self.ball2.make_hitbox()):
            self.m = -1
            self.ball.color = (255,255,255)
            # self.ball.boost_color = self.ball.color
            self.ball2.color= (255,255,255)
            # self.ball2.boost_color=self.ball2.color
        else:
            self.tag = self.tag * self.m
            self.m = 1
            self.ball.color = self.ball.dust_color
            # self.ball.boost_color=self.ball.dust_color
            self.ball2.color = self.ball2.dust_color
            # self.ball2.boost_color = self.ball2.dust_color
        if self.tag == self.ball.role:
            chaser = "Ball Pink"
            self.ball.sign = 1
            self.ball2.sign=-1
            self.ball.become_chaser = True
            self.ball2.become_chaser = False
        if self.tag == self.ball2.role:
            chaser = "Ball Blue"
            self.ball.sign = -1
            self.ball2.sign= 1
            self.ball2.become_chaser = True
            self.ball.become_chaser = False

        if self.testing_value == -self.tag:
            self.testing_value=self.tag
            self.media.tag_sound.play()


        # Timer run:
        self.timer.count_down()

        # Hit the Gem
        if self.ball.make_hitbox().collidepoint(self.gem.x,self.gem.y) or self.ball2.make_hitbox().collidepoint(self.gem.x,self.gem.y):
            self.gem.get_hit = True
            self.media.gem_sound.play()
            #Try:
            if self.ball.make_hitbox().collidepoint(self.gem.x,self.gem.y):
                self.skillbar.bonus =50
            if self.ball2.make_hitbox().collidepoint(self.gem.x,self.gem.y):
                self.skillbar2.bonus = 50
            self.skillbar.after_hit = False
            self.skillbar2.after_hit = False
        else:
            self.skillbar.after_hit = True
            self.skillbar2.after_hit = True

            #Sound effect (swallow)


        # Hit the pikes:
        for spike in self.spikes:
            reflect = 20
            spike.move()
            if spike.image.colliderect(self.ball.make_hitbox()):
                self.ball.stunt_time = pygame.time.get_ticks()
                self.ball.dust_color = (100,100,100)
                if spike.horizontal == True:
                    self.ball.y += spike.y_direction* reflect
                else:
                    self.ball.x += spike.x_direction* reflect
                self.ball.stunt = True
            else:
                if pygame.time.get_ticks()-self.ball.stunt_time >1500:
                    self.ball.stunt = False
            if spike.image.colliderect(self.ball2.make_hitbox()):
                self.ball2.stunt_time = pygame.time.get_ticks()
                self.ball2.dust_color = (100, 100, 100)
                if spike.horizontal == True:
                    self.ball2.y += spike.y_direction * reflect
                else:
                    self.ball2.x += spike.x_direction * reflect
                self.ball2.stunt = True
            else:
                if pygame.time.get_ticks()-self.ball2.stunt_time >1500:
                    self.ball2.stunt = False

            if self.ball.stunt==True:
                if self.entraped==False:
                    self.entraped=True
                    self.media.hit_trap_sound.play()
            else:
                self.entraped = False

            if self.ball2.stunt == True:
                if self.entraped2 == False:
                    self.entraped2 = True
                    self.media.hit_trap_sound2.play()
            else:
                self.entraped2 = False


        # Result:
        if self.timer.timesup == True:
            if chaser == "Ball Blue":
                self.winner = "PINK WIN"
                self.loser_abuse = "Blue sucker..."
                self.winner_image = self.media.pink_win
                self.winner_color = (255,0,0)
                self.game_end = True

            if chaser == "Ball Pink":
                self.winner = "BLUE WIN"
                self.loser_abuse = "Pink sucker..."
                self.winner_image = self.media.blue_win
                self.winner_color = (0,0,255)
                self.game_end = True
            self.winner_state = self.winner_font.render(self.winner, True, self.winner_color)
            self.loser_state = self.loser_font.render(self.loser_abuse,True,(0,0,0))
            pygame.mixer.music.load("zigzag.wav")
            pygame.mixer.music.play()


        self.test = "ROLE BOARD: Chaser: {} ".format(chaser)
        pygame.display.set_caption(self.test)



    def lobby(self):

        self.screen.blit(self.lobby_image, (0, 0))
        # if self.box_clicked == True:
        #     self.media.click_sound.play()
        if self.howtoplay_box == True:
            self.screen.blit(self.media.guidline, (self.screen.get_width() / 2 - self.media.guidline.get_width() / 2, 30))
        if self.timer.input_appear == True:
            self.timer.input()
            x = 630
            y = 630
            rect = pygame.Rect(x - 8, y - 8, self.timer.input_image.get_width() + 16,
                               self.timer.input_image.get_height() + 16)
            pygame.draw.rect(self.screen, self.timer.border_color, rect, 2)
            self.screen.blit(self.timer.input_image, (x, y))
            self.gem = Gem(self.screen, self.timer)
        pygame.display.set_caption("TickyTag")
        pygame.display.update()
        self.timer.waiting_time = pygame.time.get_ticks() // 1000



    def end(self):
        center_x = self.screen.get_width() / 2
        center_y = self.screen.get_height() / 2

        self.screen.blit(self.winner_image, (0, 0))
        self.screen.blit(self.winner_state, (center_x - self.winner_state.get_width() / 2 - 10,
                                        center_y - self.winner_state.get_height() / 2 + 110))
        self.screen.blit(self.loser_state, (center_x - self.winner_state.get_width() / 2 - 10,
                                       center_y - self.winner_state.get_height() / 2 + 110 + 55))
        instruction = "(Press P to replay)"
        instruction_image = pygame.font.Font("FreeSansBold-Xgdd.ttf",30).render(instruction,True,(100,100,100))
        self.screen.blit(instruction_image,(center_x - instruction_image.get_width()/2,
                                       center_y - self.winner_state.get_height() / 2 + 110 + 55+80))
        pygame.display.update()

class Controller:
    def __init__(self, game: Game):
        self.game = game
        self.change = True


    def start_button(self,pos):
        if pos[0]>=414 and pos[0]<=570 and pos[1]>=507 and pos[1]<=569:
            # self.game.start_box = True
            self.game.lobby_image = self.game.media.start
            if self.game.start_box == False:
                self.game.start_box = True
                self.game.media.click_sound.play()
            return pos[0]>=414 and pos[0]<=570 and pos[1]>=507 and pos[1]<=569
        else:
            self.game.lobby_image = self.game.media.lobby
            self.game.start_box =False


    def settime_button(self,pos):
        if pos[0]>=382 and pos[0]<=553 and pos[1]>=629 and pos[1]<=653:
            self.game.lobby_image = self.game.media.set_time
            if self.game.settime_box == False:
                self.game.settime_box = True
                self.game.media.click_sound.play()
            return pos[0]>=382 and pos[0]<=553 and pos[1]>=629 and pos[1]<=653
        else:
            self.game.settime_box = False

    def howtoplay_button(self,pos):
        if pos[0]>=382 and pos[0]<=621 and pos[1]>=707 and pos[1]<=734:
            self.game.lobby_image = self.game.media.howto
            if self.game.howtoplay_box == False:
                self.game.howtoplay_box = True
                self.game.media.click_sound.play()
        else:
            self.game.howtoplay_box = False


    def get_and_handle_events(self):
        """
        [Describe what keys and/or mouse actions cause the game to ...]
        """

        ball = self.game.ball
        ball2 = self.game.ball2
        if self.game.game_start == False:
            # if
            self.start_button(pygame.mouse.get_pos())
            self.settime_button(pygame.mouse.get_pos())
            self.howtoplay_button(pygame.mouse.get_pos())

        events = pygame.event.get()
        pressed_keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            # Click start
            if (event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE])or (event.type == pygame.MOUSEBUTTONDOWN and self.start_button(pygame.mouse.get_pos())):
                self.game.game_start = True
                self.game.media.click_sound.play()
                pygame.mixer.music.load("rocket.wav")
                pygame.mixer.music.play()
            # Click_timer:
            if event.type == pygame.MOUSEBUTTONDOWN and self.settime_button(pygame.mouse.get_pos()):
                self.game.timer.input_appear = True
                self.change =True
            # Get input:
            if self.game.timer.input_appear == True and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.change == True:
                        self.game.timer.border_color = (121,230,154)
                        self.change = not self.change
                        self.game.timer.dash = ''
                    else:
                        self.game.timer.input_appear = False
                        self.game.timer.border_color = (255,255,255)
                        self.game.timer.dash = '_'
                elif event.key == pygame.K_BACKSPACE:
                    self.game.timer.time_set_string = self.game.timer.time_set_string[:-1]
                else:
                    self.game.timer.time_set_string+= event.unicode
                    if self.game.timer.time_set_string.isnumeric():
                        self.game.timer.time_limit = int(self.game.timer.time_set_string)

            # Replay the game:
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_p]:
                self.game.game_end = False
                self.game.game_replay = True

            # Skill:
            if self.game.game_start == True:
                if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_l]:
                    if self.game.skillbar.mana < self.game.skillbar.starting_x - 120:
                        ball.dust_color = (237,28,36)
                        self.game.skillbar.mana += 120
                        ball.speed = 2
                        ball.skill_time = pygame.time.get_ticks()//1000
                        self.game.media.boost_sound.play()
                if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_g]:
                    if self.game.skillbar2.mana > self.game.skillbar2.starting_x + 120+1:
                        ball2.dust_color = (0,110,245)
                        self.game.skillbar2.mana += -120
                        ball2.speed = 2
                        ball2.skill_time = pygame.time.get_ticks() // 1000
                        self.game.media.boost_sound.play()

                if event.type==pygame.KEYDOWN and pressed_keys[pygame.K_k]:
                    if self.game.skillbar.mana <= self.game.skillbar.starting_mana+1:
                        self.game.skillbar.mana = self.game.skillbar.starting_x
                        ball.wave_activate = True
                        ball.wave_time = pygame.time.get_ticks()
                        self.game.media.wave_sound.play()
                if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_f]:
                    if self.game.skillbar2.mana >= self.game.skillbar2.starting_mana-1:
                        self.game.skillbar2.mana = self.game.skillbar2.starting_x+1
                        ball2.wave_activate = True
                        ball2.wave_time = pygame.time.get_ticks()
                        self.game.media.wave_sound.play()

        if self.game.game_start == True :
            if ball.stunt == False:
                # Player 1:
                if pressed_keys[pygame.K_UP]:
                    ball.dust_activate = True
                    ball.y = ball.y -ball.velocity- ball.speed
                else:
                    ball.dust_activate = False
                if pressed_keys[pygame.K_DOWN]:
                    ball.dust_activate = True
                    ball.y = ball.y +ball.velocity + ball.speed
                if pressed_keys[pygame.K_LEFT]:
                    ball.dust_activate = True
                    ball.x = ball.x -ball.velocity - ball.speed
                if pressed_keys[pygame.K_RIGHT]:
                    ball.dust_activate = True
                    ball.x = ball.x +ball.velocity + ball.speed
            if ball2.stunt == False:
                # Player 2:
                if pressed_keys[pygame.K_w]:
                    ball2.dust_activate = True
                    ball2.y = ball2.y - ball2.velocity - ball2.speed
                else:
                    ball2.dust_activate = False
                if pressed_keys[pygame.K_s]:
                    ball2.dust_activate = True
                    ball2.y = ball2.y + ball2.velocity + ball2.speed
                if pressed_keys[pygame.K_a]:
                    ball2.dust_activate = True
                    ball2.x = ball2.x - ball2.velocity - ball2.speed
                if pressed_keys[pygame.K_d]:
                    ball2.dust_activate = True
                    ball2.x = ball2.x + ball2.velocity + ball2.speed


    @staticmethod
    def exit_if_time_to_quit(events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

    @staticmethod
    def key_was_pressed_on_this_cycle(key, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False

class View:
    def __init__(self, screen: pygame.Surface, game: Game):
        self.screen = screen
        self.game = game
        self.background_color = pygame.Color("black")  # DONE: Choose your own color

    def draw_everything(self):
        self.screen.fill(self.background_color)
        self.game.draw_game()  # DONE: Implement draw_game in your Game
        pygame.display.update()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()
    media = Media()
    game = Game(screen,media)
    viewer = View(screen, game)
    controller = Controller(game)
    frame_rate = 120
    # Music:
    pygame.mixer.music.load("opening.wav")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.2)

    while True:
        clock.tick(frame_rate)
        controller.get_and_handle_events()

        #Lobby window:
        if game.game_start == False:
            game.lobby()
            continue

        #Game End:
        if game.game_end == True:
            game.end()
            continue

        #Game Run:
        # pygame.mixer.music.stop()
        game.run_one_cycle()
        viewer.draw_everything()

        #Game Reset:
        if game.game_replay == True:
            game = Game(screen,media)
            viewer = View(screen, game)
            controller = Controller(game)
            pygame.mixer.music.stop()


main()






