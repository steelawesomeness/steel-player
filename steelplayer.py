import os
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from pygame import mixer

class SteelPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.audio_extensions = ['.mp3', '.ogg', '.wav', '.flac', '.m4a']
        self.playlist = []
        self.current_track = None
        self.is_playing = False

        mixer.init()
        self.load_playlist()
        self.play_next()  # start playing a random track when playlist is loaded

        # Set up a timer to check if the music has stopped
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # Check every second
        self.timer.timeout.connect(self.check_music)
        self.timer.start()

    def initUI(self):
        # main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # track info
        self.track_info = QLabel("no track playing", self)
        self.track_info.setAlignment(Qt.AlignCenter)
        self.track_info.setFont(QFont('Arial', 14))
        self.main_layout.addWidget(self.track_info)

        # controls layout
        self.controls_layout = QHBoxLayout()
        self.main_layout.addLayout(self.controls_layout)

        # control buttons
        self.prev_button = QPushButton(self)
        self.prev_button.setText("<")
        self.prev_button.setFixedSize(60, 60)
        self.prev_button.clicked.connect(self.play_previous)
        self.controls_layout.addWidget(self.prev_button)

        self.play_pause_button = QPushButton(self)
        self.play_pause_button.setText("pause")
        self.play_pause_button.setFixedSize(60, 60)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.controls_layout.addWidget(self.play_pause_button)

        self.next_button = QPushButton(self)
        self.next_button.setText(">")
        self.next_button.setFixedSize(60, 60)
        self.next_button.clicked.connect(self.play_next)
        self.controls_layout.addWidget(self.next_button)

        # window settings
        self.setWindowTitle('steel player (VERY COOL AWESOME!!)')
        self.setGeometry(300, 300, 250, 100)
        self.show()

    def load_playlist(self):
        self.playlist = [f for f in os.listdir() if any(f.endswith(ext) for ext in self.audio_extensions)]
        if not self.playlist:
            self.track_info.setText("no audio is in this folder :(")
            return

    def play_audio(self, file_to_play):
        mixer.music.load(file_to_play)
        mixer.music.play()
        self.current_track = file_to_play
        self.is_playing = True
        self.track_info.setText(f"playing: {os.path.basename(file_to_play)}")
        self.play_pause_button.setText("pause")

    def toggle_play_pause(self):
        if mixer.music.get_busy():
            if self.is_playing:
                mixer.music.pause()
                self.play_pause_button.setText("play")
                self.is_playing = False
            else:
                mixer.music.unpause()
                self.play_pause_button.setText("pause")
                self.is_playing = True
        else:
            if self.current_track:
                self.play_audio(self.current_track)
            else:
                self.play_next()

    def play_previous(self):
        if not self.playlist:
            return

        if self.current_track in self.playlist:
            index = self.playlist.index(self.current_track)
            prev_index = (index - 1) % len(self.playlist)
            file_to_play = self.playlist[prev_index]
            self.play_audio(file_to_play)
        else:
            self.play_next()

    def play_next(self):
        if not self.playlist:
            return

        if self.current_track in self.playlist:
            index = self.playlist.index(self.current_track)
            next_index = (index + 1) % len(self.playlist)
        else:
            next_index = random.randint(0, len(self.playlist) - 1)

        file_to_play = self.playlist[next_index]
        self.play_audio(file_to_play)

    def check_music(self):
        if not mixer.music.get_busy() and self.is_playing:
            self.play_next()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = SteelPlayer()
    sys.exit(app.exec_())
