from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
from kivy.config import Config

from functools import partial

from dict_android import *

Config.set('kivy', 'keyboard_mode', 'systemandmulti')

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press: root.manager.current = 'search_page'
        Button:
            text: 'Quit'

<SearchPage>:
    name: "search_page"

""")

# Declare both screens
class MenuScreen(Screen):
    pass

class SearchPage(Screen):
    def on_pre_enter(self, *args):
       sbp = SearchBoxPage()
       sbp.build()
       self.add_widget(sbp)
    
class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SearchPage(name='search_page'))

        return sm

if __name__ == '__main__':
    TestApp().run()