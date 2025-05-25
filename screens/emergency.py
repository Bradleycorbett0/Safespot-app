from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import webbrowser
import json
import os

CONTACTS_FILE = "emergency_contacts.json"

class EmergencyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.softinput_mode = 'resize'
        self.build_ui()

    def build_ui(self):
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)  # Warm background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_background, pos=self.update_background)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(layout)
        self.layout = layout  # store for reloading
        self.add_widget(scroll)

        self.load_contacts()

        back_btn = Button(
            text="Back",
            size_hint=(1, None),
            height=60,
            background_color=(0.6, 0.5, 0.8, 1),
            font_size='20sp'
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def load_contacts(self):
        self.layout.clear_widgets()
        if not os.path.exists(CONTACTS_FILE):
            return

        with open(CONTACTS_FILE, "r") as f:
            contacts = json.load(f)

        for item in contacts:
            label = item.get("label", "Unknown")
            link_type = item.get("type")
            value = item.get("value")

            btn = Label(
                text=f"[u][color=0000FF]{label}[/color][/u]",
                markup=True,
                font_size='18sp',
                size_hint_y=None,
                height=60
            )
            btn.bind(on_touch_down=self.get_callback(link_type, value))
            self.layout.add_widget(btn)

    def get_callback(self, link_type, value):
        def callback(instance, touch):
            if instance.collide_point(*touch.pos):
                if link_type == "call":
                    self.call_number(value)
                elif link_type == "web":
                    webbrowser.open(value)
        return callback

    def call_number(self, number):
        webbrowser.open(f"tel:{number}")