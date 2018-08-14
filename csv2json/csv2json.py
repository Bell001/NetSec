#!/usr/bin/python
import sys
import matplotlib.pyplot as plt
import os
import random
import csv

rangeX = (-800, 800)
rangeY = (-800, 800)

AS_IP = {}
AS_Name = {'AS4652':'CAT-IX (Bangrak/ Nonthaburi)','AS45788':'BB Connect-IX (UIH/ BEENET)','AS45265':'CSL-IX','AS45642':'JasTel-IX','AS45458':'AWN-IX (SBN)','AS132880':'SYMC-IX','AS45667':'TCCT-IX',
	   'AS38081':'TIG-IX','AS37930':'TOT-IX','AS133543':'DTAC-IX','AS63529':'BKNIX (Bangkok Neutral Internet eXchange)','AS4651':'CAT-IIG','AS45430':'AWN-IIG (SBN)','AS45796':'BB Connect-IIG (UIH/ BEENET)','AS7568':'CSL-IIG (CS Loxinfo)','AS10089':'DTAC-IIG','AS45629':'JasTel-IIG','AS132876':'SYMC-IIG (Symphony)','AS58430':'TCCT-IIG','AS38082':'TIG-IIG (TRUE)','AS38040':'TOT-IIG','AS134509':'1-TO-ALL','AS45458':'AWN-ISP (SBN)','AS9931':'CAT-ISP','AS24187':'KIRZ','AS38566':'NTT (TH)','AS4765':'Pacific Internet','AS56309':'SiamData','AS23884':'PROEN Internet','AS24475':'ThaiREN','AS45758':'Triple T Internet','AS38794':'UIH(BeeNet)'}
AS_Type = {}
AS_Con = {}
edge = []

def check_dict(a_dict,value):
	try:
		a_dict[value] += 0
	except KeyError:
		a_dict[value] = 0
	return a_dict
file = sys.argv[1]
name = sys.argv[2]
temp = open(file)
json = open(name+".json","w")

for i in temp:
	index = i.split(",")
	try:
		weight = float(index[4])
	except ValueError:
		pass
	word = "["+index[0]+","+index[1]+"]"
        reword =  "["+index[1]+","+index[0]+"]"
        if ~(word in edge) and ~(reword in edge) and index[0].replace("\xef\xbb\xbf","") != "":
	    edge.append(word)
	    AS_Type[word] = index[3]
            AS_Con[word] = index[6]
	    AP_IP = check_dict(AS_IP, index[0].replace("\xef\xbb\xbf","")) 
	    AP_IP = check_dict(AS_IP, index[1].replace("\xef\xbb\xbf",""))
	    AP_IP[index[0].replace("\xef\xbb\xbf","")] += weight
	    AS_IP[index[1].replace("\xef\xbb\xbf","")] += weight
	    AS_Name[index[1].replace("\xef\xbb\xbf","")] = index[2]

number_of_colors = len(AS_IP)

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

json.write("{\"nodes\":[")

number = 0
 
for i in AS_IP:
        json.write("{\"color\":\""+color[number]+"\""+",\"label\":\""+str(AS_Name[i])+"\""+",\"attributes\":{},\"y\":"+str(random.randrange(*rangeX))+",\"x\":"+str(random.randrange(*rangeY))+",\"id\":"+"\""+str(i)+"\""+",\"size\":"+str(AS_IP[i]/36)+"}")
	if len(AS_IP)-1 == number:
		json.write("],")
	else:
		json.write(",")
	number += 1
number = 0

json.write("\"edges\":[")

for i in edge:
	temp = i.split(",")
	c1 = temp[0].replace("[","")
	c2 = temp[1].replace("]","")
	json.write("{\"sourceID\":\""+c1+"\",\"attributes\":{},\"targetID\":\""+c2+"\",\"size\":1"+"}")
	if len(edge)-1 == number:
                json.write("")
        else:
                json.write(",")
	number += 1
json.write("]}")
json.close()


