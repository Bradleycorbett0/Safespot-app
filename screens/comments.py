from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import json
import os

COMMENTS_FILE = "comments.json"

class CommentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.softinput_mode = "resize"
        Clock.schedule_once(self.build_ui)

    def build_ui(self, *args):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.comment_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, padding=(5, 5))
        self.comment_layout.bind(minimum_height=self.comment_layout.setter('height'))
        self.scroll.add_widget(self.comment_layout)

        self.input = TextInput(
            hint_text="Add a comment...",
            multiline=True,
            size_hint=(1, None),
            height=150,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1),
            padding=[10, 10]
        )

        add_btn = Button(
            text="Add Comment",
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.4, 0.2, 1)
        )
        add_btn.bind(on_press=self.add_comment)

        back_btn = Button(
            text="Back",
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.1, 0.1, 1)
        )
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(self.scroll)
        layout.add_widget(self.input)
        layout.add_widget(add_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)
        self.load_comments()

    def load_comments(self):
        self.comment_layout.clear_widgets()
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, "r") as f:
                try:
                    comments = json.load(f)
                except json.JSONDecodeError:
                    comments = []
        else:
            comments = []

        for idx, entry in enumerate(comments):
            text = entry.get("text", "")
            label = Label(
                text=text,
                halign='left',
                valign='middle',
                size_hint=(0.75, None),
                text_size=(Window.width * 0.7, None),
                color=(0, 0, 0, 1),
                font_size='16sp'
            )
            label.texture_update()
            label.height = label.texture_size[1] + 20

            delete_btn = Button(
                text="Delete",
                size_hint=(0.2, None),
                height=label.height,
                background_color=(0.5, 0.2, 0.2, 1),
                font_size='14sp'
            )
            delete_btn.bind(on_press=lambda instance, i=idx: self.delete_comment(i))

            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=label.height + 10, spacing=5, padding=(5, 0))
            row.add_widget(label)
            row.add_widget(delete_btn)

            self.comment_layout.add_widget(row)

    def add_comment(self, instance):
        text = self.input.text.strip()
        if text:
            if os.path.exists(COMMENTS_FILE):
                with open(COMMENTS_FILE, "r") as f:
                    try:
                        comments = json.load(f)
                    except json.JSONDecodeError:
                        comments = []
            else:
                comments = []

            comments.append({"text": text})
            with open(COMMENTS_FILE, "w") as f:
                json.dump(comments, f)

            self.input.text = ""
            self.load_comments()

    def delete_comment(self, index):
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, "r") as f:
                try:
                    comments = json.load(f)
                except json.JSONDecodeError:
                    comments = []
            if 0 <= index < len(comments):
                comments.pop(index)
                with open(COMMENTS_FILE, "w") as f:
                    json.dump(comments, f)
                self.load_comments()

    def go_back(self, instance):
        self.manager.current = "home"