# Global Imports
import sys
import os
import threading
import shutil
import math
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
from pydub import AudioSegment

# TO DO
# 1. Make music folder browsable
# 2. Make UI cleaner
# 3. Make py_install
# 4. Clear all values when closing the module


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
        # Tab Orders
        self.setTabOrder(self.youtubeSongUrl, self.youtubeSongName)
        self.setTabOrder(self.youtubeSongName, self.youtubeDownloadButton)
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
        # Tab Orders
        self.setTabOrder(self.metadataName, self.metadataArtist)
        self.setTabOrder(self.metadataArtist, self.metadataAlbum)
        self.setTabOrder(self.metadataAlbum, self.metadataChangeButton)
        # Set elements default state
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
        cover_image = os.listdir(cover_image_path)[0]
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
        # Tab Orders
        self.setTabOrder(self.songCutterStartTimeCut, self.songCutterEndTimeCut)
        self.setTabOrder(self.songCutterEndTimeCut, self.songCutterCutButton)
        # Variables - global
        self.song_path = ""
        self.song_length = 0
        # Variables - initial
        self.song_length_end_minutes = 0
        self.song_length_end_seconds = 0
        # Variables - cut
        self.song_length_start_input = ""
        self.song_length_start_end = ""
        self.song_length_start_cut_minutes = 0
        self.song_length_start_cut_seconds = 0
        self.song_length_end_cut_minutes = 0
        self.song_length_end_cut_seconds = 0
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

    def cutter_song_clicked(self):
        # Get clicked song path and file itself
        song_file_name = self.songCutterList.currentIndex().data()
        self.song_path = "{}/{}".format(MUSIC_FOLDER, song_file_name)
        self.songCutterSelectedSong.setText(song_file_name)

        # Get song length in miliseconds
        self.song_length = self.get_song_length(self.song_path) * 1000

        # Set start time as it will be always 0:00
        self.songCutterStartTime.setText("0:00")

        # Set initial end time
        self.song_length_end_minutes = int((self.song_length / (1000 * 60)) % 60)
        self.song_length_end_seconds = int((self.song_length / 1000) % 60)

        # Check if seconds are below 10
        if self.song_length_end_seconds < 10:
            self.song_length_end_seconds = "0{}".format(self.song_length_end_seconds)
        self.songCutterEndTime.setText(
            "{}:{}".format(self.song_length_end_minutes, self.song_length_end_seconds)
        )

        # Set cut fields
        self.songCutterStartTimeCut.setText("0:00")
        self.songCutterEndTimeCut.setText(
            "{}:{}".format(self.song_length_end_minutes, self.song_length_end_seconds)
        )

    def change_song_length(self):
        # Split user input into list
        self.song_length_start_input = self.songCutterStartTimeCut.text().split(":")
        self.song_length_end_input = self.songCutterEndTimeCut.text().split(":")

        # Set cut variables
        self.song_length_start_cut_minutes = int(self.song_length_start_input[0])
        self.song_length_start_cut_seconds = int(self.song_length_start_input[1])
        self.song_length_end_cut_minutes = int(self.song_length_end_input[0])
        self.song_length_end_cut_seconds = int(self.song_length_end_input[1])

        # Convert cut times to milliseconds
        start_time = (
            self.song_length_start_cut_minutes * 60 * 1000
            + self.song_length_start_cut_seconds * 1000
        )
        end_time = (
            self.song_length_end_cut_minutes * 60 * 1000
            + self.song_length_end_cut_seconds * 1000
        )
        try:
            # Open file and cut it
            song = AudioSegment.from_mp3(self.song_path)
            extract = song[start_time:end_time]

            # Save cut file
            extract.export(self.song_path, format="mp3")

            # Fix file duration
            self.fix_duration(self.song_path)

            # Display result
            self.songCutterResult.setText("File Cut Succesfully!")
            threading.Timer(3, self.clear_info).start()
        except Exception:
            self.songCutterResult.setText("Something went wrong.")
            threading.Timer(3, self.clear_info).start()

    def clear_info(self):
        self.songCutterResult.setText("")

    def fix_duration(self, filepath):
        ##  Create a temporary name for the current file.
        temp_filepath = filepath[: len(filepath) - len(".mp3")] + "_temp" + ".mp3"

        ##  Rename the file to the temporary name.
        os.rename(filepath, temp_filepath)

        ##  Run the ffmpeg command to copy this file.
        ##  This fixes the duration and creates a new file with the original name.
        command = (
            'ffmpeg -v quiet -i "' + temp_filepath + '" -acodec copy "' + filepath + '"'
        )
        os.system(command)

        ##  Remove the temporary file that had the wrong duration in its metadata.
        os.remove(temp_filepath)

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