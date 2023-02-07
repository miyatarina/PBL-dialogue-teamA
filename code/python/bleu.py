# coding: utf-8

import sys
from janome.tokenizer import Tokenizer
from nltk.translate.bleu_score import corpus_bleu


def tokenize(tokenizer, sentence):
	return [token.surface for token in tokenizer.tokenize(sentence)]


def main():
	tokenizer = Tokenizer()
	# reference
	fin = open(sys.argv[1], "r")
	list_of_references = [[tokenize(tokenizer, sentence) for sentence in line.strip().split("\t")] for line in fin]
	fin.close()
	# hypothesis
	fin = open(sys.argv[2], "r")
	hypotheses = [tokenize(tokenizer, line.strip()) for line in fin]
	fin.close()
	# BLEU
	bleu = corpus_bleu(list_of_references, hypotheses)
	print("BLEU = %.3f" % bleu)


if __name__ == '__main__':
	main()
