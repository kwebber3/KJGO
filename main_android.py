from kivy.app import App
from kivy.properties import DictProperty
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.lang import Builder
from functools import partial

from jisho_api.word import Word

class SearchResult(BoxLayout):
    entry = DictProperty()
    
    def on_entry(self, instance, new_obj):
        # handle the DictProperty named show
        
        for ch in self.children:
            if isinstance(ch, BoxLayout):
                # remove any previous obj instances
                self.remove_widget(ch)
                break
        
        self.entry = new_obj
        self.japanese = dict(self.entry)["japanese"][0]["word"]
        print(self.japanese)
        self.reading = dict(self.entry)["japanese"][0]["reading"]
        print(self.reading)
        if self.japanese == None:
            self.japanese = self.reading
        self.orientation = "horizontal"
        self.add_widget(Label(text = self.japanese, font_name = "DroidSansJapanese"))
        self.add_widget(Label(text = self.reading, font_name = "DroidSansJapanese"))
        print("added")
    
    def __init__(self, **kwargs):
        super(SearchResult, self).__init__(**kwargs)   
        if self.entry != {}:
            self.japanese = dict(self.entry)["japanese"][0]["word"]
            self.reading = dict(self.entry)["japanese"][0]["reading"]
            self.add_widget(Label(text = self.japanese, font_name = "DroidSansJapanese"))
            self.add_widget(Label(text = self.reading, font_name = "DroidSansJapanese"))
        else:
            print("nothing")

Builder.load_string('''
<ResultsView>:
    viewclass: "SearchResult"
    RecycleBoxLayout:
        size_hint_y: None
        height: self.minimum_height
        orientation: "vertical"
    
''')

class ResultsView(RecycleView):
    entry = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def update_data(self, newData):
        self.data = newData
        print("cat")

class HomePage(App):
    eachEntry = DictProperty()

    def search(self, instance):
        answer =  Word.request(self.searchBox.text).dict()["data"]
        new_data = []
        for eachEntry in answer:
            self.eachEntry = eachEntry
            new_data.append({"entry": self.eachEntry})
            print(type(self.eachEntry))
        
        self.resultsBox.update_data(new_data)
        self.resultsBox.refresh_from_data()

    def build(self):
        self.mybox = BoxLayout (orientation = "vertical")
        self.searchbar = BoxLayout(orientation = "horizontal")
        self.searchBox = TextInput()
        self.resultsBox = ResultsView()
        self.mySearchBtn = Button(text = "Press me", on_press = partial(self.search))
        self.searchbar.add_widget(self.searchBox)
        self.searchbar.add_widget(self.mySearchBtn)
       # self.mybox.add_widget(SearchResult(Word.request("cow").dict()["data"][0])) #test
        self.mybox.add_widget(self.searchbar)
        self.mybox.add_widget(self.resultsBox)
        return self.mybox

if __name__ == "__main__":
    myHomePage = HomePage()
    myHomePage.run()
        