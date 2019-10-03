
class BeDict( dict ):
	def Listify(self, buildElem ):
		if buildElem.key not in self:
			self[ buildElem.key ] = buildElem
		else:
			buildElem = self[ buildElem.key ]
		return buildElem
		


if __name__ == '__main__':
	pass