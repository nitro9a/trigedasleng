from kivy.app import App
from kivy.lang import Builder

root = Builder.load_string('''
<ScaleLabel@Label>:
	_scale: 1. if self.texture_size[0] < self.width else float(self.width) / self.texture_size[0]
	background_color: 0,0,0,1
	canvas.before:
		PushMatrix
		Scale:
			origin: self.center
			x: self._scale or 1.
			y: self._scale or 1.
		Color:
			rgba: self.background_color
		Rectangle:
			pos: self.pos
			size: self.size
	canvas.after:
		PopMatrix
<-ScaleButton@Button>:
	state_image: self.background_normal if self.state == 'normal' else self.background_down
	disabled_image: self.background_disabled_normal if self.state == 'normal' else self.background_disabled_down
	_scale: 1. if self.texture_size[0] < self.width else float(self.width) / self.texture_size[0]
	canvas:
		Color:
			rgba: self.background_color
		BorderImage:
			border: self.border
			pos: self.pos
			size: self.size
			source: self.disabled_image if self.disabled else self.state_image
		PushMatrix
		Scale:
			origin: self.center
			x: self._scale or 1.
			y: self._scale or 1.
		Color:
			rgba: self.disabled_color if self.disabled else self.color
		Rectangle:
			texture: self.texture
			size: self.texture_size
			pos: int(self.center_x - self.texture_size[0] / 2.), int(self.center_y - self.texture_size[1] / 2.)
		PopMatrix
		
BoxLayout:
	orientation: 'vertical'
	ScaleLabel:
		size_hint_y: 0.2
		text: 'my scale text here (%d, %.2f)' % (self.width, self._scale)
		padding: dp(12), dp(12)
		font_size: self.height * 0.5
		bcolor: (1,1,1,1)

	ScaleButton:
		size_hint_y: 0.2
		text: 'scale button'
		padding: dp(0), dp(0)
		font_size: self.height * 0.5
		
	Widget
''')

class TestApp(App):
	def build(self):
		return root

if __name__ == '__main__':
    TestApp().run()