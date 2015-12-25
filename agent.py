# -*-coding:utf-8-*-
# Author: Shen Shen
# Email: dslwz2002@163.com

import numpy as np
from tools import *

class Agent(object):
    def __init__(self):
        # random initialize a agent
        self.mass = 60.0
        self.radius = 0.3
        self.desiredV = 0.8
        self.direction = np.array([0.0, 0.0])
        self.actualV = np.array([0.0,0.0])
        self.acclTime = 10.0
        self.pos = np.array([10.0, 10.0])
        self.dest = np.array([100.0,10.0])
        self.bodyFactor = 120000
        self.slideFricFactor = 240000
        self.A = 2000
        self.B = 0.08

    # def step(self):
    #     # 初始速度和位置
    #     v0 = self.actualV
    #     r0 = self.pos
    #     self.direction = normalize(self.dest - self.pos)
    #     # 计算受力
    #     adapt = self.adaptVel()
    #     peopleInter = self.peopleInteraction()
    #     wallInter = self.wallInteraction()
    #     sumForce = adapt + peopleInter + wallInter
    #     # 计算加速度
    #     accl = sumForce/self.mass
    #     # 计算速度
    #     self.actualV = v0 + accl # consider dt = 1
    #     # 计算位移
    #     self.pos = r0 + v0 + 0.5*accl
    #     print(accl,self.actualV,self.pos)

    def adaptVel(self):
        deltaV = self.desiredV*self.direction - self.actualV
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)
        return deltaV*self.mass/self.acclTime

    def peopleInteraction(self, other):
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = (self.A*np.exp((rij-dij)/self.B) + self.bodyFactor*g(rij-dij))*nij
        tij = np.array([-nij[1],nij[0]])
        deltaVij = (self.actualV - other.actualV)*tij
        second = self.slideFricFactor*g(rij-dij)*deltaVij*tij
        return first + second

    def wallInteraction(self, wall):
        ri = self.radius
        diw,niw = distanceP2W(self.pos,wall)
        first = (self.A*np.exp((ri-diw)/self.B) + self.bodyFactor*g(ri-diw))*niw
        tiw = np.array([-niw[1],niw[0]])
        second = self.slideFricFactor*g(ri-diw)*(self.actualV*tiw)*tiw
        return first - second
