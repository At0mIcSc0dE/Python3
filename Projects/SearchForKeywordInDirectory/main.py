import os


path = "D:/Applications/Steam/steamapps/common/Kerbal Space Program - NecMods - S-Test/GameData"
targetKeyword = "sunflare"
# targetKeyword2 = "RealismOverhaul"

with open("output.txt", "w") as ostream:
    ostream.write("")

filesChecked = 0
filesFound = 0
for directory in os.walk(path):
    for filename in os.listdir(directory[0]):
        if filename.endswith(".cfg") or filename.endswith(".txt") or filename.endswith(".json") or filename.endswith(".cpp") or filename.endswith(".h") or filename.endswith(".hpp") or filename.endswith(".cc") or filename.endswith(".cs") or filename.endswith(".csproj") or filename.endswith(".vcxproj") or filename.endswith(".log") or filename.endswith(".html") or filename.endswith(".xml"):
            filesChecked += 1
            try:
                with open(directory[0] + "/" + filename) as stream:
                    with open("output.txt", "a+") as ostream:
                        try:
                            # Read file and check if keyword is contained within
                            ranloop = False
                            for line in stream.readlines():
                                if targetKeyword.lower() in line.lower():
                                    ranloop = True
                                    break
                            if ranloop:
                                filesFound += 1
                                pathToFile = directory[0] + \
                                    "/" + filename + "\n"
                                ostream.write(
                                    pathToFile.replace("\\", "/"))
                        except UnicodeDecodeError:
                            continue
            except PermissionError:
                continue

            # for windows
            if os.name == "nt":
                os.system("cls")
            # for mac-os and linux
            else:
                os.system("clear")
            print("Files Checked: " + str(filesChecked) +
                  "\nFiles Found: " + str(filesFound))


with open("output.txt", "a+") as ostream:
    ostream.write("\n\n\n\n\n" + "***DEBUG INFO***\n\n" + "Files Checked: " +
                  str(filesChecked) + "\nFiles Found: " + str(filesFound) + "\n\n***END DEBUG INFO***\n\n\n\n\n")
