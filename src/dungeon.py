from panda3d.core import *
loadPrcFileData("", "window-title ダンジョンをカーソルキーで移動し床の穴を見つけて穴に入ろう！")
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight
from direct.actor.Actor import Actor
import sys
from math import pi, sin, cos

MAP_WIDTH_HEIGHT = 20
angleDelta = (0,15,-15,30,-30,45,-45,60,-60)
dungeonMap = [
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
  0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,
  0,1,1,1,0,0,0,0,1,0,0,0,0,0,1,2,1,0,0,0,
  0,1,1,1,0,0,0,0,1,1,1,1,1,0,1,1,1,0,0,0,
  0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,1,0,
  0,0,1,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,1,0,
  0,0,1,0,1,0,1,0,1,0,0,0,1,1,1,1,0,0,1,0,
  0,0,1,1,1,0,1,0,1,0,0,1,1,0,0,1,0,0,1,0,
  0,0,0,0,1,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,
  0,1,1,0,1,0,0,0,0,0,0,1,0,1,1,1,0,0,1,0,
  0,1,1,1,1,0,0,0,0,0,1,1,0,1,0,0,0,1,1,0,
  0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,1,1,1,0,0,
  0,1,0,0,1,1,1,1,1,1,1,0,0,1,0,1,0,0,0,0,
  0,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,
  0,1,1,0,0,0,1,0,0,0,1,1,1,1,0,1,1,1,0,0,
  0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,
  0,1,1,0,0,0,1,1,1,1,0,0,1,1,1,0,0,1,1,0,
  0,1,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0,
  0,1,1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,1,0,
  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
]

class DungeonGame(ShowBase):
  walls = []
  mySound = None

  def __init__(self):
    ShowBase.__init__(self)
    self.win.setClearColor((0, 0, 0, 1))
    self.setWalls()
    self.setPlayer()
    self.setKeys()
    self.setLights()
    self.mySound = base.loader.loadSfx("sounds/GameClear.wav")
    taskMgr.add(self.move, "moveTask")

  def setPlayer(self):
    self.actor = Actor()
    self.actor.reparentTo(render)
    self.actor.setPos((25, 25, 5))
    self.actor.setH(180)

  def setLights(self):
    ambientLight = AmbientLight("ambientLight")
    ambientLight.setColor((0.5,0.5,0.5,1))
    directionalLight = DirectionalLight("directionalLight")
    directionalLight.setDirection((-5, -2, -4))
    directionalLight.setColor((1,1,1,1))
    render.setLight(render.attachNewNode(ambientLight))
    render.setLight(render.attachNewNode(directionalLight))

  def setKeys(self):
    self.keyMap = {
      "left": 0, "right": 0, "forward": 0}
    self.accept("escape", sys.exit)
    self.accept("arrow_left", self.setKey, ["left", True])
    self.accept("arrow_right", self.setKey, ["right", True])
    self.accept("arrow_up", self.setKey, ["forward", True])
    self.accept("arrow_left-up", self.setKey, ["left", False])
    self.accept("arrow_right-up", self.setKey, ["right", False])
    self.accept("arrow_up-up", self.setKey, ["forward", False])
    self.disableMouse()

  def setKey(self, key, value):
    self.keyMap[key] = value

  def setWalls(self):
    for y in range(MAP_WIDTH_HEIGHT):
      for x in range(MAP_WIDTH_HEIGHT):
        if dungeonMap[y*MAP_WIDTH_HEIGHT+x] == 1:
          self.setWall(render,x,y+1,0,0,0,0)
          self.setWall(render,x,y,1,0,180,0)
          if dungeonMap[(y+1)*MAP_WIDTH_HEIGHT+x] == 0:
            self.setWall(render,x,y+1,1,0,90,0)
          if dungeonMap[(y-1)*MAP_WIDTH_HEIGHT+x] == 0:
            self.setWall(render,x,y,0,0,-90,0)
          if dungeonMap[y*MAP_WIDTH_HEIGHT+(x+1)] == 0:
            self.setWall(render,x+1,y+1,0,0,0,-90)
          if dungeonMap[y*MAP_WIDTH_HEIGHT+(x-1)] == 0:
            self.setWall(render,x,y+1,1,0,0,90)
        elif dungeonMap[y*MAP_WIDTH_HEIGHT+x] == 2:
          self.setWall(render,x,y,1,0,180,0)

  def setWall(self,render,x,y,z,h,p,r):
    self.walls.append(loader.loadModel("models/wall.egg"))
    self.walls[-1].reparentTo(render)
    self.walls[-1].setPos((x*10,y*10,z*10))
    self.walls[-1].setHpr(h,p,r)

  def move(self, task):
    dt = globalClock.getDt()
    self.control(dt)
    self.setCamera()
    return task.cont

  def control(self,dt):
    if self.keyMap["left"]:
      self.actor.setH(self.actor.getH() + 100 * dt)
    if self.keyMap["right"]:
      self.actor.setH(self.actor.getH() - 100 * dt)
    if self.keyMap["forward"]:
      for delta in angleDelta:
        if self.colMap(delta,dt):
          break

  def setCamera(self):
    self.camera.setPos(self.actor.getPos())
    self.camera.setY(self.actor,10)
    self.camera.lookAt(self.actor)

  def colMap(self,angle,dt):
    pos = self.actor.getPos()
    degrees = self.actor.getH() + angle
    radians = degrees * (pi / 180.0)
    x = pos[0] + sin(radians)*3
    y = pos[1] - cos(radians)*3
    val = int(y/10)*MAP_WIDTH_HEIGHT+int(x/10)
    if dungeonMap[val] == 1:
      x = pos[0] + sin(radians) * 20 * dt
      y = pos[1] - cos(radians) * 20 * dt
      self.actor.setPos(x,y,5)
      return True
    elif dungeonMap[val] == 2:
      dungeonMap[val] = 1
      self.mySound.play()
    return False

game = DungeonGame()
game.run()
