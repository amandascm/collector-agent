from enum import Enum
from xmlrpc.client import Boolean
import pygame
import random
 
# colors
class Color:
    def __init__(self) -> None:     
        self.BLACK = pygame.Color(0, 0, 0)
        self.WHITE = pygame.Color(255, 255, 255)
        self.RED = pygame.Color(255, 0, 0)
        self.GREEN = pygame.Color(0, 255, 0)
        self.BLUE = pygame.Color(0, 0, 255)
color = Color()

# directions
class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

class Agent:
    def __init__(self, speed=20, color=color.GREEN, default_position=[0,0]) -> None:
        self.speed = speed
        self.color = color
        self.default_position = default_position
        self.position = self.default_position
        self.direction:Direction = Direction.RIGHT
        self.score = 0

    def next_action(self, goal_position):
        x_diff = self.position[0] - goal_position[0]
        y_diff = self.position[1] - goal_position[1]

        if x_diff != 0:
            if x_diff > 0:
                self.direction = Direction.LEFT
            else:
                self.direction = Direction.RIGHT
        elif y_diff != 0:
            if y_diff > 0:
                self.direction = Direction.UP
            else:
                self.direction = Direction.DOWN
        else:
            self.score += 1
            return None

        return self.direction

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
        self.food_position = [random.randrange(1, (self.window["width"]//10)) * 10,
                        random.randrange(1, (self.window["height"]//10)) * 10]

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

            direction = self.agent.next_action(self.food_position)
            # moving agent
            if direction == Direction.UP:
                self.agent.position[1] -= 10
            if direction == Direction.DOWN:
                self.agent.position[1] += 10
            if direction == Direction.LEFT:
                self.agent.position[0] -= 10
            if direction == Direction.RIGHT:
                self.agent.position[0] += 10
            if direction == None:
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
