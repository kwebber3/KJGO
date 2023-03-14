from kivy.app import App
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

from jisho_api.word import Word

class AddButton(Button):
    def __init__(self, Entry, **kwargs):
        super(AddButton, self).__init__(**kwargs)
        self.entry = Entry
        self.text = "Make Flashcard"

    

class SearchResult(BoxLayout):
    entry = DictProperty()
    on_press = ObjectProperty()

    def add_card(self):
        print(self.entry)



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
                    self.japanese = ""
                if self.reading == None:
                    self.reading = ""
                label = Label(text = self.japanese + "「" + self.reading + "」", font_name = "DroidSansJapanese", color = self.myColor)
                label.bind(size=label.setter('text_size'))    
                jbox.add_widget(label)
                self.english = ""
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

class HomePage(Screen):
    eachEntry = DictProperty()
    current = ObjectProperty()

    def makeFlashCard(self, entry, instance):
        i = 0
        self.japanese = []
        self.reading = []
        self.english = []
        print(entry)
        for eachForm in dict(entry)["japanese"]:
            self.japanese.append(eachForm["word"])
            # print(self.japanese)
            self.reading.append(eachForm["reading"])
            #print(self.reading)
            if self.japanese == None:
                self.japanese = ""
            if self.reading == None:
                self.reading = ""
            self.eng = ""
            if i < len(dict(entry)["senses"]):
                eachEng =  dict(entry)["senses"][i]
                for eachDef in eachEng["english_definitions"]:
                    self.eng = self.eng + "," + eachDef
                self.english.append(self.eng[1:])
            i = i + 1

        print(self.english)
        print(self.japanese)
        print(self.reading)

    def search(self, instance):
        response = Word.request(self.searchBox.text)
        new_data = []
        if response != None:
            answer =  response.dict()["data"]
           
            for eachEntry in answer:
                self.eachEntry = eachEntry
                current = partial(self.makeFlashCard,self.eachEntry)
                new_data.append({"on_press": current,"entry": self.eachEntry, })
              #  print(type(self.eachEntry))
            
        self.resultsBox.update_data(new_data)
        self.resultsBox.refresh_from_data()

    def build(self):
        self.mybox = BoxLayout (orientation = "vertical")
        self.searchbar = BoxLayout(orientation = "horizontal", size_hint_y = 0.5)
        self.searchBox = TextInput()
        self.resultsBox = ResultsView()
        self.mySearchBtn = Button(text = "Search", on_press = partial(self.search), size_hint_x = 0.2, background_color = (1,0,1,1))
        self.searchbar.add_widget(self.searchBox)
        self.searchbar.add_widget(self.mySearchBtn)
       # self.mybox.add_widget(SearchResult(Word.request("cow").dict()["data"][0])) #test
        self.mybox.add_widget(self.searchbar)
        self.mybox.add_widget(self.resultsBox)
        return self.mybox

if __name__ == "__main__":
    myHomePage = HomePage()
    myHomePage.run()
        