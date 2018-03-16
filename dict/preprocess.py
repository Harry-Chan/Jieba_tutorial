# -*- coding: utf-8 -*-
import os, json, opencc, jieba
import jieba.posseg as pseg
from collections import OrderedDict
from collections import defaultdict
import re

creat_dir_paht = "test"

def GetAllFiles(path):
	FileList=[]
	for root, dirs, files in os.walk(path):#讀取指定目錄下所有的檔案
		for f in files:
			FileList.append(os.path.join(root, f))
	return FileList

def SentenceSegmentation(context):
	return jieba.cut(context, HMM= False)

def FilterpuntList(wordlist):
	regular = re.compile(u"[\u4e00-\u9fa5]+|[a-zA-z]+|[0-9]+")
	return [ word for word in wordlist if regular.match(word) ]

def traditionalize(context): 
	return opencc.convert(context, config='zhs2zht.ini').encode('utf8')

def Read_Json_Data(dir_path):
	for path in GetAllFiles(dir_path):
		tmp_dir_name = path[path.find("/",path.find("/")+1)+1:path.find(".")]
		print tmp_dir_name
		if not os.path.exists("EventData/"+creat_dir_paht):
			os.makedirs("EventData/"+creat_dir_paht)
		# print tmp_dir_name
		with open(path) as f:
			texts = list()
			for line in f:
				text = SentenceSegmentation(traditionalize(line.replace("\n"," ")).lower())
				texts.append(" ".join(FilterpuntList(text)))


			with open("EventData/"+creat_dir_paht+"/"+tmp_dir_name+".txt","a") as out_f:
				for text in texts:
					out_f.write(text.encode("utf8")+"\n")

def main():
	jieba.initialize("/home/Ming-Yi/MingYi/Behavior/Behavior/dict/dict.txt.big")
	jieba.load_userdict("/home/Ming-Yi/MingYi/Behavior/Behavior/dict/NameDict_Ch_v2")
	Read_Json_Data("rawdata/"+creat_dir_paht)


if __name__ == '__main__':
	main()