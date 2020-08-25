import random

from plane.airplane import Airplane
from plane.airplane_draw_engine import AirplaneDrawEngine
from plane.draw_engine import DrawEngine
from plane.pillar import Pillars
from plane.pillar_draw_engine import PillarDrawEngine

PLAY_STATE = 0
RESUME_STATE = 1
GAME_OVER_STATE = 2

class PaperPlane:
    def __init__(self, canvas):
        self.__score = 0
        self.__gameState = GAME_OVER_STATE
        self.plane = Airplane(100, 200)
        self.pillars = Pillars()

        self.drawEngine = DrawEngine(canvas, self)
        self.planeDrawEngine = AirplaneDrawEngine(canvas, self.plane)
        self.drawEngine.add(self.planeDrawEngine)
        self.pillarDrawEngine = PillarDrawEngine(canvas, self.pillars)
        self.drawEngine.add(self.pillarDrawEngine)

    def init(self):
        self.plane.init()
        self.pillars.init()
        self.__initScore()

    def __initScore(self):
        self.__score = 0

    def __increaseScore(self):
        self.__score += 10 + random.randint(0, 5)

    def move_up(self):
        if self.isPlayState():
            self.plane.up()

    def move(self):
        if not self.isPlayState():
            return

        self.__increaseScore()

        self.plane.down()
        self.planeDrawEngine.tick()

        self.pillars.move()
        self.isAlive()

    def draw(self):
        if self.isPlayState():
            self.drawEngine.draw()
        else:
            self.drawEngine.drawStart()

    def isAlive(self):
        for p in self.pillars.get():
            if self.plane.isUpCrash(p[0], p[0] + 60, 60 + p[1] * 60) or \
               self.plane.isDownCrash(p[0], p[0] + 60, 540 - p[2] * 60):
                 self.__gameState = GAME_OVER_STATE
                 return False
        return True

    def isPlayState(self):
        return self.__gameState == PLAY_STATE

    def score(self):
        return self.__score

    def start(self):
        if self.__gameState == GAME_OVER_STATE:
            self.init()
        self.__gameState = PLAY_STATE

    def reume(self):
        if self.isPlayState():
            self.__gameState = RESUME_STATE