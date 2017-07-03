#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import heapq # for retrieval topK
import multiprocessing
import numpy as np
from time import time

import sys

def read_pos(filename):
	positives = []
	f1 = open(filename)
	ii = 0
	for line in f1:
		ii += 1
		arr = line.strip().split("\t")
		positive = []
		for x in arr[1: ]:
			positive.append(int(x))
		positives.append(positive)
	f1.close()
	return positives,ii
	
def read_score(filename, col_score):
	scores = []
	f1 = open(filename)
	ii2 = 0
	pre = ""
	score = {}
	for line in f1:
		line = line.strip().split("\t")
		if ii2 == 0:
			pre = line[0]
			ii2 += 1
		if line[0] != pre:
			ii2 += 1
			scores.append(score)
			score = {}
			pre = line[0]
		score[eval(line[1])] = eval(line[col_score])
	scores.append(score)
	f1.close()
	return scores, ii2

def My_evalue(positives, scores, ii, ii2, K, fileWrite):
	assert ii == ii2
	ii *= 1.0
	pk,rk,MAP,MRR,F1 = 0.0,0.0,0.0,0.0,0.0
	ii2 = 0
	for positive,score in zip(positives,scores):
		ii2 += 1
		if ii2%10000==0:
			print ii2
		x1,x2,x3,x4,x5 = evaluate(positive,score,K)
		pk += x1
		rk += x2
		MAP += x3
		MRR += x4
		F1 += x5
	pk /= ii
	rk /= ii
	MAP /= ii 
	MRR /= ii
	F1 /= ii
	f = open(fileWrite,'a')
	f.write("p@"+str(K)+":"+str(pk)+"\n")
	f.write("r@"+str(K)+":"+str(rk)+"\n")
	f.write("MAP"+":"+str(MAP)+"\n")
	f.write("MRR"+":"+str(MRR)+"\n")
	f.write("F1"+":"+str(F1)+"\n\n\n")
	f.close()
	
def main_deal(fileTest, fileScore, fileWrite):
	positives,ii = read_pos(fileTest)
	scores,ii2 = read_score(fileScore, 2)
	My_evalue(positives, scores, ii, ii2, 10, fileWrite)
	My_evalue(positives, scores, ii, ii2, 50, fileWrite)

def evaluate(positive,score,K):
	length = len(score)
	pk,rk,MAP,MRR,F1 = 0.0,0.0,0.0,0.0,0.0
	ct = 0
	ct2 = 0
	ranklist = heapq.nlargest(length, score, key=score.get)
	for i in xrange(len(ranklist)):
		item = ranklist[i]
		if i<K:
			if item in positive:
				ct += 1.0
				ct2 += 1.0
				MAP += ct2/(i+1.0)
				#print ct2,i,MAP
		else:
			if item in positive:
				ct2 += 1.0
				MAP += ct2/(i+1.0)
				#print ct2,i,MAP
		if ct2==1.0 and MRR==0.0:
			MRR=1/(i+1.0)
	pk = ct/K
	rk = ct/len(positive)
	if pk+rk==0:
		F1 = 0.0
	else:
		F1 = 2*pk*rk/(pk+rk)
	MAP /= len(positive)
	return pk,rk,MAP,MRR,F1

if __name__ == '__main__':
	print "python My_evalue.py test_file score_file output"
	main_deal(sys.argv[1],sys.argv[2],sys.argv[3])
