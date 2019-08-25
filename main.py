import csv
import random
import sqlite3
from plyer import notification, facades
from utils import database, scalelabel, scrollablelabel
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.effects import kinetic, scroll
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import _cached_views, _view_base_cache
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.loader import Loader

Loader.loading_image = 'images/trikru_flag.png'

dgrey = (45/255, 45/255, 45/255, 1)
red = (155/255, 10/255, 10/255, 1)
white = (1,1,1,1)
black = (0,0,0,1)

obj_text_list = []

current_word = "test"

def reset_dbs(self):

    def create_database(csv_file, database, execute_create, execute_insert):
        f = open(csv_file,'r', encoding='utf-8', errors= 'ignore')
        next(f, None)
        reader = csv.reader(f)

        sql = sqlite3.connect(database)
        cursor = sql.cursor()
        cursor.execute(execute_create)

        for row in reader:
            cursor.execute(execute_insert, row)

        f.close()
        sql.commit()
        sql.close()

    def delete_database_all(database):
        sql = sqlite3.connect(database)
        cursor = sql.cursor()
        cursor.execute("DROP TABLE Word_table")

    def delete_database_unread(database):
        sql = sqlite3.connect(database)
        cursor = sql.cursor()
        cursor.execute("DROP TABLE Word_table")

    def delete_database_read(database):
        sql = sqlite3.connect(database)
        cursor = sql.cursor()
        cursor.execute("DROP TABLE Word_table")

    delete_database_all('words_all.db')
    delete_database_unread('words_unread.db')
    delete_database_read('words_read.db')

    create_database('words.csv', 'words_all.db', '''CREATE TABLE IF NOT EXISTS Word_table 
    (Word, Pronunciation, English, Read)''', "INSERT INTO Word_table VALUES (?,?,?,0)")

    create_database('words.csv', 'words_unread.db', '''CREATE TABLE IF NOT EXISTS Word_table 
    (Word, Pronunciation, English, Read)''', "INSERT INTO Word_table VALUES (?,?,?,0)")

    create_database('words_read.csv', 'words_read.db', '''CREATE TABLE IF NOT EXISTS Word_table
    (Word, Pronunciation, English, Read)''', "INSERT INTO Word_table VALUES (?,?,?,0)")

def add_to_faves(self):
    con = sqlite3.connect('words_favorites.db')
    cursor = con.cursor()
    global current_word
    try:
        w = obj_text_list[0]
        current_word = obj_text_list[0]
        cursor.execute("SELECT Word from Word_table WHERE Word=?", (w,))
        entry = cursor.fetchone()

        if w in str(entry):
            pass
        else:
            database.add_word('words_favorites.db', obj_text_list[0], obj_text_list[1], obj_text_list[2], Read=1)

    except IndexError:
        pass

    obj_text_list.clear()

class MessageBox(Popup):
    global obj_text_list
    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):

        super(MessageBox, self).__init__(**kwargs)
        self.obj = obj

        # set the Popup text to the pronunciation and translation
        # from the unread_dict
        word_data = kv.get_screen('unread').unread_dict[obj.text]
        self.obj_text = word_data[0] + word_data[1] + '\n\n' + word_data[2]

        obj_text_list.extend([word_data[0], word_data[1], word_data[2]])

    def add_to_favorites(self):
        add_to_faves(self)

    def clear(self):
        obj_text_list.clear()

class MessageBoxRead(Popup):

    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):
        global obj_text_list
        super(MessageBoxRead, self).__init__(**kwargs)
        self.obj = obj

        # set the Popup text to the pronunciation and translation
        # from the unread_dict
        word_data = kv.get_screen('read').read_dict[obj.text]
        self.obj_text = word_data[0] +  word_data[1] + '\n\n' + word_data[2]

        obj_text_list.extend([word_data[0], word_data[1], word_data[2]])

    def add_to_favorites(self):
        add_to_faves(self)

    def clear(self):
        obj_text_list.clear()

