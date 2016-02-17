import threading
import random
import os
import time
import vlc

from os.path import expanduser

class MusicPlayer(threading.Thread):
    def __init__(self, playlists):
        threading.Thread.__init__(self)
        self.vlcInstance = vlc.Instance()
        self.vlcPlayer = self.vlcInstance.media_player_new()
        self.previousPosition = -1
        for playlist in playlists:
            open(self.playlistPath(playlist), "a").close()
        open(self.playlistPath("All"), "a").close()
        self.running = True
    
    def stop(self):
        self.running = False

    def playlistPath(self, playlist):
        return expanduser("~/.smashplaylists/" + playlist + ".m3u")
    
    def setPlaylist(self, playlist):
        self.path = self.getRandomMusicPath(playlist)

    def run(self):
        self.playMusic()

        #loop when music reaches end of track
        while self.running:
            time.sleep(1)
            print(self.vlcPlayer.get_position())
            if self.vlcPlayer.get_position() == self.previousPosition:
                self.playMusic()
            self.previousPosition = self.vlcPlayer.get_position()
        self.vlcPlayer.stop()

    def playMusic(self):
        Media = self.vlcInstance.media_new_path(self.path)
        self.vlcPlayer.set_media(Media)
        self.vlcPlayer.play()

    def getRandomMusicPath(self, playlistName):
        playlistPath = self.playlistPath(playlistName)
        with open(playlistPath) as playlistFile:
            playlist = playlistFile.readlines()
            if len(playlist) > 0:
                index = random.randint(0, len(playlist)-1)
                path = playlist[index].strip()
                return os.path.realpath(path)
            elif playlistName != "All":
                return self.getRandomMusicPath("All")

#TODO: split up song selection and vlc manipulating
