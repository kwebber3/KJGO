from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')

from functools import partial

from dict_android import *
from listening_android import *
from speaking_android import *
from reading_android import *
from writing_android import *


from kivy.app import App
from kivy.base import EventLoop
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
import os

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import pandas as pd

import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
        self.user_path = USER_PATH

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(SaveDialog, self).__init__(**kwargs)
        self.user_path = USER_PATH


class FilePage(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(FilePage, self).__init__(**kwargs)
        self.user_path = USER_PATH

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        filepath = str(os.path.join(path, filename[0]))


        x = read_table(filepath_or_buffer=filepath, delimiter="\t",encoding = "UTF-16")

        columns_exist = True
        for eachColumn in [KANJI_HEADER,R_HEADER,ENGLISH_HEADER,K_SENTENCE_HEADER,JP_SENTENCE_HEADER,ENG_SENTENCE_HEADER]:
            if  not eachColumn in x.columns:
                columns_exist = False
        for eachScoreCol in [L_SCORE_HEADER,S_SCORE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER]:
            if  not eachScoreCol in x.columns:
                x[eachScoreCol] = 0            

        if columns_exist:
            x.to_csv(USER_FILENAME, mode='a', header = False, sep="\t", encoding="UTF-16", index=False)
        else: 
            print("Error: Missing Column")

        self.dismiss_popup()

    def save(self, path, filename):
        if len(filename) > 0:
            filepath = str(os.path.join(path, filename))
        else:
            filepath = str(path)
        x = read_table(filepath_or_buffer=USER_FILENAME, delimiter="\t",encoding = "UTF-16")

        x.to_csv(filepath,sep="\t", encoding="UTF-16",index=False, header= True)

        self.dismiss_popup()




OPERATING_SYSTEM = os.name
WINDOWS_KEY = "nt"
ANDROID_KEY = "posix"
if OPERATING_SYSTEM == ANDROID_KEY:
    from android.storage import app_storage_path
    app_storage_directory_path = app_storage_path()
    USER_FILENAME =  app_storage_directory_path+"/User_Loaded.txt"
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
    USER_PATH = "/storage/emulated/0/"
    if not os.path.isfile(DICTIONARY_NAME):
        x = read_table(filepath_or_buffer="User_Loaded.txt", delimiter="\t",encoding = "UTF-16")
        x.to_csv(DICTIONARY_NAME, sep = "\t",encoding = "UTF-16",index=False)
else:
    USER_FILENAME = "../User_Loaded.txt"
    USER_PATH = "../"
DICTIONARY_NAME =  USER_FILENAME
    


# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: "vertical"
        Button:
            text: 'Go to Dictionary'
            on_release: root.manager.current = 'search_page'
        Button:
            text: 'Go to Flashcards'
            on_release: root.manager.current = 'learn_page'
        Button:
            text: 'Load/Export Files'
            on_release: root.manager.current = 'file_page'

<SearchPage>:
    name: "search_page"

<LearningMainPage>
    name: "learn_page"
    BoxLayout:
        orientation: "vertical"
        Button:
            text: "Listening"
            on_release: root.manager.current = "listening_page"
        Button:
            text: "Speaking"
            on_release: root.manager.current = "speaking_page"
        Button:
            text: "Reading"
            on_release: root.manager.current = "reading_page"
        Button:
            text: "Writing"
            on_release: root.manager.current = "writing_page"

            
<FilePage>
    name: "file_page"
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Load'
            on_release: root.show_load()
        Button:
            text: 'Save'
            on_release: root.show_save()

        

<SpeakingPage>
    name: "speaking_page"    

<ReadingPage>
    name: "reading_page"

<WritingPage>
    name: "writing_page"  

<LoadDialog>:
    user_path: root.user_path
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            rootpath: root.user_path
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 60
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)

<SaveDialog>:
    text_input: text_input
    user_path: root.user_path
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            rootpath: root.user_path
            on_selection: text_input.text = self.selection and self.selection[0] or ''

        TextInput:
            id: text_input
            size_hint_y: None
            height: 60
            multiline: False

        BoxLayout:
            size_hint_y: None
            height: 60
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Save"
                on_release: root.save(filechooser.path, text_input.text)
    
""")

# Declare both screens
class MenuScreen(Screen):
    pass

class LearningMainPage(Screen):
    pass



class ListeningPage(Screen):
    def on_pre_enter(self, *args):
       self.lbp = ListeningBox()
       self.lbp.build()
       self.add_widget(self.lbp)

class SpeakingPage(Screen):
    def on_pre_enter(self, *args):
       self.sbp = SpeakingBox()
       self.sbp.build()
       self.add_widget(self.sbp)

class ReadingPage(Screen):
    def on_pre_enter(self, *args):
       self.rbp = ReadingBox()
       self.rbp.build()
       self.add_widget(self.rbp)

class WritingPage(Screen):
    def on_pre_enter(self, *args):
       self.wbp = WritingBox()
       self.wbp.build()
       self.add_widget(self.wbp)

class SearchPage(Screen):
    def on_pre_enter(self, *args):
       sbp = SearchBoxPage()
       sbp.build()
       self.add_widget(sbp)
    
class TestApp(App):

    def build(self):
        # Create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(SearchPage(name='search_page'))        
        self.sm.add_widget(LearningMainPage(name='learn_page'))
        self.sm.add_widget(ListeningPage(name='listening_page'))
        self.sm.add_widget(SpeakingPage(name='speaking_page'))
        self.sm.add_widget(ReadingPage(name='reading_page'))
        self.sm.add_widget(WritingPage(name='writing_page'))
        self.sm.add_widget(FilePage(name='file_page'))
        return self.sm
    
    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key in [27,1001]:
            if self.sm.current == "listening_page":
                self.sm.get_screen("listening_page").lbp.SaveResults()
                self.sm.current = "learn_page"
            elif self.sm.current == "speaking_page":
                self.sm.get_screen("speaking_page").sbp.SaveResults()
                self.sm.current = "learn_page"
            elif self.sm.current == "reading_page":
                self.sm.get_screen("reading_page").rbp.SaveResults()
                self.sm.current = "learn_page"
            elif self.sm.current == "writing_page":
                self.sm.get_screen("writing_page").wbp.SaveResults()
                self.sm.current = "learn_page"            
            else:#dictionary and file page
                self.sm.current = "menu"
            return True

if __name__ == '__main__':
    TestApp().run()