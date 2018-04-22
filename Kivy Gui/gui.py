from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.label import Label 
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput

# class HomeScreen(GridLayout):
#     def __init__(self, **kwargs):
#         super(HomeScreen,self).__init__(**kwargs)
#         self.cols = 2
#         self.add_widget(Label(text="Filename:"))
#         self.filename = TextInput(multiline=False)
#         self.add_widget(self.filename)

# Intro page

class WFSApp(App):
    def build(self):
        g = FloatLayout()
#        lbl=Label(text='WELCOME TO WINDOWS FORENSICS SUITE',font=("Arial Bold", 30)) 
        wimg = Image(source='WFS LOGO2.png')

        # Button

        b1=Button(text='Enter', font_size=14)
        b1.on_press()
#        g.add_widget(lbl)
        g.add_widget(wimg)
        g.add_widget(b1)
        
        return g

if __name__ == '__main__': 

   WFSApp().run()
