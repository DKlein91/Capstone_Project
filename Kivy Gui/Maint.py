from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os

from connect import Connect

class Filename(Screen):
    def do_filename(self, filenameText, usernameText):
        app = App.get_running_app()

        app.Username = filenameText
        app.username = usernameText

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['filename'].text = ""
        self.ids['username'].text = ""

class FilenameApp(App):
    Username = StringProperty(None)
    username = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Filename(name='filename'))
        manager.add_widget(Connected(name='connected'))

        return manager

    def get_application_config(self):
        if(not self.Username):
            return super(FilenameApp, self).get_application_config()

        conf_directory = self.User_data_dir + '/' + self.Username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(FilenameApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    FilenameApp().run()