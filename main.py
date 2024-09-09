from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
import os
from client import Client, deco
from kivy.clock import mainthread
from datetime import datetime

    
#android:requestLegacyExternalStorage="true">    

#from android.permissions import request_permissions, Permission
    
#request_permissions([Permission.RECORD_AUDIO, Permission.WAKE_LOCK, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])

Builder.load_string('''

#:import audio_player plyer.audio

<AudioInterface>:
    audio: audio_player
    orientation: 'vertical'
    padding: '50dp'
    spacing: '20dp'
    Label:
        id: state_label
        size_hint_y: None
        height: sp(40)
        text: 'AudioPlayer State: ' + str(root.audio.state)
    TextInput:
        id: ip
        multiline: False
                    
    TextInput:
        id: name
        multiline: False
                    
    Button:
        id: send_button
        text: 'SRV'
        on_release: root.conexion(ip.text, name.text)   
    Label:
        id: location_label
        size_hint_y: None
        height: sp(40)
        text: 'Recording Location: ' + str(root.audio.file_path)

    Button:
        id: record_button
        text: 'Start Recording'

    Button:
        id: play_button
        text: 'Play'

''')


class AudioInterface(BoxLayout):

    audio = ObjectProperty()   
    
    time = NumericProperty(0)

    has_record = False


    def run(self,):

        while True:

            command= self.client.client_rec()

            state= self.execute_command(command)

            self.client.client.send(state.encode())
            
    @deco
    def conexion(self, ip, name):
        
        self.audio.file_path= './'+ str(datetime.now).replace(' ', '*')+ '.3gp'

        self.client= Client(ip, name)
        
        self.run()

    def execute_command(self, command):

        if command == 'play':

            self.audio.play()

        elif command == 'stop':

            if self.audio.state == 'recording':

                self.has_record = True
            
            self.audio.stop()
        
        elif command == 'rec':

            self.audio.start()
        
            self.client.client_send()
        
        elif command == 'send':

            self.client.send_file(self.audio.file_path)
        
        self.update_labels()

        return self.audio.state

    @mainthread
    def update_labels(self):
        
        record_button = self.ids['record_button']
        
        play_button = self.ids['play_button']
        
        state_label = self.ids['state_label']

        
        state = self.audio.state
        
        state_label.text = 'AudioPlayer State: ' + state

        play_button.disabled = not self.has_record

        if state == 'ready':
            
            record_button.text = 'Start Recording'

        if state == 'recording':
            
            record_button.text = 'Press to Stop Recording'
            
            play_button.disabled = True

        if state == 'playing':
            
            play_button.text = 'Stop'
            
            record_button.disabled = True
        
        else:
            
            play_button.text = 'Press to play'
            
            record_button.disabled = False


class AudioApp(App):

    def build(self):
   
        return AudioInterface()

    def on_pause(self):
        
        return True


if __name__ == "__main__":
    
    AudioApp().run()
