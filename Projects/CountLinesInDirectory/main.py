import os

path = "D:/dev/Cpp/Projects/NodePlanningEditor"

printContentsToFile = True

excludePaths = ["vendor", "extern", "build-Debug-Windows-x64"]
fileEndings = [".cpp", ".h", ".c", ".cc", ".hpp",
               ".hh", ".c++", ".h++", ".def", ".hlsl", ".glsl"]

excludeTokens = ["///"]

# Data:
# Blender:
#   lines: 6597252 files: 27892 with    lib\\win64_vc15
#   lines: 3200622 files: 08880 without lib\\win64_vc15

if printContentsToFile:
    with open("output.txt", "w") as writer:
        writer.write("")


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

                    if printContentsToFile:
                        with open("output.txt", "a") as writerstream:
                            writerstream.write(
                                "\n\n==========  Line-Count-New-File ==========\n\n")

                    with open(directory[0] + "/" + filename) as stream:
                        try:
                            # Read file and check if keyword is contained within

                            ranloop = False
                            for line in stream.readlines():
                                for excludeToken in excludeTokens:
                                    if excludeToken not in line and not line.isspace() and len(line) > 0:
                                        if printContentsToFile:
                                            with open("output.txt", "a") as writerstream:
                                                writerstream.write(line)
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
