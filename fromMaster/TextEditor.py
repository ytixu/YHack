import os
try:
   import cPickle as pickle
except:
   import pickle

from pyh import *
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.gesture import Gesture, GestureDatabase
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout


import wolframSearch

class TextLabel(Label):

    def __init__(self, text, size):
        Label.__init__(self)
        self.padding = (-20, -20)
        self.bind(size=self.setter('text_size')) 
        # self.bind(minimum_hight = self.setter('height'))
        self.text_size = size
        self.text = text
        self.size_hint = (1,None)

class DisplayLabel(StackLayout):
    def __init__(self):
        StackLayout.__init__(self, orientation = "tb-lr")
        self.data = {}
        index = 0

    def update(self, lines):
        self.clear_widgets()
        text = ''
        for l in lines:
            if l not in self.data:
                text += l+"\n"
            else:
                if text:
                    self.add_widget(TextLabel(text, self.size))
                    text = ''
                image = self.data[l]
                self.add_widget(Image(source=image, size_hint=(1,None)))
        if text:
            self.add_widget(TextLabel(text, self.size))

    def addImage(self, image, line):
        self.data[line] = image


class TextInputer(TextInput):

    def __init__(self):
        TextInput.__init__(self)
        self.ctrl = False
        self.data = []

    def set_textdisplay(self,textdisplay):
        self.textdisplay = textdisplay

    def insert_text(self, substring, from_undo=False):
        self.textdisplay.cursor = self.cursor
        Clock.schedule_once(lambda dt: self.textdisplay.update(self.text.split('\n')))
        return super(TextInputer, self).insert_text(substring)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.textdisplay.cursor = self.cursor
        Clock.schedule_once(lambda dt: self.textdisplay.update(self.text.split('\n')))
        return super(TextInputer, self).do_backspace(from_undo, mode)

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        # print keycode, modifiers
        _, keyname = keycode 
        if keyname == 'ctrl':
            self.ctrl = True
        if self.ctrl and keyname == 'spacebar':
            self.ctrl = False
            self.selectMath()
        super(TextInputer, self)._keyboard_on_key_down(window, keycode, text, modifiers)

    def _keyboard_on_key_up(self, window, keycode):
        self.ctrl = False
        return super(TextInputer, self)._keyboard_on_key_up(window, keycode)

    def delete_selection(self, from_undo=False):
        Clock.schedule_once(lambda dt: self.textdisplay.update(self.text.split('\n')))
        return super(TextInputer, self).delete_selection(from_undo)

    def selectMath(self): # almost the same as double tap
        ci = self.cursor_index()
        cc = self.cursor_col
        line = self._lines[self.cursor_row]
        len_line = len(line)
        start = ci - cc
        self.select_text(start, start+len_line)
        print self.selection_text
        # result = wolframSearch.getQueryFromCommand(line)
        result = "math.png"
        self.textdisplay.addImage(result, line)
        Clock.schedule_once(lambda dt: self.textdisplay.update(self.text.split('\n')))


class MenuStack(GridLayout):

    def __init__(self, **kwargs):
        GridLayout.__init__(self, cols=1, rows=3, **kwargs)
        self.new = Button(text="new",size_hint_x=None, width=50)
        self.save = Button(text="save",size_hint_x=None, width=50)
        self.load = Button(text="load",size_hint_x=None, width=50)
        for btn in [self.new, self.save, self.load]:
            self.add_widget(btn)


class TextEditor(GridLayout):
    
    def __init__(self, **kwargs):
        GridLayout.__init__(self, cols=1, rows=2, **kwargs)
        textdisplay = DisplayLabel()
        textdisplay.readonly = True
        scroll_view = ScrollView(do_scroll_x=False, pos_hint={'right':1,'top':.99})
        scroll_view.add_widget(textdisplay)
        self.textinput = TextInputer()
        self.textinput.set_textdisplay(textdisplay)
        self.textinput.focus = True
        self.add_widget(scroll_view)
        self.add_widget(self.textinput)

class MainPanel(BoxLayout):
    def __init__(self):
        BoxLayout.__init__(self)
        self.orientation = "horizontal"
        self.btns = MenuStack(size_hint_x=None, width=50)
        self.txte = TextEditor()
        self.add_widget(self.btns)
        self.add_widget(self.txte)

        self.btns.new.bind(on_press=self.new)
        self.btns.save.bind(on_press=self.save)
        self.btns.load.bind(on_press=self.load)

    def new(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

class SimpleEditorApp(App):
    def build(self):
        self.root = MainPanel()
        return self.root

      
if __name__ == '__main__':
    SimpleEditorApp().run()