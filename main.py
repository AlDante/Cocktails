import pprint
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
from tabulate import tabulate

"""
    # kv rules are not applied until the original Widget has finished instantiating. 
    # This means that ids are only populated when the Manager has finished instantiating.
    # The following is a solution
    # https://stackoverflow.com/questions/26916262/why-cant-i-access-the-screen-ids
    class RootWidget(Screen):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.grid = self.ids.grid
        # etc
"""


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

        # Get cocktails list data
        rv_grandparent = rv.parent.parent

        for key, value in rv_grandparent.ids.selectable_cocktails_list.data[index].items():
            print(key, value)

        my_string = 'Gin: {Gin}\n' \
                    + 'Dark rum: {DarkRum}\n' \
                    + 'Dry Vermouth: {DryVermouth}\n' \
                    + 'Cointreau: {Cointreau}\n' \
                    + 'Zitronensaft: {Zitronensaft}\n' \
                    + 'Ananassaft: {Ananassaft}\n' \
                    + 'Glas: {Glas}\n' \
                    + 'Mixen: {Mixen}\n' \
                    + 'To finish: {ToFinish}\n' \
                    + 'Deko: {Deko}\n' \
                    + 'Geschmack: {Geschmack}\n' \
                    + 'Typ: {Typ}\n' \
                    + 'Gelegenheit: {Gelegenheit}\n' \
                    + 'Seite: {Seite}\n' \
                    + 'Anpassungen: {Anpassungen}\n'

        my_text = my_string.format(
            Gin=rv_grandparent.ids.selectable_cocktails_list.data[index]["Gin"],
            DarkRum=rv_grandparent.ids.selectable_cocktails_list.data[index]["DarkRum"],
            DryVermouth=rv_grandparent.ids.selectable_cocktails_list.data[index]["DryVermouth"],
            Cointreau=rv_grandparent.ids.selectable_cocktails_list.data[index]["Cointreau"],
            Zitronensaft=rv_grandparent.ids.selectable_cocktails_list.data[index]["Zitronensaft"],
            Ananassaft=rv_grandparent.ids.selectable_cocktails_list.data[index]["Ananassaft"],
            Glas=rv_grandparent.ids.selectable_cocktails_list.data[index]["Glas"],
            Mixen=rv_grandparent.ids.selectable_cocktails_list.data[index]["Mixen"],
            ToFinish=rv_grandparent.ids.selectable_cocktails_list.data[index]["ToFinish"],
            Deko=rv_grandparent.ids.selectable_cocktails_list.data[index]["Deko"],
            Geschmack=rv_grandparent.ids.selectable_cocktails_list.data[index]["Geschmack"],
            Typ=rv_grandparent.ids.selectable_cocktails_list.data[index]["Typ"],
            Gelegenheit=rv_grandparent.ids.selectable_cocktails_list.data[index]["Gelegenheit"],
            Seite=rv_grandparent.ids.selectable_cocktails_list.data[index]["Seite"],
            Anpassungen=rv_grandparent.ids.selectable_cocktails_list.data[index]["Anpassungen"]
        )

        # Update details window
        for child in rv.parent.children:
            if (isinstance(child, Label)):
                print(child.text)
                child.text = my_text


class CocktailsList(BoxLayout):
    selectable_cocktails = ObjectProperty()


class CocktailsScreen(Screen):
    alcohol: str = None
    flavour: str = None
    cocktailtype: str = None

    def on_pre_enter(self, *args):
        """
        Populate the list of cocktails in the child widget
        :param args:
        :return:
        """
        print("Screen pre-enter")

        my_app = App.get_running_app()

        for child in self.children:
            if 'selectable_cocktails_list' in child.ids:
                # The conditional at the end checks if the cocktail contains gin (is not empty).
                child.selectable_cocktails.data = [{'text': x['RecipeName'],
                                                    'Gin': x['Gin'],
                                                    'DarkRum': x['DarkRum'],
                                                    'DryVermouth': x['DryVermouth'],
                                                    'Cointreau': x['Cointreau'],
                                                    'Zitronensaft': x['Zitronensaft'],
                                                    'Ananassaft': x['Ananassaft'],
                                                    'Glas': x['Glas'],
                                                    'Mixen': x['Mixen'],
                                                    'ToFinish': x['ToFinish'],
                                                    'Deko': x['Deko'],
                                                    'Geschmack': x['Geschmack'],
                                                    'Typ': x['Typ'],
                                                    'Gelegenheit': x['Gelegenheit'],
                                                    'Seite': x['Seite'],
                                                    'Anpassungen': x['Anpassungen']

                                                    } for x in my_app.cocktails_list \
                                                   if ((self.alcohol and x[self.alcohol].strip()) or \
                                                       (self.flavour and self.flavour in x['Geschmack']) or \
                                                       (self.cocktailtype and self.cocktailtype == x['Typ'].strip()))]
                break


class HerbScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(HerbScreen, self).__init__(**kwargs)
        self.flavour = 'herb'


class WuerzigScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(WuerzigScreen, self).__init__(**kwargs)
        self.flavour = 'würzig'


class TrockenScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(TrockenScreen, self).__init__(**kwargs)
        self.flavour = 'trocken'


class FruchtScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(FruchtScreen, self).__init__(**kwargs)
        self.flavour = 'früchtig'


class FrischScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(FrischScreen, self).__init__(**kwargs)
        self.flavour = 'frisch'


class LieblichScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(LieblichScreen, self).__init__(**kwargs)
        self.flavour = 'lieblich'


class FizzScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(FizzScreen, self).__init__(**kwargs)
        self.cocktailtype = 'Fizz'

class FlipScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(FlipScreen, self).__init__(**kwargs)
        self.cocktailtype = 'Flip'

class LongdrinkScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(LongdrinkScreen, self).__init__(**kwargs)
        self.cocktailtype = 'Longdrink'


class ShortdrinkScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(ShortdrinkScreen, self).__init__(**kwargs)
        self.cocktailtype = 'Shortdrink'


class SektScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(SektScreen, self).__init__(**kwargs)
        self.cocktailtype = 'Sektcocktail'


class SourScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(SourScreen, self).__init__(**kwargs)
        self.cocktailtype = 'Sour'


class GinScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(GinScreen, self).__init__(**kwargs)
        self.alcohol = 'Gin'


class RumScreen(CocktailsScreen):
    def __init__(self, **kwargs):
        super(RumScreen, self).__init__(**kwargs)
        self.alcohol = 'DarkRum'


class MainScreen(Screen):
    pass


class FlavourScreen(Screen):
    pass


class TypeScreen(Screen):
    pass


class MyManager(ScreenManager):
    pass


class CocktailsApp(App):
    cocktails_list = ObjectProperty()

    def build(self):
        self.init_cocktails()
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

    def init_cocktails(self):
        df = self.read_cocktail_recipes()

        # Data needs to be a list of dictionaries
        thislist = [{'RecipeName': df.iloc[x].RecipeName,
                     'RecipeID': str(df.iloc[x].RecipeID),
                     'Gin': str(df.iloc[x].Gin),
                     'DarkRum': str(df.iloc[x].DarkRum),
                     'DryVermouth': str(df.iloc[x].DryVermouth),
                     'Cointreau': str(df.iloc[x].Cointreau),
                     'Zitronensaft': str(df.iloc[x].Zitronensaft),
                     'Ananassaft': str(df.iloc[x].Ananassaft),
                     'Glas': str(df.iloc[x].Glas),
                     'Mixen': str(df.iloc[x].Mixen),
                     'ToFinish': str(df.iloc[x].ToFinish),
                     'Deko': str(df.iloc[x].Deko),
                     'Geschmack': str(df.iloc[x].Geschmack),
                     'Typ': str(df.iloc[x].Typ),
                     'Gelegenheit': str(df.iloc[x].Gelegenheit),
                     'Seite': str(df.iloc[x].Seite),
                     'Anpassungen': str(df.iloc[x].Anpassungen)
                     }
                    for x in range(len(df))]

        self.cocktails_list = thislist

    def read_cocktail_recipes(self, database_name: str = "cocktails.db") -> pd.DataFrame:
        '''Read the recipes from the database
        :database_name: name of cocktails database. Must contain a table named Recipes and a column RecipeName
        :return: pd.DataFrame containing recipes ordered by recipe name
        '''
        conn = sqlite3.connect(database_name)

        df_cocktail_recipes = pd.read_sql_query("SELECT * FROM Recipes ORDER BY RecipeName", conn)

        conn.close()

        pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(df_cocktail_recipes)
        print(tabulate(df_cocktail_recipes, headers='keys', tablefmt='psql'))

        """
        RecipeID|RecipeName|Gin|DarkRum|DryVermouth|Cointreau|Zitronensaft|Ananassaft|Glas|Mixen|ToFinish|
        Deko|Geschmack|Typ|Gelegenheit|Seite|Anpassungen
        """

        return df_cocktail_recipes


if __name__ == '__main__':
    CocktailsApp().run()
