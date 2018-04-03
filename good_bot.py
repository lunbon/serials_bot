from functions import (
					get_last_episode, 
					save_user_link_episode,
					get_or_create_server_file)
from discord.ext import commands
import discord
import pickle
import asyncio

token='NDE3Njk2Nzc4OTkzNzk1MDcy.DaT9iw.ZnnKcAyFm16PZ6g_vxHxrnNu2ZI'
bot=commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-'*18)

async def check_new_eps():
	await bot.wait_until_ready()
	servers = list(bot.servers)
	while not bot.is_closed:
		for server in servers:
			server_name=str(server)+'pickle'
			try:
				with open(server_name,'rb') as f:
					channel,titles = pickle.load(f)
			except FileNotFoundError:
				continue
			for title in titles:
				last_episode = get_last_episode(title.url)
				if last_episode == "404" or last_episode == "ConnectionError":	
					last_episode = '0'
					await bot.send_message(channel, "Ошибка при обработке - "+title.url)
				if title.last_episode < last_episode:
					message = ', '.join(title.users) + ' Вышли новые серии!\n' + title.url
					await bot.send_message(channel, message)
					title.last_episode = last_episode
			with open(str(server)+'pickle','wb') as f:
				pickle.dump(titles, f)
			await asyncio.sleep(3)
		await asyncio.sleep(3600)

@bot.event
async def on_message(message):

	if message.content.startswith('?save'):
		server_file = get_or_create_server_file(message.server,message.channel)
		try:
			_, url= message.content.split(' ')
			last = get_last_episode(url)
			
			if last == "404" or last == "ConnectionError":
				await bot.send_message(message.channel,'Ошибка - не рабочий url')
			else:
				save_user_link_episode(str(message.raw_mentions),url,last,server_file)
				await bot.send_message(message.channel,'Последни эпизод - '+last)
		except ValueError:
			await bot.send_message(message.channel,'Ошибка - больше одного аргумента (?save <url>)')		
	await bot.process_commands(message)

bot.loop.create_task(check_new_eps())
bot.run(token)