from kivy.app import App 
from kivy.uix.label import Label
from kivy.animation import Animation


class DraggableLabel(Label):
    '''A label you can drag upside-down'''
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # assure ourselves we will get the updates of this motion
            touch.grab(self)
            return True

        return super(DraggableLabel, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # really straightforward...
            self.y = touch.y
            return True

        return super(DraggableLabel, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # check if the movement direction was up or down
            if touch.dy < 0:
                a = Animation(y=0) # down? put the bar all the way down
            else:
                a = Animation(top=self.parent.top) # up? put it at the top

            a.start(self) # actually start the animation
            return True

        return super(DraggableLabel, self).on_touch_up(touch)


class TabApp(App):
    pass


TabApp().run()