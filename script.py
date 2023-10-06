from PIL import Image
import sys
import json 
import subprocess
import math
import os
import re
import json
import time

# image= Image.open('./uploads/'+file)
#image.show()
import cv2
import numpy as np
from IPython.display import Image, display

from nltk.corpus import words
from bs4 import BeautifulSoup

keywords = ["Name", "Age","Roll","Phone","Mobile No.", "Aadhar Number"]

# img = cv2.imread('./uploads/'+file)

class Linked_Structure :
	def __init__(self,wordStruct) :
		self.name = wordStruct[0]
		self.x1 = wordStruct[1][0]
		self.y1 = wordStruct[1][1]
		self.x2 = wordStruct[1][2]
		self.y2 = wordStruct[1][3]
		self.acc_level = wordStruct[2]
		self.marker = False
		self.neighbours = []
		self.type = None

	def __str__(self) :
		return self.name + "(%s,%s) , (%s,%s)"%(self.x1,self.y1,self.x2,self.y2)

	def __add__(self,obj2) :
		new_name = self.name + " " + obj2.name
		nx1 = self.x1
		nx2 = obj2.x2
		ny1 = min(self.y1,obj2.y1)
		ny2 = min(self.y2,obj2.y2)
		nacc = (self.acc_level*obj2.acc_level)**0.5
		to_ret = Linked_Structure( [new_name, [nx1,ny1,nx2,ny2],nacc ] )
		to_ret.type = self.type
		return to_ret


def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)




def get_str(file1) :

	# image= Image.open('./uploads/'+file1)
	#image.show()

	# keywords = ["Name","Age","Roll","Phone","No.","Number","DATE","PHONE",'state','zip','birth']
	# keywords = [ re.sub('[^A-Za-z0-9 ]+', '', i).lower() for i in keywords]
	# # img = cv2.imread('./uploads/'+file1)
	# print("doing")
	img = cv2.imread(file1)

	os.system("tesseract %s output hocr"%(file1))

	html_doc = BeautifulSoup(open('output.hocr'), 'html.parser')

	final_list = []
	for div_ele in html_doc.find_all('div', {'class' : 'ocr_carea'}):
			for span in div_ele.find_all('span', {'class' : 'ocrx_word'}):
					word = span.text
					word = re.sub('[^A-Za-z0-9 ]+', ' ', word)
					if len(word.strip()) > 0:
							splitted = span['title'].split()
							bbox = splitted[1:4] + [splitted[4][0:-1]]
							confidence = splitted[6]
							final_list.append([word.strip(" ‘"),tuple(map(int,bbox)),int(confidence)])

	# for i in final_list :
	# 	x1,y1,x2,y2 = i[1]
	# 	if i[0].strip() != "" :
	# 		print(i[0])
	# 		img1=cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
	# 		cv2.imshow("heading",img1)
	# 		cv2.waitKey(1000)

	
	# quit()
	return (final_list)




