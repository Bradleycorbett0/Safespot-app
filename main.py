from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import json

# Load safe spots from file
def load_spots():
    try:
        with open("safespots.json", "r") as f:
            return json.load(f)
    except:
        return []

# Home screen
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="SafeSpot", font_size=32))

        layout.add_widget(Button(text="View Safe Spots", on_press=self.go_spots))
        layout.add_widget(Button(text="Add New Spot", on_press=self.go_add))
        layout.add_widget(Button(text="Events Feed", on_press=self.go_events))
        layout.add_widget(Button(text="Emergency", on_press=self.go_emergency))

        self.add_widget(layout)

    def go_spots(self, instance):
        self.manager.current = 'spots'

    def go_add(self, instance):
        self.manager.current = 'add'

    def go_events(self, instance):
        self.manager.current = 'events'

    def go_emergency(self, instance):
        self.manager.current = 'emergency'

# Safe Spots screen
class SafeSpotsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.update_list()
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.update_list()

    def update_list(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Safe Spots Near You", font_size=24))
        for spot in load_spots():
            self.layout.add_widget(Label(text=f"{spot['name']} - {spot['type']} - {spot['location']}"))
        self.layout.add_widget(Button(text="Back", on_press=self.go_home))

    def go_home(self, instance):
        self.manager.current = 'home'

# Add Spot screen
class AddSpotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.name_input = TextInput(hint_text="Name", multiline=False)
        self.type_input = TextInput(hint_text="Type (library, park, etc)", multiline=False)
        self.location_input = TextInput(hint_text="Location", multiline=False)

        layout.add_widget(Label(text="Add a New Safe Spot", font_size=24))
        layout.add_widget(self.name_input)
        layout.add_widget(self.type_input)
        layout.add_widget(self.location_input)
        layout.add_widget(Button(text="Submit", on_press=self.save_spot))
        layout.add_widget(Button(text="Back", on_press=self.go_home))
        self.add_widget(layout)

    def save_spot(self, instance):
        new_spot = {
            "name": self.name_input.text,
            "type": self.type_input.text,
            "location": self.location_input.text
        }
        try:
            with open("safespots.json", "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(new_spot)
        with open("safespots.json", "w") as f:
            json.dump(data, f, indent=2)

        self.name_input.text = ""
        self.type_input.text = ""
        self.location_input.text = ""

    def go_home(self, instance):
        self.manager.current = 'home'

# Event screen
class EventScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="Free Events", font_size=24))
        events = [
            {"title": "Youth Football", "day": "Saturday"},
            {"title": "Art Club", "day": "Wednesday"},
        ]
        for e in events:
            layout.add_widget(Label(text=f"{e['title']} - {e['day']}"))
        layout.add_widget(Button(text="Back", on_press=self.go_home))
        self.add_widget(layout)

    def go_home(self, instance):
        self.manager.current = 'home'

# Emergency screen
class EmergencyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text="Emergency Contacts", font_size=24))
        layout.add_widget(Label(text="Police: 999\nShelter: 0800 123 456"))
        layout.add_widget(Button(text="Back", on_press=self.go_home))
        self.add_widget(layout)

    def go_home(self, instance):
        self.manager.current = 'home'

# Main app
class SafeSpotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SafeSpotsScreen(name='spots'))
        sm.add_widget(AddSpotScreen(name='add'))
        sm.add_widget(EventScreen(name='events'))
        sm.add_widget(EmergencyScreen(name='emergency'))
        return sm

if __name__ == '__main__':
    SafeSpotApp().run()
