# -*-coding:utf-8-*-
# Author: Shen Shen
# Email: dslwz2002@163.com

import pygame
import pygame.draw
import numpy as np
from config import *
from agent import *
from tools import *

SCREENSIZE = config['screen_size']
RESOLUTION = config['resolution']
AGENTSNUM = config['agents_num']
BACKGROUNDCOLOR = config['background_color']
AGENTCOLOR = config["agent_color"]
LINECOLOR = config["line_color"]
AGENTSIZE = config["agent_size"]
AGENTSICKNESS = config["agent_sickness"]
WALLSFILE = config["walls_file"]

screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Social Force Model')

# initialize walls
walls = []
for line in open(WALLSFILE):
    coords = line.split(',')
    wall = []
    wall.append(float(coords[0]))
    wall.append(float(coords[1]))
    wall.append(float(coords[2]))
    wall.append(float(coords[3]))
    walls.append(wall)

# initialize agents
agents = []
for n in range(AGENTSNUM):
    agent = Agent()
    agents.append(agent)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
        # elif event.type == pygame.MOUSEBUTTONUP:

    screen.fill(BACKGROUNDCOLOR)

    # draw walls
    for wall in walls:
        startPos = np.array([wall[0],wall[1]])
        endPos = np.array([wall[2],wall[3]])
        startPx = worldCoord2ScreenCoord(startPos,SCREENSIZE,RESOLUTION)
        endPx = worldCoord2ScreenCoord(endPos,SCREENSIZE,RESOLUTION)
        pygame.draw.line(screen, LINECOLOR,startPx,endPx)

    # draw agents
    pygame.draw.circle(screen, AGENTCOLOR, [400,300], AGENTSIZE, AGENTSICKNESS)

    # 计算相互作用力
    for idxi,ai in enumerate(agents):
        # 初始速度和位置
        v0 = ai.actualV
        r0 = ai.pos
        ai.direction = normalize(ai.dest - ai.pos)
        # 计算受力
        adapt = ai.adaptVel()
        peopleInter = 0.0
        wallInter = 0.0

        # for idxj,aj in enumerate(agents):
        #     if idxi == idxj:
        #         continue
        #     peopleInter += ai.peopleInteraction(aj)

        for wall in walls:
            wallInter += ai.wallInteraction(wall)

        sumForce = adapt + peopleInter + wallInter
        # 计算加速度
        accl = sumForce/ai.mass
        # 计算速度
        ai.actualV = v0 + accl # consider dt = 1
        # 计算位移
        ai.pos = r0 + v0 + 0.5*accl
        print(accl,ai.actualV,ai.pos)

    for agent in agents:
        scPos = worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
        pygame.draw.circle(screen, AGENTCOLOR, scPos, AGENTSIZE, AGENTSICKNESS)

    pygame.display.flip()