def findMatch( wordStruct):
	
	possiblenames = []
	possiblevalues = []
	wordStruct = [Linked_Structure(i) for i in wordStruct]
	max_distance_bw_names = 20
	word_list = words.words()

	for i in wordStruct :
		if i.acc_level > 85:
			i.type = "names"
			possiblenames.append(i)
		elif i.acc_level > 50:
			if i.name.lower() in word_list:
				if any(char.isdigit() for char in i.name) == True:
					i.type = "values"
					possiblevalues.append(i)
				else:
					i.type = "names"
					possiblenames.append(i)
			else:
				i.type = "values"
				possiblevalues.append(i)
		else:
			i.type = "values"
			possiblevalues.append(i)
	

	for i in possiblenames :
		print(i)
	possiblevalues.sort(key= (lambda x : x.y1))
	new_possiblevalues = []
	curr = possiblevalues[0]
	new_arr = [curr]
	for i in range(1,len(possiblevalues)) :
		if abs( new_arr[-1].y1 - possiblevalues[i].y1) < 10 :
			new_arr.append(possiblevalues[i])
		else :
			new_possiblevalues.append(new_arr)
			new_arr = [possiblevalues[i]]
	new_possiblevalues.append(new_arr)
	[ i.sort(key= (lambda x : x.x1)) for i in new_possiblevalues ]
	possiblevalues = []

	for i in new_possiblevalues :
		curr = i[0]
		for j in range(1,len(i)) :
			if abs(curr.x2 - i[j].x1) < 10 :
				curr = curr + i[j]
			else :
				possiblevalues.append(curr)
				curr = i[j]
		possiblevalues.append(curr)


	possiblenames.sort(key= (lambda x : x.y1))
	new_possiblenames = []
	curr = possiblenames[0]
	new_arr = [curr]
	for i in range(1,len(possiblenames)) :
		if abs( new_arr[-1].y1 - possiblenames[i].y1) < 10 :
			new_arr.append(possiblenames[i])
		else :
			new_possiblenames.append(new_arr)
			new_arr = [possiblenames[i]]
	new_possiblenames.append(new_arr)
	[ i.sort(key= (lambda  x : x.x1 )) for i in new_possiblenames ]
	possiblenames = []
	for i in new_possiblenames :
		curr = i[0]
		for j in range(1,len(i)) :
			if abs(curr.x2 - i[j].x1) < 20 :
				 curr = curr + i[j]
			else :
				if not hasNumbers(curr.name) :
					possiblenames.append(curr)
				else :
					curr.type = "values"
					possiblevalues.append(curr)
				curr = i[j]
		if not hasNumbers(curr.name) :
			possiblenames.append(curr)
		else :
			curr.type = "values"
			possiblevalues.append(curr)
	
	
	
	
	alldata = possiblenames + possiblevalues
	alldata.sort(key= (lambda x : x.y1))
	new_alldata = []

	new_arr = [alldata[0]]
	for i in range(1,len(alldata)) :
		if abs( new_arr[-1].y1 - alldata[i].y1) < 10 :
			new_arr.append(alldata[i])
		else :
			new_alldata.append(new_arr)
			new_arr = [alldata[i]]
	new_alldata.append(new_arr)
	[ i.sort(key= (lambda  x : x.x1 )) for i in new_alldata ]
	alldata = []
	for i in new_alldata :
		curr_cont = False
		for j in range(len(i)-1) :
			if curr_cont :
				if curr.type == i[j+1].type :
					curr = curr + i[j+1]
				else :
					alldata.append(curr)
					curr_cont = False
				continue  

			if i[j].type != i[j+1].type :
				alldata.append(i[j])
			else :
				curr = i[j] + i[j+1]
				curr_cont = True
		if curr_cont == True :
			alldata.append(curr)
		else :
			alldata.append(i[len(i)-1])
	
	possiblenames= []
	possiblevalues = []

	for i in alldata :
		if i.type == "names" :
			possiblenames.append(i)
		else :
			possiblevalues.append(i)
	
	matchdict = {}

	for i in possiblevalues :
		mini = []
		for j in possiblenames :
			if abs(i.y1 - j.y1) < 30 and j.x1 < i.x1:
				mini.append(j)
		if len(mini) == 0 :
			continue
		mini.sort(key= (lambda  x : x.x1 ), reverse=True)
		its_me = mini[0]
		matchdict[its_me.name] = i.name
		possiblenames.remove(its_me)
	
	return matchdict


if __name__ == "__main__" :
	file=sys.argv[1]
	catch = get_str(file)
	entry = findMatch(catch)

	try :
		name = ("_".join(entry['Name'].split()))
	except :
		try :
			name = ("_".join(entry['Patient'].split()))
		except :
			name = "Some_patient"
	
	entryJson = json.dumps(entry)
	print(entryJson)
	file_id=os.path.splitext('IPWebcam.png')[0]
	myfname = '%s_%s.json'%(name,file_id)
	f = open(myfname, 'w')
	f.write(entryJson)
	f.close()

	# import pymongo
	# #import base64
	# #import bson
	# #from bson.binary import Binary

	# # establish a connection to the database
	# connection = pymongo.MongoClient()
	# db = connection.Users
	# coll = db.health_records
	# entryJson = json.dumps(entry)
	# print(entryJson)
	# file_id=os.path.splitext(file)[0]
	# #version= coll.find("file": newRegExp('^' +'_'+ filename+ '$', 'i').count) + 1
	# import re
	# regexp = re.compile('_'+file_id, re.IGNORECASE)
	# version= coll.find({"filename": regexp },'i').count()
	# print(version)
	# myfname = '%s_%s_%s.json'%('V'+str(version),name,file_id)
	# f = open(myfname, 'w')
	# f.write(entryJson)
	# f.close()

	
	# #get a handle to the test database

	# #file_meta = db.file_meta
	# file_used = myfname


	
	# with open(file_used, "r") as f:
	# 		encoded = f.read()
	# print("hello")
	# coll.insert_one({"filename": file_used, "file": encoded})
	# print("hh")
