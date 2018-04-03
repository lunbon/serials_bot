import requests
from bs4 import BeautifulSoup as bs
import re 
import pickle
from models import Title

def get_last_episode(url):
	try:
		html=requests.get(url)
	except:
		return "ConnectionError"
	if html.status_code == 404:
		return "404"
	text=html.text
	return re.findall('[0-9]* сезон \d* серия',text)[0]
def get_or_create_server_file(server,channel):
	server=str(server)+".pickle"
	try:
		 open(server,'rb')
	except FileNotFoundError:
		with open(server,'wb') as f:
			pickle.dump((channel,[]),f)

	return server
def save_user_link_episode(user, url, episode,file):
	with open(file,'rb') as f:
			channel,titles=pickle.load(f)
			for title in titles:
				if url == title.url:
					title.users.append(user)
					break
			else:
				titles.append(Title(user, url, episode))
			
	with open(file,'wb') as f:
		pickle.dump((channel,titles),f)


