from functions import (
					get_last_episode,
					save_user_link_episode,
					get_list,get_users_list,
					update_tv_last)
from discord.ext import commands
import discord
import pickle
import asyncio

description=(
	"""

	Бот. Напоминает. О выходе новых серий. Но это не точно.

	""")
token=token
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
	last = get_last_episode(url)
	if last == "404" or last == "ConnectionError":
		await bot.say('Ошибка - не рабочий url')
	else:
		save_user_link_episode(ctx.message.channel.id,url,last)
		await bot.send_message(ctx.message.channel,
								'Последни эпизод - '+last)


@bot.command(pass_context=True)
async def show(ctx):
	"""Показать список сериалов - ?show"""
	for i in get_list(ctx.message.channel.id):
		await bot.send_message(ctx.message.channel,i[0]+' - '+i[1])

async def check_new_eps():
	await bot.wait_until_ready()
	while not bot.is_closed:
		users_list = get_users_list()
		for title in users_list:
			last = get_last_episode(title[0])
			if last > title[1]:
				update_tv_last(title[0],last,title[2])
				channel=discord.Object(id=title[2])
				if channel == None:raise ValueError
				await bot.send_message(channel,
			 				"Вышли новые серии - "+title[0])
		await asyncio.sleep(3600)

bot.loop.create_task(check_new_eps())
bot.run(token)