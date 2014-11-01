from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.label import Label

import editor

class BottomBar(BoxLayout):
    pass

class SideBar(BoxLayout):
    pass

class EditorApp(App):
    def build(self):
        self.root = FloatLayout()
        self.sidebar = SideBar(orientation="vertical",size_hint=(.05,1))
        self.root.add_widget(self.sidebar)
        self.sidebar.add_widget(Button(text="New",size_hint=(1,1)))
        self.sidebar.add_widget(Button(text="Save",size_hint=(1,1)))
        self.sidebar.add_widget(Button(text="Load",size_hint=(1,1)))
        self.sidebar.add_widget(Button(text="Edit",size_hint=(1,1)))
        self.editor = editor.EditorWindow(size_hint=(.95,.95),pos_hint={'x':.05, 'y':.05})
        self.root.add_widget(self.editor)
        self.bottombar = BottomBar(orientation="horizontal",size_hint=(1,.1))
        self.root.add_widget(self.bottombar)
        self.bottombar.add_widget(Label(text="doc.txt",size_hint=(.5,.5)))
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