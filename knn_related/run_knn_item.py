import math
from math import sqrt
import sys

def read_sim(filename, topN):
	f = open(filename)
	dic_sim = {}
	item = 0
	for line in f:
		line = line.strip().split(" ")
		item = int(line[0])
		dic_sim.setdefault(item, {})
		length = min(topN +1, len(line))
		for i in range(1, length):
			temp = line[i].split(":")
			dic_sim[item][int(temp[0])] = eval(temp[1])
	return dic_sim
	
def predict(user, item, traindata, dic_sim):
	ws = 0.00
	total = 0.00
	for item2 in dic_sim[item]:
		if item2 in traindata and user in traindata[item2]:
			ws += dic_sim[item][item2]
			total += dic_sim[item][item2] * traindata[item2][user]
	if ws > 0:
		return total/ws, ws
	else:
		return 0.00, 0.00
	
	
def loadMovieLensTrain(fileName='u1.base'):
	prefer = {}
	for line in open(fileName,'r'):
		(userid, movieid, rating) = line.strip().split("\t")
		prefer.setdefault(int(movieid)-1, {})
		prefer[int(movieid)-1][int(userid)-1] = float(rating)
	return prefer
	
def main_deal(sim_file, train_file, test_file, num_K, output):
	traindata = loadMovieLensTrain(train_file)
	dic_sim = read_sim(sim_file, num_K)
	f = open(test_file)
	f1 = open(output, "w")
	for line in f:
		line = line.strip().split(" ")
		user = int(line[0]) - 1
		item = int(line[1]) - 1
		if item not in traindata or item not in dic_sim:
			f1.write(line[0] + "\t" + line[1] + "\t" + str(-1) + "\n")
			continue
		score1, score2 = predict( user, item, traindata, dic_sim)
		f1.write(line[0] + "\t" + line[1] + "\t" + str(score2) +"\n")
	f.close()
	f1.close()
	
if __name__ == '__main__':
	print "usage python run_itemknn.py sim_file train_file test_file num_K output"
	main_deal(sys.argv[1], sys.argv[2], sys.argv[3], eval(sys.argv[4]), sys.argv[5])