from kivy.app import App
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
 
# ---------- Homegui.kv  ----------
 
# Reference Homegui.py
#: import main Homegui
#: import ListAdapter kivy.adapters.listadapter.ListAdapter
#: import ListItemButton kivy.uix.listview.ListItemButton
 
# Homegui:
 
<Homegui>:
    orientation: "vertical"
    file_name_text_input: file_name
    User_name_text_input: User_name
    name_list: names_list_view
    padding: 10
    spacing: 10
 
    BoxLayout:
        size_hint_y: None
        height: "40dp"
 
        Label:
            text: "First Name"
        TextInput:
            id: file_name
        Label:
            text: "User Name"
        TextInput:
            id: User_name
 
    BoxLayout:
        size_hint_y: None
        height: "40dp"
        Button:
            text: "Submit"
            size_hint_x: 15
            on_press: root.submit_name()
        Button:
            text: "Delete"
            size_hint_x: 15
            on_press: root.delete_name()

 
    # Define starting data and point to the ListItemButton
    # in the Python code
    ListView:
        id: names_list_view
        adapter:
            ListAdapter(data=["LNK"], cls=main.NameButton)
 
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
 
<SampGridLayout>:
    rows: 2
 
    BoxLayout:
        size_hint_y: None
        height: 30
        spacing: 10
 
        # Make the background for the toolbar white
        canvas:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            background_normal: 'open.png'
            background_down: 'open_dn.png'
            size_hint_x: None
            width: 30
        Button:
            background_normal: 'disk.png'
            background_down: 'disk_dn.png'
            size_hint_x: None
            width: 30
        Button:
            background_normal: 'exit.png'
            background_down: 'exit_dn.png'
            size_hint_x: None
            width: 30