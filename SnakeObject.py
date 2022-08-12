from ursina import *
from random import randrange

class Apple(Entity):
    def __init__(self, sizeOfMap, **kwargs):
        super().__init__(**kwargs)
        self.sizeOfMap = sizeOfMap
        self.creatRandomPosition()

    def creatRandomPosition(self):
        self.position = (randrange(self.sizeOfMap) + 0.5, randrange(self.sizeOfMap)+0.5,-0.5)

class SnakeBody(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Boom(Entity):
    def __init__(self, sizeOfMap, **kwargs):
        super().__init__(**kwargs)
        self.sizeOfMap = sizeOfMap
        self.creatRandomPosition()

    def creatRandomPosition(self):
        self.position = (randrange(self.sizeOfMap) + 0.5, randrange(self.sizeOfMap)+0.5,-0.5)


class Snake:
    def __init__(self, sizeOfMap):
        self.sizeOfMap = sizeOfMap
        self.segment_len = 1
        self.pos_len = self.segment_len + 1
        self.segment_pos=[Vec3(randrange(sizeOfMap)+0.5 , randrange(sizeOfMap)+0.5,-0.5)]
        self.segment_entities = []
        self.create_segment(self.segment_pos[0])
        self.directions = {'a':Vec3(-1,0,0), 'd':Vec3(1,0,0), 'w' :Vec3(0,1,0), 's':Vec3(0,-1,0)}
        self.direction = Vec3(0,0,0)
        self.permissions = {'a':1, 'd':1, 'w':1, 's':1}
        self.movement = {'a':'d', 'd' : 'a', 'w' :'s', 's':'w'}
        self.speed, self.score = 12,0
        self.frame_counter = 0

    def control(self):
        for key in 'wasd':
            if held_keys[key] and self.permissions[key]:
                self.direction = self.directions[key]
                self.permissions = dict.fromkeys(self.permissions,1)
                self.permissions[self.movement[key]] = 0
                break

    def run(self):
        self.frame_counter += 1
        if not self.frame_counter % self.speed:
            self.control()
            self.segment_pos.append(self.segment_pos[-1] + self.direction)
            self.segment_pos = self.segment_pos[-self.segment_len:]
            for segment , segment_pos in zip(self.segment_entities , self.segment_pos):
                segment.position = segment_pos

    def create_segment(self, position):
        entity = SnakeBody(position=position)
        SnakeBody(model='sphere', color=color.green, position=position).add_script(SmoothFollow(speed=12, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0,entity)

    def addSegment(self):
        self.segment_len +=1
        self.pos_len +=1
        self.score +=1
        self.speed = max(self.speed -1,5)
        self.create_segment(max(self.segment_pos[0]))

