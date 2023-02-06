# coding: utf-8

import sys

def main():
    with open("/home/miyata/pbl/code/python/out_sentence.txt", "r") as f:
        for src in f:
            response = ''.join(src.strip().split()).replace('▁', ' ')
            return response


if __name__ == '__main__':
    main()
