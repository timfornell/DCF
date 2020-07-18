import PySimpleGUI as sg

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

class GUI():
    def __init__(self):
        self._window = sg.Window("Demo", layout)

    def get_track_ROIs(self):
        pass

    def update_window(self):
        event, values = self._window.Read()
        return event, values

    def close_window(self):
        self._window.Close()