import sqlite3

import pandas as pd
from kivy.app import App
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
import pprint


# from kivy.adapters.listadapter import ListAdapter
# from kivy.uix.listview import SelectableView
# from kivy.adapters.models import SelectableDataItem


def read_cocktail_recipes(database_name="cocktails.db"):
    '''Read the recipes from the database
    '''
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    # t = ('Attaboy',)
    # cur.execute('SELECT * FROM Recipes WHERE RecipeName=?', t)
    # print cur.fetchone()

    # cur.execute('SELECT * FROM Recipes ORDER BY RecipeName')
    # l_cocktail_recipes = cur.fetchall()
    df_cocktail_recipes = pd.read_sql_query("SELECT * FROM Recipes ORDER BY RecipeName", conn)

    conn.close()

    # print (l_cocktail_recipes)
    print(df_cocktail_recipes)
    return df_cocktail_recipes


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class AddLocationForm(BoxLayout):
    selectable_cocktails = ObjectProperty()

class CocktailsScreen(Screen):
    cocktails_list = ObjectProperty()

    def on_pre_enter(self, *args):
        print("Screen pre-enter")
        self.populate()

        form = None
        for child in self.children:
            if 'selectable_cocktails_list' in child.ids:
                child.selectable_cocktails.data = [{'text': x['name.text']} for x in self.cocktails_list]
                break

    def populate(self):
        df = read_cocktail_recipes()

        # Data needs to be a list of dictionaries
        thislist = [{'name.text': df.iloc[x].RecipeName,
                     'value': str(df.iloc[x].RecipeID)
                     }
                    for x in range(len(df))]

        self.cocktails_list = thislist


class MainScreen(Screen):
    pass


class FlavourScreen(Screen):
    pass


class TypeScreen(Screen):
    pass


class MyManager(ScreenManager):
    pass


class CocktailsApp(App):
    def build(self):
        return MyManager()

    def gin_choice(self):
        # choose a gin cocktail - switch to select screen with gin filter
        print('Gin chosen')
        popup = Popup(title='Gin popup',
                      content=Label(text='Gin world'),
                      size_hint=(None, None), size=(400, 400))

    def rum_choice(self):
        # Choose a rum cocktail - switch to select screen with rum filter
        print('Rum chosen')

    def flavour_choice(self):
        # Choose by cocktail flavour - switch to flavour screen
        print('Flavour chosen')

    def type_choice(self):
        # Choose by cocktail type - switch to type screen
        print('Type chosen')

    def lucky_choice(self):
        # choose a random cocktail - remain on main screen
        print('Lucky choice')


cocktail_recipes = read_cocktail_recipes("cocktails.db")
print(cocktail_recipes)

if __name__ == '__main__':
    CocktailsApp().run()
