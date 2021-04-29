# Global Imports
import sys
import os
import threading
from PyQt5 import QtWidgets

# UI Modules Imports
import modules.main_widnow as main_menu
import modules.youtube_downloader as youtube_downloader
import modules.metadata_changer as metadata_changer
import modules.song_cutter as song_cutter

# Youtube Downloader Imports
import youtube_dl

MUSIC_FOLDER = "H:/MuzykaYT"

# -- Main Menu --
class UltimateMusicHandler(QtWidgets.QMainWindow, main_menu.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Modules
        self.ytd = Youtube_Downloader()
        self.mdc = Metadata_Changer()
        self.sc = Song_Cutter()
        # Music Folder
        self.menuFolderBrowserDefault.setChecked(True)
        self.menuFolderBrowserLine.setText(MUSIC_FOLDER)
        self.menuFolderBrowserLine.setEnabled(False)
        self.menuOpenFolderButton.clicked.connect(self.open_music_folder)
        # Menu Buttons
        self.menuYoutubeDownloaderButton.clicked.connect(
            lambda: self.show_window(self.ytd)
        )
        self.menuMetadataChangerButton.clicked.connect(
            lambda: self.show_window(self.mdc)
        )
        self.menuSongCutterButton.clicked.connect(lambda: self.show_window(self.sc))

    def show_window(self, window):
        window.show()

    def open_music_folder(self):
        path = os.path.realpath(MUSIC_FOLDER)
        os.startfile(path)


# -- Youtube Downloader --
class Youtube_Downloader(QtWidgets.QMainWindow, youtube_downloader.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.youtubeMenuButton.clicked.connect(self.hide)
        self.download_folder = MUSIC_FOLDER
        # Youtube parameters
        self.ydl_opts = {
            # Output folder
            "outtmpl": "{self.download_folder}/%({title})s-%(id)s.%(ext)s",
            # Parameters
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        self.youtubeDownloadButton.clicked.connect(self.download_song)

    def download_song(self):
        url = self.youtubeSongUrl.text()
        name = self.youtubeSongName.text()
        try:
            # Check if name field is empty - if its not, name the file as written in the video name
            if len(name) > 0:
                self.ydl_opts["outtmpl"] = "{}/{}.%(ext)s".format(
                    self.download_folder, name
                )
            else:
                self.ydl_opts["outtmpl"] = "{}/%(title)s-%(id)s.%(ext)s".format(
                    self.download_folder
                )

            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
                self.youtubeResult.setText("Succesfully downloaded!")
                self.clear_fields()
                threading.Timer(3, self.clear_info).start()

        except Exception:
            self.youtubeResult.setText("Could not download.")
            threading.Timer(3, self.clear_info).start()

    def clear_fields(self):
        self.youtubeSongUrl.setText("")
        self.youtubeSongName.setText("")

    def clear_info(self):
        self.youtubeResult.setText("")


# -- Metadata Changer --
class Metadata_Changer(QtWidgets.QMainWindow, metadata_changer.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.metadataMenuButton.clicked.connect(self.hide)


# --Song Cutter --
class Song_Cutter(QtWidgets.QMainWindow, song_cutter.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.songCuterMenuButton.clicked.connect(self.hide)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = UltimateMusicHandler()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()