#!/usr/bin/python
import sys
import matplotlib.pyplot as plt
import os
import random
import csv

rangeX = -200
rangeY = 200
AS_Cat = {}
AS_IP = {}
AS_Name = {'AS4652':'CAT-IX (Bangrak/ Nonthaburi)','AS45788':'BB Connect-IX (UIH/ BEENET)','AS45265':'CSL-IX','AS45642':'JasTel-IX','AS45458':'AWN-IX (SBN)','AS132880':'SYMC-IX','AS45667':'TCCT-IX',
	   'AS38081':'TIG-IX','AS37930':'TOT-IX','AS133543':'DTAC-IX','AS63529':'BKNIX (Bangkok Neutral Internet eXchange)','AS4651':'CAT-IIG','AS45430':'AWN-IIG (SBN)','AS45796':'BB Connect-IIG (UIH/ BEENET)','AS7568':'CSL-IIG (CS Loxinfo)','AS10089':'DTAC-IIG','AS45629':'JasTel-IIG','AS132876':'SYMC-IIG (Symphony)','AS58430':'TCCT-IIG','AS38082':'TIG-IIG (TRUE)','AS38040':'TOT-IIG','AS134509':'1-TO-ALL','AS45458':'AWN-ISP (SBN)','AS9931':'CAT-ISP','AS24187':'KIRZ','AS38566':'NTT (TH)','AS4765':'Pacific Internet','AS56309':'SiamData','AS23884':'PROEN Internet','AS24475':'ThaiREN','AS45758':'Triple T Internet','AS38794':'UIH(BeeNet)'}
AS_Type = {'AS38082':'IIG','AS132876':'IIG','AS45629':'IIG','AS24475':'ISP-Govt','AS7568':'IIG','AS38566':'ISP-Local','AS4651':'IIG','AS45265':'NIX','AS45458':'NIX','AS132880':'NIX','AS45667':'NIX','AS38081':'NIX','AS37930':'NIX','AS133543':'NIX','AS63529':'NIX'}
AS_Con = {'AS38082':'IPv4/IPv6 Dual Stack','AS132876':'IPv6 Dual Stack','AS45629':'Transit/ IPv6 Dual Stack','AS24475':'IPv6 Dual Stack','AS7568':'IPv4','AS38566':'IPv6 Dual Stack','AS4651':'Transit/ IPv6 Dual Stack','AS45265':'IPv6 Dual Stack','AS45458':'IPv4','AS132880':'IPv6 Dual Stack','AS45667':'IPv4','AS38081':'IPv4','AS37930':'IPv6 Dual Stack','AS133543':'IPv4','AS63529':'Peering/ IPv6 Native'}
edge = {}

def check_dict(a_dict,value):
	try:
		a_dict[value] += 0
	except KeyError:
		a_dict[value] = 0
	return a_dict

def check_edge(a_dict, c1, c2, weight):
        word = "["+c1+","+c2+"]"
        reword = "["+c2+","+c1+"]"
        try:
		if ~have_dict(a_dict, word) and ~have_dict(a_dict, reword):
                        a_dict[word] = weight
        except KeyError:
                a_dict[word] = 0
        return a_dict

def  have_dict(a_dict, word):
     flag = True
     try:
         a_dict[word] += 0
     except KeyError:
         flag = False 
     return  flag

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
        if index[0].replace("\xef\xbb\xbf","") != "":
            edge = check_edge(edge, index[0], index[1], weight)
	    AS_Type[index[1]] = index[3]
            AS_Con[word] = index[6]
	    AP_IP = check_dict(AS_IP, index[0].replace("\xef\xbb\xbf","")) 
	    AP_IP = check_dict(AS_IP, index[1].replace("\xef\xbb\xbf",""))
	    AP_IP[index[0].replace("\xef\xbb\xbf","")] += weight
	    AS_IP[index[1].replace("\xef\xbb\xbf","")] += weight
	    AS_Name[index[1].replace("\xef\xbb\xbf","")] = index[2]
            #index[6] = index[6].replace("\n","").replace("\r","")
            #AS_Cat[index[1].replace("\xef\xbb\xbf","")] = index[6]
	    
number_of_colors = len(AS_IP)

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

json.write("{\"nodes\":[")

number = 0

AS_Name

def check_error(a_dict, value):
    try:
        a_dict[value] += "a"
    except KeyError:
        print a_dict
        print value
 
#print(len(AS_IP))
typeA = []
for i in AS_IP:
	json.write("{\"color\":\""+color[number]+"\""+",\"label\":\""+str(AS_Name[i])+"\""+",\"attributes\":{},\"y\":"+str(rangeY)+",\"x\":"+str(rangeX)+",\"id\":"+"\""+str(i)+"\""+",\"size\":"+str(AS_IP[i]/100)+",\"category\":"+"\""+str(AS_Type[i])+"\""+"}")
	if len(AS_IP)-1 == number:
		json.write("],")
	else:
		json.write(",")
	number += 1
	rangeX += 40
        typeA.append(AS_Type[i])
number = 0
json.write("\"edges\":[")
mylist = list(set(typeA))
print(mylist)
for key, value in edge.iteritems():
	temp = key.split(",")
        c1 = temp[0].replace("[","")
        c2 = temp[1].replace("]","")
        json.write("{\"sourceID\":\""+c1+"\",\"attributes\":{},\"targetID\":\""+c2+"\",\"size\":"+str(value)+"}")
        if len(edge)-1 == number:
                json.write("")
        else:
                json.write(",")
        number += 1

json.write("]}")
json.close()


