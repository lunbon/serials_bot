from functions import (
					get_last_episode,
					check_new_eps, 
					save_user_link_episode,
					get_or_create_server_file)
from discord.ext import commands
import discord
import pickle
import asyncio

description=(
	"""

	Бот. Напоминает. О выходе новых серий. Но это не точно.

	""")
token='NDE3Njk2Nzc4OTkzNzk1MDcy.DaZ1zA.BryXV3N31iH02Knk_JMUchGi4Dw'
bot=commands.Bot(command_prefix='?',description=description)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('-'*18)

@bot.command(pass_context=True)
async def save(ctx, url:str = ''):
	"""добавить сериал в список напоминаний - ?save <url>"""
	if url =='':
		await bot.say("url не найден!")
		return
	server_file = get_or_create_server_file(
			ctx.message.server,ctx.message.channel)
	last = get_last_episode(url)
			
	if last == "404" or last == "ConnectionError":
		await bot.say('Ошибка - не рабочий url')
	else:
		save_user_link_episode(str(ctx.message.author.mention),
			url,last,server_file)
		await bot.send_message(ctx.message.channel,
			'Последни эпизод - '+last)



bot.loop.create_task(check_new_eps(bot))
bot.run(token)