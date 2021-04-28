"""
I tryed to recreat the iconic game flappy bird from scratch nd implent an AI to play it by his own using only python 
Date Modified:  27/04/2021
Author: Oussama Trabelsi 
Estimated Work Time: 25 hours (20 just for that damn AI)
"""
import pygame
import random
import os
import time
import neat
import pickle
pygame.font.init()  # init le font

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

gen = 0

class Bird:
    """
    Bird class representing El 3asfour
    """
    MAX_ROTATION = 25
    IMGS = bird_images
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        Initialize the 3asfour 
        :return: None
        """
        self.x = x
        self.y = y
        self.tilt = 0  # Tiltation
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """
        make the 3asfour ynagez
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        make the 3asfou yetharak
        :return: None
        """
        self.tick_count += 1

        #  Down acceleration
        d = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  #displacement
        # -10.5+1.5*1 = natl3ou  9 pixels up (-9) 
        if d >= 16:
            d =16  #speed of falling down try to finnnndddddddd !!!! .  

        if d < 0:
            d -= 1 # jump try to finnd zedaa !   

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:  # tilt up
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
         el window ta2 elo3ba =win
        animation el 3asfour
        :return: None
        loop for the images 
        """
        self.img_count += 1


        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        #if the 3asfour falling don't animate (Can't be bothered after thought )**************
        
        """if self.tilt<=90:
            self.img"""
        # tilt el 3asfour
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt) #copied from stackover flow i don't know how it works 

    def get_mask(self):
        """
        :return: None
        """
        return pygame.mask.from_surface(self.img)


class Pipe():
    """
    represents el ja3ba
    """
    GAP = 200
    VEL = 5

    def __init__(self, x):
        """
        :return" None
        """
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True) # besh ne9lbou taswyret el pipe cuz the top pipe is the same boottom flipped
        self.PIPE_BOTTOM = pipe_img

        self.passed = False 

        self.set_height()

    def set_height(self):
        """
       kobr el ja3ba the upper one
        :return: None
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height() #calculate the top pipe  
        self.bottom = self.height + self.GAP

    def move(self):
        """
        :return: None
        """
        self.x -= self.VEL

    def draw(self, win):
        """
        :return: None
        """
        # ja3ba up 
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # ja3ba down
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird, win):
        """
        if lost (intersection el pipe o el 3asfour) we can use pixels like boxes mais using mask is more 
        more efficant nd dosn't look like a bug   
        :return: Bool
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True #if intersection  

        return False

class Base:
    """
    moving floor
    """
    VEL = 5
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        """        
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        moving the floooor
        :return: None
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH #THiisss isss creatiiiiive 

    def draw(self, win):
        """
        2 florrs moving togther to draw the illution of moving  
        :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blitRotateCenter(surf, image, topleft, angle):
    """
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    """
    draws the windows for the main game loop 
    blit is draw on the window ta3 el game 
    :return: None
    """
    if gen == 0:
        gen = 1
    win.blit(bg_img, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        #lines from bird to j3ab 
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # draw 3asfour
        bird.draw(win)

    # score 
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations lel 3safar so it's faster 
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # 9adesh men 3asfour still breathing
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def eval_genomes(genomes, config): #paramater dyyma stable
    """
    runs the simulation of the current population 
    birds and sets their fitness from score 
    """
    global WIN, gen
    win = WIN
    gen += 1

   #keep tach the neuron network contrning the birds 
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1                                                                 # pipe on the screen for neural network input

        for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # check for accidant
            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird)) #pop remove ya3ny  

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)



def run(config_file):
    """
        :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file) #same configiration file aly ktebneh khdyna menou those parametre 

    p = neat.Population(config) #generat the population men el config file 

    p.add_reporter(neat.StdOutReporter(True)) #give us some stats fitnes nd bla bla bla
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run 50 3asfour.
    winner = p.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner)) #show us the stats 


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__) #give us the path to our local directory 
    config_path = os.path.join(local_dir, 'config-feedforward.txt') #giv the exact absulute file nd join it 
    run(config_path) #run the configuration file aly ktebneh