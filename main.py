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
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.clock import Clock

class MainTextInput(TextInput):
    def __init__(self):
        TextInput.__init__(self)
        
        self.start_convert = 0
        self.math_mode = 0
        self.data = []
        self.image_dir = {}

        self.saved_file = ''
        self.HTML_file = ''

        self.original_textbox = TextInput()


    def insert_text(self, substring, from_undo=False):
        if (substring == "$"):
            self.math_mode = 1-self.math_mode 
            if not self.math_mode: # ending an equation
                text = self._get_text()[self.start_convert:]
                ### TODO: search on wolfram 
                ### possibly save picture in disk, and just use the file directory
                result_image = None 
                self.image_dir[text] = result_image 
            self.start_convert = self.cursor_index() + 1
        self.original_textbox.insert_text(substring, from_undo=from_undo)
        return super(MainTextInput, self).insert_text(substring, from_undo=from_undo)

    def convert_to_data(self):
        texts = self._get_text().split("$")
        cursor_index = 0
        for i, text in enumerate(texts):
            cursor_index += 1
            if not text:
                continue
            if i%2 == 0: # equations
                 self.data.append(())
            
        print self.data

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

    # def to_HTML(self, file_name = None):
    #     # assume no break within math mode
    #     # assume break before and after math mode indicate equation centered
    #     self.save_data()

    #     if not file_name:
    #         file_name = self.HTML_file
    #         if not file_name:
    #             # no file directory
    #             return False
    #     else:
    #         self.HTML_file = file_name

    #     page = PyH('title to be modified')
    #     # page.addCSS('...', ...)

    #     current_para = ""
    #     for d in self.data:
    #         if type(d) == str:
    #             paragraphs = d.split('\n')
    #             paragraphs[0] = current_para + " " + paragraphs[0]
    #             if d[-1] == '\n'
    #                 current_para = ''
    #             else:
    #                 current_para = paragraphs[-1]
    #                 paragraphs = paragraphs[:-1]
    #             for para in paragraphs:
    #                 page << p(para)
    #         else: # tuple
    #             if current_para:
    #                 current_para += '<img src=%s, class="inline_img")>' % d[1] 
    #                             # supposingly in a css file, we have descriptions for inline_img
    #             else:
    #                 page << center() << img(src=d[1])

    #     page.printOut()


class TextInputer(TextInput):

    def __init__(self):
        TextInput.__init__(self)
        self.ctrl = False

    def set_textdisplay(self,textdisplay):
        self.textdisplay = textdisplay

    def insert_text(self, substring, from_undo=False):
        self.textdisplay.cursor = self.cursor
        Clock.schedule_once(lambda dt: self.display_t(self.textdisplay.insert_text, substring, from_undo))
        return super(TextInputer, self).insert_text(substring)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.textdisplay.cursor = self.cursor
        Clock.schedule_once(lambda dt: self.display_t(self.textdisplay.do_backspace, from_undo, mode))
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
        super(TextInputer, self)._keyboard_on_key_up(window, keycode)

    def delete_selection(self, from_undo=False):
        self.textdisplay.selection_text = self.selection_text
        self.textdisplay._selection = self._selection
        self.textdisplay._selection_from, self.textdisplay._selection_to = self._selection_from, self._selection_to
        self.display_t(self.textdisplay.delete_selection, from_undo)
        super(TextInputer, self).delete_selection(from_undo)

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


class TextEditor(GridLayout):
    
    def __init__(self):
        GridLayout.__init__(self, cols=1, rows=2)
        textdisplay = TextInput()
        textdisplay.readonly = True
        self.textinput = TextInputer()
        self.textinput.set_textdisplay(textdisplay)
        self.textinput.focus = True
        self.add_widget(textdisplay)
        self.add_widget(self.textinput)

class SimpleEditorApp(App):
    def build(self):
        self.root = TextEditor()
        # editor = TextEditor()
        # editor.focus = True
        # textinput.bind(text=on_text)
        # root.add_widget(editor)
        return self.root

      
if __name__ == '__main__':
    SimpleEditorApp().run()