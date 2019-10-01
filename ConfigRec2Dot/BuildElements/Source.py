
from BuildElements.BaseElement import BaseElement 

class Source( BaseElement ):
	
	isFinal = True
	
	def CanUse( self, line ):
		if line[:23] == 'version                ':
			return True
		else:
			return False

	def extractName( self, line ):
		fullName = line[24:].split( ' ', 1 )[0]
		fullName = fullName.split( '@', 1 )[0]
		return fullName
