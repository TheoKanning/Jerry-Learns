import pygame
import pymunk
import sys
from pygame.locals import *
from pygame.color import *
from math import pi
from math import sin

LEG_COLLISION_TYPE = 1
motor = None


def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y + 600)


def add_ground(space):
    """
    Adds a ground line to the specified space object
    :param space: pymunk space
    :return: line segment
    """

    line_body = pymunk.Body()
    line_body.position = (300, 100)
    segment = pymunk.Segment(line_body, (-300, 0), (300, 0), 10)
    space.add(segment)
    return segment


def add_test_bodies(space):
    """
    Creates a test body consisting of two circles connected by a pivot joint
    :param space:
    :return:
    """
    mass = 1
    width = 5
    inertia = pymunk.moment_for_segment(mass, (0, 50), (0, -50))

    # top_circle_body = pymunk.Body(mass, inertia)
    top_circle_body = pymunk.Body()
    top_circle_body.position = 299, 275
    top_circle_shape = pymunk.Segment(top_circle_body, (0, 50), (0, -50), width)
    top_circle_shape.collision_type = LEG_COLLISION_TYPE

    bottom_circle_body = pymunk.Body(mass, inertia)
    bottom_circle_body.position = 300, 175
    bottom_circle_shape = pymunk.Segment(bottom_circle_body, (0, 50), (0, -50), width)
    bottom_circle_shape.collision_type = LEG_COLLISION_TYPE

    pivot = pymunk.PivotJoint(top_circle_body, bottom_circle_body, (0, -50), (0, 50))
    # rotary_limit = pymunk.RotaryLimitJoint(top_circle_body, bottom_circle_body, -2 * pi / 3, -.5)
    global motor
    motor = pymunk.SimpleMotor(top_circle_body, bottom_circle_body, 1)
    space.add(top_circle_shape, bottom_circle_body, bottom_circle_shape, pivot, motor)
    # space.add(top_circle_body, top_circle_shape, bottom_circle_body, bottom_circle_shape, pivot, rotary_limit)
    return top_circle_shape, bottom_circle_shape


def draw_ball(screen, ball):
    p = int(ball.body.position.x), 600 - int(ball.body.position.y)
    pygame.draw.circle(screen, THECOLORS["blue"], p, int(ball.radius), 2)


def draw_lines(screen, lines, line_color=THECOLORS["lightgray"]):
    for line in lines:
        body = line.body
        pv1 = body.position + line.a.rotated(body.angle)  # 1
        pv2 = body.position + line.b.rotated(body.angle)
        p1 = to_pygame(pv1)  # 2
        p2 = to_pygame(pv2)
        pygame.draw.lines(screen, line_color, False, [p1, p2])


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("ANW Simulation")
    clock = pygame.time.Clock()
    running = True
    force_time = 0

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)
    space.add_collision_handler(LEG_COLLISION_TYPE, LEG_COLLISION_TYPE, begin=lambda x, y: False)

    ground = add_ground(space)

    test_shapes = add_test_bodies(space)

    while running:
        screen.fill(THECOLORS["white"])

        force = -sin(force_time * pi) * 1
        motor.rate = force
        force_time+=0.01

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        draw_lines(screen, test_shapes, line_color=THECOLORS["blue"])

        draw_lines(screen, (ground,))
        space.step(1 / 50.0)
        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    sys.exit(main())
