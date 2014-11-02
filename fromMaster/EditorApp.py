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
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.loader import Loader

import os

import wolframSearch
import thread

class DisplayBox(TextInput):
     def __init__(self, *args, **kwargs):
        super(DisplayBox, self).__init__(*args, **kwargs)

     def insert_text(self, substring, from_undo=False):
        print substring
        print self._lines
        return super(DisplayBox, self).insert_text(substring)

class InputBox(TextInput):
    def __init__(self, *args, **kwargs):
        super(InputBox, self).__init__(*args, **kwargs)
        self.ctrl = False

    def set_textdisplay(self,textdisplay):
        self.textdisplay = textdisplay

    def insert_text(self, substring, from_undo=False):
        self.textdisplay.cursor = self.cursor
        Clock.schedule_once(lambda dt: self.display_t(self.textdisplay.insert_text, substring, from_undo))
        return super(InputBox, self).insert_text(substring)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.textdisplay.cursor = self.cursor
        Clock.schedule_once(lambda dt: self.display_t(self.textdisplay.do_backspace, from_undo, mode))
        return super(InputBox, self).do_backspace(from_undo, mode)

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        # print keycode, modifiers
        _, keyname = keycode 
        if keyname == 'ctrl':
            self.ctrl = True
        if self.ctrl and keyname == 'spacebar':
            self.ctrl = False
            self.selectMath()
        super(InputBox, self)._keyboard_on_key_down(window, keycode, text, modifiers)

    def _keyboard_on_key_up(self, window, keycode):
        self.ctrl = False
        super(InputBox, self)._keyboard_on_key_up(window, keycode)

    def delete_selection(self, from_undo=False):
        self.textdisplay.selection_text = self.selection_text
        self.textdisplay._selection = self._selection
        self.textdisplay._selection_from, self.textdisplay._selection_to = self._selection_from, self._selection_to
        self.display_t(self.textdisplay.delete_selection, from_undo)
        super(InputBox, self).delete_selection(from_undo)

    def selectMath(self): # almost the same as double tap
        ci = self.cursor_index()
        cc = self.cursor_col
        line = self._lines[self.cursor_row]
        len_line = len(line)
        start = max(0, len(line[:cc]) - line[:cc].rfind(u' ') - 1)
        end = line[cc:].find(u' ')
        end = end if end > - 1 else (len_line - cc)
        self.select_text(ci - start, ci + end)
        print self.selection_text 
        # TODO: to image and blah...

    def display_t(self, func, *args):
        # print self.textdisplay.selection_text
        self.textdisplay.readonly = False
        func(*args)  
        self.textdisplay.readonly = True

class BottomLabel(BoxLayout):
    pass

class SideBar(BoxLayout):
     pass

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    inputbox = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class TextEditor(FloatLayout):
    input_box = ObjectProperty(None)
    display_box = ObjectProperty(None)
    side_bar = ObjectProperty(None)
    bottom_bar = ObjectProperty(None)
    
    def __init__(self):
        super(TextEditor, self).__init__()
        print self.display_box
        self.input_box.set_textdisplay(self.display_box)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.input_box.text)

        self.dismiss_popup()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.inputbox.text = stream.read()

        self.dismiss_popup()

class EditorApp(App):
   
    def build(self):
        self.root = TextEditor()
        return self.root
      
if __name__ == '__main__':
    EditorApp().run()