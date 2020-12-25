import sqlite3
from random import sample, randint
from string import ascii_lowercase


from kivy.app import App
#from kivy.adapters.listadapter import ListAdapter
from kivy.uix.recycleview.views import RecycleDataAdapter


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.uix.listview import SelectableView
from kivy.uix.recycleview import RecycleView

#from kivy.adapters.models import SelectableDataItem
from kivy.properties import ListProperty, StringProperty
import pandas as pd


def read_cocktail_recipes(database_name="cocktails.db"):
    '''Read the recipes from the database
    '''
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    #t = ('Attaboy',)
    #cur.execute('SELECT * FROM Recipes WHERE RecipeName=?', t)
    #print cur.fetchone()

    #cur.execute('SELECT * FROM Recipes ORDER BY RecipeName')
    #l_cocktail_recipes = cur.fetchall()
    df_cocktail_recipes = pd.read_sql_query("SELECT * FROM Recipes ORDER BY RecipeName", conn)

    conn.close()

    #print (l_cocktail_recipes)
    print (df_cocktail_recipes)
    return df_cocktail_recipes

class CocktailsScreen(Screen):

    def populate(self):
        df = read_cocktail_recipes()
#        self.rv.data = df.set_index('RecipeID').T.to_dict('records')
        thislist = [
            {'name.text': ''.join(sample(ascii_lowercase, 6)),
             'value': str(randint(0, 2000))}
            for x in range(50)]

        thislist = [{'name.text': df.iloc[x].RecipeName,
                     'value': str(df.iloc[x].RecipeID)
                     }
                    for x in range(len(df))]


        self.rv.data = thislist

    def sort(self):
        self.rv.data = sorted(self.rv.data, key=lambda x: x['name.text'])

    def clear(self):
        self.rv.data = []

    def insert(self, value):
        self.rv.data.insert(0, {
            'name.text': value or 'default value', 'value': 'unknown'})

    def update(self, value):
        if self.rv.data:
            self.rv.data[0]['name.text'] = value or 'default new value'
            self.rv.refresh_from_data()

    def remove(self):
        if self.rv.data:
            self.rv.data.pop(0)

class MainScreen(Screen):
    pass

class CocktailsScreenOrig(Screen):
    '''Implementation of a simple list view with 100 items.
    '''
    my_list=read_cocktail_recipes()
    print (my_list)
    my_string = [ ''.join(item[1]) for item in my_list ]
    print (my_string)

    my_data = ListProperty(my_string)
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
print (cocktail_recipes)

if __name__ == '__main__':
    CocktailsApp().run()
