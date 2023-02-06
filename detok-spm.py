# coding: utf-8

import sys

def main():
    fname = sys.argv[1]
    fout = open(fname.replace(".txt", ".detok.txt"), "w")
    fin = open(fname, "r")
    for line in fin:
        response = ''.join(line.strip().split()).replace('▁', ' ')
        fout.write(response + "\n")
    fin.close()
    fout.close()


if __name__ == '__main__':
    main()
