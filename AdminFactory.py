import Admin


class AdminFactory():
	#create admin object
	def makeAdminObj(username, password):
		return Admin.AdminSingleton(username, password)