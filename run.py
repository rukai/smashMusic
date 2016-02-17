#!/bin/env python3

from mw import MemoryWatcher
from os.path import expanduser
from musicplayer import MusicPlayer

class SmashMusic:
    def __init__(self):
        self.stageNames = ["Menu", "PrincessPeachsCastle", "RainbowCruise", "KongoJungle", "JungleJapes", "GreatBay", "Temple", "YoshisStory", "YoshisIsland", "FountainOfDreams", "GreenGreens", "Corneria", "Venom", "Brinstar", "BrinstarDepths", "Onett", "Fourside", "MuteCity", "BigBlue", "PokemonStadium", "PokeFloats", "MushroomKingdom", "MushroomKingdomII", "IcicleMountain", "FlatZone", "Battlefield", "FinalDestination", "DreamLand", "YoshisIsland64", "KongoJungle64"]
        self.playerSet = False
        self.gamePlayed = False
        self.setStage(-1)
        self.generateLocationsFile()

    def generateLocationsFile(self):
        #mkdir -p .dolphin-emu/MemoryWatcher
        with open(expanduser("~/.dolphin-emu/MemoryWatcher/Locations.txt"), "w") as dest:
            with open("locations/GALE01.txt") as origin: #directory needs to refer to location script is from
                for line in origin:
                    output = line[:line.find('#')]
                    if output != "":
                        dest.write(output + '\n')

    def run(self):
        watch = MemoryWatcher(expanduser("~/.dolphin-emu/MemoryWatcher/MemoryWatcher"))
        for address, data in watch:
            #get stage id
            if address == "804D6CAC":
                stage = data[2]
                stageStart = data[3]
                if stageStart == 1:
                    self.setStage(stage)
            #check if out of game
            #by checking for removal of current musicID
            elif address == "8049e760":
                if data == b'\xff\xff\xff\xff':
                    #SSBM clears the current musicID before setting it for the first time
                    if self.gamePlayed:
                        self.setStage(-1)
                    self.gamePlayed = True

    def stageIDtoName(self, stageID):
        return self.stageNames[stageID+1]

    def setStage(self, stageID):
        if self.playerSet:
            self.player.stop()
        self.player = MusicPlayer(self.stageNames)
        self.player.setPlaylist(self.stageIDtoName(stageID))
        self.player.start()
        self.playerSet = True
        print("stageID: " + str(stageID))
    

sm = SmashMusic()
sm.run()
