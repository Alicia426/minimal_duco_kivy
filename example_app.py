from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

# Disabling False positive about Button
# pylint: disable=E1101

class AppLayout(GridLayout):
    def __init__(self, **kwargs):
        super(AppLayout,self).__init__(**kwargs)
        self.cols=1

        self.inside=GridLayout()
        self.inside.cols=2

        self.inside.add_widget(Label(text='First Name:'))
        self.name=TextInput(multiline=False)
        self.inside.add_widget(self.name)

        self.inside.add_widget(Label(text='Last Name:'))
        self.last_name=TextInput(multiline=False)
        self.inside.add_widget(self.last_name)

        self.inside.add_widget(Label(text='Email:'))
        self.email=TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.add_widget(self.inside)

        self.submit=Button(text='Submit', font_size=30)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        fname=self.name.text
        lname=self.last_name.text
        email=self.email.text
        print(fname,lname,email)
        self.name.text=""
        self.last_name.text=""
        self.email.text=""


class MyApp(App):
    def build(self):
        return AppLayout()


if __name__ == "__main__":
    MyApp().run()