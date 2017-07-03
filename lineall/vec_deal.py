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
	
def rand_vec_2(num_dim):
	vec = []
	length = 0.00
	random.seed()
	for i in range(0, num_dim):
		temp = random.random()
		vec.append(temp)
	return vec	
	
def rand_vec(num_dim):
	vec = []
	length = 0.00
	random.seed()
	for i in range(0, num_dim):
		temp = random.random()
		length += math.pow(temp, 2)
		vec.append(temp)
	normal = math.sqrt(length)
	for i in range(0, num_dim):
		vec[i] /= normal
	return vec
	
def get_items(filename):
	f = open(filename)
	items = set()
	users = set()
	for line in f:
		line = line.strip().split("\t")
		items.add("i_" + line[1])
		users.add("u_" + line[0])
	return users,items
	
def calc_score(vec1, vec2):
	if len(vec1) != len(vec2):
		print "Error !"
	score = 0.00
	for i in range(0, len(vec1)):
		score += vec1[i] * vec2[i]
	return score
	
def main_deal(vec_file, testfile, output):
	vecs, num_dim = read_vec(vec_file)
	users,items = get_items(testfile)
	item_out_count = 0
	user_out_count = 0
	f = open("out_ids", "w")
	for item in items:
		if item not in vecs:
			vecs[item] = rand_vec_2(num_dim)
			item_out_count += 1
			f.write(item + "\n")
	for user in users:
		if user not in vecs:
			vecs[user] = rand_vec_2(num_dim)
			user_out_count += 1
			f.write(user + "\n")
	print "random stage end"
	print str(item_out_count) + " item is not in items of traindata"
	print str(user_out_count) + " user is not in users of traindata"
	f.close()
	f = open(testfile)
	f1 = open(output, "w")
	for line in f:
		line = line.strip().split("\t")
		user = "u_" + line[0]
		item = "i_" + line[1]
		score = calc_score(vecs[user], vecs[item])
		f1.write(line[0] + "\t" + line[1] + "\t" + str(score) + "\n")
	f.close()
	f1.close()
	
if __name__ == '__main__':
	print "usage python vec_deal.py filename output"
	main_deal(sys.argv[1], sys.argv[2], sys.argv[3])