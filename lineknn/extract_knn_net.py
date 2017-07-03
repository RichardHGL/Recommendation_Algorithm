import sys

def read_sim(filename, topN, output, binary):
	f = open(filename)
	f1 = open(output, "w")
	for line in f:
		line = line.strip().split(" ")
		length = min(topN +1, len(line))
		for i in range(1, length):
			temp = line[i].split(":")
			if binary == 1:
				f1.write(line[0] + " " + temp[0] + " " + str(1) + "\n")
			else:
				f1.write(line[0] + " " + temp[0] + " " + temp[1] + "\n")
	f1.close()
	f.close()
	
if __name__ == '__main__':
	print "Usage: python extract.py input topN output binary"
	read_sim(sys.argv[1], eval(sys.argv[2]), sys.argv[3], eval(sys.argv[4]))