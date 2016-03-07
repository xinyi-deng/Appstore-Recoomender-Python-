import math
from pymongo import MongoClient
import operator

class DataService(object):

	def init(self,client):
		self.client = client;
		self.db = client.appstore
		self.download_history = self.db.user_download_history
		self.app_info = self.db.app_info
	def get_user_download_history(self):
		result = {}
		history_info = self.download_history.find()
		for history in history_info:
			result[history["user_id"]] = history["download_history"]
		return result

	def update_info(self,filter_dic,update):
		self.download_history.update_one(filter_dic,update,True)




# input: lists of users' favorite movie
# output: similarity of two users
def similarity(list1,list2):
	count = 0
	for i in xrange(len(list1)):
		if list1[i] in list2:
			count = count+1
	return float(count)/math.sqrt(len(list1)*len(list2))

def top5(user,download_history):
	# a dictionrary used to record similarity of all other apps
	similarity_dict = {}
	download_history_value = download_history.values();
	user_history_value = download_history[user]
	for history_value in download_history_value:
		# calculate the similarity between this app and a user
		simi = similarity(user_history_value,history_value)

		for app in history_value:
			if app in user_history_value:
				continue
			else:
				if similarity_dict.has_key(app):
					similarity_dict[app]+=simi
				else:
					similarity_dict[app] = simi
	# sort dictionary by value, return a list of tuple
	sorted_tuple = sorted(similarity_dict.items(),key=operator.itemgetter(1),reverse=True)
	# get the first five elements.
	if len(sorted_tuple)>=5:
		top5_app = [sorted_tuple[0][0],sorted_tuple[1][0],sorted_tuple[2][0],sorted_tuple[3][0],sorted_tuple[4][0]]
		return top5_app
	else:
		top5_app=[]
		for i in xrange(len(sorted_tuple)):
			top5_app[i] = sroted[i][0]
		return top5_app


def main():
	try:
		client = MongoClient('localhost',27017)
		dataService = DataService()
		dataService.init(client)
		user_download_history = dataService.get_user_download_history()
		for user in user_download_history.keys():
			top5_app = top5(user,user_download_history)
			dataService.update_info({"user_id":user},{'$set':{'top_5_app':top5_app}})
	except Exception as e:
		print e
	finally:
		print "done"
		if 'client' in locals():
			client.close()
if __name__ == "__main__":
		main()





