import os
import exifread
from pathlib import Path
from shutil import copyfile
from PIL import Image


class TimeData:
    year = 0
    month = 0


def get_time_created(path: str):
    dt = TimeData()
    dt.month = 0
    dt.year = 0

    try:
        #     with open(path, "rb") as fh:
        #         tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        #         try:
        #             dateTaken = tags["EXIF DateTimeOriginal"]
        #         except KeyError:
        #             dateTaken = tags["EXIF QuickTime"]

        i = Image.open(path)._getexif()[36867]
        # dt.year = int(dateTaken.values[:4])
        # dt.month = int(dateTaken.values[5:7])
        dt.year = int(i[:4])
        dt.month = int(i[5:7])
        return dt
    except:
        pass
    return dt


def get_time_created_png(path: str):
    lines = list()
    line = ""
    with open(path, "rb") as reader:
        lines = reader.readlines()

    for line in lines:
        if line.find("<photoshop:DateCreated>") and line.find("</photoshop:DateCreated>"):
            line = line.strip("<photoshop:DateCreated>").strip(
                "</photoshop:DateCreated>")
            line = line[: 10]
    return line


def move_files(min_year: int, max_year: int, searchDir: str, pasteDir: str):

    months = ["Januar", "Februar", "März", "April", "Mai", "Juni",
              "Juli", "August", "September", "Oktober", "November", "Dezember"]

    files = list()
    filesName = list()
    for directory in os.walk(searchDir):
        for filename in os.listdir(directory[0]):
            if(filename.lower().endswith(".jpg")):
                files.append(directory[0] + "\\" + filename)
                filesName.append(filename)
                print("Found file " + directory[0] + "\\" + filename + '\n')

    filesAmnt = len(files)
    for i in range(min_year, max_year + 1):
        for j in range(0, 12):
            Path(pasteDir + str(i) + '\\' + months[j]
                 ).mkdir(parents=True, exist_ok=True)

    with open("output.txt", "w") as writer:
        writer.write("Found " + str(len(files)) + " files\n")

    filesCoppied = 0
    for fileId in range(len(files)):
        dt = get_time_created(files[fileId])
        if (dt.year == 0 or dt.month == 0 or dt.month > 12 or dt.year > 2030 or dt.month < 1 or dt.year < 1900):
            with open("output.txt", "a") as writer:
                try:
                    if(files[fileId].find("\\\\._") != -1 or files[fileId].find("\\._") != -1):
                        print("Skipping " + files[fileId])
                        filesAmnt -= 1
                        continue

                    print("Skipping " + files[fileId])
                    writer.write("Skipping: " + files[fileId] + '\n')
                    copyfile(files[fileId], "F:\\Temp\\" + filesName[fileId])
                    filesAmnt -= 1

                except:
                    pass
            continue

        for i in range(min_year, max_year + 1):
            if i == dt.year:
                for j in range(0, 12):
                    if j + 1 == dt.month:
                        filesCoppied += 1
                        copyfile(files[fileId], pasteDir + str(i) +
                                 '\\' + months[j] + '\\' + filesName[fileId])
                        print(
                            str(round(filesCoppied * 100 / filesAmnt, 4)) + "%\n")


# print(get_time_created(
#     R"F:\Photos\C - Photos ab Sommer 2016\A - Schulfest 2016\DSC01198.JPG"))

# folderList = ["F:\\Photos\\C - Photos ab Sommer 2016\\",
#               R"F:\Photos\D - Photos 30. Sept. 16 bis Mitte Juni 17 i-phone", R"F:\Photos\E - Almevent Laising 2017", R"F:\Photos\F - Mallorca 2017", R"F:\Photos\G", R"F:\Photos\H - Herz eines Adlers - Lilith Sommer 2019", R"F:\Photos\I - Vor 10. 11. 19 oder so", R"F:\Photos\J - ca. Herbst 2019 bis 10. April 2020"]

# filesList = list()
# for root, subdirs, files in os.walk("F:\\Test\\"):
#     for file in files:
#         filesList.append(file)

# with open("output.txt", "w") as writer:
#     pass

# k = 0
# for i in range(0, 8):
#     for root, subdirs, files in os.walk(folderList[i]):
#         for file in files:

#             if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg', '.png', '.PNG'):
#                 if(file not in filesList):
#                     with open("output.txt", "a") as writer:
#                         writer.write(file + '\n')
#                     k += 1

# print(k)

# Trailing backslash is mandatory
move_files(2016, 2020, "F:\\Photos\\", "F:\\Test\\")
# 394 coppied
#
