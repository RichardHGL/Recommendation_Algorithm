import sys
import struct
import random
import math

def read_vec(filename):
	f = open(filename, "r")
	vecs = {}
	idx = 0
	num_dim = 0
	num_vertices = 0
	print "start"
	for line in f:
		if idx == 0:
			idx = 1
			line = line.strip().split(" ")
			num_vertices = int(line[0])
			num_dim = int(line[1])
			print num_vertices, num_dim
			continue
		line = line.strip().split(" ")
		vecs.setdefault(line[0], [])
		for i in range(1, len(line)):
			vecs[line[0]].append(eval(line[i]))		
	f.close()
	print "Process Successful!"
	return vecs,num_dim
	
def calc_score(vec1, vec2):
	if len(vec1) != len(vec2):
		print "Error !"
	score = 0.00
	for i in range(0, len(vec1)):
		score += vec1[i] * vec2[i]
	return score
	
def topKMatches(vecs, item):
	scores = []
	for item2 in vecs:
		if item2 == item:
			continue
		simi = calc_score(vecs[item], vecs[item2])
		scores.append((simi,item2))
	scores.sort()
	scores.reverse()

	return scores	
	
def main_deal(vec_file, output):
	vecs, num_dim = read_vec(vec_file)
	f1 = open(output, "w")
	for item in vecs:
		rating = topKMatches(vecs, item)
		length = min(1000, len(rating))
		f1.write(item)
		for i in range(0, length):
			f1.write(" " + rating[i][1] + ":" + str(rating[i][0]))
		f1.write("\n")
	f1.close()
	
if __name__ == '__main__':
	print "usage python vec_deal.py filename output"
	main_deal(sys.argv[1], sys.argv[2])