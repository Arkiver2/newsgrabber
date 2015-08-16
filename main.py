import time
import os
import shutil
import threading
import requests
import re
from services import *
import codecs
import subprocess

def checkrefresh():
	for root, dirs, files in os.walk("./services"):
		for services in files:
			if services.startswith("web__") and services.endswith(".py"):
				with open("./temp/refresh" + str(eval(services[:-3] + ".refresh")), "ab+") as refreshfile:
					print(services[:-3])
					refreshfile.write(services[:-3] + "\n")

def checkurl(service, url):
	response = requests.get(url)
	extractedurls = []
	count = 0
	for extractedurl in re.findall(r'="(https?://[^"]+)"', response.text):
		extractedurls.append(re.sub("&amp;", "&", extractedurl))
	for extractedurl in re.findall(r"='(https?://[^']+)'", response.text):
		extractedurls.append(re.sub("&amp;", "&", extractedurl))
	for extractedurl in re.findall(r'="(/[^"]+)"', response.text):
		if extractedurl.startswith('//'):
			extractedurls.append("http:" + re.sub("&amp;", "&", extractedurl))
		else:
			extractedurls.append(re.match(r'^(https?://[^/]+)/', url).group(1) + re.sub("&amp;", "&", extractedurl))
	for extractedurl in re.findall(r"='(/[^']+)'", response.text):
		if extractedurl.startswith('//'):
			extractedurls.append("http:" + re.sub("&amp;", "&", extractedurl))
		else:
			extractedurls.append(re.match(r'^(https?://[^/]+)/', url).group(1) + re.sub("&amp;", "&", extractedurl))
	for extractedurl in re.findall(r'>(https?://[^<]+)<', response.text):
		extractedurls.append(re.sub("&amp;", "&", extractedurl))
	extractedurls = list(set(extractedurls))
	if not os.path.isdir("./donefiles"):
		os.makedirs("./donefiles")
	if os.path.isfile('./donefiles/' + service):
		donefile = codecs.open('./donefiles/' + service, 'r', 'utf-8').read()
	else:
		donefile = 'NOTHING'
	if os.path.isfile('list'):
		listfile = codecs.open('list', 'r', 'utf-8').read()
	else:
		listfile = 'NOTHING'
	with codecs.open('./donefiles/' + service + '_webpage', 'w', 'utf-8') as pagefile:
		pagefile.write(response.text)
	for extractedurl in extractedurls:
		extractedurl = re.sub("&amp;", "&", extractedurl)
		with codecs.open('./donefiles/' + service, 'a', 'utf-8') as doneurls:
			if not extractedurl in donefile:
				#print(extractedurl)
				doneurls.write(extractedurl + '\n')
				with codecs.open('list', 'a', 'utf-8') as listurls:
					if not extractedurl in listfile:
						listurls.write(extractedurl + '\n')
						count += 1
#	with codecs.open('./donefiles/' + service, 'r', 'utf-8') as donefile:
#		with codecs.open('./donefiles/' + service + '-temp', 'a', 'utf-8') as doneurls:
#			with codecs.open('./donefiles/' + service + '_webpage', 'r', 'utf-8') as pagefile:
#				page = pagefile.read()
#				print(page)
#				for doneurl in donefile:
#					if doneurl in response.text:
#						doneurls.write(doneurl + '\n')
#					if re.match(r'^https?://[^/]+(/.*)', doneurl):
#						if re.match(r'^https?://[^/]+(/.*)', doneurl).group(1) in page:
#							print("yessssssssssssss")
#							doneurls.write(doneurl)
#					elif re.match(r'^https?(://.*)', doneurl):
#						if re.match(r'^https?(://.*)', doneurl).group(1) in page:
#							doneurls.write(doneurl)
#					#print(re.match(r'^https?://[^/]+(/.*)', doneurl).group(1))
#					
#	os.remove('./donefiles/' + service)
#	os.rename('./donefiles/' + service + '-temp', './donefiles/' + service)
	print('EXTRACTED ' + str(count) + ' URLS')

def refresh1():
	while True:
		if os.path.isfile("./temp/refresh1"):
			with open("./temp/refresh1", "r") as refresh1file:
				for service in refresh1file:
					urlnum = 0
					for url in eval(service[:-1] + ".urls"):
						checkurl(service[:-1] + str(urlnum), url)
						urlnum += 1
		time.sleep(300)

def refresh2():
	while True:
		if os.path.isfile("./temp/refresh2"):
			with open("./temp/refresh2", "r") as refresh1file:
				for service in refresh1file:
					urlnum = 0
					for url in eval(service[:-1] + ".urls"):
						checkurl(service[:-1] + str(urlnum), url)
						urlnum += 1
		time.sleep(300)

def refresh3():
	while True:
		if os.path.isfile("./temp/refresh3"):
			with open("./temp/refresh3", "r") as refresh1file:
				for service in refresh1file:
					urlnum = 0
					for url in eval(service[:-1] + ".urls"):
						checkurl(service[:-1] + str(urlnum), url)
						urlnum += 1
		time.sleep(1800)

def refresh4():
	while True:
		if os.path.isfile("./temp/refresh4"):
			with open("./temp/refresh4", "r") as refresh1file:
				for service in refresh1file:
					urlnum = 0
					for url in eval(service[:-1] + ".urls"):
						checkurl(service[:-1] + str(urlnum), url)
						urlnum += 1
		time.sleep(3600)

def refresh5():
	while True:
		if os.path.isfile("./temp/refresh5"):
			with open("./temp/refresh5", "r") as refresh1file:
				for service in refresh1file:
					urlnum = 0
					print(service[:-1])
					for url in eval(service[:-1] + ".urls"):
						checkurl(service[:-1] + str(urlnum), url)
						urlnum += 1
		time.sleep(7200)

def dashboard():
	os.system('~/.local/bin/gs-server')

def processfiles():
	while True:
		os.system('python movefiles.py')
		command2 = subprocess.Popen(['python', 'uploader.py'])
		time.sleep(300)

def grab():
	while True:
		time.sleep(10)
		if os.path.isfile('list_temp'):
			os.remove('list_temp')
		if os.path.isfile('list'):
			os.rename('list', 'list_temp')
			threading.Thread(target=grablist).start()
			print("STARTED GRAB")
		time.sleep(1790)

def grablist():
	os.system('~/.local/bin/grab-site --input-file list_temp --level=0 --no-sitemaps --concurrency=20 --1')

def main():
	if os.path.isdir("./temp"):
		shutil.rmtree("./temp")
	if not os.path.isdir("./temp"):
		os.makedirs("./temp")
	if not os.path.isdir("./ready"):
		os.makedirs("./ready")
	for root, dirs, files in os.walk("./ready"):
		for file in files:
			if file.endswith(".upload"):
				os.remove(os.path.join(root, file))
	checkrefresh()
	threading.Thread(target = dashboard).start()
	threading.Thread(target = processfiles).start()
	threading.Thread(target = refresh1).start()
	threading.Thread(target = refresh2).start()
	threading.Thread(target = refresh3).start()
	threading.Thread(target = refresh4).start()
	threading.Thread(target = refresh5).start()
	threading.Thread(target = grab).start()

if __name__ == '__main__':
	main()
