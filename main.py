from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.gesture import Gesture, GestureDatabase
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.loader import Loader
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from functools import partial
from kivy.uix.slider import Slider
import re
import os

import wolframSearch
import thread

class InputBox(TextInput):
    
    def __init__(self, *args, **kwargs):
        super(InputBox, self).__init__(*args, **kwargs)
        self.result = ["no_stored_result"]
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'enter' and self.selection_text != '':
            # self.wolf_box.text = "Querying..."

            thread.start_new_thread(wolframSearch.createPopupFromCommand, (self.selection_text,self.result))
            Clock.schedule_once(self.queryHelper,2)
            
        else:
            super(InputBox, self)._keyboard_on_key_down(window, keycode, text, modifiers)
    def queryHelper(self,dt):
        if self.result[0] != "no_stored_result":
            match = re.match(r'.*\.png?$',self.result[0],re.I)
            self.wolf_box.clear_widgets()
            if match is None:
                self.wolf_box.add_widget(Label(text=self.result[0], size_hint=(1,None), text_size=self.wolf_box.size))
            else:
                self.wolf_box.add_widget(Image(source=self.result[0], size_hint=(1,None)))
            self.result[0] = "no_stored_result"
        else:
            Clock.schedule_once(self.queryHelper,dt)
        

    def insert_text(self, substring, from_undo=False):
        # s = substring.upper()
        return super(InputBox, self).insert_text(substring, from_undo=from_undo)

    def on_double_tap(self):
        tap = super(InputBox, self).on_double_tap()
        Clock.schedule_once(lambda dt: self.display_t())
        return tap

    def display_t(self):
        print(self.selection_text)

class BottomLabel(BoxLayout):
    doc_id = ObjectProperty(None)
    cursor_pos = ObjectProperty(None)
    def changeID(self,s):
        self.doc_id.text = s
    def update_cursor_pos(self, cursor, *args):
        pos_x = cursor.cursor_col
        pos_y = cursor.cursor_row
        self.cursor_pos.text = "Line: " + str(pos_y+1) + " Column: " + str(pos_x)
        Clock.schedule_once(partial(self.update_cursor_pos,cursor),.5)


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
    side_bar = ObjectProperty(None)
    bottom_bar = ObjectProperty(None)

    
    def __init__(self):
        super(TextEditor, self).__init__()
        self.wolf_box = GridLayout(cols=1, spacing=20,size_hint_y=None)
        self.wolf_box.bind(minimum_height=self.wolf_box.setter('height'))
        self.scroll_view = ScrollView(size_hint=(.3,.2), do_scroll_x=False, pos_hint={'right':.95,'top':.95})
        self.scroll_view.add_widget(self.wolf_box)
        self.input_box.wolf_box = self.wolf_box
        self.add_widget(self.scroll_view)
        Clock.schedule_once(partial(self.bottom_bar.update_cursor_pos,self.input_box),.5)

       
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.input_box.text)
       
        self.bottom_bar.changeID(path + "/" +filename)
        self.input_box.text = ''
        self.dismiss_popup()

    def new_save(self, trashVariable):
        self.dismiss_popup()
        self.show_save()
        self.bottom_bar.changeID("doc_id.txt")

    def new_no_save(self, trashVariable):
        self.dismiss_popup()
        self.input_box.text = ''
        self.bottom_bar.changeID("doc_id.txt")

    def show_new(self):
        if (self.input_box.text) != '': #inputbox not empty
            self._popup = Popup(title='Unsaved Work',
                content=FloatLayout(),
                size_hint=(None, None), size=(400, 300), auto_dismiss=False)
            saveBtn = Button(text = 'Save', size_hint = (0.3333, 0.15), pos_hint={'x':0, 'y':0})
            noSaveBtn = Button(text = 'Don\'t Save', size_hint = (0.3333, 0.15), pos_hint={'x':0.3333, 'y':0})
            cnclBtn = Button (text = 'Cancel', size_hint=(0.3333,0.15), pos_hint={'x':0.6667, 'y':0})
            saveWork = Label (text = 'Save Progress?', pos_hint={'x':0, 'y':0})
            self._popup.content.add_widget(saveBtn)
            self._popup.content.add_widget(noSaveBtn)            
            self._popup.content.add_widget(cnclBtn)
            self._popup.content.add_widget(saveWork)

            saveBtn.bind(on_release = self.new_save) #clear input and change directory name
            noSaveBtn.bind(on_release = self.new_no_save)
            cnclBtn.bind(on_release = self._popup.dismiss)
            self._popup.open()

        #else: print ("empty") #do nothing(?) - change directory name  
        
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.input_box.text = stream.read()
        self.bottom_bar.changeID(filename[0])
        self.dismiss_popup()

        self.dismiss_popup()
    def slider_r_update(self, slider, *args):
        self.input_box.foreground_color[0] = slider.value
    def slider_g_update(self, slider, *args):
        self.input_box.foreground_color[1] = slider.value
    def slider_b_update(self, slider, *args):
        self.input_box.foreground_color[2] = slider.value
    def slider_size_update(self, slider, *args):
        self.input_box.font_size = slider.value
    def show_edit(self):
        self._popup = Popup(title="Editing options",content=BoxLayout(orientation="vertical"),size_hint=(0.9, 0.9))
        colour_lbl = Label(text="Colour: (RGB sliders)")
        slider_r = Slider(min=0, max=255, value=204)
        slider_r.bind(value=self.slider_r_update)
        slider_g = Slider(min=0, max=255, value=204)
        slider_g.bind(value=self.slider_g_update)
        slider_b = Slider(min=0, max=255, value=204)
        slider_b.bind(value=self.slider_b_update)
        size_lbl = Label(text="Font_size: (8 to 72)")
        slider_size = Slider(min=8, max=72, value=10)
        slider_size.bind(value=self.slider_size_update)
        button = Button(text="Done")
        button.bind(on_release = self._popup.dismiss)
        self._popup.content.add_widget(colour_lbl)
        self._popup.content.add_widget(slider_r)
        self._popup.content.add_widget(slider_g)
        self._popup.content.add_widget(slider_b)
        self._popup.content.add_widget(size_lbl)
        self._popup.content.add_widget(slider_size)
        self._popup.content.add_widget(button)
        self._popup.open()
       

class EditorApp(App):
   
    def build(self):
        self.root = TextEditor()
        

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