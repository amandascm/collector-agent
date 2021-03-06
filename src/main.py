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
    
    def show_caption(self, color, font, size, text, minimum_y):
        caption_font = pygame.font.SysFont(font, size)
        caption_surface = caption_font.render(text, True, color)
        caption_rect = caption_surface.get_rect()
        caption_rect.y = minimum_y
        self.environment_window.blit(caption_surface, caption_rect)
    
    def show_captions(self, captions):
        minimum_y = 0
        for c in captions:
            self.show_caption(c["color"], c["font"], c["size"], c["text"], minimum_y)
            minimum_y += c["size"]
    
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
            
            # displaying captions countinuously
            captions = [
                {"color":color.WHITE, "font":"times new roman", "size":15, "text": 'Score: ' + str(self.agent.score)},
                {"color":self.agent.color, "font":"times new roman", "size":15, "text": 'Agent position: ' + str(self.agent.position)},
                {"color":color.RED, "font":"times new roman", "size":15, "text": 'Food position: ' + str(self.food_position)}
            ]
            self.show_captions(captions)
            
            # Refresh game screen
            pygame.display.update()
        
            # Frame Per Second /Refresh Rate
            self.fps.tick(self.agent.speed)

def main():
    World()

if __name__ == '__main__':
    main()
