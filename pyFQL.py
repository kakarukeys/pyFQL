import requests

# auth user -> get token

# #pyfacebook --------
# import facebook

# MY_API_KEY = "e1e9cfeb5e0d7a52e4fbd5d09e1b873e"
# MY_SECRET_KEY = "1bebae7283f5b79aaf9b851addd55b90"

# fb = facebook.Facebook(MY_API_KEY, MY_SECRET_KEY)
# fb.auth.createToken()
# fb.login()
# fb.auth_token
# #-------------------

# #facebook-sdk ------
# import facebook

# user = facebook.get_user_from_cookie(self.request.cookies, MY_API_KEY, MY_SECRET_KEY)
# user["access_token"]
# #-------------------

# #django-facebook ---
# token = FacebookAuthorization.convert_code(code)	#or
# # get from FacebookProfile object after authentication
# #-------------------

TABLES = ("album", "app_role", "application", "apprequest", "checkin", "comment", "comments_info", "connection", "cookies", "developer", "domain", "domain_admin", "event", "event_member", "family", "friend", "friend_request", "friendlist", "friendlist_member", "group", "group_member", "insights", "like", "link", "link_image_src", "link_stat", "location_post", "mailbox_folder", "message", "note", "notification", "object_url", "offer", "page", "page_admin", "page_blocked_user", "page_fan", "page_global_brand_child", "page_milestone", "permissions", "permissions_info", "photo", "photo_src", "photo_tag", "place", "privacy", "privacy_setting", "profile", "profile_pic", "profile_tab", "profile_view", "question", "question_option", "question_option_votes", "review", "score", "square_profile_pic", "square_profile_pic_size", "standard_friend_info", "standard_user_info", "status", "stream", "stream_filter", "stream_tag", "subscription", "thread", "translation", "unified_message", "unified_message_count", "unified_message_sync", "unified_thread", "unified_thread_action", "unified_thread_count", "unified_thread_sync", "url_like", "user", "video", "video_tag")

class Condition(object):
	def __init__(self, expression):
		self.expression = expression

class Column(object):
	def __init__(self, name):
		self.name = name

	def __eq__(self, other):
		return Condition(self.name + ' = ' + str(other))

class QueryError(Exception):
	pass

class Query(object):
	access_token = None

	def __init__(self, table_name, column_names):
		self.expression = "select {0} from {1}".format(', '.join(column_names), table_name)

	def __iter__(self):
		r = requests.get("https://graph.facebook.com/fql", params={'q': self.expression, "access_token": self.access_token})
		return iter(r.json()["data"])

	def where(self, condition):
		if "where" in self.expression:
			raise QueryError("You may call 'where' method only once.")
		else:
			self.expression += " where " + condition.expression
		return self

class Table(object):
	def __init__(self, name):
		self.name = name

	def __getattr__(self, name):
		return Column(name)

	def select(self, *args):
		return Query(self.name, (column.name for column in args))

for name in TABLES:
	vars()[name] = Table(name)
