from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class testBody(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class testGame(Widget):
    body = ObjectProperty(None)
    # user = ObjectProperty(None)

    def start(self):
        self.body.center = self.center
        self.body.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.body.move()

        # #bounce of touch
        # self.user.collision(self.body)

        # bounce off top and bottom
        if (self.body.y < 0) or (self.body.top > self.height):
            self.body.velocity_y *= -1

        # bounce off left and right
        if (self.body.x < 0) or (self.body.right > self.width):
            self.body.velocity_x *= -1

    # def on_touch_move(self, touch):
    #     if touch.x < self.width / 3:
    #         self.player1.center_y = touch.y
    #     if touch.x > self.width - self.width / 3:
    #         self.player2.center_y = touch.y

class testApp(App):
    def build(self):
    	game = testGame()
    	game.start()
    	Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    testApp().run()