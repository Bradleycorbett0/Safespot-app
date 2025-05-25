from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.bind(size=self.update_background, pos=self.update_background)

        with self.canvas.before:
            self.bg_color = Color(1, 0.98, 0.94, 1)  # warm background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        layout.add_widget(Image(source='logo.png', size_hint=(1, 0.4), allow_stretch=True))

        buttons = [
            ('Add Safe Spot', 'add'),
            ('View Safe Spots', 'spots'),
            ('Emergency Contacts', 'emergency'),
            ('Events', 'events'),
            ('Settings', 'settings'),
            ('About', 'about'),
            ('Comments', 'comments'),  # NEW BUTTON
        ]

        for text, screen_name in buttons:
            btn = Button(text=text, size_hint=(1, None), height='50dp',
                         background_color=(0.95, 0.6, 0.4, 1))
            btn.bind(on_press=lambda inst, s=screen_name: setattr(self.manager, 'current', s))
            layout.add_widget(btn)

        self.add_widget(layout)

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size