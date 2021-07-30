import os, sys, re


def findInFile(path):
    excludedLines = []
    with open(path, "r") as file:
        lines = file.readlines()
        wList = list(enumerate([l.strip(" ") for l in lines]))
        newLines = []
        for line in wList:
            l = str((line[1]))
            if l[-1] == '\n':
                l = str((line[1])[:-1])
            if l != "":
                newLines.append([line[0], l])
        for line in newLines:
            if line[1][:6] == "print(" and line[1][-1] == ")":
                excludedLines.append(line[0])
        file.close()
    return excludedLines


def clearFile(path, lines):
    with open(path, "r") as file:
        fileContents = file.readlines()
    with open(path, "w") as file:
        for number, line in enumerate(fileContents):
            if number not in lines:
                file.write(line)


try:
    where = sys.argv[1]
except (IndexError):
    print("You donkey, give me a location!")
    quit()

path = os.path.dirname(__file__)  # Get the path of the current file.

path += "/"

clear = []
for p in os.walk(path + where, topdown=False):
    if "/." not in p[0]:
        clear.append(p)

for data in clear:
    p = data[0] + '/'
    for f in data[2]:
        try:
            if f[-3:] == ".py":
                found = findInFile(p + f)
                if found != []:
                    clearFile(p + f, found)
                    print(str(len(found)) + " print statements removed in: " + p + f)
        except (IndexError):
            continue
