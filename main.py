#!/usr/bin/env python
try:
   import cPickle as pickle
except:
   import pickle
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


import os

# class Menu(BoxLayout):
# class MenuDialog(BoxLayout):
#     pass

class MainTextInput(TextInput):
    def __init__(self):
        self.start_convert = 0
        self.math_mode = 0
        self.data = []
        self.saved_file = ''
        TextInput.__init__(self)

    def insert_text(self, substring, from_undo=False):
        # s = substring.upper()

        if (substring == "$"):
            self.math_mode = 1-self.math_mode 
            if self.math_mode: # starting an equation
                text = self._get_text()[self.start_convert:]
                self.data.append(text)
            else: # ending an equation
                text = self._get_text()[self.start_convert:]
                ### TODO: search on wolfram 
                ### possibly save picture in disk, and just use the file directory
                result_image = None 
                self.data.append((text, result_image))
            self.start_convert = self.cursor_index() + 1
        print self.data
        return super(MainTextInput, self).insert_text(substring, from_undo=from_undo)

    # serialization
    def save_data(self, file_name = None):
        if math_mode:
            # can't serialize now
            return False

        if not file_name:
            file_name = self.saved_file
            if not file_name:
                # need input name
                return False
        else:
            self.saved_file = file_name

        try:
            pickle.dump( self, open( file_name, "wb" ) )
            return True
        except:
            # invalid file_name
            return False

    def load_data(self, file_name):
        self.save_data()

        try:
            return pickle.load( open( file_name, "rb" ) )
        except:
            # invalid file_name
            return None

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    #editor = ObjectProperty(None)
    #menu = ObjectProperty(None)
    #infobar = ObjectProperty(None)
    text_input = MainTextInput()
    # menu = ObjectProperty(None)


    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        self.text_input.save_data(os.path.join(path, filename))
        # with open(os.path.join(path, filename), 'w') as stream:
        #     stream.write(self.text_input.text)

        self.dismiss_popup()


class Editor(App):
    pass


# Factory.register('MenuDialog', cls=MenuDialog)
#Factory.register('MenuDialog', cls=MenuDialog)


if __name__ == '__main__':
    Editor().run()