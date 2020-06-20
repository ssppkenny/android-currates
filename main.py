# import kivy module
import kivy
import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pandas.plotting import register_matplotlib_converters
from kivy.cache import Cache
from kivy.core.window import Window
import certifi, os

register_matplotlib_converters()
from kivy.app import App

kivy.require('1.9.0')
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from history_rates import FxtopRate

os.environ['SSL_CERT_FILE']=certifi.where()

class ImageScreen(GridLayout):
    def __init__(self, **kwargs):
        super(ImageScreen,self).__init__(**kwargs)
        self.image = Image(source="out.png")
        self.add_widget(self.image)

class Buttons(BoxLayout):
    def __init__(self, **kwargs):
        super(Buttons,self).__init__(**kwargs)
        self.label = Label(text='Currency rates', font_size='20sp', color=[105, 106, 188, 1])
        self.add_widget(self.label)
        self._from = 'CHF'
        self._to = 'RUB'
        self.years = 1
        self.dropdownFrom = DropDown()
        self.dropdownTo = DropDown()

        self.buttonFrom = self.createButton("From", self.dropdownFrom, True)
        self.buttonTo = self.createButton("To", self.dropdownTo, False)

        self.add_widget(self.buttonFrom)
        self.add_widget(self.buttonTo)

        self.yearsDropdown = DropDown()
        self.years = self.createYearsButton("Years", self.yearsDropdown)
        self.add_widget(self.years)

        btn = Button(text='Show',size_hint_y=None, size_hint_x=None, height=40)
        btn.bind(on_release=lambda btn: self.on_release(btn))
        self.add_widget(btn)


    def get_from(self):
        return self._from

    def get_to(self):
        return self._to

    def on_release(self, btn):
        _from = self.get_from()
        _to = self.get_to()
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        self.parent.image_screen.image.texture = self.get_texture()
        ##self.image.reload()

    def create_figure(self, date_str, from_cur, to_cur, years):
        fxtop = FxtopRate(date_str, from_cur, to_cur, years)
        fig = fxtop.plot()
        return fig

    def set_button_text(self, button, x):
        button.text = x

    def dropdown_select(self, btn, dropdown):
        text = btn.text
        dropdown.select(btn.text)
        self.years = int(text)

    def dropdown_to_select(self, btn, dropdown):
        text = btn.text
        dropdown.select(btn.text)
        self._to = text

    def dropdown_from_select(self, btn, dropdown):
        text = btn.text
        dropdown.select(btn.text)
        self._from = text

    def dropdown_on_release(self, button, dropdown):
        ##print(button.text)
        dropdown.open(button)

    def get_texture(self):
        today = datetime.date.today()
        now = today.strftime("%Y%m%d")
        fig = self.create_figure(now, self._from, self._to, self.years)
        output = BytesIO()
        FigureCanvas(fig).print_png(output)

        # self.buttonFrom.bind(on_release = lambda btn: ddh.select(btn))

        with open("out.png", "wb") as outfile:
            outfile.write(output.getbuffer())
            return CoreImage.load("out.png").texture


    def createYearsButton(self, s, dropdown):
        for i in range(1,20):
            btn = Button(text=str(i), size_hint_y=None, size_hint_x=None, height=40)
            btn.bind(on_release=lambda btn: self.dropdown_select(btn, dropdown))
            dropdown.add_widget(btn)
        button = Button(text=s,size_hint_y=None, size_hint_x=None, height=40)
        button.bind(on_release=lambda btn: self.dropdown_on_release(btn, dropdown))

        dropdown.bind(on_select=lambda instance, x: self.set_button_text(button, x))
        return button


    def createButton(self, s, dropdown, _from=True):
        currencies = ['CHF','RUB','USD', 'EUR']
        if _from:
            for cur in currencies:
                btn = Button(text=cur, size_hint_y=None, size_hint_x=None, height=40)
                btn.bind(on_release=lambda btn: self.dropdown_from_select(btn, dropdown))
                dropdown.add_widget(btn)
        else:
            for cur in currencies:
                btn = Button(text=cur, size_hint_y=None, size_hint_x=None, height=40)
                btn.bind(on_release=lambda btn: self.dropdown_to_select(btn, dropdown))
                dropdown.add_widget(btn)


        button = Button(text=s,size_hint_y=None, size_hint_x=None, height=40)
        button.bind(on_release=lambda btn: self.dropdown_on_release(btn, dropdown))

        dropdown.bind(on_select=lambda instance, x: self.set_button_text(button, x))
        return button

class RatesScreen(GridLayout):
    def __init__(self, **kwargs):
        super(RatesScreen, self).__init__(**kwargs)

        self.buttons = Buttons(size_hint=(1,0.1))
        #self.buttons = Buttons(cols=2,rows=2, row_default_height=40, row_force_default=True, height=80, size_hint=(1,None))
        self.add_widget(self.buttons)
        self.image_screen = ImageScreen(rows=1, size_hint=(1,1))
        self.add_widget(self.image_screen)


class MyApp(App):

    def build(self):
        return RatesScreen(rows=2)


Window.clearcolor = (1, 1, 1, 1)
MyApp().run()










