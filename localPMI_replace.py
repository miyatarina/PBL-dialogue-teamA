import re
import sys

fin = open(sys.argv[1], "r")
content = fin.read()
content = content.replace("), ", "), \n")
content = content.replace(", \n", " \n")
f = open("tmp.txt", "w")
f.write(content)
fin.close()
f.close()

fin = open("tmp.txt", "r")
f = open(sys.argv[2], "w")
for line in fin:
    line = re.sub("^\[", "", line)
    line = re.sub("\]$", "", line)
    line = re.sub("^\(", "", line)
    line = re.sub("\) \n$", "\n", line)
    line = re.sub("\)$", "", line)
    line = re.sub("^'", "", line)
    line = re.sub("', ", "\t", line)
    f.write(line)
fin.close()
f.close()