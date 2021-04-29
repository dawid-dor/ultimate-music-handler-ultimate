# Global Imports
import sys
import os
import threading
from PyQt5 import QtWidgets, QtCore

# UI Modules Imports
import modules.main_widnow as main_menu
import modules.youtube_downloader as youtube_downloader
import modules.metadata_changer as metadata_changer
import modules.song_cutter as song_cutter

# Youtube Downloader Imports
import youtube_dl

# Metadata Changer Imports
import eyed3

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
        self.metadataCoverCheck.setChecked(True)
        self.metadataChangeButton.setDisabled(True)
        self.song_file = ""
        # Populate songs
        self.fileModel = QtWidgets.QFileSystemModel(self)
        self.fileModel.setRootPath(MUSIC_FOLDER)
        self.metadataList.setModel(self.fileModel)
        self.metadataList.setRootIndex(self.fileModel.index(MUSIC_FOLDER))
        # Fire up when clicking on the list item
        self.metadataList.selectionModel().selectionChanged.connect(
            self.metadata_song_clicked
        )
        # Fire up when clicking the change button
        self.metadataChangeButton.clicked.connect(self.change_metadata)

    def metadata_song_clicked(self):
        # Enable the change button
        self.metadataChangeButton.setDisabled(False)
        # Get clicked song path and file itself
        song_file_name = self.metadataList.currentIndex().data()
        song_path = "{}/{}".format(MUSIC_FOLDER, song_file_name)
        self.song_file = eyed3.load(song_path)
        # Set form fields to songs's current metadata
        current_name = self.song_file.tag.title
        current_artist = self.song_file.tag.artist
        current_album = self.song_file.tag.album
        self.metadataName.setText(current_name)
        self.metadataArtist.setText(current_artist)
        self.metadataAlbum.setText(current_album)

    def change_metadata(self):
        # Get values from the form
        new_name = self.metadataName.text()
        new_artist = self.metadataArtist.text()
        new_album = self.metadataAlbum.text()

        # Change values in the file
        self.song_file.tag.title = new_name
        self.song_file.tag.artist = new_artist
        self.song_file.tag.album = new_album

        # Save values
        self.song_file.tag.save()

        # Display result
        self.metadataResult.setText("Succesfully changed")

        # Clear fields and results
        self.clear_fields()
        threading.Timer(3, self.clear_info).start()

    def clear_fields(self):
        self.metadataName.setText("")
        self.metadataArtist.setText("")
        self.metadataAlbum.setText("")

    def clear_info(self):
        self.metadataResult.setText("")


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