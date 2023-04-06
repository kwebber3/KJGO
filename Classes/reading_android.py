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

DICTIONARY_NAME = "../User_Loaded.txt"

JP_INDEX = 0
ENG_INDEX = 1
R_INDEX = 2
JP_SENT_INDEX = 3
R_EXP_INDEX = 4
ENG_SENT_INDEX = 5


class ReadingBox(BoxLayout,):
    def build(self):
        self.my_scored_cards, self.score_weights, self.number_of_cards = load_reading_dictionary(DICTIONARY_NAME)      
        self.last_score = -1
        self.last_card = []
        self.orientation = "vertical"
        self.buttonBar = BoxLayout(orientation = "horizontal")
        self.show_button = Button(text="Show Example", on_press=partial(self.ShowExample))
        self.buttonBar.add_widget(self.show_button)

        self.answer_button = Button(text="Show Answer", on_press=partial(self.ShowAnswer))
        self.buttonBar.add_widget(self.answer_button)

        self.addButton = Button(text="Correct", on_press=partial(self.AddPoint))
        self.buttonBar.add_widget(self.addButton)

        self.subtractButton = Button(text="Wrong", on_press=partial(self.SubtractPoint))
        self.buttonBar.add_widget(self.subtractButton)

        
        self.add_widget(self.buttonBar)

        self.cardPrompt = Label(font_name = "TakaoMincho")
        self.add_widget(self.cardPrompt)
        self.example = Label(font_name = "TakaoMincho")
        self.example.bind(size=self.example.setter('text_size'))    
        self.add_widget(self.example)
        self.reading = Label(font_name = "TakaoMincho")
        self.add_widget(self.reading)
        self.answer = Label(font_name = "TakaoMincho")
        self.add_widget(self.answer)
        self.sentence_answer = Label(font_name = "TakaoMincho")
        self.add_widget(self.sentence_answer)
        self.sentence_answer.bind(size=self.sentence_answer.setter('text_size'))    

        

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
        export_readingLibrary_to_txt(self.my_scored_cards,DICTIONARY_NAME)

    def GetCard(self):
        self.score_weights = update_weights(self.my_scored_cards, self.number_of_cards)
        self.current_score = random.choices(range(1,len(self.score_weights)+1),weights = self.score_weights)[0]
        self.current_score, self.current_card, status, self.index = get_card_reading(self.current_score,self.last_card,self.my_scored_cards, self.score_weights)
        self.saved = False
        
        if status == "GOOD":
            #print(self.current_card)
            Japanese = '\n'.join(self.current_card[JP_INDEX])
            self.cardPrompt.text = Japanese
            self.English = '\n'.join(self.current_card[ENG_INDEX])
            self.Japanese_Sentence = '\n'.join(self.current_card[JP_SENT_INDEX])
            self.KanjiReadings = '\n'.join(self.current_card[R_INDEX])
            self.English_Example = '\n'.join(self.current_card[ENG_SENT_INDEX])
            self.Japanese_Sentence = re.sub("<[/]*b>","",self.Japanese_Sentence)
            self.Kanji_Example = '\n'.join(self.current_card[R_EXP_INDEX])
            self.Kanji_Example = re.sub("<[/]*b>","",self.Kanji_Example)


        elif status == "ERROR":
            self.cardPrompt.text = "PRACTICE SPEAKING MORE"
            self.Japanese = ""
            self.English_Example = ""
            self.Japanese_Sentence = ""
            self.KanjiReadings = ""
            self.Kanji_Example = ""
            self.addButton.disabled = True
            self.subtractButton.disabled = True
        else:
            self.cardPrompt.text = "Unknown Status"
            self.Japanese = ""
            self.English_Example = ""
            self.Japanese_Sentence = ""
            self.KanjiReadings = ""
            self.Kanji_Example = ""
            self.addButton.disabled = True
            self.subtractButton.disabled = True

    def refresh(self):
        self.cardPrompt.text = ""
        self.answer.text = ""
        self.example.text = ""
        self.sentence_answer.text = ""
        self.reading.text = ""

    def ShowExample(self, instance):
        self.example.text = self.Kanji_Example

    def ShowAnswer(self, instance):
        self.reading.text = self.KanjiReadings
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
        self.GetCard()
        #print(this_card)