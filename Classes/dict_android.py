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
import re
from pandas import *
import pandas as pd

from jisho_api.word import Word
from jisho_api.sentence import Sentence
import os

OPERATING_SYSTEM = os.name
WINDOWS_KEY = "nt"
ANDROID_KEY = "posix"

if OPERATING_SYSTEM == ANDROID_KEY:
    from android.storage import app_storage_path
    app_storage_directory_path = app_storage_path()
    USER_FILENAME =  app_storage_directory_path+"/User_Loaded.txt"
else:
    USER_FILENAME = "../User_Loaded.txt"

KANJI_HEADER = "Kanji"
R_HEADER = "Reading"
ENGLISH_HEADER = "English"
K_SENTENCE_HEADER = "Japanese Example"
JP_SENTENCE_HEADER = "Example Reading"
ENG_SENTENCE_HEADER = "English Sentence"
L_SCORE_HEADER = "listening score"
S_SCORE_HEADER = "speaking score"
R_SCORE_HEADER = "reading score"
W_SCORE_HEADER = "writing score"


class AddButton(Button):
    def __init__(self, Entry, **kwargs):
        super(AddButton, self).__init__(**kwargs)
        self.entry = Entry
        self.text = "Make Flashcard"

class SearchResult(BoxLayout):
    entry = DictProperty()
    on_press = ObjectProperty()

    def on_entry(self, instance, new_obj):
        # handle the DictProperty named show
        #print(new_obj)
        for ch in self.children:
            if isinstance(ch, BoxLayout):
                # remove any previous obj instances
                self.remove_widget(ch)
                break
        if True:
            self.clear_widgets()
            self.added = False
            #print("resetting")
        j = 1
        if not self.added:
            self.entry = new_obj
            if(self.entry["is_common"]):
                self.myColor = (1,0,1,1)
            else:
                self.myColor = (0,0,1,1)
            
            i = 0
            #print(self.on_press)
            jbox = BoxLayout(orientation = "vertical", size_hint_x = 2)
            ebox = BoxLayout(orientation = "vertical", size_hint_x = 2)  
            button = Button(on_press = self.on_press, text = "Make Flashcard")  
           # print("cat")

            for eachForm in dict(self.entry)["japanese"]:
                self.japanese = eachForm["word"]
                # print(self.japanese)
                self.reading = eachForm["reading"]
                #print(self.reading)
                if self.japanese == None:
                    self.japanese = " "
                if self.reading == None:
                    self.reading = " "
                label = Label(text = self.japanese + "「" + self.reading + "」", font_name = "DroidSansJapanese", color = self.myColor)
                label.bind(size=label.setter('text_size'))    
                jbox.add_widget(label)
                self.english = " "
                if i < len(dict(self.entry)["senses"]):
                    eachEng =  dict(self.entry)["senses"][i]
                    for eachDef in eachEng["english_definitions"]:
                        self.english = self.english + "," + eachDef
                    elabel = Label(text = self.english[1:])
                    elabel.bind(size=elabel.setter('text_size'))    
                    ebox.add_widget(elabel)
                i = i + 1
                j = j + 1
            self.add_widget(jbox)         
            self.add_widget(ebox)
            self.add_widget(button)
            #print("added")
            self.added = True
            self.height = self.minimum_height*(j)
        else:
            print("skipped")
        

    def __init__(self, **kwargs):
        super(SearchResult, self).__init__(**kwargs)   
        if self.entry != None and self.entry != {}:
            self.japanese = dict(self.entry)["japanese"][0]["word"]
            self.reading = dict(self.entry)["japanese"][0]["reading"]
            self.add_widget(Label(text = self.japanese, font_name = "DroidSansJapanese"))
            self.add_widget(Label(text = self.reading, font_name = "DroidSansJapanese"))
            print("****************")
        else:
            print("-")
            self.added = False
        self.orientation = "horizontal"
        self.height = self.minimum_height
        self.size_hint_x = 1
        

Builder.load_string('''
<ResultsView>:
    viewclass: 'SearchResult'
    size_hint_x: 1
    spacing: 40
    space_x: self.size[0]
    RecycleBoxLayout:
        default_size: None, dp(150)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height 
        orientation: 'vertical'
        outline_width: 10
        outline_colour: (0, 1, 0, 0)
<BoxLayout>        
    canvas.before:
        Color:
            rgba: 0, 1, 0, 0.5
        Line:    # --- adds a border --- #
            width: 1
            rectangle: self.x, self.y, self.width, self.height
''')

class ResultsView(RecycleView):
    entry = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.orientation = "vertical"

    def update_data(self, newData):
        self.data = []
        self.refresh_from_data()
        self.data = newData
        self.refresh_from_data()

        #print("cat")

