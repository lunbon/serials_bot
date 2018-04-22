import requests
import re 
import sqlite3
from models import Title
import asyncio

conn = sqlite3.connect('Rin.db')
cursor = conn.cursor()

def get_last_episode(url):
	try:
		html=requests.get(url)
	except:
		return "ConnectionError"
	if html.status_code == 404:
		return "404"
	text=html.text
	return re.findall('[0-9]* сезон \d* серия',text)[0]

def check_user_raw(id):
	response = cursor.execute("""
								SELECT * 
								FROM users
								WHERE user_id = %s;"""%id)
	for i in response:return True
	else:return False
def create_user_raw(id):
	cursor.execute("""
					INSERT INTO users
					VALUES(%s)
					"""%id)
	conn.commit()
def check_tv_raw(id,url):
	s="""SELECT *
		FROM users_list
		WHERE user_id = %s AND link = '%s';"""
	response=cursor.execute(s%(id,url))
	for i in response:return True
	else:return False
def create_tv_raw(id,url,last_episode):
	cursor.execute("""
					INSERT INTO users_list
					VALUES('%s','%s','%s')
					"""%(url,last_episode,id))
	conn.commit()
def update_tv_last(url,last,id):
	cursor.execute("""
					UPDATE users_list
					SET last_episode = '%s'
					WHERE user_id=%s AND link = '%s'; 
					"""%(last,id,url))
	conn.commit()
def save_user_link_episode(id,url,last_episode):
	print(not check_tv_raw(id,url))
	if not check_user_raw(id):
		create_user_raw(id)
	if not check_tv_raw(id,url):
		create_tv_raw(id,url,last_episode)
def get_list(id):
	if check_user_raw(id):
		response=cursor.execute("""SELECT *
					FROM users_list
					WHERE user_id='%s'"""%id)
		return response
def get_users_list():
	response=cursor.execute("""SELECT *
							FROM users_list;""")
	return response
