import eel
from base64 import b64encode
import uuid
from pymongo import MongoClient
from tkinter import filedialog
global fp
global explored
global search 
global explore
explored=[]
explore=[]
eel.init('web')
client=MongoClient("mongodb+srv://socialize:inyourfaceskanda@socialize.mggs2.mongodb.net/socialize?retryWrites=true&w=majority")

@eel.expose
def update(idd):
	with open("donttouchitplease.txt","a+") as f:
		f.write(idd+",")
@eel.expose
def returnsongs():
	songs=[]
	db=client["concord"]["other"]
	for song in db.find().limit(100):
		songs.append(song)
	return songs
@eel.expose
def updatesearch(sear):
	global search
	search=sear
@eel.expose
def results():
	global search
	res=[]
	db=client["concord"]["other"]
	try:
		for song in db.find({"artist":search}).limit(5):
			res.append(song)
	except:
		pass
	try:
		for song in db.find({"songname":search}).limit(5):
			res.append(song)
	except:
		pass
	return res
@eel.expose
def recommend():
	try:
		global explore
		db=client["concord"]["other"]
		with open("donttouchitplease.txt","r") as f:
			ids=f.read().split(",")
		ids.pop(-1)
		dictionary={}
		for i in range(0,len(ids)):
			try:
				dictionary[db.find_one({"uuid":ids[i]})["artist"]]+=1
			except:
				dictionary[db.find_one({"uuid":ids[i]})["artist"]]=1
		for key in dictionary:
			dictionary[key]=dictionary[key]/len(ids)
		songs=[]
		for song in db.find({"artist":max(dictionary,key=dictionary.get)}).limit(5):
			if song not in explore:
				songs.append(song)
				explore.append(song)
			else:
				pass
		print(dictionary,max(dictionary,key=dictionary.get))
		return songs
	except Exception as e:
		pass
@eel.expose
def play(idd):
	global fp
	db=client["concord"]["music"]
	fp=db.find_one({"uuid":idd})["data"]
@eel.expose
def recent():
	global explored
	db=client["concord"]["other"]
	with open("donttouchitplease.txt","r") as f:
		try:
			ids=f.read().split(",")
		except Exception as e:
			print(e)
	ids.pop(-1)
	songs=[]
	try:
		for i in range(0,len(ids)):
			if ids[i] not in explored:
				songs.append(db.find_one({"uuid":ids[i]}))
				explored.append(ids[i])
			else:
				pass
	except Exception as e:
		print(e)
	return songs
@eel.expose
def fetchplay():
	global fp
	return fp
@eel.expose
def upload(x,y):
	dbs=client["concord"]["music"]
	db=client["concord"]["other"]
	file=filedialog.askopenfilename(filetypes=(("MP3","*.mp3"),("All","*.mp3")))
	image=filedialog.askopenfilename(filetypes=(("PNG","*.png"),("All","*.png")))
	iddd=str(uuid.uuid4())
	with open(image,"rb") as f:
		image="data:image/png;base64,"+b64encode(f.read()).decode("utf-8")
	with open(file,"rb") as f:
		dbs.insert_one({"data":"data:audio/mp3;base64,"+b64encode(f.read()).decode("utf-8"),"uuid":iddd})
	db.insert_one({"songname":x,"artist":y,"image":image,"uuid":iddd})
eel.start("main.html")
