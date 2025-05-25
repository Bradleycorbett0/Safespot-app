from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import os

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.bind(size=self.update_background, pos=self.update_background)

        with self.canvas.before:
            self.bg_color = Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        scrollview = ScrollView(size_hint=(1, 1))

        content = GridLayout(cols=1, size_hint_y=None, padding=[10, 10], spacing=15)
        content.bind(minimum_height=content.setter('height'))

        text = (
            "SafeSpot is your personal map of safety and support.\n\n"
            "Whether you're facing a crisis or just need a moment of peace, "
            "SafeSpot helps you remember and return to places that made you feel safe — "
            "be it a local church, café, library, or community center.\n\n"
            "This app is made for anyone who’s ever needed somewhere to go, someone to talk to, "
            "or simply a breather from life’s pressures.\n\n"
            "With SafeSpot, you can:\n"
            "• Save and label your own trusted places.\n"
            "• Discover emergency services and mental health resources.\n"
            "• Stay informed about free meals, workshops, and events nearby.\n\n"
            "This isn’t just an app — it’s a lifeline, a reminder that you’re not alone, "
            "and a step toward reclaiming your peace of mind."
        )

        label = Label(
            text=text,
            font_size='16sp',
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            halign='left',
            valign='top',
            text_size=(Window.width - 40, None)
        )
        label.bind(texture_size=lambda inst, size: setattr(label, 'height', size[1]))

        content.add_widget(label)
        scrollview.add_widget(content)
        layout.add_widget(scrollview)

        back_btn = Button(
            text='Back',
            size_hint=(1, None),
            height='50dp',
            background_color=(0.95, 0.6, 0.4, 1)
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        # Add logo if available
        logo_path = "/storage/emulated/0/safespot/logo.png"
        if os.path.exists(logo_path):
            logo = Image(source=logo_path, size_hint=(1, None), height='80dp', allow_stretch=True, keep_ratio=True)
            layout.add_widget(logo)

        self.add_widget(layout)

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size