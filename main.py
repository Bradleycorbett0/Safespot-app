from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# Set warm, calm background color
Window.clearcolor = (1, 0.98, 0.94, 1)

# Import all screens
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.add import AddSpotScreen
from screens.spots import SpotListScreen
from screens.about import AboutScreen
from screens.settings import SettingsScreen
from screens.events import EventsScreen
from screens.emergency import EmergencyScreen
from screens.comments import CommentsScreen

class SafeSpotApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))        # FIRST screen shown
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddSpotScreen(name='add'))
        sm.add_widget(SpotListScreen(name='spots'))
        sm.add_widget(AboutScreen(name='about'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(EventsScreen(name='events'))
        sm.add_widget(EmergencyScreen(name='emergency'))
        sm.add_widget(CommentsScreen(name='comments'))
        sm.current = 'login'  # Explicitly set the start screen
        return sm

if __name__ == '__main__':
    SafeSpotApp().run()