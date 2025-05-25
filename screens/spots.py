import os
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

SPOTS_FILE = "spots.json"

class SpotListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=15)
        self.bind(size=self.update_background, pos=self.update_background)

        with self.canvas.before:
            self.bg_color = Color(1, 0.98, 0.94, 1)  # Warm cream background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        # Title
        title = Label(text="Saved Safe Spots", font_size='20sp', color=(0.2, 0.2, 0.2, 1), size_hint_y=None, height=40)
        self.layout.add_widget(title)

        # Scrollable list
        scroll = ScrollView(size_hint=(1, 0.8))
        self.spots_layout = GridLayout(cols=1, spacing=12, size_hint_y=None)
        self.spots_layout.bind(minimum_height=self.spots_layout.setter('height'))
        scroll.add_widget(self.spots_layout)
        self.layout.add_widget(scroll)

        # Back button
        back_btn = Button(text="Back to Home", size_hint=(1, 0.1), background_color=(0.8, 0.5, 0.2, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)
        self.refresh_spots()

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def refresh_spots(self):
        self.spots_layout.clear_widgets()
        spots = self.load_spots()
        sorted_spots = sorted(spots, key=lambda s: s.get("name", "").lower())

        for i, spot in enumerate(sorted_spots):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            name = Label(
                text=spot.get("name", "Unnamed Spot"),
                font_size='16sp',
                color=(0.1, 0.1, 0.1, 1),
                halign='left',
                valign='middle'
            )
            name.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
            delete_btn = Button(text="Delete", size_hint_x=None, width=80, background_color=(0.9, 0.4, 0.4, 1))
            delete_btn.bind(on_press=lambda inst, index=i: self.delete_spot(index))
            row.add_widget(name)
            row.add_widget(delete_btn)
            self.spots_layout.add_widget(row)

    def delete_spot(self, index):
        spots = self.load_spots()
        if 0 <= index < len(spots):
            spots.pop(index)
            self.save_spots(spots)
            self.refresh_spots()

    def load_spots(self):
        if os.path.exists(SPOTS_FILE):
            with open(SPOTS_FILE, "r") as f:
                return json.load(f)
        return []

    def save_spots(self, spots):
        with open(SPOTS_FILE, "w") as f:
            json.dump(spots, f, indent=2)