
from BuildElements.BaseElement import BaseElement 

class DerivedObject( BaseElement ):

	def extractName( self, line ):
		fullName = line[24:].split( ' ', 1 )[0]
		if '@' in fullName:
			fullName = fullName.split('@')[0]
		return fullName
