class Title(object):
	def __init__(self, user, url, episode):
		self.url=url
		self.users=[user]
		self.last_episode = episode
	def __str__(self):
		return str(users)+url
