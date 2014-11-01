from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

class MainTextInput(TextInput):
    def __init__(self):
        self.start_convert = 0
        self.math_mode = 0
        self.data = []
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
                result_image = None 
                self.data.append((text, result_image))
            self.start_convert = self.cursor_index() + 1
        print self.cursor_index()
        print self.data
        return super(MainTextInput, self).insert_text(substring, from_undo=from_undo)

class SimpleEditorApp(App):
    def build(self):
        root = FloatLayout(orientation='horizontal', size_hint=(1, 1))
        textinput = MainTextInput()
        textinput.focus = True
        # textinput.bind(text=on_text)
        root.add_widget(textinput)
        return root
      
if __name__ == '__main__':
    SimpleEditorApp().run()


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