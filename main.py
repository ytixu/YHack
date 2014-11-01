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

import os

class InputBox(TextInput):
    def __init__(self, **kwargs):
        super(InputBox, self).__init__(**kwargs)
        self.selection_text = super(InputBox, self).selection_text
    def insert_text(self, substring, from_undo=False):
        s = substring.upper()
        return super(InputBox, self).insert_text(s, from_undo=from_undo)

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
    def __init__(self):
        super(TextEditor, self).__init__()
        self.inputbox = InputBox()
        self.sidebar = SideBar()
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            print "Double Tap!"
            print self.inputbox.selection_text
        if self.inputbox.selection_text == '':
            super(TextEditor, self).on_touch_down(touch)
        else:
            print self.inputbox.selection_text
        
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.inputbox.text)

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
        # self.root.sidebar = SideBar()
        self.root.sidebar.savedialog = SaveDialog()
        self.root.sidebar.loaddialog = LoadDialog()
        # self.root.inputbox = InputBox()

        return self.root
      
if __name__ == '__main__':
    EditorApp().run()


# math/code/science mode (i.e. latex interpretation but with natural language (wolfram?))
# free draw mode (possibly with drawing recoginition? i.e. draw-to-text)
# graph mode, charts, diagrams, webs, flow charts etc etc etc 
# timeline creation from input dates
# map mode (tex to map)
# create a link between places in your notes
# auto-completion
# vocab storage
# headings
# marking as important
# term - def - example structure
# collapsable everything (images and defs and such)
# lists, bulletting
# subject based themes
# quick pull relevant images off the internet
# orgranization
# pre-dated; already have course info
# quick wizard when creating notes for a new class
# pull examples from other peoples notes? (Sharing based)
# word command followed by common symbol or key sequence	
# heading hierarchy HEADING - SUBHEADING etc...
# ability to click on words and get definition from previous areas in notes
# highlighting words with options
# be able to quick pull more information about what you're taking notes on in general