class MessageBoxFavorites(Popup):
    favorite_list = []
    current_favorite = ''
    def popup_dismiss(self):
        self.dismiss()

    obj = ObjectProperty(None)
    obj_text = StringProperty('')

    def __init__(self, obj, **kwargs):

        super(MessageBoxFavorites, self).__init__(**kwargs)
        self.obj = obj

        word_data = kv.get_screen('favorites').favorites_dict[obj.text]
        self.obj_text = word_data[0] + word_data[1] + '\n\n' + word_data[2]
        self.favorite_list.extend([word_data[0], word_data[1], word_data[2]])

    def remove_from_favorites(self):

        con = sqlite3.connect('words_favorites.db')
        cursor = con.cursor()

        try:
            w = self.favorite_list[0]
            self.current_favorite = self.favorite_list[0]
            cursor.execute("SELECT Word from Word_table WHERE Word=?", (w,))
            entry = cursor.fetchone()
            database.remove_word('words_favorites.db', w)

        except IndexError:
            pass

    def clear(self):
        self.favorite_list.clear()

class MessageBoxFinished(Popup):
    def popup_dismiss(self):
        self.dismiss()
    def reset_databases(self):
        reset_dbs(self)

class MessageBoxConfirmation(Popup):
    def popup_dismiss(self):
        self.dismiss()
    def reset_databases(self):
        reset_dbs(self)

