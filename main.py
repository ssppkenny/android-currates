# Program to explain how to creat drop-down in kivy  
# import kivy module     
import kivy
import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.image import Image as CoreImage
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pandas.plotting import register_matplotlib_converters
from kivy.cache import Cache
import certifi, os
register_matplotlib_converters()
from kivy.app import App

kivy.require('1.9.0')
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from history_rates import FxtopRate

os.environ['SSL_CERT_FILE']=certifi.where()

register_matplotlib_converters()
class ImageScreen(StackLayout):
    def __init__(self, **kwargs):
        super(ImageScreen,self).__init__(**kwargs)
        #self.cols = 1
        self.image = Image(source="out.png")
        self.add_widget(self.image)



class RatesScreen(StackLayout):
    def __init__(self, **kwargs):
        super(RatesScreen, self).__init__(**kwargs)
        self._from = 'CHF'
        self._to = 'RUB'
        #self.cols = 4
        #self.rows = 2
        self.dropdownFrom = DropDown()
        self.dropdownTo = DropDown()

        self.buttonFrom = self.createButton("From", self.dropdownFrom, True)
        self.buttonTo = self.createButton("To", self.dropdownTo, False)

        self.add_widget(self.buttonFrom)
        self.add_widget(self.buttonTo)

        #self.image = Image(source="", size=(900, 900))
        #self.add_widget(self.image)
      
        btn = Button(text='Show',size_hint_y=None, size_hint_x=None, height=40)
        btn.bind(on_release=lambda btn: self.on_release(btn))
        self.add_widget(btn)
        self.label = Label(text='Currency rates', font_size='20sp', pos=(0,0), size_hint_y=None, size_hint_x=1, halign="right", width=100, height=40)
        self.add_widget(self.label)

        self.image_screen = ImageScreen()
        self.add_widget(self.image_screen)


    def get_from(self):
        return self._from

    def get_to(self):
        return self._to

    def on_release(self, btn):
        _from = self.get_from()
        _to = self.get_to()
        Cache.remove('kv.image')
        Cache.remove('kv.texture')
        self.image_screen.image.texture = self.get_texture()
        ##self.image.reload()

    def create_figure(self, date_str, from_cur, to_cur, years):
        fxtop = FxtopRate(date_str, from_cur, to_cur, years)
        fig = fxtop.plot()
        return fig

    def set_button_text(self, button, x):
        button.text = x

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

    def createButton(self, s, dropdown, _from=True):
        if _from:
            btn1 = Button(text='CHF', size_hint_y=None, size_hint_x=None, height=40)
            btn1.bind(on_release=lambda btn: self.dropdown_from_select(btn, dropdown))
            dropdown.add_widget(btn1)
            btn2 = Button(text='RUB', size_hint_y=None, size_hint_x=None, height=40)
            btn2.bind(on_release=lambda btn: self.dropdown_from_select(btn, dropdown))
            dropdown.add_widget(btn2)
        else:
            btn1 = Button(text='CHF', size_hint_y=None, size_hint_x=None, height=40)
            btn1.bind(on_release=lambda btn: self.dropdown_to_select(btn, dropdown))
            dropdown.add_widget(btn1)
            btn2 = Button(text='RUB', size_hint_y=None, size_hint_x=None,height=40)
            btn2.bind(on_release=lambda btn: self.dropdown_to_select(btn, dropdown))
            dropdown.add_widget(btn2)


        button = Button(text=s,size_hint_y=None, size_hint_x=None, height=40)
        button.bind(on_release=lambda btn: self.dropdown_on_release(btn, dropdown))

        dropdown.bind(on_select=lambda instance, x: self.set_button_text(button, x))
        return button

    def get_texture(self):
        today = datetime.date.today()
        now = today.strftime("%Y%m%d")

        fig = self.create_figure(now, self._from, self._to, 1)
        output = BytesIO()
        FigureCanvas(fig).print_png(output)

        # self.buttonFrom.bind(on_release = lambda btn: ddh.select(btn))

        with open("out.png", "wb") as outfile:
            outfile.write(output.getbuffer())
            return CoreImage.load("out.png").texture



class MyApp(App):

    def build(self):
        return RatesScreen()



MyApp().run()



