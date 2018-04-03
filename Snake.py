# Import a library of functions called 'pygame'
import pygame
from math import pi
from enum import Enum
import random
import sys
import copy


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Result(Enum):
    EAT = 1
    NORMAL = 2
    CRUSH = 3


class Point(object):
    def __init__(self, px=0, py=0):
        self.x = px
        self.y = py


class PyDraw(object):
    def __init__(self):
        # Initialize the game engine
        pygame.init()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.size = [400, 330]
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.speed = 10

    def draw(self, pysnake):
        self.clock.tick(self.speed)
        self.screen.fill(self.WHITE)
        snake = pysnake.getsnake()
        length = pysnake.getlength()
        food = pysnake.getfood()
        for i in range(length):
            pygame.draw.rect(self.screen, self.BLACK, [(snake[i].x - 1) * 10, (snake[i].y - 1) * 10 + 30,
                                                       10, 10], 2)
        pygame.draw.rect(self.screen, self.GREEN, [(food.x - 1) * 10, (food.y - 1) * 10 + 30,
                                                   10, 10])
        pygame.draw.line(self.screen, self.RED, (0, 30), (400, 30), 2)
        font = pygame.font.Font('simsun.ttc', 16)
        text = font.render("总得分：%4d" % (length-5), True, self.BLUE)
        textbox = text.get_rect()
        textbox.center = (340, 15)
        self.screen.blit(text, textbox)
        pygame.display.flip()

    def draw_restart(self):
        self.clock.tick(self.speed)
        self.screen.fill(self.WHITE)
        font = pygame.font.Font('simsun.ttc', 16)
        text = font.render("游戏结束！按[R]键重新开始!", True, self.BLUE)
        textbox = text.get_rect()
        textbox.center = (200, 150)
        self.screen.blit(text, textbox)
        pygame.display.flip()

    def speed_modify(self, ud):
        if ud and self.speed < 200:
            self.speed = self.speed + 5
        elif (not ud) and self.speed > 10:
            self.speed = self.speed - 5


class PySnake(object):
    def __init__(self):
        self.__length = 5
        self.__snake = []
        self.__dir = Direction.RIGHT
        self.__food = Point(20, 10)
        self.__crushed = False
        self.__width = 40
        self.__height = 30
        for i in range(1000):
            self.__snake.append(Point())
        self.reset()

    def getsnake(self):
        return self.__snake

    def getlength(self):
        return self.__length

    def getdir(self):
        return self.__dir

    def setdir(self, dir):
        self.__dir = dir

    def getcrushed(self):
        return self.__crushed

    def getfood(self):
        return self.__food

    def reset(self):
        self.__length = 5
        self.__dir = Direction.RIGHT
        self.__food = Point(20, 10)
        self.__crushed = False
        for i in range(5):
            self.__snake[i].x = 10 - i
            self.__snake[i].y = 10

    def if_eat(self):
        if self.__dir == Direction.UP:
            for i in range(1, self.__length):
                if self.__snake[0].y - 1 == self.__snake[i].y and self.__snake[0].x == self.__snake[i].x:
                    return Result.CRUSH
            if self.__snake[0].y - 1 == self.__food.y and self.__snake[0].x == self.__food.x:
                return Result.EAT
            else:
                return Result.NORMAL
        elif self.__dir == Direction.DOWN:
            for i in range(1, self.__length):
                if self.__snake[0].y + 1 == self.__snake[i].y and self.__snake[0].x == self.__snake[i].x:
                    return Result.CRUSH
            if self.__snake[0].y + 1 == self.__food.y and self.__snake[0].x == self.__food.x:
                return Result.EAT
            else:
                return Result.NORMAL
        elif self.__dir == Direction.RIGHT:
            for i in range(1, self.__length):
                if self.__snake[0].y == self.__snake[i].y and self.__snake[0].x + 1 == self.__snake[i].x:
                    return Result.CRUSH
            if self.__snake[0].y == self.__food.y and self.__snake[0].x + 1 == self.__food.x:
                return Result.EAT
            else:
                return Result.NORMAL
        elif self.__dir == Direction.LEFT:
            for i in range(1, self.__length):
                if self.__snake[0].y == self.__snake[i].y and self.__snake[0].x - 1 == self.__snake[i].x:
                    return Result.CRUSH
            if self.__snake[0].y == self.__food.y and self.__snake[0].x - 1 == self.__food.x:
                return Result.EAT
            else:
                return Result.NORMAL
        else:
            return Result.NORMAL

    def creat_food(self):
        while True:
            succ = True
            self.__food.x = random.randint(1, self.__width)
            self.__food.y = random.randint(1, self.__height)
            for i in range(self.__length):
                if self.__food.x == self.__snake[i].x and self.__food.y == self.__snake[i].y:
                    succ = False
                    break
            if succ:
                break

    def update(self):
        R = self.if_eat()
        if R == Result.CRUSH:
            self.__crushed = True
        elif R == Result.EAT:
            self.__length = self.__length + 1
            self.__snake[1:self.__length] = copy.deepcopy(self.__snake[0: self.__length - 1])
            self.__snake[0] = copy.deepcopy(self.__food)
            self.creat_food()
        elif R == Result.NORMAL:
            self.__snake[1:self.__length] = copy.deepcopy(self.__snake[0: self.__length - 1])
            if self.__dir == Direction.UP:
                self.__snake[0].y = self.__snake[0].y - 1
            elif self.__dir == Direction.DOWN:
                self.__snake[0].y = self.__snake[0].y + 1
            elif self.__dir == Direction.LEFT:
                self.__snake[0].x = self.__snake[0].x - 1
            elif self.__dir == Direction.RIGHT:
                self.__snake[0].x = self.__snake[0].x + 1
            if self.__snake[0].y > self.__height:
                self.__snake[0].y = 1
            if self.__snake[0].x > self.__width:
                self.__snake[0].x = 1
            if self.__snake[0].y <= 0:
                self.__snake[0].y = self.__height
            if self.__snake[0].x <= 0:
                self.__snake[0].x = self.__width


def main():
    py_snake = PySnake()
    py_draw = PyDraw()
    while True:
        if not py_snake.getcrushed():
            e = pygame.event.get()
            print(len(e))
            for event in e:
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:  # 键被按下
                    if event.key == pygame.K_w:
                        if py_snake.getdir() != Direction.DOWN:
                            py_snake.setdir(Direction.UP)
                            break
                    elif event.key == pygame.K_s:
                        if py_snake.getdir() != Direction.UP:
                            py_snake.setdir(Direction.DOWN)
                            break
                    elif event.key == pygame.K_d:
                        if py_snake.getdir() != Direction.LEFT:
                            py_snake.setdir(Direction.RIGHT)
                            break
                    elif event.key == pygame.K_a:
                        if py_snake.getdir() != Direction.RIGHT:
                            py_snake.setdir(Direction.LEFT)
                            break
                    elif event.key == pygame.K_n:
                        py_draw.speed_modify(False)
                        break
                    elif event.key == pygame.K_m:
                        py_draw.speed_modify(True)
                        break
            py_snake.update()
            py_draw.draw(py_snake)
        else:
            while True:
                pressed = False
                py_draw.draw_restart()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:  # 键被按下
                        if event.key == pygame.K_r:
                            pressed = True
                            break
                if pressed:
                    py_snake.reset()
                    break


if __name__ == '__main__':
    main()
