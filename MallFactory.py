import Mall

class MallFactory():
	#create mall object using Singleton
	def makeMallObj(idIn, name, address, postalcode, shoparray):
		return Mall.MallSingleton(idIn, name, address, postalcode, shoparray)