class MessageBoxFavoritesConfirmation(Popup):
    def popup_dismiss(self):
        self.dismiss()
    def reset_favorites(self):
        Favorites.reset_favorites(self)

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """

class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def update_changes(self, txt):
        self.text = txt

class SelectableButtonUnread(SelectableButton):
    def on_press(self):
        popup = MessageBox(self)
        popup.open()

class SelectableButtonRead(SelectableButton):
    def on_press(self):
        popup = MessageBoxRead(self)
        popup.open()

class SelectableButtonFavorites(SelectableButton):
    def on_press(self):
        popup = MessageBoxFavorites(self)
        popup.open()

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

class WindowManager(ScreenManager):
    pass

class WordADay(Screen):
    word_a_day = []
    word_dict = {}

    get = ObjectProperty(None)
    translation = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WordADay, self).__init__(**kwargs)
        self.unread_dict = {}

    def random_word(self):
        con = sqlite3.connect('words_unread.db')
        cursor = con.cursor()
        cursor.execute("SELECT * from Word_table")
        rowcount = len(cursor.fetchall())

        def get_words(database):
            count = -1
            for word in database:

                count += 1

                entry = {
                    count : {
                        'Word': word[0],
                        'Pronunciation': word[1],
                        'English': word[2],
                        'Read': word[3]
                }
                }

                self.word_dict.update(entry)

        def get_random_word():
            self.word_a_day.clear()
            #get words from the unread table and add them to word_dict using function "get_words"
            get_words(database.access_word_table('words_unread.db'))

            #get a row from word_dict

            try:
                #get a row from word_dict
                random_w = random.choice(self.word_dict)

                #random_w is the entire dictionary entry - I need to access just the 'Word' portion
                word = (str(random_w['Word']))
                pro = (str(random_w['Pronunciation']))
                eng =  (str(random_w['English']))

                text_result = (f'{str(word)}{str(pro)}\n\n{str(eng)}')
                self.word_a_day.extend([word, pro, eng])

                self.translation.text = text_result

                #mark as read in the all table
                database.mark_as_read('words_all.db', str(random_w['Word']))

                #remove fetched word from the unread table
                database.remove_word('words_unread.db', str(random_w['Word']))

                #add fetched word to the read table
                database.add_word('words_read.db', random_w['Word'], random_w['Pronunciation'], random_w['English'], Read=1)

                self.word_dict.clear()


            except KeyError:
                print("key error")

        if rowcount == 0:
            popup = MessageBoxFinished()
            popup.open()

        elif rowcount >= 1:
            get_random_word()

    def add_to_favorites(self):
        con = sqlite3.connect('words_favorites.db')
        cursor = con.cursor()

        try:
            w = self.word_a_day[0]
            cursor.execute("SELECT Word from Word_table WHERE Word=?", (w,))
            entry = cursor.fetchone()

            if w in str(entry):
                pass
            else:
                database.add_word('words_favorites.db', self.word_a_day[0], self.word_a_day[1], self.word_a_day[2], Read=1)

        except IndexError:
            print(IndexError)

    obj_text_list.clear()

class UnreadWords(Screen):

    unread_dict = {}

    unread_table = ObjectProperty(None)
    reset = ObjectProperty(None)
    rows = ListProperty([("Word", "Pronunciation", "English")])

    def __init__(self, **kwargs):
        super(UnreadWords, self).__init__(**kwargs)
        self.unread_dict = {}

    def display_database(self):
        con = sqlite3.connect('words_unread.db')
        cursor = con.cursor()
        cursor.execute("SELECT Word, Pronunciation, English from Word_table")
        self.rows = cursor.fetchall()
        self.unread_dict.clear()
        ReadWords.read_dict.clear()
        Favorites.favorites_dict.clear()

        for row in self.rows:
            self.unread_dict[row[0]] = [row[0], row[1], row[2]]

        self.ids.dat.data = [{'text': key} for key in self.unread_dict.keys()]

    def confirmation_popup(self):
        popup = MessageBoxConfirmation()
        popup.open()

class ReadWords(Screen):

    read_dict = {}

    read_table = ObjectProperty(None)
    reset = ObjectProperty(None)
    rows = ListProperty([("Word", "Pronunciation", "English")])

    def __init__(self, **kwargs):
        super(ReadWords, self).__init__(**kwargs)
        self.read_dict = {}

    def display_database(self):
        con = sqlite3.connect('words_read.db')
        cursor = con.cursor()
        cursor.execute("SELECT Word, Pronunciation, English from Word_table")
        self.rows = cursor.fetchall()
        self.read_dict.clear()
        UnreadWords.unread_dict.clear()
        Favorites.favorites_dict.clear()

        for row in self.rows:
            self.read_dict[row[0]] = [row[0], row[1], row[2]]

        self.ids.dat.data = [{'text': key} for key in self.read_dict.keys()]

    def confirmation_popup(self):
        popup = MessageBoxConfirmation()
        popup.open()

class Favorites(Screen):

    favorites_dict = {}

    favorites_table = ObjectProperty(None)
    reset = ObjectProperty(None)
    rows = ListProperty([("Word", "Pronunciation", "English")])

    def __init__(self, **kwargs):
        super(Favorites, self).__init__(**kwargs)
        self.favorites_dict = {}

    def display_database(self):
        con = sqlite3.connect('words_favorites.db')
        cursor = con.cursor()
        cursor.execute("SELECT Word, Pronunciation, English from Word_table")
        self.rows = cursor.fetchall()
        self.favorites_dict.clear()
        UnreadWords.unread_dict.clear()
        ReadWords.read_dict.clear()

        for row in self.rows:
            self.favorites_dict[row[0]] = [row[0], row[1], row[2]]

        self.ids.dat.data = [{'text': key} for key in self.favorites_dict.keys()]

    def reset_favorites(database):

        def delete_favorites(database):
            sql = sqlite3.connect(database)
            cursor = sql.cursor()
            cursor.execute("DROP TABLE Word_table")

        def create_favorites(csv_file, database, execute_create, execute_insert):
            f = open(csv_file,'r')
            next(f, None)
            reader = csv.reader(f)

            sql = sqlite3.connect(database)
            cursor = sql.cursor()
            cursor.execute(execute_create)

            for row in reader:
                cursor.execute(execute_insert, row)

            f.close()
            sql.commit()
            sql.close()

        delete_favorites("words_favorites.db")

        create_favorites('words_favorites.csv', 'words_favorites.db', '''CREATE TABLE IF NOT EXISTS Word_table 
        (Word, Pronunciation, English, Read)''', "INSERT INTO Word_table VALUES (?,?,?,0)")

    def confirmation_popup(self):
        popup = MessageBoxFavoritesConfirmation()
        popup.open()

class Pronunciation(Screen):
    pass

kv = Builder.load_file("layout.kv")

class WordApp(App):
    def build(self):
        return kv

    def on_start(self):

        self.root.get_screen('unread').display_database()
        self.root.get_screen('read').display_database()
        self.root.get_screen('favorites').display_database()

        #to set current page at start use: self.root.current = ('word')

if __name__=="__main__":
    WordApp().run()

    #TODO Notifications - Plyer


    #TODO Add Search
    #TODO Dynamically Refine Search
    #TODO Make it easier to scroll through list (a-z selection?) goto_node(key, last_node, last_node_idx)
    #https://kivy.org/doc/stable/api-kivy.uix.recycleview.layout.html
    #see scroll effect
    #TODO Figure out why the scrolling db in recycleview can be pushed further down and fix it
    #TODO Word a Day Android Widget
    #TODO add random Mando phrases to the loading page
    #TODO add color options

    # Reminder: since there is no pronunciation in entries in this app, I have kept the code for pronunciations but removed
    # the extra new lines and added in a blank space in the csv where it would have gone.  This is so I still have an
    # intact template for other languages with a pronunciation guide







    