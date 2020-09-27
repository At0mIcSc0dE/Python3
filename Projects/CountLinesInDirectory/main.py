import os

path = "D:/dev/Cpp/ProjectsArchive/ThirdPartyProjects/Blender"

excludePaths = ["lib\\win64_vc15"]
fileEndings = [".cpp", ".h", ".c", ".cc", ".hpp", ".hh", ".c++", ".h++"]

# Data:
# Blender:
#   lines: 6597252 files: 27892 with    lib\\win64_vc15
#   lines: 3200622 files: 08880 without lib\\win64_vc15

lines = 0
files = 0
for directory in os.walk(path):
    for filename in os.listdir(directory[0]):
        for fileEnding in fileEndings:
            if filename.endswith(fileEnding):
                try:
                    exclude = False
                    for excludePath in excludePaths:
                        if excludePath in (directory[0] + "/" + filename):
                            exclude = True

                    if exclude:
                        continue

                    with open(directory[0] + "/" + filename) as stream:
                        try:
                            # Read file and check if keyword is contained within

                            ranloop = False
                            for line in stream.readlines():
                                if "//" not in line and ("/" not in line and "*" not in line):
                                    pathToFile = directory[0] + \
                                        "/" + filename
                                    lines += 1
                            print(pathToFile.replace("\\", "/"))
                            files += 1
                        except UnicodeDecodeError:
                            print("UnicodeDecodeError :" +
                                  directory[0] + "/" + filename)
                            continue
                except PermissionError:
                    print("PermissionError :" +
                          directory[0] + "/" + filename)
                    continue

print(f"Lines:\t{lines}")
print(f"Files:\t{files}")
