from good_doctor import get_last_episode, save_user_link_episode
from discord.ext import commands
import discord
import pickle
import asyncio

token='NDE3Njk2Nzc4OTkzNzk1MDcy.DZ5qvA._IXuQ58stGLycSwJHIT1auSKOWU'
bot=commands.Bot(command_prefix='?')
channel_id=417269196850987029

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-'*18)

async def check_new_eps():
	await bot.wait_until_ready()
	channel = discord.Object(id=channel_id)
	while not bot.is_closed:
		with open('users.pickle','rb') as f:
			titles = pickle.load(f)
		for title in titles:
			last_episode = get_last_episode(title.url)
			if last_episode == "404" or last_episode == "ConnectionError":	
				last_episode = '0'
				await bot.send_message(channel, "Ошибка при обработке - "+title.url)
			if title.last_episode < last_episode:
				message = ', '.join(title.users) + ' Вышли новые серии!\n' + title.url
				await bot.send_message(channel, message)
				title.last_episode = last_episode
				with open('users.pickle','wb') as f:
						pickle.dump(titles, f)
		await asyncio.sleep(3600)

@bot.event
async def on_message(message):

	if message.content.startswith('?save'):
		try:
			_, url= message.content.split(' ')
			last = get_last_episode(url)
			
			if last == "404" or last == "ConnectionError":
				await bot.send_message(message.channel,'Ошибка - не рабочий url')
			else:
				save_user_link_episode(str(message.author),url,last)
				await bot.send_message(message.channel,'Последни эпизод - '+last)
		except ValueError:
			await bot.send_message(message.channel,'Ошибка - больше одного аргумента (?save <url>)')		
	await bot.process_commands(message)

bot.loop.create_task(check_new_eps())
bot.run(token)