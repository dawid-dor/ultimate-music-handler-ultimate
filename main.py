# Global Imports
import sys
import os
import threading
import shutil
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
from google_images_download import (
    google_images_download,
)  # IMPORTANT FOR IMAGE DOWNLOADING: delete previous version and download this one - pip install git+https://github.com/Joeclinton1/google-images-download.git

# Song Cutter Imports
from mutagen.mp3 import MP3

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
        # Set selected song field
        self.metadataSelectedSong.setText(song_file_name)

    def change_metadata(self):
        # Set flag to monitore if cover photo was changed
        cover_changed = False

        # Get values from the form
        new_name = self.metadataName.text()
        new_artist = self.metadataArtist.text()
        new_album = self.metadataAlbum.text()

        # Change values in the file
        self.song_file.tag.title = new_name
        self.song_file.tag.artist = new_artist
        self.song_file.tag.album = new_album

        # Check if cover field is checked - if it is then change the cover photo
        if self.metadataCoverCheck.isChecked():
            query = new_artist + " " + new_name
            self.change_cover_photo(query)
            cover_changed = True

        # Save values
        self.song_file.tag.save()

        # Display result
        if not cover_changed:
            self.metadataResult.setText("Succesfully changed")
        else:
            self.metadataResult.setText("Succesfully changed w/ cover")

        # Clear fields and results
        self.clear_fields()
        threading.Timer(3, self.clear_info).start()

    def change_cover_photo(self, query):
        # Download first image from google (query is song's name and song's artist)
        self.download_cover_photo(query)

        # Set paths of the file
        cover_image_path = "{}/{}".format(MUSIC_FOLDER, query)
        print(cover_image_path)
        cover_image = os.listdir(cover_image_path)[0]
        print(cover_image)
        cover_image_full_path = "{}/{}".format(cover_image_path, cover_image)

        # Set cover image
        self.song_file.tag.images.set(
            3, open("{}".format(cover_image_full_path), "rb").read(), "image/jpeg"
        )
        self.song_file.tag.save(version=eyed3.id3.ID3_V2_3)

        # Delete downloaded image(folder)
        shutil.rmtree(cover_image_path)

    def download_cover_photo(self, query):
        response = google_images_download.googleimagesdownload()
        arguments = {
            "keywords": query,
            "output_directory": MUSIC_FOLDER,
            "format": "jpg",
            "limit": 1,
            "print_urls": False,
            "size": "medium",
            "aspect_ratio": "square",
        }
        try:
            response.download(arguments)
        except FileNotFoundError:
            arguments = {
                "keywords": query,
                "output_directory": MUSIC_FOLDER,
                "format": "jpg",
                "limit": 1,
                "print_urls": False,
                "size": "medium",
            }
            try:
                response.download(arguments)
            except Exception:
                pass

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
        # Variables
        self.song_path = ""
        self.song_length = 0
        self.song_length_seconds = ""
        self.song_length_minutes = ""
        self.song_length_multiplier = 0
        # Populate songs
        self.fileModel = QtWidgets.QFileSystemModel(self)
        self.fileModel.setRootPath(MUSIC_FOLDER)
        self.songCutterList.setModel(self.fileModel)
        self.songCutterList.setRootIndex(self.fileModel.index(MUSIC_FOLDER))
        # Fire up when clicking on the list item
        self.songCutterList.selectionModel().selectionChanged.connect(
            self.cutter_song_clicked
        )
        # Fire up when clicking the cut button
        self.songCutterCutButton.clicked.connect(self.change_song_length)
        # Fire up when moving the start slider
        self.songCutterStartSlider.sliderMoved.connect(self.start_slider_moved)

    def cutter_song_clicked(self):
        # Get clicked song path and file itself
        song_file_name = self.songCutterList.currentIndex().data()
        song_path = "{}/{}".format(MUSIC_FOLDER, song_file_name)
        self.song_length = self.get_song_length(song_path)
        self.length_seconds = str(self.song_length)
        self.length_minutes = (
            str(int(self.song_length / 60)) + ":" + str(int(self.song_length % 60))
        )

        self.songCutterEndTime.setText(self.length_minutes)
        self.songCutterSelectedSong.setText(song_file_name)
        self.songCutterResult.setText(str(self.song_length))

        # Set multiplier
        self.song_length_multiplier = self.song_length / 100
        # Start slider options
        self.songCutterStartSlider.setMinimum(0)
        self.songCutterStartSlider.setMaximum(self.song_length)
        self.songCutterStartSlider.setSingleStep(self.song_length_multiplier)

    def start_slider_moved(self):
        self.songCutterStartTime.setText(str(self.songCutterStartSlider.value()))

    def change_song_length(self):
        self.songCutterResult.setText("Cut button clicked")

    def get_song_length(self, path):
        try:
            audio = MP3(path)
            length = audio.info.length
            return length
        except:
            return None


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = UltimateMusicHandler()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()