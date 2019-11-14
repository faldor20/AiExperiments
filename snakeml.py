from enum import Enum
import pygame
from random import randint


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Snake:
    def __init__(self, direction: Direction, bounds: (int, int)):
        self.direction = direction
        self.segmentsPos = [(bounds[0]/2, bounds[1]/2)]

    direction: Direction
    segmentsPos: [(int, int)]


class World:
    def __init__(self, snake: Snake, foodPos: (int, int), tickLength: int):
        self.snake = snake
        self.foodPos = foodPos
        self.tickLength = tickLength
# TODO: Make a endstate


""" def endGame(snake: Snake):
    win.addstr('score='+len(snake.segmentsPos), 10) """


def move(snake: Snake, direction: (int, int)) -> Snake:
    if(len(snake.segmentsPos) > 1):
        for i in reversed(range(len(snake.segmentsPos))):
            if (i == 0):
                break
            snake.segmentsPos[i] = snake.segmentsPos[i-1]

    oldPos = snake.segmentsPos[0]
    snake.segmentsPos[0] = (direction[0]+oldPos[0], direction[1]+oldPos[1])

    return snake


def UpdateWorld(world: World, bounds: (int, int)) -> World:
    world.snake = move(world.snake, world.snake.direction.value)

    if(outOfBounds(bounds, world.snake.segmentsPos[0])):
        """  endGame(snake) """
        print("game ended")
        pygame.done = True

    world = CheckIfSnakeIsOnFood(world)

    if(world.foodPos == (-10, -10)):
        world.foodPos = MakeNewFood(world.snake)

    return world


def CheckIfSnakeIsOnFood(world: World) -> World:
    if(world.snake.segmentsPos[0] == world.foodPos):
        world.snake.segmentsPos.extend(MakeSegments(
            foodValue, world.snake.segmentsPos[-1]))
        world.foodPos = (-10, -10)
        world.tickLength = round(world.tickLength-world.tickLength/5)
        print("ate food")
    return world


def MakeNewFood(snake: Snake) -> (int, int):
    newPos = (randint(0, bounds[0]-1), randint(0, bounds[1]-1))
    for segment in snake.segmentsPos:
        if(segment == newPos):
            return MakeNewFood(snake)

    return newPos


def MakeSegments(number: int, lastSegment: (int, int)) -> [(int, int)]:
    segments: [(int, int)] = []
    for i in range(number):
        segments.append(lastSegment)
    return segments


def outOfBounds(bounds: (int, int), segement: (int, int)) -> bool:
    if(segement[0] > bounds[0] or segement[0] < 0 or segement[1] > bounds[1] or segement[1] < 0):
        return True
    else:
        return False


def HandleInput(snake: Snake, events):
    #  key = win.getch()

    for event in events:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.direction = Direction.LEFT
            if event.key == pygame.K_RIGHT:
                snake.direction = Direction.RIGHT
            if event.key == pygame.K_DOWN:
                snake.direction = Direction.DOWN
            if event.key == pygame.K_UP:
                snake.direction = Direction.UP

# TODO: Draw the graphics


def DrawGraphics(world: World, bounds: (int, int), screen):
    for segment in world.snake.segmentsPos:
        # Add this somewhere after the event pumping and before the display.flip()
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(
            segment[0]*scale, segment[1]*scale, 0.9*scale, 0.9*scale))

    pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(
        world.foodPos[0]*scale, world.foodPos[1]*scale, 0.9*scale, 0.9*scale))


startDirection = Direction.LEFT

bounds: (int, int) = (20, 20)
startingLength = 4
foodValue = 3
startsnake = Snake(startDirection, bounds)
foodPos = MakeNewFood(startsnake)

pygame.init()
scale = 32
screen = pygame.display.set_mode((20*scale, 20*scale))
done = False

currentSnake: Snake = Snake(Direction.LEFT, bounds)
world = World(currentSnake, foodPos, 300)
while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))
    HandleInput(world.snake, events)
    UpdateWorld(world, bounds,)
    DrawGraphics(world, bounds, screen)

    pygame.display.update()

    pygame.time.delay(world.tickLength)
