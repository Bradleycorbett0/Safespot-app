from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from firebase_config import save_to_firebase
import datetime

Window.softinput_mode = 'resize'  # Makes layout adjust when keyboard appears

class AddSpotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = FloatLayout()

        scroll = ScrollView(size_hint=(1, 1))
        box = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        title = Label(
            text="Add a Safe Spot",
            font_size='24sp',
            size_hint=(1, None),
            height='40dp',
            color=(0.2, 0.2, 0.2, 1)
        )
        box.add_widget(title)

        self.spot_input = TextInput(
            hint_text="Describe where and why it feels safe...",
            multiline=True,
            size_hint=(1, None),
            height='200dp',
            font_size='18sp'
        )
        box.add_widget(self.spot_input)

        submit_btn = Button(
            text="Save Safe Spot",
            size_hint=(1, None),
            height='60dp',
            background_color=(0.3, 0.6, 0.4, 1),
            font_size='20sp'
        )
        submit_btn.bind(on_press=self.save_spot)
        box.add_widget(submit_btn)

        back_btn = Button(
            text="Back",
            size_hint=(1, None),
            height='50dp',
            background_color=(0.9, 0.6, 0.5, 1),
            font_size='18sp'
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        box.add_widget(back_btn)

        scroll.add_widget(box)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def save_spot(self, instance):
        text = self.spot_input.text.strip()
        if not text:
            self.show_popup("Missing Info", "Please describe the safe spot.")
            return

        data = {
            "text": text,
            "timestamp": str(datetime.datetime.now())
        }

        if save_to_firebase("spots", data):
            self.show_popup("Success", "Spot saved.")
            self.spot_input.text = ""
        else:
            self.show_popup("Error", "Failed to save. Try again.")

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.75, 0.4))
        popup.open()