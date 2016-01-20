import vlc

class MusicPlayer:
    def __init__(self, playlists):
        self.vlcInstance = vlc.Instance()
        self.vlcPlayer = self.vlcInstance.media_player_new()
        for playlist in playlists:
            open(self.playlistPath(playlist), "a").close()
        open(self.playlistPath("All"), "a").close()

    def playlistPath(self, playlist):
        return "Playlists/" + playlist + ".m3u"
    
    def play(self, playlist):
        path = self.getRandomMusicPath(playlist)
        Media = self.vlcInstance.media_new_path(path)
        self.vlcPlayer.set_media(Media)
        self.vlcPlayer.play()

    def getRandomMusicPath(self, playlistPath):
        playlistPath = self.playlistPath(playlistPath)
        with open(playlistPath) as playlistFile:
            playlist = playlistFile.readlines()
            if len(playlist) > 0:
                return playlist[0].strip() #random dice roll
            else:
                pass #return self.getRandomMusicPath("All")
