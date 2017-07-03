# -*- coding: utf-8 -*-
import math
from math import sqrt
from datetime import datetime
import sys

def MyPearson(vec1, vec2, avg1, avg2):
    su = 0.0
    l1 = 0.0
    l2 = 0.0
    if len(vec1)==0 or len(vec2)==0:
        return 0.00,0
    num = 0
    for item in vec1:
        if item in vec2:
            num += 1
            l1 += math.pow(vec1[item] - avg1, 2)
            l2 += math.pow(vec2[item] - avg2, 2)
            su += (vec1[item] - avg1) * (vec2[item] - avg2)
	'''
	temp1 = 0.0
    temp2 = 0.0
    for item in vec1:
	    temp1 += vec1[item]
    for item in vec2:
        temp2 += vec2[item]
    avg1 = temp1/len(vec1)
    avg2 = temp2/len(vec2)
    for item in items:
        if item in vec1:
            temp1 = vec1[item] - avg1
        else:
            temp1 = -avg1
        if item in vec2:
            temp2 =  vec2[item] - avg2
        else:
            temp2 = -avg2
        l1 += math.pow(temp1, 2)
        l2 += math.pow(temp2, 2)
        su += temp1 * temp2
	'''
    temp = l1 * l2
    if temp != 0:
        similarity = su / math.sqrt(temp)
    else:
        similarity = 0.0
    return similarity,num
	
def topKMatches(prefer, AVG, person, users, items, sim=MyPearson):
    scores = []
    num = 0
    if person not in prefer:
        return scores
    if len(prefer[person])==0:
        return scores
    for other in users:
        if other==person or other not in prefer:
            continue
        simi,num = sim(prefer[person], prefer[other], AVG[person], AVG[other])
        if num >= 15 and simi > 0.01:
            scores.append((simi,other))
    # 按相似度排序
    scores.sort()
    scores.reverse()

    return scores

def loadMovieLensTrain(fileName='u1.base'):
    #str1 = './ml-100k/'                         # 目录的相对地址
    
    prefer = {}
    AVG = {}
    num = {}
    item_set = set()
    for line in open(fileName,'r'):       # 打开指定文件
        (userid, movieid, rating) = line.strip().split("\t")     # 数据集中每行有4项
        prefer.setdefault(int(userid)-1, {})      # 设置字典的默认格式,元素是user:{}字典
        prefer[int(userid)-1][int(movieid)-1] = float(rating)    
        AVG.setdefault(int(userid)-1,0.0)
        AVG[int(userid)-1] += float(rating) 
        num.setdefault(int(userid)-1,0.0)
        num[int(userid)-1] += 1.0  
    for userid in AVG:
        AVG[userid] /= num[userid]
    return prefer,AVG      # 格式如{'user1':{itemid:rating, itemid2:rating, ,,}, {,,,}}

def loadItem(itemsfile):
    f = open(itemsfile,'r')
    items = set()
    users = set()
    for line in f:
        line = line.strip().split(" ")
        items.add(eval(line[1])-1)
        users.add(eval(line[0])-1)
    f.close()
    return list(users),list(items)

def getAllUserRating(fileTrain='u1.base', output='u1.test', itemsfile="../movie/movies_new.csv"):
    traindata,AVG = loadMovieLensTrain(fileTrain)  # 加载训练集
    users,items = loadItem(itemsfile)
    f = open(output,'w')
    print "users:",len(users)
    time1 = datetime.now()
    for i,user in enumerate(users):  # test集中每个项目
        if i%500==0:
            print "id:",user
        rating = topKMatches(traindata,AVG, user, users, items)  # 基于训练集预测用户评分(用户数目<=K)
        f.write(str(user))
        if rating!=[]:
            for x in rating:
                f.write(" "+str(x[1])+":"+str(x[0]))
        f.write("\n")
        time2 = datetime.now()
        if i%500==0:
            print "time:",(time2-time1).seconds
        time1 = time2
    f.close()

############    主程序   ##############
if __name__ == "__main__":
    print "Usage python Itemknn.py traindata output K test_data"
    getAllUserRating(sys.argv[1], sys.argv[2], sys.argv[3])