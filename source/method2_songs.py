import csv
from os import listdir
import os
from os.path import isfile, join

nowPath = os.getcwd()

csvFiles = [f for f in listdir(nowPath + "/assets/songs_like") if isfile(join(nowPath + "/assets/songs_like", f))]

playList = dict() # key : Playlist File name / value : [song ID, song Name]

for oneFile in csvFiles:
   with open(nowPath + "/assets/songs_like/" + oneFile, 'r') as file:
      songsList = []
      reader = csv.reader(file)
      countLine = 0
      for row in reader:
         if(countLine != 0):
            songsList.append([row[0], row[2]])
         countLine +=1
      playList[oneFile[:-4]] = songsList

def recommend_songs(user_input, filename):
   # compare first playList
   print("recommend playlist")
   firstPlayList = user_input
   maxCount = 0
   maxSamePlayList = ""
   otherSongs = []

   for secondPlayList in csvFiles:
      if(secondPlayList[:-4] != filename[:-4]):
         tempCount = 0
         for firstSong in firstPlayList:
            for secondSong in playList[secondPlayList[:-4]]:
               if(firstSong == secondSong[0]):
                  tempCount += 1
         if(tempCount > maxCount):
            maxCount = tempCount
            maxSamePlayList = secondPlayList[:-4]
   print("maxSamePlayList " + maxSamePlayList)

   temp = 0
   for fsongs in firstPlayList:
      for ssongs in playList[maxSamePlayList]:
         if(fsongs[0]!=ssongs and temp < 10):
            otherSongs.append(ssongs[1])
            temp +=1 
   return otherSongs