class SearchBoxPage(BoxLayout):
    eachEntry = DictProperty()
    current = ObjectProperty()

    def makeFlashCard(self, entry, instance):
        i = 0
        new_lines = pd.DataFrame({KANJI_HEADER: [],
                                R_HEADER: [],
                                ENGLISH_HEADER: [],
                                K_SENTENCE_HEADER: [],
                                JP_SENTENCE_HEADER: [],
                                ENG_SENTENCE_HEADER: [],
                                L_SCORE_HEADER: [],
                                S_SCORE_HEADER: [],
                                R_SCORE_HEADER: [],
                                W_SCORE_HEADER: []}
        )
        for eachForm in dict(entry)["japanese"]:
            current_dict = pd.DataFrame(columns=[L_SCORE_HEADER,S_SCORE_HEADER,R_SCORE_HEADER,W_SCORE_HEADER],data=[[1,1,1,1]])
            if eachForm["reading"] == None:
                current_dict[R_HEADER] = " "
            else:
                current_dict[R_HEADER] = eachForm["reading"]
            if eachForm["word"] == None:
                current_dict[KANJI_HEADER] = " "
                current_dict[ENG_SENTENCE_HEADER] = " "
                current_dict[JP_SENTENCE_HEADER] = " "
                current_dict[K_SENTENCE_HEADER] = " "
            else:
                current_dict[KANJI_HEADER] = eachForm["word"]
                sent_entry = Sentence.request(eachForm["word"])
                if sent_entry == None:
                    print("no sentences found")
                    current_dict[ENG_SENTENCE_HEADER] = " "
                    current_dict[JP_SENTENCE_HEADER] = " "
                    current_dict[K_SENTENCE_HEADER] = " " 
                elif len(sent_entry)>0:
                    sent_entry = sent_entry.dict()["data"]
                    current_dict[ENG_SENTENCE_HEADER] = sent_entry[0]["en_translation"]
                    #Remove Kanji and leave blanks as furigana are weird sometimes
                    
                    x = re.sub("[\u3300-\u33ff]","_",sent_entry[0]["japanese"])
                    x = re.sub("[\ufe30-\ufe4f]","_",x)
                    x = re.sub("[\uf900-\ufaff]","_",x)
                    x = re.sub("[\U0002F800-\U0002fa1f]","_",x)
                    x = re.sub("[\u4e00-\u9fff]","_",x)
                    x = re.sub("[\u3400-\u4dbf]","_",x)
                    x = re.sub("[\U00020000-\U0002a6df]","_",x)
                    x = re.sub("[\U0002a700-\U0002b73f]","_",x)
                    x = re.sub("[\U0002b740-\U0002b81f]","_",x)
                    x = re.sub("[\U0002b820-\U0002ceaf]","_",x)
                    current_dict[JP_SENTENCE_HEADER] = x
                    #Remove Hiragana in parenthesis for kanji sentence
                    y = re.sub("\\([\u3040-\u309f]\\)","",sent_entry[0]["japanese"])
                 
                    #Remove Katakana in parenthesis
                    current_dict[K_SENTENCE_HEADER] = re.sub("\\([\u30a0-\u30ff]*\\)","",y)
                else:
                    print("0 sentences found")
                    current_dict[ENG_SENTENCE_HEADER] = " "
                    current_dict[JP_SENTENCE_HEADER] = " "
                    current_dict[K_SENTENCE_HEADER] = " "
            eng = ""
            if i < len(dict(entry)["senses"]):
                eachEng =  dict(entry)["senses"][i]
                for eachDef in eachEng["english_definitions"]:
                    eng = eng + "," + eachDef
                current_dict[ENGLISH_HEADER] = eng[1:]
            else:
                print("not enough definitions for this form")
            
            new_lines = pd.concat([new_lines, current_dict])
            i = i + 1

        #print(new_lines)
        new_lines.to_csv(USER_FILENAME, mode='a', header = False,sep ="\t", encoding="UTF-16",index=False)

    def search(self, instance):
        #print(instance)
        response = Word.request(self.searchBox.text)
        new_data = []
        if response != None:
            answer =  response.dict()["data"]
           
            for eachEntry in answer:
                self.eachEntry = eachEntry
                current = partial(self.makeFlashCard,self.eachEntry)
                new_data.append({"on_press": current,"entry": self.eachEntry, })
              #  print(type(self.eachEntry))
            
        print("cow")
        self.resultsBox.update_data(new_data)
        self.resultsBox.refresh_from_data()

    def build(self):
        self.name = "search_page"
        self.orientation = "vertical"
        self.searchbar = BoxLayout(orientation = "horizontal", size_hint_y = 0.5)
        self.searchBox = TextInput(font_name = "TakaoMincho",keyboard_suggestions=True,write_tab=False)
        self.resultsBox = ResultsView()
        self.mySearchBtn = Button(text = "Search", on_press = partial(self.search), size_hint_x = 0.2, background_color = (1,0,1,1))
        self.searchbar.add_widget(self.searchBox)
        self.searchbar.add_widget(self.mySearchBtn)
       # self.mybox.add_widget(SearchResult(Word.request("cow").dict()["data"][0])) #test
        self.add_widget(self.searchbar)
        self.add_widget(self.resultsBox)

if __name__ == "__main__":
    myHomePage = Main()
    myHomePage.run()
        