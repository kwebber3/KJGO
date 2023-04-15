from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.lang import Builder
from functools import partial
from kivy.core.window import Window
import requests
import random
import re

from background_android import *

import os

OPERATING_SYSTEM = os.name
WINDOWS_KEY = "nt"
ANDROID_KEY = "posix"

if OPERATING_SYSTEM == ANDROID_KEY:
    from android.storage import app_storage_path
    app_storage_directory_path = app_storage_path()
    DICTIONARY_NAME =  app_storage_directory_path+"/User_Loaded.txt"
else:
    DICTIONARY_NAME = "../User_Loaded.txt"

JP_INDEX = 0
ENG_INDEX = 1
R_INDEX = 2
JP_SENT_INDEX = 3
R_EXP_INDEX = 4
ENG_SENT_INDEX = 5


class WritingBox(BoxLayout,):
    def build(self):
        self.my_scored_cards, self.score_weights, self.number_of_cards = load_writing_dictionary(DICTIONARY_NAME)      
        self.last_score = -1
        self.last_card = []
        self.orientation = "vertical"
        self.buttonBar = BoxLayout(orientation = "horizontal")
        self.show_button = Button(text="Show Example", on_release=partial(self.ShowExample))
        self.buttonBar.add_widget(self.show_button)

        self.answer_button = Button(text="Show Answer", on_release=partial(self.ShowAnswer))
        self.buttonBar.add_widget(self.answer_button)

        self.addButton = Button(text="Correct", on_release=partial(self.AddPoint))
        self.buttonBar.add_widget(self.addButton)

        self.subtractButton = Button(text="Wrong", on_release=partial(self.SubtractPoint))
        self.buttonBar.add_widget(self.subtractButton)

        
        self.add_widget(self.buttonBar)

        self.cardPrompt = Label(font_name = "TakaoMincho")
        self.add_widget(self.cardPrompt)
        self.example = Label(font_name = "TakaoMincho")
        self.add_widget(self.example)
        self.example.bind(size=self.example.setter('text_size'))    
        self.reading = Label(font_name = "TakaoMincho")
        self.add_widget(self.reading)
        self.answer = Label(font_name = "TakaoMincho")
        self.add_widget(self.answer)
        self.sentence_answer = Label(font_name = "TakaoMincho")
        self.add_widget(self.sentence_answer)
        self.sentence_answer.bind(size=self.sentence_answer.setter('text_size'))    

        self.trashcard_button = Button(text="Trash Word Card", on_release=partial(self.TrashCard))
        self.add_widget(self.trashcard_button)
        self.GetCard()
        
    def TrashCard(self, instance):
        #print(self.current_score)
        self.my_scored_cards[self.current_score].pop(self.index)
        self.trashcard_button.disabled = True
        self.GetCard()

    def __init__(self, **kw):
        super().__init__(**kw)
        Window.bind(on_request_close=self.end_func)

    def end_func(self, *args):
        self.SaveResults()
        #print("cow died")
        Window.close()
        return True


    def SaveResults(self):
        export_writingLibrary_to_txt(self.my_scored_cards,DICTIONARY_NAME)

    def GetCard(self):
        self.score_weights = update_weights(self.my_scored_cards, self.number_of_cards)
        self.current_score = random.choices(range(1,len(self.score_weights)+1),weights = self.score_weights)[0]
        self.current_score, self.current_card, status, self.index = get_card_writing(self.current_score,self.last_card,self.my_scored_cards, self.score_weights)
        self.saved = False
        
        if status == "GOOD":
            Japanese = '\n'.join(self.current_card[R_INDEX])
            self.cardPrompt.text = Japanese
            self.English = '\n'.join(self.current_card[ENG_INDEX])
            self.Japanese_Sentence = '\n'.join(self.current_card[R_EXP_INDEX])
            self.Kanji = '\n'.join(self.current_card[JP_INDEX])
            self.English_Example = '\n'.join(self.current_card[ENG_SENT_INDEX])
            self.Japanese_Sentence = re.sub("<[/]*b>","",self.Japanese_Sentence)
            self.Kanji_Sentence = '\n'.join(self.current_card[JP_SENT_INDEX])
            self.Kanji_Sentence = re.sub("<[/]*b>","",self.Kanji_Sentence)
            self.trashcard_button.disabled = False


        elif status == "ERROR":
            self.cardPrompt.text = "PRACTICE SPEAKING MORE"
            self.Japanese = ""
            self.English_Example = ""
            self.Japanese_Sentence = ""
            self.Kanji = ""
            self.Kanji_Sentence = ""
            self.addButton.disabled = True
            self.subtractButton.disabled = True
            self.trashcard_button.disabled = True

        else:
            self.cardPrompt.text = "Unknown Status"
            self.Japanese = ""
            self.English_Example = ""
            self.Japanese_Sentence = ""
            self.Kanji = ""
            self.Kanji_Sentence = ""
            self.addButton.disabled = True
            self.subtractButton.disabled = True

    def refresh(self):
        self.cardPrompt.text = ""
        self.answer.text = ""
        self.example.text = ""
        self.sentence_answer.text = ""
        self.reading.text = ""

    def ShowExample(self, instance):
        self.example.text = self.Japanese_Sentence

    def ShowAnswer(self, instance):
        self.reading.text = self.Kanji
        self.answer.text = self.English
        self.sentence_answer.text = self.English_Example

    def AddPoint(self, instance):
       # print(self.current_score)
        this_card = self.my_scored_cards[self.current_score].pop(self.index)
        if (self.current_score + 1 > MAX_SCORE):
            new_score = MAX_SCORE
        else:
            new_score = self.current_score + 1
        self.my_scored_cards[new_score].append(this_card)
        self.refresh()
        self.last_score = new_score
        self.last_card = this_card
        self.GetCard()
    
    def SubtractPoint(self, instance):
        #print(self.current_score)
        this_card = self.my_scored_cards[self.current_score].pop(self.index)
        if (self.current_score - 1 < START_SCORE):
            new_score = START_SCORE
        else:
            new_score = self.current_score - 1
        self.my_scored_cards[new_score].append(this_card)
        self.refresh()
        self.last_score = new_score
        self.last_card = this_card
        self.GetCard()
        #print(this_card)