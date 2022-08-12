from SnakeObject import *

class SnakeGame(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.black
        #window.fullscreen = True
        Light(type='ambient', color=(0.5,0.5, 0.5,1))
        Light(type='directional', color=(0.5,0.5,0.5,1),direction=(1, 1, 1))
        self.SizeOfMap = 20
        self.map(self.SizeOfMap)
        self.snake = Snake(self.SizeOfMap)
        self.apple = Apple(self.SizeOfMap, model='sphere', color=color.red)
        self.boom = Boom(self.SizeOfMap,model='quad',texture = 'unnamed.png',scale =(1.3,2.6))
        camera.position = (self.SizeOfMap//2,-20.5,-20)
        camera.rotation_x = -58

    def map(self,SizeOfMap):
        Entity(model='quad', scale=SizeOfMap , position=(SizeOfMap//2,SizeOfMap//2,0), color=color.dark_gray)
        Entity(model=Grid(SizeOfMap,SizeOfMap),scale=SizeOfMap,position=(SizeOfMap//2,SizeOfMap//2,-0.01) , color=color.white)

    def newGame(self):
        scene.clear()
        self.map(self.SizeOfMap)
        self.snake = Snake(self.SizeOfMap)
        self.apple = Apple(self.SizeOfMap, model='sphere', color=color.red)
        self.boom = Boom(self.SizeOfMap,model='quad',texture = 'unnamed.png',scale =(1.3,2.6))

    def input(self, key):
        if key == '2':
            camera.rotation_x = 0
            camera.position = (self.SizeOfMap // 2, self.SizeOfMap // 2, -50)
        elif key == '3':
            camera.position = (self.SizeOfMap // 2, -20.5, -20)
            camera.rotation_x = -58
        super().input(key)

    def checkApple(self):
        if self.snake.segment_pos[-1] == self.apple.position:
            self.snake.addSegment()
            self.apple.creatRandomPosition()
            self.boom.creatRandomPosition()

    def check_game_over(self):
        snake = self.snake.segment_pos
        if 0 < snake[-1][0] < self.SizeOfMap and 0 < snake[-1][1] < self.SizeOfMap and len(snake) == len(set(snake)) and self.snake.segment_pos[-1] != self.boom.position:
            return
        print_on_screen('GAME OVER', position=(-0.7, 0.1), scale=10, duration=1)
        self.snake.direction = Vec3(0, 0, 0)
        self.snake.permissions = dict.fromkeys(self.snake.permissions, 0)
        invoke(self.newGame, delay=1)


    def update(self):
        print_on_screen(f'Score: {self.snake.score}', position=(-0.70, 0.45), scale=3, duration=1 / 20)
        self.checkApple()
        self.check_game_over()
        self.snake.run()


if __name__ == '__main__':
    game = SnakeGame()
    update = game.update
    game.run()
