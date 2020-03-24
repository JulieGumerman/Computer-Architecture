import sys

if len(sys.argv) != 2:
    print("usage: file.py filename")
    sys.exit()

filename = sys.argv[1]

try:
    with open(filename) as f:
        for line in f:
            print(line)
            #ignore comments
            comment_split = line.split("#")
            #strip out white space
            num = comment_split.strip() #strip() removes white space
            #ignore blank lines
            if num == "":
                continue
            
            val = int(num)
except FileNotFoundError:
    print("File not found")
    sys.exit(2)