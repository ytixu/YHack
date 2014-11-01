try:
   import cPickle as pickle
except:
   import pickle

from pyh import *
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput


class MainTextInput(TextInput):
    def __init__(self):
        self.start_convert = 0
        self.math_mode = 0
        self.data = []

        self.saved_file = ''
        self.HTML_file = ''

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

    def to_HTML(self, file_name = None):
        # assume no break within math mode
        # assume break before and after math mode indicate equation centered
        self.save_data()

        if not file_name:
            file_name = self.HTML_file
            if not file_name:
                # no file directory
                return False
        else:
            self.HTML_file = file_name

        page = PyH('title to be modified')
        # page.addCSS('...', ...)

        current_para = ""
        for d in self.data:
            if type(d) = str:
                paragraphs = d.split('\n')
                paragraphs[0] = current_para + " " + paragraphs[0]
                if d[-1] == '\n'
                    current_para = ''
                else:
                    current_para = paragraphs[-1]
                    paragraphs = paragraphs[:-1]
                for para in paragraphs:
                    page << p(para)
            else: # tuple
                if current_para:
                    current_para += '<img src=%s, class="inline_img")>' % d[1] 
                                # supposingly in a css file, we have descriptions for inline_img
                else:
                    page << center() << img(src=d[1])

        page.printOut()




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