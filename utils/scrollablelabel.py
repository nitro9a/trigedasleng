from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder

long_text = 'yay moo cow foo bar moo baa ' * 100

Builder.load_string('''
<ScrollableLabel>:
    bcolor: 3,3,0,1
    color: 0,0,0,1
    fsize: 100
    Label:
        markup: True
        font_name: 'fonts/Roboto_Mono/RobotoMono-Regular.ttf'
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        color: root.color
        text: root.text
        font_size: root.fsize
        valign: "top"

        canvas.before:          
            Color:
                rgba: root.bcolor
            Rectangle:
                pos: self.pos
                size: self.size

''')

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class ScrollApp(App):
    def build(self):
        return ScrollableLabel(text=long_text)

if __name__ == "__main__":
    ScrollApp().run()