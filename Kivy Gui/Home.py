from kivy.uix.label import Label
from kivy.app import App 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton


 class NameButton(ListItemButton):
    pass
 
 
class Homegui(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    file_name_text_input = ObjectProperty()
    User_name_text_input = ObjectProperty()
    name_list = ObjectProperty()
 
    def submit_name(self):
 
        # Get the name name from the TextInputs
        name_name = self.file_name_text_input.text + " " + self.User_name_text_input.text
 
        # Add the name to the ListView
        self.name_list.adapter.data.extend([name_name])
 
        # Reset the ListView
        self.name_list._trigger_reset_populate()
 
    def delete_name(self, *args):
 
        # If a list item is selected
        if self.name_list.adapter.selection:
 
            # Get the text from the item selected
            selection = self.name_list.adapter.selection[0].text
 
            # Remove the matching item
            self.name_list.adapter.data.remove(selection)
 
            # Reset the ListView
            self.name_list._trigger_reset_populate()
 
    def replace_name(self, *args):
 
        # If a list item is selected
        if self.name_list.adapter.selection:
 
            # Get the text from the item selected
            selection = self.name_list.adapter.selection[0].text
 
            # Remove the matching item
            self.name_list.adapter.data.remove(selection)
 
            # Get the name name from the TextInputs
            name_name = self.file_name_text_input.text + " " + self.User_name_text_input.text
 
            # Add the updated data to the list
            self.name_list.adapter.data.extend([name_name])
 
            # Reset the ListView
            self.name_list._trigger_reset_populate()
 
 
class HomeguiApp(App):
    def build(self):
        return Homegui()
 
 
dbApp = HomeguiApp()
 
dbApp.run()

# Here are the text and entry box
# class HomeScreen(GridLayout):
#     def __init__(self, **kwargs):
#         super(Homescreen, self).__init__(**kwargs)
#         self.cols = 2

#         self.add_widget(Label(text="Start Date:"))
#         self.tfa = TextInput(multiline=False)
#         self.add_widget(self.enddate)

#         self.add_widget(Label(text="End Date:"))
#         self.tfa = TextInput(multiline=False)
#         self.add_widget(self.enddate)

#         self.add_widget(Label(text="Filename:"))
#         self.filename = TextInput(multiline=False)
#         self.add_widget(self.filename)

#         self.add_widget(Label(text="UserName:"))
#         self.Username = TextInput(multiline=False)
#         self.add_widget(self.Username)


# class SimpleKivy(App):
#     def build(self):
#         return HomeScreen()

# if _name_ == "__main__":
#     SimpleKivy().run()

    # FileName and Username .kv 

     orientation: "vertical"
     start_date_text_input: start_date
    end_date_text_input: end_date
    file_name_text_input: file_name
    User_name_text_input: User_name
   
    padding: 10
    spacing: 10
 
    BoxLayout:
        size_hint_y: None
        height: "40dp"
         Label:
            text: "Start Date"
        TextInput:
            id: file_name
        Label:
            text: "End Date"
        TextInput:
            id: User_name
        Label:
            text: "Fileame"
        TextInput:
            id: file_name
        Label:
            text: "Userame"
        TextInput:
            id: User_name
 
    BoxLayout:
        size_hint_y: None
        height: "40dp"
        Button:
            text: "Search"
            size_hint_x: 15
            on_press: root.search_csv()
        Button:
            text: "Delete"
            size_hint_x: 15
            on_press: root.delete_csv()
     
    # Define starting data and point to the ListItemButton
  
    # ListView:
    #     id: Inspector
    #     adapter:
    #         ListAdapter(data=["Prefetch"], cls=main.InspectorButton)
 
# ---------- kivytut.py  ----------
 
import kivy
kivy.require("1.9.0")
 
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
 
class SampGridLayout(GridLayout):
    pass
 
class SampleApp(App):
 
    def build(self):
        return SampGridLayout()
 
sample_app = SampleApp()
sample_app.run()
 
# ---------- sample.kv  ----------
 
# <SampGridLayout>:
#     rows: 2
 
#     BoxLayout:
#         size_hint_y: None
#         height: 30
#         spacing: 10
 
        # Make the background for the toolbar white
        # canvas:
        #     Color:
        #         rgba: 1, 1, 1, 1
        #     Rectangle:
        #         pos: self.pos
        #         size: self.size
        # Button:
        #     background_normal: 'open.png'
        #     background_down: 'open_dn.png'
        #     size_hint_x: None
        #     width: 30
        # Button:
        #     background_normal: 'disk.png'
        #     background_down: 'disk_dn.png'
        #     size_hint_x: None
        #     width: 30
        # Button:
        #     background_normal: 'exit.png'
        #     background_down: 'exit_dn.png'
        #     size_hint_x: None
        #     width: 30