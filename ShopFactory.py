import Shop

class ShopFactory():
	#create Shop Singleton Object
	def makeShopObj(shopid, unitnum, shopname, category, mallid, mallarray):
		return Shop.ShopSingleton(shopid, unitnum, shopname, category, mallid, mallarray)