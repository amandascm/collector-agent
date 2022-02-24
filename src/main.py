from enum import Enum
from xmlrpc.client import Boolean
import pygame
import random
import numpy as np
# Vector2
vec = pygame.math.Vector2
 
# colors
class Color:
    def __init__(self) -> None:     
        self.BLACK = pygame.Color(0, 0, 0)
        self.WHITE = pygame.Color(255, 255, 255)
        self.RED = pygame.Color(255, 0, 0)
        self.GREEN = pygame.Color(0, 255, 0)
        self.BLUE = pygame.Color(0, 0, 255)
color = Color()

class Agent:
    def __init__(self, speed=18, color=color.GREEN, default_position=vec(0,0)) -> None:
        self.speed = speed
        self.color = color
        self.default_position = default_position
        self.position:vec = self.default_position
        self.score = 0

    def next_action(self, goal_position:vec):
        diff_vec = goal_position - self.position
        dist = self.position.distance_to(goal_position)
        if dist <= 14.15:
            self.score += 1
            return None
        else:
            factor = dist/self.speed
            self.position += diff_vec/factor
        return True

class World:
    def __init__(self) -> None:
        self.window = {"width": 720, "height": 480, "color": color.BLACK}
        self.agent = Agent()

        pygame.init()
        self.initialise_env_window()
        self.new_food()
        self.loop()

    # initialise environment window
    def initialise_env_window(self):
        pygame.display.set_caption('Collector Agent')
        self.environment_window = pygame.display.set_mode((self.window["width"], self.window["height"]))

        # FPS controller
        self.fps = pygame.time.Clock()

    def new_food(self):
        self.food_position = vec(random.randrange(1, (self.window["width"])),
                        random.randrange(1, (self.window["height"])))

    def show_score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score: ' + str(self.agent.score), True, color)
        score_rect = score_surface.get_rect()
        self.environment_window.blit(score_surface, score_rect)
    
    def loop(self):
        while True:        
            # handling key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # quit all
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # moving agent
            action = self.agent.next_action(self.food_position)
            if action == None:
                self.new_food()
            
            # draw background
            self.environment_window.fill(self.window["color"])
            
            # draw agent
            pygame.draw.rect(self.environment_window, self.agent.color, pygame.Rect(
                self.agent.position[0], self.agent.position[1], 10, 10))
            
            # draw food
            pygame.draw.rect(self.environment_window, color.RED, pygame.Rect(
                self.food_position[0], self.food_position[1], 10, 10))
            
            # displaying score countinuously
            self.show_score(color.WHITE, 'times new roman', 20)
            
            # Refresh game screen
            pygame.display.update()
        
            # Frame Per Second /Refresh Rate
            self.fps.tick(self.agent.speed)

def main():
    World()

if __name__ == '__main__':
    main()
