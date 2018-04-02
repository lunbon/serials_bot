import requests
from bs4 import BeautifulSoup as bs
import re 
import pickle
from good_users import Title

def get_last_episode(url):
	try:
		html=requests.get(url)
	except:
		return "ConnectionError"
	if html.status_code == 404:
		return "404"
	text=html.text
	return re.findall('[0-9]* сезон \d* серия',text)[0]

def save_user_link_episode(user, url, episode,file='users.pickle'):
	with open(file,'rb') as f:
			titles=pickle.load(f)
			titles.append(Title(user, url, episode))
			
	with open(file,'wb') as f:
		pickle.dump(titles,f)


