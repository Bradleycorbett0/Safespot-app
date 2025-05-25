from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import json
import os

COMMENTS_FILE = "comments.json"

class CommentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        with self.canvas.before:
            Color(1, 0.98, 0.94, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_background, pos=self.update_background)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        scroll = ScrollView(size_hint=(1, 0.9))
        self.comments_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=[10, 10])
        self.comments_layout.bind(minimum_height=self.comments_layout.setter('height'))

        scroll.add_widget(self.comments_layout)
        layout.add_widget(scroll)

        back_btn = Button(
            text="Back",
            size_hint=(1, 0.1),
            background_color=(0.4, 0.25, 0.2, 1),
            font_size='20sp'
        )
        back_btn.bind(on_press=lambda instance: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        self.add_widget(layout)
        self.load_comments()

    def update_background(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def load_comments(self):
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, "r", encoding='utf-8') as f:
                try:
                    comments = json.load(f)
                    if isinstance(comments, list):
                        for comment in comments:
                            if isinstance(comment, str):  # Ensure it's a string
                                label = Label(
                                    text=comment,
                                    size_hint_y=None,
                                    height=60,
                                    font_size='18sp',
                                    halign='left',
                                    valign='middle',
                                    text_size=(self.width - 40, None)
                                )
                                self.comments_layout.add_widget(label)
                except json.JSONDecodeError:
                    print("Invalid JSON format in comments.json")