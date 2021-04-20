from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

class CalendarGUI(BoxLayout):

    split = BoxLayout(
        padding=[0, 60],
        orientation = 'horizontal'
    )
    split.add_widget(Label(text='Calendar Name', font_size='20sp'))
    split.add_widget(TextInput(
        multiline=False,
        hint_text='Input Calendar Name',
        font_size='16sp'))

    username = BoxLayout(
        padding=[0, 60],
        orientation = 'horizontal'
    )
    username.add_widget(Label(
        text='Google Cal e-mail',
        font_size='20sp'
    ))
    username.add_widget(TextInput(
        multiline=False,
        hint_text='Input email',
        font_size='16sp'))

    password = BoxLayout(
        padding=[0, 60],
        orientation='horizontal'
    )
    password.add_widget(Label(
        text='Google Cal Password',
        font_size='20sp'
    ))
    password.add_widget(TextInput(
        multiline=False,
        password=True,
        font_size='16sp'))

    def __init__(self, **kwargs):
        super(CalendarGUI, self).__init__(**kwargs)
        print(Window.size)
        self.orientation = 'vertical'
        self.add_widget(Label(
            text=' Google Calendar Config',
            font_size='25sp'))

        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(self.split)

        add_new_cal = Button(
            text='Add Another Calendar'
        )
        add_new_cal.bind(on_press=self.add_calendar_inp)
        finished = Button(
            text='Finish'
        )
        finished.bind(on_press=self.finish_gathering)
        grid_root = GridLayout(
            rows = 1,
            cols = 2,
            padding = [20, 20, 20, 20]
        )
        grid_root.add_widget(add_new_cal)
        grid_root.add_widget(finished)
        self.add_widget(grid_root)


    def add_calendar_inp(self, instance):
        new_split = BoxLayout(
        padding=[0, 60],
        orientation = 'horizontal'
    )
        new_split.add_widget(Label(text='Calendar Name', font_size='20sp'))
        new_split.add_widget(TextInput(
        multiline=False,
        hint_text='Input Calendar Name',
        font_size='16sp'))
        self.add_widget(
            widget=new_split,
            index=1
        )
        Window.size = (AppGUI.sz[0], AppGUI.sz[1] + instance.height)
        AppGUI.sz = (AppGUI.sz[0], AppGUI.sz[1] + instance.height)
        return


    def finish_gathering(self, instance):
        for child in self.children:
            if isinstance(child, BoxLayout):
                for i in child.children:
                    if isinstance(i, TextInput):
                        print(i.text)


class AppGUI(App):
    inp_pad = [0, 60]
    sz = (450, 450)
    def build(self):
        Window.size = self.sz
        return CalendarGUI()

if __name__ == '__main__':
    AppGUI().run()