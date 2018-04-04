import requests
#from bs4 import BeautifulSoup as bs
import re 
import pickle
from models import Title
import asyncio
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

async def check_new_eps(bot):
	await bot.wait_until_ready()
	servers = list(bot.servers)
	while not bot.is_closed:
		for server in servers:
			server_name=str(server)+'.pickle'
			try:
				with open(server_name,'rb') as f:
					channel,titles = pickle.load(f)
			except FileNotFoundError:
				continue
			for title in titles:
				last_episode = get_last_episode(title.url)
				if last_episode == "404" or last_episode == "ConnectionError":	
					await bot.send_message(channel, "Ошибка при обработке - "+title.url)
					continue
				if title.last_episode < last_episode:
					message = ', '.join(title.users) + ' Вышли новые серии!\n' + title.url
					await bot.send_message(channel, message)
					title.last_episode = last_episode
			with open(str(server)+'.pickle','wb') as f:
				pickle.dump((channel,titles), f)
				await asyncio.sleep(3)
		await asyncio.sleep(3600)

