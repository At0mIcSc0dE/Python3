import os

path1 = "D:/Applications/Steam/steamapps/common/Kerbal Space Program - NecMods/GameData"
path2 = "D:/Applications/Steam/steamapps/common/Kerbal Space Program - NecMods - NoGraphicsMods/GameData"


path1Folders = os.listdir(path1)
path2Folders = os.listdir(path2)


with open("output.txt", "w") as ostream:
    ostream.write("")


with open("output.txt", "a+") as ostream:
    for dir1 in path1Folders:
        if dir1 not in path2Folders:
            ostream.write(dir1 + "\n")
