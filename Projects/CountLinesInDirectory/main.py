import os

path = "D:/dev/Cpp/ProjectsArchive/ThirdPartyProjects/Blender"

excludePaths = []

# Data:
# Blender:
#   lines: 6094154 files: 26965 with    lib\\win64_vc15
#   lines: 2744706 files: 08236 without lib\\win64_vc15

lines = 0
files = 0
for directory in os.walk(path):
    for filename in os.listdir(directory[0]):
        if filename.endswith(".cpp") or filename.endswith(".h") or filename.endswith(".c") or filename.endswith(".cc") or filename.endswith(".hpp"):
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
                        print("UnicodeDecodeError")
                        continue
            except PermissionError:
                print("PermissionError")
                continue

print(f"Lines:\t{lines}")
print(f"Files:\t{files}")
