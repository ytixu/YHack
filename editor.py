# Editor.py
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

class EditorWindow(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring.upper()
        return super(EditorWindow, self).insert_text(s, from_undo=from_undo)