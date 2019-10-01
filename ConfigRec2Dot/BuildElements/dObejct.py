
from BuildElements.BaseElement import BaseElement 


class DerivedObject( BaseElement ):

	def extractName( self, line ):
		fullName = line[24:].split( ' ', 1 )[0]
		return fullName
